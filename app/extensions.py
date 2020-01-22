# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : extensions.py
@Time    : 2020/1/13 17:29
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 初始化扩展
@Software: PyCharm
"""
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
