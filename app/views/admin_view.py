# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : admin_view.py
@Time    : 2020/1/19 21:21
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template, request
from flask_login import login_required

from app.decorators import admin_required
from app.main import admin

print('视图文件加载')


@admin.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    print('蓝图请求成功！')
    return render_template('admin.html')
