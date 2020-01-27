# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : config.py
@Time    : 2020/1/10 16:30
@Author  : iBoy
@Email   : iboy@iboy.tech
@Software: PyCharm
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 基类配置
class Config:
    FLASK_RUN_HOST = '127.0.0.1'
    FLASK_RUN_PORT = 80
    PIPENV_DONT_LOAD_ENV = 1
    FLASK_DEBUG = True
    SECRET_KEY = os.urandom(24) #随机秘钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    FLASKY_MAIL_SUBJECT_PREFIX = ['Flasky']
    FLASKY_MAIL_SENDER = 'FLASK Admin <547142436@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')


    @staticmethod
    def init_app(app):
        print('app初始化了')
        pass


# 开发环境的子类配置
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'


# 测试环境的子类配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'


# 生产环境的配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'


# 注册不同的开发环境和默认的开发环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
