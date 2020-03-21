# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : check_data.py
@Time    : 2020/3/21 9:34
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 对用户请求内容做合法性校验
@Software: PyCharm
"""
from functools import wraps

from flask import request


def check(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # 用户登陆自助解封
        req = request.json

        return func(*args, **kwargs)

        return decorated_view

    return decorated_view