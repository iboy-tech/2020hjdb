# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : found_view.py
@Time    : 2020/1/24 20:35
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import base64
import os
import uuid
from datetime import datetime
from io import BytesIO
from random import randint

from PIL import Image
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db, OpenID, redis_client
from app.config import PostConfig
from app.decorators import wechat_required, admin_required
from app.models.category_model import Category
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.page import found
from app.utils import restful
from app.utils.img_compress import change_all_img_scale, change_img_scale, change_all_img_to_jpg, find_big_img
from app.utils.mail_sender import send_email
from app.utils.time_util import get_time_str
from app.utils.tinify_tool import tinypng
from app.utils.wxpusher import WxPusher
from tasks import celery


@found.route('/', methods=['GET'], strict_slashes=False)
@login_required
@wechat_required
def index():
    return render_template('found.html')


@found.route('/getall', methods=['POST'], strict_slashes=False)
@login_required
# @cache.cached(timeout=10 * 60, query_string=True, key_prefix='found-getall')  # 缓存10分钟 默认为300s
def get_all():
    req = request.json
    page = int(req['pageNum'])
    pagesize = int(req['pageSize'])
    # 后台分页动态调整
    if current_user.kind > 1 and req.get("flag") is not None:
        total_page = db.session.query(LostFound).count()
        mid = total_page // 10
        print('总的页数', total_page, mid)
        if pagesize < mid:
            pagesize = mid
    else:
        # 前端请求的最大页数
        if pagesize > PostConfig.PAGESIZE_OF_USER:
            return restful.params_error()

    print('我是前端获取的分页数据', req)
    # print('get_users收到请求')
    keyword = req['keyword']
    if req['kind'] == -1 and req['category'] == '' and req['username'] == '' and keyword == '':
        pagination = LostFound.query.order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1,
                                                                                                       per_page=pagesize,
                                                                                                       error_out=False)

    elif req['kind'] == -1 and req['category'] != '':
        c = Category.query.filter_by(name=req['category']).first()
        pagination = LostFound.query.filter_by(category_id=c.id).order_by(LostFound.status,
                                                                          LostFound.create_time.desc()).paginate(
            page + 1, per_page=pagesize, error_out=False)
    elif req['username'] != '':
        # print('这是用户个人查询')
        u = User.query.filter_by(username=req['username']).first()
        pagination = LostFound.query.filter_by(user_id=u.id).order_by(LostFound.status,
                                                                      LostFound.create_time.desc()).paginate(page + 1,
                                                                                                             per_page=
                                                                                                             pagesize,
                                                                                                             error_out=False)
    elif req['kind'] != -1 and req['category'] != '':
        # print('这是分类查询')
        # print(req['category'])
        c = Category.query.filter_by(name=req['category']).first()
        # print('Category.query.',c)
        pagination = LostFound.query.filter_by(category_id=c.id, kind=req['kind']).order_by(
            LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                     error_out=False)
    elif req['kind'] != -1 and req['category'] == '':
        # print('这是分类查询')
        c = Category.query.filter_by(name=req['category']).first()
        pagination = LostFound.query.filter_by(kind=req['kind']).order_by(LostFound.status,
                                                                          LostFound.create_time.desc()).paginate(
            page + 1,
            per_page=
            pagesize,
            error_out=False)
    elif keyword != '':
        # print('这是分类查询')
        c = Category.query.filter(Category.name.like(("%" + keyword + "%"))).first()
        u = User.query.filter(or_(User.real_name.like("%" + keyword + "%"),
                                  User.username.like("%" + keyword + "%")
                                  )).first()
        if c is not None and u is not None:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.category_id == c.id,
                    LostFound.user_id == u.id)
            ).order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                                error_out=False)
        elif c is not None and u is None:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.category_id == c.id)
            ).order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                                error_out=False)
        elif c is None and u is not None:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.user_id == u.id)
            ).order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                                error_out=False)
        elif ('寻物' or '寻' or '启' or '事') in keyword:
            pagination = LostFound.query.filter(
                LostFound.kind == 0
            ).order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                                error_out=False)
        elif ('认领' or '失' or '招' or '领' or '认') in keyword:
            pagination = LostFound.query.filter(
                LostFound.kind == 1
            ).order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                                error_out=False)
        else:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.location.like("%" + keyword + "%"))
            ).order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                                error_out=False)
    else:
        pagination = LostFound.query.filter(
            or_(LostFound.title.like("%" + keyword + "%"),
                LostFound.about.like("%" + keyword + "%"),
                )).order_by(LostFound.status, LostFound.create_time.desc()).paginate(page + 1,
                                                                                     per_page=pagesize,
                                                                                     error_out=False)
    data = get_search_data(pagination, page, pagesize)
    # print('分类查询：',data)
    return data


