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

from flask import render_template
from flask_login import current_user

from app import OpenID


def permission_required(permission_name):
    def dercorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            print('验证权限')
            if not current_user.can(permission_name) and current_user.kind != 1:
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
            elif not current_user.can(permission_name) and current_user.kind == 1:
                messages = {
                    'msg': '非法访问'
                }
                return render_template('mails/go.html', messages=messages)
            return func(*args, **kwargs)

        return decorator_function

    return dercorator


def admin_required(func):
    return permission_required('ADMIN')(func)


def super_admin_required(func):
    return permission_required('SUPER_ADMIN')(func)

    # :param func: 其实就是要装饰的函数


def wechat_required(func=None, param=None):
# def wechat_required(func, *args, **kwargs):
    # def dercorator(func):
    @wraps(func)
    def func_wx(*args, **kwargs):
        op = OpenID.query.filter(OpenID.user_id == current_user.id)
        print('判断用户是否关注公众号', )
        if op is None:
            messages = {
                'msg': '请完成微信绑定'
            }
            return render_template('mails/go.html', messages=messages)
        return func(*args, **kwargs)  # 通过

    return func_wx

# return dercorator
