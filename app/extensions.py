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
from flask_mail_sendgrid import MailSendGrid
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

bootstrap = Bootstrap()
mail = MailSendGrid()
migrate = Migrate()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