# 对上传图片进行格式转换并裁剪
def change_bs4_to_png(imglist):
    files = []
    for img in imglist:
        bas4_code = img.split(',')
        filename = uuid.uuid4().hex + '.jpg'
        files.append(filename)
        myfile = os.path.join(os.getenv("PATH_OF_UPLOAD"), filename)
        print("保存的路径", myfile)
        image = base64.b64decode(bas4_code[1])
        image = BytesIO(image)
        image = Image.open(image)
        image = image.convert('RGB')
        image.save(myfile)
        # 生成缩略图
        change_img_scale(filename)
        # 后台检查图片大小
        if os.path.getsize(myfile) / 1024 > PostConfig.UPLOAD_MAX_SIZE:
            try:
                os.remove(myfile)
                os.remove(os.getenv("MINI_IMG_PATH") + filename)
                # 一张图片超过上限返回空值
                return ''
            except Exception as e:
                print(str(e))
                print("图片太大,移除列表中的元素")
    if files:
        print('对上传图片进行异步压缩')
        tinypng.delay(files)
    print(files, '我是文件名')
    return files


def check_pup(data):
    if data['title'] == "" or data['about'] == "":
        return True
    else:
        return False


@found.route('/pub', methods=['POST', 'OPTIONS'], strict_slashes=False)
@login_required
def pub():
    data = request.json
    print(data)
    # print(data['images'], type(data['images']))
    if check_pup(data):
        return restful.params_error(success=False, msg="参数错误")
    print(type(data['images']), len(data['images']))
    # strs = data['images'][0]
    imgstr = ''
    if len(data['images']) != 0 and len(data['images']) <= 3:
        imgstr = change_bs4_to_png(data['images'])
    elif len(data['images']) > 3:
        return restful.params_error(success=False, msg="照片数量超过上限")
    info = data['info']
    # print(type(imgstr), imgstr)
    print(data['location'])
    lost = LostFound(kind=data['applyKind'], category_id=data['categoryId'],
                     images=str(imgstr), location=data['location'].replace('/(<（[^>]+）>)/script', ''),
                     title=data['title'].replace('/(<（[^>]+）>)/script', ''),
                     about=data['about'].replace('/(<（[^>]+）>)/script', ''), user_id=current_user.id)
    try:
        db.session.add(lost)
        print('帖子的ID')
    except Exception as e:
        db.session.rollback()
        # 出现异常删除照片
        remove_imglist(imgstr)
        return restful.params_error(msg=str(e))
    if info != '':
        lost_users = User.query.filter(or_(User.username == info, User.real_name == info))
        if not lost_users:
            print('失主没有注册')
        else:
            print('可能的失主', lost_users)
            print('有人捡到您的东西了')
            print('微信公众号和邮件通知失主')
            for u in lost_users:
                print(u)
                dict = {
                    'lost_user': u.real_name,
                    'found_user': current_user.real_name,
                    'connect_way': current_user.qq,
                    'pub_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'pub_content': lost.about,
                    'pub_location': lost.location,
                    'url': os.getenv('SITE_URL') + 'detail.html?id=' + str(lost.id)
                }
                op = OpenID.query.filter_by(user_id=u.id).first()
                if op is not None and op.wx_id is not None:
                    print('发送消息')
                    uids = [op.wx_id]
                    send_message_by_pusher.delay(dict, uids, 3)
                    send_email.apply_async(args=(u.qq, '失物找回通知', 'foundNotice', dict), countdown=randint(1, 30))
                db.session.commit()
    # cache.delete('found-getall')  # 删除缓存

    return restful.success()


@celery.task
def send_message_by_pusher(msg, uid, kind):
    print('即将要发送的消息', msg)
    if kind == 0:  # 寻物认领
        content = render_template('msgs/' + 'WXLostNotice.txt', messages=msg)
    elif kind == 1:  # 招领认领
        content = render_template('msgs/' + 'WXFoundNotice.txt', messages=msg)
    elif kind == 2:  # 删除通知
        content = render_template('msgs/' + 'WXDeleteNotice.txt', messages=msg)
    elif kind == 3:  # 发布招领匹配
        content = render_template('msgs/' + 'WXNotice.txt', messages=msg)
    elif kind == 4:
        content = render_template('msgs/' + 'WXCommentNotice.txt', messages=msg)
    print(content)
    msg_id = WxPusher.send_message(content=u'' + str(content), uids=uid, content_type=2, url=msg['url'])
    print('我是消息的ID', msg_id)
    # html=render_template('mails/WXNotice.html', messages=messages)
    # WxPusher.send_message(content=str(msg), uids=uid,content_type=2)


