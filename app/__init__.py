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

from flask import Flask
from .extensions import *
from flask_cors import CORS

# .表示当前路径
from config import config  # 导入存储配置的字典

#  会记录客户端 IP
# 地址和浏览器的用户代理信息，如果发现异动就登出用户
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# 工厂函数
def creat_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)#产生n个字节的字符串
    temp=app.config['SECRET_KEY']
    print('我是SECRET_KEY',temp,type(temp))
    # print(temp.decode("utf-8","strict"))
    # print(str(temp,encoding='gb18030'))
    CORS(app, resources=r'/*')  # 允许所有域名跨域
    print('工厂函数执行了')
    # app.logger.info('工厂函数执行了')
    # app.config.from_pyfile('settings.py')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 实例化扩展
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # migrate.init_app(db,app)
    # 附加路由和自定义错误页面@app.route() @app.errorhandler
    from app.main import admin as admin_blueprint
    # 蓝本在工厂函数 create_app() 中注册到程序上
    app.register_blueprint(admin_blueprint)  # 管理员

    from app.main import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)  # 认证

    from app.main import user as user_blueprint
    app.register_blueprint(user_blueprint)  # 用户

    from app.main import page as page_blueprint
    app.register_blueprint(page_blueprint)  # 分页

    from app.main import category as category_blueprint
    app.register_blueprint(category_blueprint)  # 分类

    from app.main import notice as notice_blueprint
    app.register_blueprint(notice_blueprint)  # 通知

    from app.main import userlist as  userlist_blueprint
    app.register_blueprint(userlist_blueprint)  # 用户管理

    from app.main import found as  found_blueprint
    app.register_blueprint(found_blueprint)  # 用户管理

    from app.main import feedback as  feedback_blueprint
    app.register_blueprint(feedback_blueprint)  # 用户管理

    from app.main import detail as  detail_blueprint
    app.register_blueprint(detail_blueprint)  # 用户管理

    return app
