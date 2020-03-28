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


class AdminConfig:
    # 用于接收系统通知
    SUPER_ADMIN_QQ = '管理员QQ'


# 日志记录模块
class LogConfig:
    REDIS_ERROR_LOG_KEY = "-error-log"
    REDIS_INFO_LOG_KEY = "-info-log"
    REDIS_ADMIN_LOG_KEY = "-admin-log"
    REDIS_EXPIRE_TIME = 3600 * 24 * 30  # 过期时间设置为一个月


class PostConfig:
    # Reids中浏览量的阈值
    REDIS_MAX_VIEW = 20
    POST_REDIS_PREFIX = '-post-view-times'
    # 前端分页每页的数量上限
    PAGESIZE_OF_USER = 15
    TINYPNG_REDIS_KEY = 'tinypng-keys'
    # 压缩的下限 单位KB
    MAX_IMG_SIZE = 200
    # 上传的上限 单位KB
    UPLOAD_MAX_SIZE = 400
    # celery异步多线程任务中每个线程处理的图片数量
    IMG_NUM_IN_THREAD = 2
    MAX_COMMENT_LENGTH = 100  # 评论最大字数
    MAX_UPLOAD_IMG_NUM = 3  # 最多上传3张图片
    AVATER_API = "#"  # 头像的api接口备用反代接口
    # AVATER_API = "https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100" #官方接口https不稳定
    ALLOW_UPLOAD_FILE_TYPE = ["jpeg", "png"]  # 允许上传的文件类型


class LoginConfig:
    LOGIN_ERROR_MAX_TIMES = 6  # 最大尝试次数
    LOGIN_REDIS_PREFIX = '-fail-login-times'  # redis前缀
    LOGIN_FAIL_KEY_EXPIRED = 60 * 60  # 一小时之内错误次数限制在5次
    LOGIN_INFO_API = "http://whois.pconline.com.cn/ipJson.jsp?ip={}&json=true"


# 基类配置
class BaseConfig:
    PIPENV_DONT_LOAD_ENV = 1  # 禁止pipenv加载.env
    SECRET_KEY = os.urandom(24)  # 随机秘钥
    # SECRET_KEY = '#'
    # 设置成True会导致传递对象有错误
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MXA_ATTEMPT_NUMBER = 5
    # REDIS数据库配置
    REDIS_URL = 'redis://127.0.0.1:6379/1'
    SESSION_REDIS = 'redis://127.0.0.1:6379/4'  # session缓存
    # REDIS数据库配置

    # 缓存配置
    # CACHE_DEFAULT_TIMEOUT = 10 * 6  # 缓存默认过期时间
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    CACHE_REDIS_URL = 'redis://127.0.0.1:6379/0'  # 缓存
    # CACHE_KEY_PREFIX='flask-cache-' # 设置cache_key的前缀
    CACHE_TYPE = 'redis'
    # 缓存配置
    # 默认31天过期
    # PERMANENT_SESSION_LIFETIME = timedelta(days=31)  # session 的有效期，单位是秒
    SESSION_KEY_PREFIX = 'flask'
    MONGODB_SETTINGS = {
        'db': 'swzl',
        'host': '127.0.0.1',
        'port': 27107,
        'username': '#',
        'password': '#'
    }
    SUPER_ADMIN_USERNAME = os.getenv('SUPER_ADMIN_USERNAME')

    # 发送邮件的相关配置开始
    """
    MAIL_SERVER = '#'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    """
    MAIL_SERVER = '#'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_SUBJECT_PREFIX = '邮件前缀:'
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USERNAME = '邮箱地址'
    MAIL_PASSWORD = '邮箱密码'
    MAIL_DEFAULT_SENDER = '发件人别名 <邮箱地址>'
    # 邮件配置结束
    """
    事务邮件发送
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_SUBJECT_PREFIX = '邮箱前缀：'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = '发件人别名 <邮箱地址>'
    MAIL_SENDGRID_API_KEY = os.getenv('MAIL_SENDGRID_API_KEY')
    """


# 开发环境的子类配置
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CACHE_NO_NULL_WARNING = True  # 关闭缓存警告信息
    SQLALCHEMY_DATABASE_URI = 'mysql://用户名:密码@127.0.0.1/数据库?charset=utf8mb4'
    print('现在是开发环境数据库', SQLALCHEMY_DATABASE_URI)


# 测试环境的子类配置
class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://用户名:密码@127.0.0.1/测试环境数据库?charset=utf8mb4'


# 生产环境的配置
class ProductionConfig(BaseConfig):
    CACHE_TYPE = 'redis'  # 生产环境下开启redis缓存
    SQLALCHEMY_DATABASE_URI = 'mysql://用户名:密码@127.0.0.1/数据库?charset=utf8mb4'
    print('现在是生产环境数据库', SQLALCHEMY_DATABASE_URI)


# 注册不同的开发环境和默认的开发环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