def get_search_data(pagination, pageNum, pagesize):
    losts = pagination.items
    # print(losts)
    datalist = []
    for l in losts:
        if l.images == "":
            imglist = []
        else:
            l.images = l.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
            imglist = l.images.strip().split(',')
        # print(imglist, type(imglist))
        user = User.query.get(l.user_id)
        key = str(l.id) + PostConfig.POST_REDIS_PREFIX
        view_count = redis_client.get(key)
        if view_count is None:
            # 防止redis迁移导致的数据丢失
            look_count = l.look_count
            redis_client.set(key, l.look_count)
        else:
            look_count = int(bytes.decode(view_count))
        dict = {
            "id": l.id,
            "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
            "kind": l.kind,
            "status": l.status,
            "claimantId": l.claimant_id,
            "userId": l.user_id,
            "username": user.username,
            "realName": user.real_name,
            "time": get_time_str(l.create_time),
            "location": l.location,
            "title": l.title,
            "about": l.about,
            "images": imglist,
            "category": Category.query.get(l.category_id).name,
            "lookCount": look_count,
            "commentCount": len(Comment.query.filter_by(lost_found_id=l.id).all()),
            "ustatus": user.status
        }
        datalist.append(dict)
    data = {
        "page": {
            "total": pagination.total,
            "totalPage": pagination.pages,
            "pageNum": pageNum,
            "pageSize": pagesize,
            "list": datalist
        }
    }
    return restful.success(data=data)


@found.route('/deleteAll', methods=['POST'])
@login_required
@admin_required
@cross_origin()
def delete_losts():
    req = request.json
    print(req)
    if req:
        lost_founds = LostFound.query.filter(LostFound.id.in_(req))
        for l in lost_founds:
            u = User.query.get_or_404(l.user_id)
            # 管理员删帖或用户自身删帖
            if l is not None and (l.user_id == current_user.id or current_user.kind > u.kind):
                if l.images != "":
                    l.images = l.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                    imglist = l.images.strip().split(',')
                    remove_imglist.delay(imglist)
                key = str(l.id) + PostConfig.POST_REDIS_PREFIX
                # # 删除浏览量，不存在的key会被忽略
                redis_client.delete(key)
                delete_post_notice.delay(current_user.kind, current_user.id, l.to_dict())
            db.session.delete(l)
    try:
        db.session.commit()
        print("try块内")
    except Exception as e:
        db.session.rollback()
        return restful.success(False, msg=str(e))
    return restful.success(msg="删除成功")


@found.route('/delete', methods=['POST'])
@login_required
@cross_origin()
def delete_lost():
    req = request.args.get('id')
    if not req:
        return restful.params_error()
    else:
        l = LostFound.query.get_or_404(int(req))
        u = User.query.get_or_404(l.user_id)
        # 管理员删帖或用户自身删帖
        if l is not None and (l.user_id == current_user.id or current_user.kind > u.kind):
            if l.images != "":
                l.images = l.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                imglist = l.images.strip().split(',')
                remove_imglist.delay(imglist)
            key = str(l.id) + PostConfig.POST_REDIS_PREFIX
            # # 删除浏览量，不存在的key会被忽略
            redis_client.delete(key)
            delete_post_notice(current_user.kind, current_user.id, l.to_dict())
            db.session.delete(l)
            db.session.commit()
            # db.session.close()
            return restful.success(msg='删除成功')
        else:
            return restful.params_error()


# 对之前的图片进行批量裁剪
@found.route('/compress', methods=['GET'])
@login_required
@admin_required
@cross_origin()
def compress():
    change_all_img_to_jpg()
    change_all_img_scale()
    return restful.success(msg="压缩成功")


@celery.task
def compress_imgs_in_freetime():
    big_img = find_big_img()
    if big_img:
        tinypng(big_img)
    else:
        print("没有图片无需压缩")
    return restful.success(msg="压缩成功")


# 通过接口进行无损压缩
@found.route('/tinypng', methods=['GET'])
@login_required
@admin_required
@cross_origin()
def compress_from_api():
    compress_imgs_in_freetime()
    return restful.success(msg="压缩成功")


@celery.task  # 删除帖子给用户发送通知
def delete_post_notice(kind, id, l):
    # 管理删除的和自己删除的不通知
    if kind > 1 and l['user_id'] != id:
        u = User.query.get_or_404(l['user_id'])
        op = OpenID.query.filter_by(user_id=u.id).first_or_404()
        if op is not None:
            dict = {
                'post_user': u.real_name,
                'post_title': l['title'],
                'post_content': l['about'],
                'handle_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'qq_group': '878579883',
                'url': os.getenv('SITE_URL')
            }
            print('删除帖子要发送的消息', dict)
            print('管理员删帖发送消息')
            uids = [op.wx_id]
            send_message_by_pusher(msg=dict, uid=uids, kind=2)


@celery.task
def remove_imglist(imgs):
    # os.chdir("O:/Python/Flask-WC/")
    for img in imgs:
        print(img)
        file = os.path.join(os.getenv("PATH_OF_UPLOAD"), img)
        try:
            print('要删除的文件', file)
            os.remove(file)
            os.remove(os.path.join(os.getenv("MINI_IMG_PATH"), img))
        except Exception as e:
            print('删除文件', str(e))
