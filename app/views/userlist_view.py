# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : userlist_view.py
@Time    : 2020/1/23 22:41
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template, request, current_app
from sqlalchemy import desc

from app import db
from app.main import userlist
from app.models.user_model import User


@userlist.route('/', methods=['POST', 'GET', 'OPTIONS'], strict_slashes=False)
def index():
    return render_template('userlist.html')
    # return data


@userlist.route('/getall', methods=['POST', 'GET', 'OPTIONS'], strict_slashes=False)
def get_all():

    req = request.json
    print(req)
    print('get_users收到请求')
    page=int(req['pageNum'])
    pagination = User.query.order_by(User.kind.desc()).paginate(page+1, per_page=current_app.config[
        'ARTISAN_POSTS_PER_PAGE'], error_out=False)
    users = pagination.items
    # users = User.query.order_by(desc('kind')).all()
    print(users)
    list = []
    cnt = len(users)
    for u in users:
        dict = {
            "userId": u.id,
            "name": u.real_name,
            "username": u.username,
            "gender": '男' if u.gender == 0 else '女',
            "qq": u.qq,
            "classNum": u.class_name,
            "major": u.major,
            "academy": u.academy,
            "lastLogin": u.last_login.strftime('%Y-%m-%d %H:%M:%S'),
            "status": "正常" if u.status == 1 else '已冻结',
            "kind": u.kind
        }
        list.append(dict)
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "page": {
                "total": pagination.total,
                "totalPage": pagination.pages,
                "pageNum": req['pageNum'],
                "pageSize": current_app.config['ARTISAN_POSTS_PER_PAGE'],
                "list": list
            }
        },
        "ext": None
    }
    return data


@userlist.route('/freeze', methods=['POST'], strict_slashes=False)
def user_freeze_or_unfreeze():
    req = request.args.get('userId')
    u = User.query.get(int(req))
    u.status = 1 if u.status == 0 else 0
    db.session.commit()
    data = {
        "success": True,
        "code": 1001,
        "msg": "发生异常：Failed messages: com.sun.mail.smtp.SMTPSendFailedException: 501 Mail from address must be same as authorization user.\n;\n  nested exception is:\n\tcom.sun.mail.smtp.SMTPSenderFailedException: 501 Mail from address must be same as authorization user.\n",
        "data": {},
        "ext": "org.springframework.mail.MailSendException"
    }
    print('要给用户发送提醒邮件')
    return data


@userlist.route('/resetPassword', methods=['POST'], strict_slashes=False)
def reset_pssword():
    req = request.args.get('userId')
    print('request.args', req)
    u = User.query.get(int(req))
    u.password = '123456'
    db.session.commit()
    print('发送邮件')
    data = {
        "success": True,
        "code": 1001,
        "msg": "发生异常：Failed messages: com.sun.mail.smtp.SMTPSendFailedException: 501 Mail from address must be same as authorization user.\n;\n  nested exception is:\n\tcom.sun.mail.smtp.SMTPSenderFailedException: 501 Mail from address must be same as authorization user.\n",
        "data": {},
        "ext": "org.springframework.mail.MailSendException"
    }
    return data


@userlist.route('/setAsAdmin', methods=['POST'], strict_slashes=False)
def set_or_cancle_admin():
    req = request.args.get('userId')
    print('request.args', req)
    u = User.query.get(int(req))
    u.kind = 2 if u.kind==1 else 1
    db.session.commit()
    print('发送邮件')
    data = {
        "success": True,
        "code": 1001,
        "msg": "发生异常：Failed messages: com.sun.mail.smtp.SMTPSendFailedException: 501 Mail from address must be same as authorization user.\n;\n  nested exception is:\n\tcom.sun.mail.smtp.SMTPSenderFailedException: 501 Mail from address must be same as authorization user.\n",
        "data": {},
        "ext": "org.springframework.mail.MailSendException"
    }
    return data
