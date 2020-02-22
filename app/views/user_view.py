# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : user_view.py
@Time    : 2020/1/19 22:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import os
from datetime import datetime

from flask import render_template, request
from flask_cors import cross_origin
from flask_login import current_user, login_required
from .found_view import send_message_by_pusher

from app import db, OpenID
from app.main import user
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.utils import restful
from app.utils.auth_token import generate_token
from app.utils.mail_sender import send_email
from tasks import celery


@user.route('/', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
@login_required
def index():
    data = request.json
    print('user页面收到请求', data)
    return render_template('user.html')  # 所有参数都要


@user.route('/messages', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
@login_required
def get_message():
    req = request.json
    print('查询消息req', req)
    # commens=Comment.query.join(LostFound,user_id=current_user.id)
    losts = LostFound.query.filter_by(user_id=current_user.id).all()
    if len(losts) == 0:
        data = {
            "list": []
        }
        return restful.success(data=data)
    else:
        list = []
        for l in losts:
            if len(l.comments) != 0:
                for c in l.comments:
                    user = User.query.get(c.user_id)
                    dict = {
                        "id": c.id,
                        "userId": user.id,
                        "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                        "username": user.real_name + ' ' + user.username,
                        "time": c.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "title": l.title,
                        "lostFoundId": l.id,
                        "content": c.content
                    }
                    list.append(dict)
            data = {
                "list": list
            }
    return restful.success(data=data)


@user.route('/setQQ', methods=['POST'])
@login_required
@cross_origin()
def set_QQ():
    print('用户准备更改密码')
    new_qq = request.args.get('qq')
    print(new_qq)
    user_db = User.query.get(current_user.id)
    token = generate_token(user=user_db, operation='change-qq', qq=new_qq)
    messages = {
        'real_name': user_db.real_name,
        'token': token
    }
    send_email.delay(new_qq, 'QQ更改', 'changeQQ', messages=messages)
    return restful.success(success=True, msg="验证邮件已发送到您的新的QQ邮箱，可能在垃圾信箱中，确认成功才可更改")


@user.route('/setPassword', methods=['POST'])
@login_required
@cross_origin()
def set_password():
    print('用户准备更改密码')
    req = request.json
    print(req)
    u = User.query.get(current_user.id)
    if u.verify_password(req['oldPassword']):
        u.password = req['newPassword']
        db.session.commit()
        return restful.success()
    return restful.success(success=False, msg="您输入的密码有误")


@user.route('/removeComment', methods=['POST'])
@login_required
@cross_origin()
def del_comment():
    refer = request.referrer
    print(refer)
    req = request.args.get('id')
    print('删除评论：', req, type(req))
    if not req:
        return restful.params_error()
    else:
        c = Comment.query.get(int(req))
        if c is not None and (
                LostFound.query.get(c.lost_found_id).user_id == current_user.id or current_user.kind >= 2):
            db.session.delete(c)
            db.session.commit()
            return restful.success(msg='删除成功')
        else:
            return restful.params_error()


@user.route('/removeLost', methods=['POST'])
@login_required
@cross_origin()
def del_Lost():
    refer = request.referrer
    print(refer)
    req = request.args.get('id')
    print('删除帖子：', req, type(req))
    if not req:
        return restful.params_error()
    else:
        l = LostFound.query.get(int(req))
        if l is not None and (l.user_id == current_user.id or current_user.kind >= 2):
            if l.images != "":
                l.images = l.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                imglist = l.images.strip().split(',')
                remove_imglist.delay(imglist)
            db.session.delete(l)
            db.session.commit()
            return restful.success(msg='删除成功')
        else:
            return restful.params_error()


@user.route('/claim', methods=['POST'])
@login_required
@cross_origin()
def claim():
    req = request.args.get('id')
    print(req, type(req))
    if not req:
        return restful.params_error()
    else:
        l = LostFound.query.get(int(req))
        # 寻物
        if l is not None and (l.user_id != current_user.id) and l.kind == 0:
            l.status = 1
            l.claimant_id = current_user.id
            db.session.add(l)
            db.session.commit()
            lost_user = User.query.filter_by(id=l.user_id).first()
            print('通过失物正向查询失主', lost_user)
            # 改变状态，有人找到了要通知失主
            dict = {
                'lost_user': lost_user.real_name,
                'found_user': current_user.real_name,
                'connect_way': current_user.qq,
                'pub_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'pub_content': l.about,
                'pub_location': l.location,
                'url': 'http://iboy.f3322.net:8888/detail.html?id=' + str(l.id)
            }
            op = OpenID.query.filter_by(user_id=lost_user.id).first()
            if op is not None:
                print('发送消息')
                uids = [op.wx_id]
                send_message_by_pusher(dict, uids)
                send_email.delay('849464742', '失物找回通知', 'noticeLost', messages=dict)
            return restful.success(msg='上报成功,您的联系方式已发送给失主')
        # 招领
        elif l is not None and (l.user_id != current_user.id) and l.kind == 1:
            l.status = 1
            l.claimant_id = current_user.id
            db.session.add(l)
            db.session.commit()
            found_user = User.query.filter_by(id=l.user_id).first()
            # 改变状态，有人找到了要通知失主
            dict = {
                'lost_user': current_user.real_name,
                'found_user': found_user.real_name,
                'connect_way': current_user.qq,
                'pub_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'pub_content': l.about,
                'pub_location': l.location,
                'url': 'http://iboy.f3322.net:8888/detail.html?id=' + str(l.id)
            }
            op = OpenID.query.filter_by(user_id=found_user.id).first()
            if op is not None:
                print('发送消息')
                uids = [op.wx_id]
                send_message_by_pusher(dict, uids)
                send_email.delay('849764742', '失物认领通知', 'noticeFound', messages=dict)
            return restful.success(msg='认领成功,您的联系方式已发送给失主')
        else:
            return restful.params_error()


@celery.task(time_limit=10)
def remove_imglist(imgs):
    print('获取执行结果',os.getenv('CELERY_RESULT_BACKEND'))
    for img in imgs:
        file = os.getenv('PATH_OF_UPLOAD')+img
        print('要删除的文件',file)
        try:
            os.remove(file)
        except Exception as e:
            print('删除文件', str(e))
