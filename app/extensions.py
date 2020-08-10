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

import logging

from flask_limiter import Limiter
from flask_login import LoginManager
from flask_mail import Mail  # 用SMTP发邮件
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

mail = Mail()  # QQ邮箱发邮件
migrate = Migrate()
db = SQLAlchemy()
login_manager = LoginManager()
redis_client = FlaskRedis()
cache = Cache()
limiter = Limiter()
logger = logging.getLogger('gunicorn.error')
