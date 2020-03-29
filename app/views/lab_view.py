# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : lab_view.py
@Time    : 2020/3/28 21:00
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template
from flask_login import login_required

from app.decorators import super_admin_required
from app.page import lab


@lab.route('/', strict_slashes=False)
@login_required
@super_admin_required
def index():
    return render_template('lab.html')
