# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : __init__.py
@Time    : 2020/1/18 15:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 构造文件
@Software: PyCharm
"""
import json
import os
import uuid
from logging.handlers import SMTPHandler, TimedRotatingFileHandler

import click
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user

from app.config import BaseConfig, basedir, PostConfig, LogConfig, AdminConfig
# .表示当前路径
from app.config import config  # 导入存储配置的字典
from tasks import celery
from .extensions import *
#  会记录客户端 IP
# 地址和浏览器的用户代理信息，如果发现异动就登出用户
from .models.open_model import OpenID
from .models.report_model import Report
from .models.role_model import Role
from .models.user_model import Guest, User
from .utils.log_utils import get_log, get_real_ip
from .utils.mail_sender import send_email
from .views.auth_view import get_login_info

login_manager.session_protection = 'basic'

from app.page import cached
from app.page import oauth
from app.page import comment
from app.page import detail
from app.page import feedback
from app.page import found
from app.page import users
from app.page import notice
from app.page import category
from app.page import user
from app.page import auth
from app.page import chart
from app.page import report
from app.page import tool
from app.page import log
from app.page import lab
from app.page import robot


# 工厂函数
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'
    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_errors(app)  # 注册错误处理函数
    register_shell_context(app)  # 注册shell上下文处理函数
    register_commands(app)  # 注册自定义shell命令
    register_template_context(app)
    return app


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(chart)  # 管理员
    app.register_blueprint(auth)  # 认证
    app.register_blueprint(user)  # 用户
    app.register_blueprint(category)  # 分类
    app.register_blueprint(notice)  # 通知
    app.register_blueprint(users)  # 用户管理
    app.register_blueprint(found)  # 用户管理
    app.register_blueprint(feedback)  # 用户管理
    app.register_blueprint(detail)  # 用户管理
    app.register_blueprint(comment)
    app.register_blueprint(oauth)
    app.register_blueprint(cached)
    app.register_blueprint(report)
    app.register_blueprint(tool)
    app.register_blueprint(log)
    app.register_blueprint(lab)
    # QQ群机器人
    app.register_blueprint(robot)


def register_extensions(app):  # 实例化扩展
    migrate.init_app(app, db)
    mail.init_app(app)  # 发送邮件
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = '你必须登陆后才能访问该页面'
    login_manager.login_view = 'auth.login'
    login_manager.anonymous_user = Guest
    redis_client.init_app(app)
    cache.init_app(app)
    limiter.__init__(key_func=get_real_ip, default_limits=["1000 per day", "200 per minute"])
    limiter.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        from app.models.feedback_model import Feedback
        from app.models.lostfound_model import LostFound
        from app.models.notice_model import Notice
        from app.models.permission_model import Permission
        from app.models.role_model import Role
        from app.models.user_model import User
        from app.models.comment_model import Comment
        from app.models.category_model import Category
        from app.models.robot_model import Robot

        return dict(
            app=app,
            db=db,
            User=User,
            Category=Category,
            Comment=Comment,
            Notice=Notice,
            LostFound=LostFound,
            Feedback=Feedback,
            Role=Role,
            Permission=Permission,
            OpenID=OpenID,
            Report=Report,
            Robot=Robot
        )


# 注册异步队列
def create_celery(app):
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def register_logging(app):
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            try:
                info = get_login_info(current_user, 1)
                record.url = request.url
                record.remote_addr = info.get("ip") + "- (" + info.get("addr")+")"
                record.username = "Guest" if isinstance(current_user._get_current_object(), Guest) else current_user.username
                return super(RequestFormatter, self).format(record)
            except:
                pass

    request_formatter = RequestFormatter(
        '[%(asctime)s] username:%(username)s - ip:%(remote_addr)s - url:%(url)s\n'
        '%(levelname)s thread -%(thread)d  - %(module)s - %(funcName)s line:%(lineno)d : %(message)s'
    )

    file_handler = TimedRotatingFileHandler(
        "logs/log", when="D", interval=1, backupCount=30,
        encoding="UTF-8", delay=False, utc=True)
    file_handler.setFormatter(request_formatter)
    file_handler.setLevel(logging.DEBUG)

    class SSLSMTPHandler(SMTPHandler):
        def emit(self, record):
            """
            Emit a record.
            """
            try:
                # 将错误信息的Hash值存入Redis设置过期时间，防止重复发送
                key = LogConfig.LOG_REDIS_PREFIX + str(record.exc_text.__hash__())
                obj = redis_client.get(key)
                if not obj:
                    # 如果记录以及存在，则不发送
                    messages = {
                        "msg": self.format(record)
                    }
                    send_email.apply_async(args=(AdminConfig.SUPER_ADMIN_QQ, "异常通知", 'taskError', messages),
                                           countdown=1)
                    redis_client.set(key, record.exc_text)
                    redis_client.expire(key, LogConfig.LOG_REDIS_TIME)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)

    mail_handler = SSLSMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=AdminConfig.SUPER_ADMIN_QQ,
        subject='异常通知',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    # loggers = [app.logger, logging.getLogger('sqlalchemy'), logging.getLogger('werkzeug')]
    loggers = [app.logger, logging.getLogger('sqlalchemy')]
    for logger in loggers:
        logger.addHandler(file_handler)
        logger.addHandler(mail_handler)
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)


# 模板上下文
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        # CDN加速的地址
        cdn_url = os.getenv("CDN_URL")
        return dict(cdnUrl=cdn_url)


def register_commands(app):
    @app.cli.command()
    @click.option('--content', default='世界你好')
    def hello(content):
        click.echo('Shell测试消息...')
        logger.info('这是默认消息' + content)

    @app.cli.command()
    def initrole():
        """初始化用户角色"""
        click.echo("Initing roles and permissions...")
        from app.models.role_model import Role
        Role.init_role()
        click.echo("Done.")

    @app.cli.command()
    # prompt=True二次输入
    @click.option('--username', prompt=True, help='组织用户名.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='组织.')
    @click.option('--qq', prompt=True, confirmation_prompt=True, help='官方QQ.')
    # 初始化公用账号
    def initpub(username, password, qq):
        """Building Bluelog, just for you."""
        click.echo('Initializing the publi user...')
        db.create_all()
        public = User.query.filter_by(username=username).first()
        if public is not None:
            click.echo('The administrator already exists, updating...')
            public.username = username
            public.set_password(password)
        else:
            click.echo('Creating the temporary public account...')
            public = User(username=username, password=password, real_name='三峡大学失物招领中心', academy='部门账号',
                          class_name='部门账号', major='部门账号', qq=qq, kind=1, gender=2, status=2)
            db.session.add(public)
            db.session.commit()
            op = OpenID(qq_id=None, wx_id=None, user_id=public.id)
            db.session.add(op)
            db.session.commit()


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        if not isinstance(current_user._get_current_object(), Guest):
            data = get_log()
            return render_template('errors/400.html', data=data), 400
        else:
            return redirect(url_for('auth.login')), 301

    @app.errorhandler(404)
    def page_not_found(e):
        if not isinstance(current_user._get_current_object(), Guest):
            # logger.info(e)
            return render_template('errors/404.html'), 404
        else:
            return redirect(url_for('auth.login')), 301

    # 捕获并记录错误信息
    @app.errorhandler(405)
    def method_not_allowed(e):
        # 当前用户不是匿名用户的时候执行
        if not isinstance(current_user._get_current_object(), Guest):
            logger.info("当前用户信息")
            logger.info(current_user.real_name)
            data = get_log()
            key = LogConfig.REDIS_INFO_LOG_KEY+uuid.uuid4().hex
            redis_client.set(key, json.dumps(data))
            redis_client.expire(key, LogConfig.REDIS_EXPIRE_TIME)
            return render_template('errors/405.html', data=data), 405
        else:
            return redirect(url_for('auth.login')), 301

    # 捕获并记录错误信息
    @app.errorhandler(500)
    def internal_server_error(e):
        if not isinstance(current_user._get_current_object(), Guest):
            data = get_log()
            key = LogConfig.REDIS_ERROR_LOG_KEY+uuid.uuid4().hex
            redis_client.set(key, json.dumps(data))
            redis_client.expire(key, LogConfig.REDIS_EXPIRE_TIME)
            return render_template('errors/500.html', data=data), 500
        else:
            return redirect(url_for('auth.login')), 301

    @app.errorhandler(429)
    def ratelimit_handler(e):
        if not isinstance(current_user._get_current_object(), Guest):
            data = get_log()
            data.update(user=current_user.username)
            key = LogConfig.REDIS_ERROR_LOG_KEY+uuid.uuid4().hex
            redis_client.set(key, json.dumps(data))
            redis_client.expire(key, LogConfig.REDIS_EXPIRE_TIME)
            return render_template('errors/429.html', data=data), 429
        else:
            return "403 Forbidden", 403
