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
import logging
import os
import uuid
from logging.handlers import RotatingFileHandler, SMTPHandler

import click
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from app.config import BaseConfig, basedir, PostConfig, LogConfig
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
from .views.auth_view import get_login_info
from .views.log_view import get_log

login_manager.session_protection = 'basic'

from app.page import cached as cache_bp
from app.page import oauth as pusher_bp
from app.page import comment as comment_bp
from app.page import detail as detail_bp
from app.page import feedback as feedback_bp
from app.page import found as found_bp
from app.page import userlist as userlist_bp
from app.page import notice as notice_bp
from app.page import category as category_bp
from app.page import user as user_bp
from app.page import auth as auth_bp
from app.page import chart as admin_bp
from app.page import report as report_bp
from app.page import tool as tool_bp


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
    # register_interceptor(app)  # 拦截器
    return app


def register_blueprints(app):
    app.register_blueprint(admin_bp)  # 管理员
    app.register_blueprint(auth_bp)  # 认证
    app.register_blueprint(user_bp)  # 用户
    app.register_blueprint(category_bp)  # 分类
    app.register_blueprint(notice_bp)  # 通知
    app.register_blueprint(userlist_bp)  # 用户管理
    app.register_blueprint(found_bp)  # 用户管理
    app.register_blueprint(feedback_bp)  # 用户管理
    app.register_blueprint(detail_bp)  # 用户管理
    app.register_blueprint(comment_bp)
    app.register_blueprint(pusher_bp)
    app.register_blueprint(cache_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(tool_bp)


def register_extensions(app):  # 实例化扩展
    print('注册扩展')
    migrate.init_app(app, db)
    # bootstrap.init_app(app)
    mail.init_app(app)  # 发送邮件
    # moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = '你必须登陆后才能访问该页面'
    login_manager.login_view = 'auth.login'
    login_manager.anonymous_user = Guest
    # toolbar.init_app(app)
    redis_client.init_app(app)
    cache.init_app(app)
    # mongo_client.init_app(app)


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
            Report=Report
        )


# 注册异步队列
def create_celery(app):
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


"""
    # 一般之前的配置没有这个，需要添加上
    celery.conf.ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': 'redis://localhost:6379/2',
            'default_timeout': 60 * 60
        }
    }
    """


# Attach to celery object for easy access.

def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler('logs/app.log',
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['547142436@qq.com'],
        subject='系统错误通知',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


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
        print('这是默认消息' + content)

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
            print('共有账户的ID', public.id)
            op = OpenID(qq_id=None, wx_id=None, user_id=public.id)
            print('创建开发平台ID')
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
            # print(e)
            return render_template('errors/404.html'), 404
        else:
            return redirect(url_for('auth.login')), 301

    # 捕获并记录错误信息
    @app.errorhandler(405)
    def method_not_allowed(e):
        # 当前用户不是匿名用户的时候执行
        if not isinstance(current_user._get_current_object(), Guest):
            print("当前用户信息")
            print(current_user.real_name)
            data = get_log()
            key = uuid.uuid4().hex + LogConfig.REDIS_INFO_LOG_KEY
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
            key = uuid.uuid4().hex + LogConfig.REDIS_ERROR_LOG_KEY
            redis_client.set(key, json.dumps(data))
            redis_client.expire(key, LogConfig.REDIS_EXPIRE_TIME)
            return render_template('errors/500.html', data=data), 500
        else:
            return redirect(url_for('auth.login')), 301

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        if not isinstance(current_user._get_current_object(), Guest):
            return render_template(
                'errors/400.html', description=e.description), 400
        else:
            return redirect(url_for('auth.login')), 301


def register_interceptor(app):
    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
