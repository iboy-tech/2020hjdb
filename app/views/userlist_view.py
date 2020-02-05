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
from datetime import datetime

from flask import render_template, request, current_app
from flask_login import current_user, login_required
from sqlalchemy import desc, or_

from app import db
from app.main import userlist
from app.models.user_model import User
from app.decorators import permission_required, super_admin_required, admin_required


@userlist.route('/', methods=['POST', 'GET', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def index():
    return render_template('userlist.html')
    # return data



@userlist.route('/getall', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def get_all():
    req = request.json
    print(req)
    page = int(req['pageNum'])
    keyword = req['keyword']
    if keyword == '':
        print('get_users收到请求')
        pagination = User.query.order_by(User.kind.desc(), User.status).paginate(page + 1, per_page=current_app.config[
            'ARTISAN_POSTS_PER_PAGE'], error_out=False)
        data = search(pagination, page)
        return data
    else:
        if keyword == '男':
            pagination = User.query.filter(
                User.gender == 0).order_by(User.kind.desc(), User.status).paginate(page + 1,
                                                                                   per_page=current_app.config[
                                                                                       'ARTISAN_POSTS_PER_PAGE'],
                                                                                   error_out=False)
            data = search(pagination, page)
            return data
        elif keyword == '女':
            pagination = User.query.filter(
                User.gender == 1).order_by(User.kind.desc(), User.status).paginate(page + 1,
                                                                                   per_page=current_app.config[
                                                                                       'ARTISAN_POSTS_PER_PAGE'],
                                                                                   error_out=False)
            data = search(pagination, page)
            return data
        elif '正常' in keyword:
            pagination = User.query.filter(
                User.status == 1).order_by(User.kind.desc(), User.status).paginate(page + 1,
                                                                                   per_page=current_app.config[
                                                                                       'ARTISAN_POSTS_PER_PAGE'],
                                                                                   error_out=False)
            data = search(pagination, page)
            return data
        elif '冻结' in keyword:
            pagination = User.query.filter(
                User.status == 0).order_by(User.kind.desc(), User.status).paginate(page + 1,
                                                                                   per_page=current_app.config[
                                                                                       'ARTISAN_POSTS_PER_PAGE'],
                                                                                   error_out=False)
            data = search(pagination, page)
            return data
        elif '认证' in keyword:
            pagination = User.query.filter(
                User.status == 2).order_by(User.kind.desc(), User.status).paginate(page + 1,
                                                                                   per_page=current_app.config[
                                                                                       'ARTISAN_POSTS_PER_PAGE'],
                                                                                   error_out=False)
            data = search(pagination, page)
            return data
        elif '管理' in keyword:
            pagination = User.query.filter(
                User.kind >= 2).order_by(User.kind.desc(), User.status).paginate(page + 1, per_page=current_app.config[
                'ARTISAN_POSTS_PER_PAGE'], error_out=False)
            data = search(pagination, page)
            return data
        else:
            pagination = User.query.filter(or_(
                User.real_name.like("%" + keyword + "%"),
                User.username.like("%" + keyword + "%"),
                User.qq.like("%" + keyword + "%"),
                User.class_name.like("%" + keyword + "%"),
                User.major.like("%" + keyword + "%"),
                User.academy.like("%" + keyword + "%"),
                User.kind.like("%" + keyword + "%"),
            )).order_by(User.kind.desc(), User.status).paginate(page + 1, per_page=current_app.config[
                'ARTISAN_POSTS_PER_PAGE'], error_out=False)
        data = search(pagination, page)
        return data



@userlist.route('/freeze', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def user_freeze_or_unfreeze():
    req = request.args.get('userId')
    u = User.query.get(int(req))
    u.status = 1 if u.status == 0 else 0
    db.session.commit()
    data = {
        "success": True,
        "code": 1001,
        "msg": "发生异常：Failed messages: com.sun.mails.smtp.SMTPSendFailedException: 501 Mail from address must be same as authorization user.\n;\n  nested exception is:\n\tcom.sun.mails.smtp.SMTPSenderFailedException: 501 Mail from address must be same as authorization user.\n",
        "data": {},
        "ext": "org.springframework.mails.MailSendException"
    }
    print('要给用户发送提醒邮件')
    from app.untils.mail_sender import send_email
    messages = {
        'realName': u.real_name,
        'handlerName': datetime.now.strftime('%Y-%m-%d %H:%M:%S'),
        'handlerEmail': current_user.qq + '@qq.com',
        'appName': '三峡大学失物招领处'
    }
    send_email('yang.hao@aliyun.com', '账户冻结通知', 'userFreeze', messages)
    return data



@userlist.route('/resetPassword', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
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
        "msg": "发生异常：Failed messages: com.sun.mails.smtp.SMTPSendFailedException: 501 Mail from address must be same as authorization user.\n;\n  nested exception is:\n\tcom.sun.mails.smtp.SMTPSenderFailedException: 501 Mail from address must be same as authorization user.\n",
        "data": {},
        "ext": "org.springframework.mails.MailSendException"
    }
    return data



@userlist.route('/setAsAdmin', methods=['POST'], strict_slashes=False)
@super_admin_required
def set_or_cancle_admin():
    req = request.args.get('userId')
    print('request.args', req)
    u = User.query.get(int(req))
    u.kind = 2 if u.kind == 1 else 1
    db.session.commit()
    print('发送邮件')
    data = {
        "success": True,
        "code": 1001,
        "msg": "发生异常：Failed messages: com.sun.mails.smtp.SMTPSendFailedException: 501 Mail from address must be same as authorization user.\n;\n  nested exception is:\n\tcom.sun.mails.smtp.SMTPSenderFailedException: 501 Mail from address must be same as authorization user.\n",
        "data": {},
        "ext": "org.springframework.mails.MailSendException"
    }
    return data



def search(pagination, page):
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
                "pageNum": page,
                "pageSize": current_app.config['ARTISAN_POSTS_PER_PAGE'],
                "list": list
            }
        },
        "ext": None
    }
    return data



@userlist.route('/userInfo', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def get_userinfo():
    id = int(request.args.get('userId'))
    u = User.query.get_or_404(id)
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "user": {
                "userId": u.id,
                "name": u.real_name,
                "username": u.username,
                "gender": "男" if u.gender == 0 else "女",
                "qq": u.qq,
                "classNum": u.class_name,
                "major": u.major,
                "academy": u.academy,
                "lastLogin": u.last_login.strftime('%Y-%m-%d %H:%M:%S'),
                "status": '正常' if u.status == 1 else '正常',
                "kind": u.kind
            }
        },
        "ext": None
    }
    return data
