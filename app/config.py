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
class BaseConfig:
    PIPENV_DONT_LOAD_ENV = 1
    # MAIL_PORT = int(os.getenv('MAIL_PORT', default=465))
    # MAIL_USE_SSL = True if 'true' == os.getenv('MAIL_USE_SSL') else False
    # MAIL_USE_TLS = True if 'true' == os.getenv('MAIL_USE_TLS') else False
    # SECRET_KEY = os.urandom(24)  # 随机秘钥
    SECRET_KEY = 'adsdad&*^%^$%#afcsefvdzcssef1212'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MXA_ATTEMPT_NUMBER = 5
    ARTISAN_POSTS_PER_PAGE = 120  # 分页的数量
    MAIL_SUBJECT_PREFIX = '三峡大学失物招领处：'
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
    QR_CODE_VALID_TIME = 300  # 微信二维码过期时间5分钟
    QR_CODE_SUFFIX = '-pusher_post_data'
    SESSION_KEY_PREFIX = 'flask'
    MONGODB_SETTINGS = {
        'db': 'swzl',
        'host': '127.0.0.1',
        'port': 27107,
        'username': 'root',
        'password': '123456'
    }
    MAIL_USE_SSL =True
    MAIL_SERVER ='smtp.qq.com'
    MAIL_PORT  =465
    SUPER_ADMIN_USERNAME ='2018171109'
    MAIL_USERNAME ='547142436@qq.com'
    MAIL_PASSWORD ='xgepfanashsmbffi'
    MAIL_DEFAULT_SENDER = ("三峡大学失物招领处", '547142436@qq.com')

	# MAIL_DEFAULT_SENDER = ("三峡大学失物招领处", os.getenv('MAIL_USERNAME'))

    @staticmethod
    def init_app(app):
        print('app初始化了')


# 开发环境的子类配置
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CACHE_NO_NULL_WARNING = True  # 关闭缓存警告信息
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'
    print('现在是开发环境数据库', SQLALCHEMY_DATABASE_URI)


# 测试环境的子类配置
class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/swzl'


# 生产环境的配置
class ProductionConfig(BaseConfig):
    CACHE_TYPE = 'redis'  # 生产环境下开启redis缓存
    SQLALCHEMY_DATABASE_URI = 'mysql://swzl:6hAZDJ876WiGZZ6X@127.0.0.1/swzl'
    print('现在是生产环境数据库', SQLALCHEMY_DATABASE_URI)


# 注册不同的开发环境和默认的开发环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
