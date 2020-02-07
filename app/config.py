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


# TOKEN 类配置
class Operations:
    CONFIRM_QQ = 'confirm-qq'
    RESET_PASSWORD = 'reset-password'
    CHANGE_QQ = 'change-qq'


# 基类配置
class Config:
    PIPENV_DONT_LOAD_ENV = 1
    FLASK_DEBUG = True
    # SECRET_KEY = os.urandom(24)  # 随机秘钥
    SECRET_KEY = 'adsdad&*^%^$%#afcsefvdzcssef1212'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MAIL_SUBJECT_PREFIX = '三峡大学失物招领处：'
    SUPER_ADMIN_USERNAME = '2018171109'
    SUPER_ADMIN_EMAIL = '547142436@qq.com'
    MXA_ATTEMPT_NUMBER = 5
    ARTISAN_POSTS_PER_PAGE = 120
    QQ_AVATAR_API = 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USERNAME = '547142436@qq.com'
    MAIL_PASSWORD = 'njuzsullhjwmbfec'
    MAIL_DEFAULT_SENDER ='三峡大学失物招领处 <547142436@qq.com>'
    # MAIL_SENDGRID_API_KEY =' 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'
    # MAIL_PASSWORD = 'SG.GPeGzFvVRC-9-x1ZXz1FlQ.neGc4P4lqYxbygCxfI--c4SCQVUAA3FC3-YjSi8-i20'

    # MAIL_SERVER = 'smtp.ym.163.com'
    # MAIL_USERNAME = 'iboy@iboy.tech'
    # MAIL_PASSWORD = 'yyhsyanghao'
    # MAIL_DEFAULT_SENDER = '三峡大学失物招领处 <iboy@iboy.tech>'


    @staticmethod
    def init_app(app):
        print('app初始化了')


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
