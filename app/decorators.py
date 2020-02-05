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

from flask_login import current_user


def permission_required(permission_name):
    def dercorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            print('验证权限')
            if not current_user.can(permission_name):
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
