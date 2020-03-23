# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : log_view.py
@Time    : 2020/3/23 21:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import request
from flask_login import current_user

from app import get_login_info


def get_log():
    data = get_login_info(current_user, 1)  # 仅仅获取IP信息
    print(request.url)
    print(request.query_string)
    print(data)
    data.pop("is_admin")
    ext = {
        "url": request.url,
        "username": current_user.username
    }
    data.update(ext)
    return data