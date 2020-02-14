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
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db, cache
from app.decorators import super_admin_required, admin_required
from app.main import userlist
from app.models.user_model import User
from app.untils import restful
from app.untils.mail_sender import send_email


@userlist.route('/', methods=['POST', 'GET', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def index():
    return render_template('userlist.html')


@userlist.route('/getall', methods=['POST', 'GET'], strict_slashes=False)
# @cache.cached(timeout=10 * 60)#缓存10分钟 默认为300s
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
                User.gender == 1).order_by(User.kind.desc(), User.status).paginate(page + 1
                                                                                   , per_page=current_app.config[
                    'ARTISAN_POSTS_PER_PAGE'], error_out=False)
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
                User.kind >= 2).order_by(User.kind.desc(), User.status).paginate(page + 1,
                                                                                 per_page=current_app.config[
                                                                                     'ARTISAN_POSTS_PER_PAGE'],
                                                                                 error_out=False)
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
    u = User.query.get_or_404(int(req))
    if u.status == 1:
        return restful.success(success=False, msg='该账户尚未认证，暂时无法冻结')
    elif u.status == 2:
        u.status = 0
        messages = {
            'realName': u.real_name,
            'handlerName': current_user.real_name,
            'handlerEmail': current_user.qq + '@qq.com',
        }
        send_email.apply_async(args=('849764742', '账户冻结通知', 'userFreeze', messages))
    elif u.status == 0:
        u.status = 2
        messages = {
            'realName': u.real_name,
            'handlerName': current_user.real_name,
            'handlerEmail': current_user.qq + '@qq.com',
        }
        send_email.apply_async(args=('849764742', '账户恢复通知', 'userunFreeze', messages))
    print('要给用户发送提醒邮件')
    db.session.commit()
    return restful.success()


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
    messages = {
        'username': u.username,
        'password': '123456',
        'realName': u.real_name,
        'handlerName': current_user.real_name,
        'handlerEmail': current_user.qq + '@qq.com',
    }
    send_email.apply_async(args=('849764742', '密码重置提醒', 'resetPassword', messages))
    print('要给用户发送提醒邮件')
    return restful.success()


@userlist.route('/setAsAdmin', methods=['POST'], strict_slashes=False)
@super_admin_required
def set_or_cancle_admin():
    req = request.args.get('userId')
    print('request.args', req)
    u = User.query.get(int(req))
    u.kind = 2 if u.kind == 1 else 1
    db.session.commit()
    print('发送邮件')
    return restful.success()


@cache.memoize()  # 根据参数设置缓存
def search(pagination, page):
    global data
    users = pagination.items
    # users = User.query.order_by(desc('kind')).all()
    # print(users)
    list = []
    for u in users:
        dict = u.to_dict()
        list.append(dict)
        data = {
            "page": {
                "total": pagination.total,
                "totalPage": pagination.pages,
                "pageNum": page,
                "pageSize": current_app.config['ARTISAN_POSTS_PER_PAGE'],
                "list": list
            }
        }
    return restful.success(data=data)


@userlist.route('/userInfo', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def get_userinfo():
    id = int(request.args.get('userId'))
    u = User.query.get_or_404(id)
    data = {
        "user": u.to_dict()
    }
    return restful.success(data=data)
