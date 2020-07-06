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
user = Blueprint('user', __name__, url_prefix='/user.html')
category = Blueprint('category', __name__, url_prefix='/category.html')
notice = Blueprint('notice', __name__, url_prefix='/notice.html')
userlist = Blueprint('userlist', __name__, url_prefix='/users.html')
found = Blueprint('found', __name__, url_prefix='/found.html')
feedback = Blueprint('feedback', __name__, url_prefix='/feedback.html')
detail = Blueprint('detail', __name__, url_prefix='/detail')
comment = Blueprint('comment', __name__, url_prefix='/comment')
oauth = Blueprint('oauth', __name__, url_prefix='/oauth')
cached = Blueprint('cache', __name__, url_prefix='/cache.html')
report = Blueprint('report', __name__, url_prefix='/report.html')
tool = Blueprint('tool', __name__, url_prefix='/tool.html')
log = Blueprint('log', __name__, url_prefix='/log.html')
lab = Blueprint('lab', __name__, url_prefix='/lab.html')
# 防止循环导包
from ..views import chart_view, auth_view, user_view, category_view, notice_view, comment_view, \
    feedback_view, userlist_view, found_view, detail_view, oauth_view, cache_view, report_view, tool_view, log_view, \
    lab_view
