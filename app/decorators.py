# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : decorators.py
@Time    : 2020/2/3 20:41
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from functools import wraps

from flask import render_template, url_for, redirect, request
from flask_login import current_user

from app import OpenID, redis_client
from app.config import LoginConfig


def permission_required(permission_name):
    def dercorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            print('验证权限')
            if not current_user.can(permission_name) and current_user.kind == 1:
                messages = {
                    'success': False,
                    'msg': '非法访问,已记录!'
                }
                return render_template('mails/go.html', messages=messages)

            elif not current_user.can(permission_name):
                data = {
                    "success": False,
                    "code": 403,
                    "msg": "权限不足",
                    "data": {
                        "list": []
                    },
                    "ext": None
                }
                return data
            return func(*args, **kwargs)

        return decorator_function

    return dercorator


def admin_required(func):
    return permission_required('ADMIN')(func)


def super_admin_required(func):
    return permission_required('SUPER_ADMIN')(func)


def wechat_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        op = OpenID.query.filter(OpenID.user_id == current_user.id).first()
        print('判断用户是否关注公众号', )
        if current_user.status == 0:
            return redirect(url_for('auth.login')), 301
        if op is None:
            return redirect(url_for('oauth.index')), 301
        return func(*args, **kwargs)

    return decorated_view


def unfreeze_user(func):
    def decorated_view(*args, **kwargs):
        # 用户登陆自助解封
        uid = request.args.get("uid")
        if uid:
            op = OpenID.query.filter_by(wx_id=uid).first()
            if op:
                key = op.user.username + LoginConfig.LOGIN_REDIS_PREFIX
                redis_client.delete(key)
        return func(*args, **kwargs)

    return decorated_view
