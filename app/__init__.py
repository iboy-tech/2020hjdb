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
import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler

import click
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFError

from .extensions import *
from flask_cors import CORS

# .表示当前路径
from app.config import config  # 导入存储配置的字典

#  会记录客户端 IP
# 地址和浏览器的用户代理信息，如果发现异动就登出用户
from .models.open_model import OpenID
from .models.role_model import Role
from .models.user_model import Guest, User

login_manager.session_protection = 'basic'

from app.main import admin as admin_bp
from app.main import auth as auth_bp
from app.main import user as user_bp
from app.main import page as page_bp
from app.main import category as category_bp
from app.main import notice as notice_bp
from app.main import userlist as  userlist_bp
from app.main import found as  found_bp
from app.main import feedback as  feedback_bp
from app.main import detail as  detail_bp
from app.main import comment as  comment_bp
from app.main import pusher as  pusher_bp
from app.main import cached as cache_bp


# 工厂函数
def create_app(config_name=None):
    print('MAIL_USERNAME', os.getenv('MAIL_USERNAME'))
    print('MAIL_PASSWORD', os.getenv('MAIL_PASSWORD'))
    print('MAIL_SERVER', os.getenv('MAIL_SERVER'))
    print('MAIL_PORT', os.getenv('MAIL_PORT'))
    print('MAIL_USE_SSL', os.getenv('MAIL_USE_SSL'))
    print('MAIL_DEFAULT_SENDER', os.getenv('MAIL_DEFAULT_SENDER'))
    print('QQ_AVATAR_API', os.getenv('QQ_AVATAR_API'))
    print('MAIL_SUBJECT_PREFIX', os.getenv('MAIL_SUBJECT_PREFIX'))
    print('SECRET_KEY', os.getenv('SECRET_KEY'))
    print('PATH_OF_IMAGES_DIR', os.getenv('PATH_OF_IMAGES_DIR'))

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['MAIL_DEFAULT_SENDER'] = '三峡大学失物招领处<547142436@qq.com>'
    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'
    app.config.from_object(config[config_name])
    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_errors(app)  # 注册错误处理函数
    register_shell_context(app)  # 注册shell上下文处理函数
    register_commands(app)  # 注册自定义shell命令

    CORS(app, supports_credentials=True, resources=r'/*')  # 允许所有域名跨域

    # config[config_name].init_app(app)
    return app


def register_blueprints(app):
    app.register_blueprint(admin_bp)  # 管理员
    app.register_blueprint(auth_bp)  # 认证
    app.register_blueprint(user_bp)  # 用户
    app.register_blueprint(page_bp)  # 分页
    app.register_blueprint(category_bp)  # 分类
    app.register_blueprint(notice_bp)  # 通知
    app.register_blueprint(userlist_bp)  # 用户管理
    app.register_blueprint(found_bp)  # 用户管理
    app.register_blueprint(feedback_bp)  # 用户管理
    app.register_blueprint(detail_bp)  # 用户管理
    app.register_blueprint(comment_bp)
    app.register_blueprint(pusher_bp)
    app.register_blueprint(cache_bp)


def register_extensions(app):  # 实例化扩展
    print('注册扩展')
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)  # 发送邮件
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = '你必须登陆后才能访问该页面'
    login_manager.login_view = 'auth.login'
    login_manager.anonymous_user = Guest
    toolbar.init_app(app)
    redis_client.init_app(app)
    cache.init_app(app)
    # socketio.init_app(app)


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

        return dict(app=app, db=db, User=User, Category=Category,
                    Comment=Comment, Notice=Notice, LostFound=LostFound, Feedback=Feedback, Role=Role,
                    Permission=Permission, OpenID=OpenID)


def register_logging(app):
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 日志超过10MB会被覆盖
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=os.getenv('MAIL_SERVER'),
        fromaddr=os.getenv('MAIL_USERNAME'),
        toaddrs=os.getenv('SUPER_ADMIN_EMAIL'),
        subject='应用程序错误通知',
        credentials=(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD')))

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)
    # if not app.debug:
    #     app.logger.addHandler(file_handler)
    app.logger.addHandler(file_handler)


#
# def register_template_context(app):
#     @app.context_processor
#     def make_template_context():
#         pass

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
    def createuser():
        create_test_data()


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html', ), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400
