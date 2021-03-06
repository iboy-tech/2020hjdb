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
import os
from datetime import datetime
from random import randint

from flask import request

from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db, OpenID, redis_client, cache, limiter, logger
from app.config import PostConfig
from app.decorators import admin_required
from app.models.category_model import Category
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.page import found
from app.utils import restful
from app.utils.check_data import check_post
from app.utils.delete_file import remove_files
from app.utils.img_process import change_bs4_to_png
from app.utils.log_utils import add_log
from app.utils.mail_sender import send_email
from app.utils.qq_notice import qq_group_notice
from app.utils.time_util import get_time_str
from app.utils.wechat_notice import delete_post_notice, send_message_by_pusher


@found.route('/resend/<int:id>', methods=['GET'], strict_slashes=False)
@login_required
@admin_required
def resend(id):
    article = LostFound.query.get(id)
    if article is None:
        return restful.success(False, "参数错误")
    article.claimant_id = None
    article.status = 0
    article.deal_time = None
    db.session.add(article)
    db.session.commit()
    return restful.success(msg="已重新发布")


@found.route('/page', methods=['POST'], strict_slashes=False)
@login_required
# @cache.cached(timeout=10 * 60, query_string=True, key_prefix='found-getall')  # 缓存10分钟 默认为300s
def get_all():
    req = request.json
    page = 0
    # logger.info(req['pageSize'])
    if req['pageNum']:
        page = int(req['pageNum'])
        # logger.info("这里好像有BUG")
    pagesize = int(req['pageSize'])
    # 后台分页动态调整
    if current_user.kind > 1 and req.get("flag") is not None:
        total_page = db.session.query(LostFound).count()
        mid = total_page // 10
        # logger.info('总的页数', total_page, mid)
        if pagesize < mid:
            pagesize = mid
    else:
        # 前端请求的最大页数
        if pagesize > PostConfig.PAGESIZE_OF_USER:
            # 不是搜索页面的请求
            if req.get("isSearch") is None:
                return restful.error()
    # logger.info('get_users收到请求')
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
    # logger.info('这是用户个人查询')
    elif req['username'] != '':
        u = User.query.filter_by(username=req['username']).one()
        pagination = LostFound.query.filter_by(user_id=u.id).order_by(LostFound.status,
                                                                      LostFound.create_time.desc()).paginate(page + 1,
                                                                                                             per_page=
                                                                                                             pagesize,
                                                                                                             error_out=False)
    elif req['kind'] != -1 and req['category'] != '':
        # logger.info('这是分类查询')
        # logger.info(req['category'])
        c = Category.query.filter_by(name=req['category']).first()
        # logger.info('这里好像有问题Category.query.', c)
        if c:
            pagination = LostFound.query.filter_by(category_id=c.id, kind=req['kind']).order_by(
                LostFound.status, LostFound.create_time.desc()).paginate(page + 1, per_page=pagesize,
                                                                         error_out=False)
    elif req['kind'] != -1 and req['category'] == '':
        # logger.info('这是分类查询')
        pagination = LostFound.query.filter_by(kind=req['kind']).order_by(LostFound.status,
                                                                          LostFound.create_time.desc()).paginate(
            page + 1,
            per_page=
            pagesize,
            error_out=False)
    # 用户搜索开始模糊匹配
    elif keyword != '':
        # logger.info('这是分类查询')
        c = Category.query.filter(Category.name.like(("%" + keyword + "%"))).first()
        u = User.query.filter(or_(User.real_name.like("%" + keyword + "%"),
                                  User.username == keyword)).first()
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
    # logger.info('分类查询：',data)
    return data


