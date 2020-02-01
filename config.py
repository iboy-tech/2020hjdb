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
    PIPENV_DONT_LOAD_ENV = 1
    FLASK_DEBUG = True
    SECRET_KEY = os.urandom(24) #随机秘钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '三峡大学失物招领处：'
    FLASKY_MAIL_SENDER = '三峡大学失物招领处 <ctgu@iboy.tech>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MXA_ATTEMPT_NUMBER = 5
    ARTISAN_POSTS_PER_PAGE=120
    MAIL_SENDGRID_API_KEY = 'SG.Ksvhquq2TJuXgwKPWeuJCw.9-8CZEP5Tp9mG8P8ypoouGNqgoC48vYwdb8qQTEr9Xg'
    MAIL_DEFAULT_SENDER='ctgu@iboy.tech'
    QQ_AVATAR_API='https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'


    @staticmethod
    def init_app(app):
        print('app初始化了')
        pass


# 开发环境的子类配置
class DevelopmentConfig(Config):
    DEBUG = True
    # MAIL_SERVER = 'smtp.ym.163.com'
    # MAIL_PORT = '465'
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
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
