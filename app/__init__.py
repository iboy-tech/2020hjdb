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

import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from .extensions import *
from flask_cors import CORS

# .表示当前路径
from config import config  # 导入存储配置的字典

#  会记录客户端 IP
# 地址和浏览器的用户代理信息，如果发现异动就登出用户
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
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

# 工厂函数
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'
    app.config.from_object(config[config_name])
    # register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    # register_commands(app)  # 注册自定义shell命令
    register_errors(app)  # 注册错误处理函数
    # register_shell_context(app)  # 注册shell上下文处理函数
    # register_template_context(app)  # 注册模板上下文处理函数
    # app.config['SECRET_KEY'] = os.urandom(24)  # 产生n个字节的字符串
    # temp = app.config['SECRET_KEY']
    # print('我是SECRET_KEY', temp, type(temp))
    # print(temp.decode("utf-8","strict"))
    # print(str(temp,encoding='gb18030'))
    CORS(app,supports_credentials=True, resources=r'/*')  # 允许所有域名跨域
    # print('工厂函数执行了')
    # app.logger.info('工厂函数执行了')
    # app.config.from_pyfile('settings.py')

    config[config_name].init_app(app)
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


def register_extensions(app):  # 实例化扩展
    bootstrap.init_app(app)
    mail.init_app(app)#发送邮件
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


# def register_shell_context(app):
#     @app.shell_context_processor
#     def make_shell_context():
#         pass

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400

# def register_logging(app):
#     pass
#
#
# def register_template_context(app):
#     @app.context_processor
#     def make_template_context():
#         pass
# def register_commands(app):
#     @app.cli.command()
#     @click.option('--drop', is_flag=True, help='Create after drop.')
#     def initdb(drop):
#         pass






