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
from random import randint

from flask import request, url_for
from flask_cors import cross_origin
from flask_login import current_user, login_required

from app import db, OpenID
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.page import user
from app.utils import restful
from app.utils.auth_token import generate_token
from app.utils.mail_sender import send_email
from .found_view import send_message_by_pusher
from ..decorators import wechat_required


@user.route('/messages', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
@login_required
@wechat_required
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
    print(new_qq, type(new_qq))
    if new_qq == current_user.qq:
        return restful.success(success=False, msg="您的QQ和之前一样，修改失败")
    token = str(generate_token(id=current_user.id, operation='change-qq', qq=new_qq), encoding="utf-8")
    print('我是生成的token', url_for('auth.confirm', token=token, _external=True))
    messages = {
        'real_name': current_user.real_name,
        'token': url_for('auth.confirm', token=token, _external=True)
    }
    send_email.apply_async(args=(new_qq, 'QQ更改', 'changeQQ', messages),countdown=randint(1, 30))
    return restful.success(success=True, msg="验证邮件已发送到您的QQ邮箱，请及时确认")


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


@user.route('/claim', methods=['POST'])
@login_required
@cross_origin()
def claim():
    req = request.args.get('id')
    print(req, type(req))
    if not req:
        return restful.params_error()
    else:
        try:
            l = LostFound.query.get(int(req))
            # 寻物
            if l is not  None: #查到了
                if l.kind == 0:
                    if l.user_id != current_user.id :
                        l.status = 1
                        l.deal_time=datetime.now()
                        l.claimant_id = current_user.id
                        # db.session.add(l)
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
                            'url': os.getenv('SITE_URL')+'detail.html?id=' + str(l.id)
                        }
                        send_email.apply_async(args=[lost_user.qq, '失物找回通知', 'noticeLost', dict], countdown=randint(1, 30))
                        op = OpenID.query.filter_by(user_id=lost_user.id).first()
                        if op is not None:
                            print('发送消息')
                            uids = [op.wx_id]
                            send_message_by_pusher(dict, uids,0)
                        return restful.success(msg='上报成功,您的联系方式已发送给失主')

                # l = db.session.merge(l)
                else:  # 招领
                    if l.user_id != current_user.id:
                        l.status = 1
                        l.deal_time=datetime.now()
                        l.claimant_id = current_user.id
                        # db.session.commit()
                        # l=db.session.merge(l)
                        found_user = User.query.filter_by(id=l.user_id).first()
                        # 改变状态，有人找到了要通知失主
                        dict = {
                            'lost_user': current_user.real_name,
                            'found_user': found_user.real_name,
                            'connect_way': current_user.qq,
                            'pub_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'pub_content': l.about,
                            'pub_location': l.location,
                            'url': os.getenv('SITE_URL')+'detail.html?id=' + str(l.id)
                        }
                        send_email.apply_async(args=[found_user.qq, '失物认领通知', 'noticeFound', dict], countdown=randint(1, 30))
                        op = OpenID.query.filter_by(user_id=found_user.id).first()
                        if op is not None:
                            print('发送消息')
                            uids = [op.wx_id]
                            send_message_by_pusher(dict, uids,1)
                        return restful.success(msg='认领成功,您的联系方式已发送给失主')
            else:
                return restful.params_error()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return restful.success(success=False,msg=str(e))
        finally:
            db.session.add(l)
            db.session.commit()
