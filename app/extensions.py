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
# from flask_mail_sendgrid import MailSendGrid
# from flask_celery import Celery
# from celery import Celery
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mongoengine import MongoEngine

bootstrap = Bootstrap()
# mail = MailSendGrid()
mail=Mail()
migrate = Migrate()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()
redis_client = FlaskRedis()
cache=Cache()
mongo_client=MongoEngine()
"""
Celery 客户端: 用于发布后台作业。当与 Flask 一起工作的时候，客户端与 Flask 应用一起运行。
Celery workers: 这些是运行后台作业的进程。Celery 支持本地和远程的 workers，因此你就可以在 Flask 服务器上启动一个单独的 worker，随后随着你的应用需求的增加而新增更多的 workers。
消息代理: 客户端通过消息队列和 workers 进行通信，Celery 支持多种方式来实现这些队列。最常用的代理就是 RabbitMQ 和 Redis。
"""




