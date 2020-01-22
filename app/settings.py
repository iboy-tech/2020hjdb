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
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = ['Flasky']
    FLASKY_MAIL_SENDER = 'FLASK Admin <547142436@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    APPID = 'wx18d48283a9869675'
    APPSECRET = '7d8ff3809716bba9b05aa489bb931ef6'

    @staticmethod
    def init_app(app):
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
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/lost_found'


# 测试环境的子类配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


# 生产环境的配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# 注册不同的开发环境和默认的开发环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
