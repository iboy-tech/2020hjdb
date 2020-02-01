# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : __init__.py
@Time    : 2020/1/18 12:59
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 蓝本的构造文件
@Software: PyCharm
"""
from flask import Blueprint

# 蓝本的名字和蓝本所在的包或模块。和程序一样，大多数情况下第二个参数使用 Python 的
# __name__ 变量即可。
admin = Blueprint('admin', __name__, url_prefix='/admin')
auth = Blueprint('auth', __name__)
user = Blueprint('user', __name__, url_prefix='/user')
category = Blueprint('category', __name__, url_prefix='/category')
page = Blueprint('page', __name__, url_prefix='/page')
notice = Blueprint('notice', __name__, url_prefix='/notice')
userlist = Blueprint('userlist', __name__, url_prefix='/userlist')
found = Blueprint('found', __name__, url_prefix='/found')
feedback = Blueprint('feedback', __name__, url_prefix='/feedback')
detail= Blueprint('detail', __name__, url_prefix='/detail')
comment= Blueprint('comment', __name__, url_prefix='/comment')
from ..views import admin_view, auth_view, user_view, category_view, page_view, notice_view, comment_view, \
    feedback_view, userlist_view,found_view,detail_view

print('main蓝图注册了')
