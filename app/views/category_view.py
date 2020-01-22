# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : category_view.py
@Time    : 2020/1/19 22:11
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
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

from main import category


@category.route('/')
def login():
    user = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "list": [
                {
                    "name": "书籍字画",
                    "about": "书籍、绘画等相关物品",
                    "image": None,
                    "creatorId": "1234",
                    "createTime": "2019-04-11 16:42:10",
                    "level": 1,
                    "targetId": "000"
                }
            ]
        },
        "ext": None
    }
    return render_template('home.html', user=user)


def logout():
    pass
