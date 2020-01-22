# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : home_view.py
@Time    : 2020/1/19 22:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template
from flask_cors import cross_origin

from app.main import home


@home.route('/', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
def login():
    user = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "user": {
                "studentNum": "201520180508",
                "realName": "cpwu",
                "icon": "www.baidu.com/icon.png",
                "email": "cpwu@foxmail.com",
                "phoneNumber": "15911112222",
                "schoolName": "东华理工大学",
                "gender": 1,
                "createTime": "2019-04-10 19:06:10",
                "lastLogin": "2019-04-10 19:06:10",
                "kind": 0
            }
        },
        "ext": None
    }
    return render_template('home.html', user=user)


def logout():
    pass
