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
from flask import render_template, request, g, current_app, session, redirect, url_for
from flask_cors import cross_origin
from flask_login import current_user, login_required

from app import db
from app.main import user, auth
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.untils import restful


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


@user.route('/setPassword', methods=['POST'])
@login_required
@cross_origin()
def get_all_user():
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
    print('删除评论：', req, type(req))
    if not req:
        return restful.params_error()
    else:
        l = LostFound.query.get(int(req))
        if l is not None and (
                l.user_id == current_user.id or current_user.kind >= 2):
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
    print('删除评论：', req, type(req))
    if not req:
        return restful.params_error()
    else:
        l = LostFound.query.get(int(req))
        if l is not None and (l.user_id != current_user.id) and l.kind == 1:
            l.status = 1
            l.claim_id=current_user.id
            db.session.add(l)
            db.session.commit()
            return restful.success(msg='认领成功')
        elif l is not None and (l.user_id != current_user.id) and l.kind == 0:
            l.status = 1
            l.claim_id = current_user.id
            db.session.add(l)
            db.session.commit()
            return restful.success(msg='上报成功')
        else:
            return restful.params_error()
