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

chart = Blueprint('chart', __name__, url_prefix='/chart.html')
auth = Blueprint('auth', __name__)
user = Blueprint('user', __name__, url_prefix='/user')
category = Blueprint('category', __name__, url_prefix='/categories')
notice = Blueprint('notice', __name__, url_prefix='/notices')
users = Blueprint('users', __name__, url_prefix='/users')
found = Blueprint('found', __name__, url_prefix='/lostfounds')
feedback = Blueprint('feedback', __name__, url_prefix='/feedbacks')
detail = Blueprint('detail', __name__, url_prefix='/detail')
comment = Blueprint('comment', __name__, url_prefix='/comments')
oauth = Blueprint('oauth', __name__, url_prefix='/oauth')
cached = Blueprint('cache', __name__, url_prefix='/cache.html')
report = Blueprint('report', __name__, url_prefix='/reports')
tool = Blueprint('tool', __name__, url_prefix='/tools')
log = Blueprint('log', __name__, url_prefix='/log.html')
lab = Blueprint('lab', __name__, url_prefix='/lab.html')
# QQ群机器人
robot = Blueprint('robot', __name__, url_prefix='/robots')
# 防止循环导包
from ..views import chart_view, auth_view, user_view, category_view, notice_view, comment_view, \
    feedback_view, users_view, found_view, detail_view, oauth_view, cache_view, report_view, tool_view, log_view, \
    lab_view, robot_view