@found.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
@limiter.limit(limit_value="5/minute")
@login_required
@check_post
def pub():
    data = request.json
    imgstr = ''
    flag = False
    if len(data['images']) != 0:
        flag, imgstr = change_bs4_to_png(data['images'])
    info = data.get('info')
    try:
        lost = LostFound(kind=data['applyKind'], category_id=data['categoryId'],
                         images=','.join(imgstr), location=data['location'].replace('/(<（[^>]+）>)/script', ''),
                         title=data['title'].replace('/(<（[^>]+）>)/script', ''),
                         about=data['about'].replace('/(<（[^>]+）>)/script', ''), user_id=current_user.id)
        db.session.add(lost)
        db.session.commit()
    except Exception as e:
        logger.info(str(e))
        db.session.rollback()
        # 出现异常删除照片
        if imgstr != "":
            # imglist = imgstr.split(",")
            remove_files(imgstr, 0)
        return restful.error()
    if info != '':
        lost_users = User.query.filter(or_(User.username == info, User.real_name == info))
        if lost_users:
            for u in lost_users:
                dict = {
                    'lost_user': u.real_name,
                    'found_user': current_user.real_name,
                    'connect_way': current_user.qq,
                    'pub_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'pub_content': lost.about,
                    'pub_location': lost.location,
                    'url': os.getenv('SITE_URL') + 'detail/' + str(lost.id) + ".html"
                }
                op = OpenID.query.filter_by(user_id=u.id).first()
                if op is not None and op.wx_id is not None:
                    # logger.info('发送消息')
                    uids = [op.wx_id]
                    send_message_by_pusher(dict, uids, 3)
                    send_email.apply_async(args=(u.qq, '失物找回通知', 'foundNotice', dict), countdown=randint(10, 30))
    qq_msg = {
        "kind": "失物招领" if lost.kind == 0 else "寻物启示",
        "poster": current_user.real_name,
        "category": Category.query.get(lost.category_id).name,
        "addr": "未知" if lost.location == '' else lost.location,
        "detail": lost.about,
        "url": os.getenv('SITE_URL') + 'detail/' + str(lost.id) + ".html"
    }
    qq_group_notice.apply_async(args=[qq_msg, ], countdown=5)
    cache.delete("category")
    if flag:
        return restful.success(msg="发布成功，图片太大已丢弃")
    return restful.success(msg="发布成功")


def get_search_data(pagination, pageNum, pagesize):
    losts = pagination.items
    datalist = []
    for l in losts:
        if l.images == "":
            imglist = []
        else:
            # l.images = l.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
            imglist = l.images.split(',')
        # logger.info(imglist, type(imglist))
        user = User.query.get(l.user_id)
        key = PostConfig.POST_REDIS_PREFIX + str(l.id)
        view_count = redis_client.get(key)
        if view_count is None:
            # 防止redis迁移导致的数据丢失
            look_count = l.look_count
            redis_client.set(key, l.look_count)
        else:
            look_count = int(bytes.decode(view_count))
        dict = {
            "id": l.id,
            "icon": PostConfig.AVATER_API.replace("{}", user.qq),
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


@found.route('/', methods=['DELETE'], strict_slashes=False)
@login_required
@admin_required
def delete_posts():
    req = request.json
    logger.info(req)
    if req:
        lost_founds = LostFound.query.filter(LostFound.id.in_(req)).all()
        # logger.info(lost_founds)
    try:
        for l in lost_founds:
            # logger.info(l)
            u = User.query.get_or_404(l.user_id)
            # 管理员删帖或用户自身删帖
            if l is not None and (l.user_id == current_user.id or current_user.kind > u.kind):
                if l.images != "":
                    imglist = l.images.split(',')
                    remove_files(imglist, 0)
                # l = db.session.merge(l)
                key = PostConfig.POST_REDIS_PREFIX + str(l.id)
                # # 删除浏览量，不存在的key会被忽略
                redis_client.delete(key)
                delete_post_notice.delay(current_user.kind, current_user.id, l.to_dict())
                db.session.delete(l)
                db.session.commit()
        # 记录删除日志
        add_log(0, {"num": len(req)})
        # logger.info("try块内")
    except Exception as e:
        db.session.rollback()
        return restful.error(str(e))
    finally:
        db.session.close()
    cache.delete("category")
    return restful.success(msg="删除成功")


@found.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id=-1):
    if id == -1:
        return restful.error()
    else:
        l = LostFound.query.get_or_404(id)
        # logger.info("帖子：", l)
        u = User.query.get_or_404(l.user_id)
        # logger.info("用户：", u)
        # 管理员删帖或用户自身删帖
        if l is not None and (l.user_id == current_user.id or current_user.kind > u.kind):
            if l.images != "":
                imglist = l.images.strip().split(',')
                remove_files(imglist, 0)
            key = PostConfig.POST_REDIS_PREFIX + str(l.id)
            # # 删除浏览量，不存在的key会被忽略
            redis_client.delete(key)
            if current_user.kind > 1:
                # 记录删除日志
                add_log(0, {"num": 1})
            delete_post_notice(current_user.kind, current_user.id, l.to_dict())
            db.session.delete(l)
            db.session.commit()
            db.session.close()
            cache.delete("category")
            return restful.success(msg='删除成功')
        else:
            return restful.error()
