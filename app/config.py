# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : celeryconfig.py
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
class BaseConfig:
    PIPENV_DONT_LOAD_ENV = 1
    FLASK_DEBUG = True
    # MAIL_PORT = int(os.getenv('MAIL_PORT', default=465))
    # MAIL_USE_SSL = True if 'true' == os.getenv('MAIL_USE_SSL') else False
    # MAIL_USE_TLS = True if 'true' == os.getenv('MAIL_USE_TLS') else False
    # SECRET_KEY = os.urandom(24)  # 随机秘钥
    SECRET_KEY = 'adsdad&*^%^$%#afcsefvdzcssef1212'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MXA_ATTEMPT_NUMBER = 5
    ARTISAN_POSTS_PER_PAGE = 120
    MAIL_SUBJECT_PREFIX = '三峡大学失物招领处：'
    # QQ_AVATAR_API = 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    REDIS_URL = 'redis://127.0.0.1:6379/1'
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    CACHE_REDIS_URL = 'redis://127.0.0.1:6379/0'  # 缓存
    SESSION_REDIS = 'redis://127.0.0.1:6379/2'  # session缓存
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60  # session 的有效期，单位是秒
    QR_CODE_VALID_TIME = 300  # 微信二维码过期时间10分钟
    QR_CODE_SUFFIX = '-pusher_post_data'
    SESSION_KEY_PREFIX = 'flask'
    MONGODB_SETTINGS = {
        'db': 'szwl',
        'host': '127.0.0.1',
        'port': 27107,
        'username': 'root',
        'password': '123456'
    }

    # REDIS_DB_URL = {
    #     'host': '127.0.0.1',
    #     'port': 6379,
    #     'password': '',
    #     'db': 0
    # }
    MAIL_DEFAULT_SENDER = ("三峡大学失物招领处", os.getenv('MAIL_USERNAME'))

    @staticmethod
    def init_app(app):
        print('app初始化了')


# 开发环境的子类配置
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CACHE_NO_NULL_WARNING = True  # 关闭缓存警告信息
    # MAIL_SERVER = 'smtp.ym.163.com'
    #     # MAIL_PORT = '465'
    #     # MAIL_USE_TLS = True
    #     # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #     # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #     # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #     #                           'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    QQ_AVATAR_API = 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'


# 测试环境的子类配置
class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'


# 生产环境的配置
class ProductionConfig(BaseConfig):
    CACHE_TYPE = 'redis'  # 生产环境下开启redis缓存
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'


# 注册不同的开发环境和默认的开发环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
