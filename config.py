# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : gunicorn.py
@Time    : 2020/1/18 13:07
@Author  : iBoy
@Email   : iboy@iboy.tech
@Software: PyCharm
"""
import multiprocessing
import os

# 监听本地8889端口(端口自己指定,喜欢哪个就哪个)
from logging.handlers import TimedRotatingFileHandler

import logging

bind = '127.0.0.1:8888'


# 协程运行
worker_class = 'eventlet'  # 使用eventlet模式，还可以使用sync 模式，默认的是sync模式

backlog = 2048  # 即等待服务的客户的数量

chdir = '/www/wwwroot/ctguswzl.cn'  # gunicorn要切换到的目的工作目录

timeout = 30  # 超时

# 只能设置成这个值，不然websocket无法使用
workers = multiprocessing.cpu_count()  # 进程数

threads = 8  # 指定每个进程开启的线程数


loglevel = 'debug'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置

daemon = True  # 后台运行

# logger_class = "TimedRotatingFileHandler"
# 设置gunicorn访问日志格式，错误
# access_log_format = '%(u)s %(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

# accesslog1 = os.path.join(chdir, "/logs/gunicorn/access/access.log")  # 访问日志文件
#
# errorlog1 = os.path.join(chdir, "/logs/gunicorn/error/error.log")  # 错误日志文件

# maxbytes: 1024*1024

access_handler = TimedRotatingFileHandler("/www/wwwroot/ctguswzl.cn/logs/gunicorn/access/access.log", when="D",
                                          interval=1,
                                          backupCount=30,
                                          encoding="UTF-8", delay=False, utc=True)
err_handler = TimedRotatingFileHandler("/www/wwwroot/ctguswzl.cn/logs/gunicorn/error/error.log", when="D", interval=1,
                                       backupCount=30,
                                       encoding="UTF-8", delay=False, utc=True)

err_handler.setLevel(logging.ERROR)
access_handler.setLevel(logging.INFO)

logging.getLogger('gunicorn.error').addHandler(err_handler)
logging.getLogger('gunicorn.access').addHandler(access_handler)

# logger_class="logging.handlers.RotatingFileHandler"
# logconfig=""
# logconfig_dict = {
#     # 'version':1,
#     # 'disable_existing_loggers': False,
#     # 'loggers':{
#     #     "gunicorn.error": {
#     #         "level": "DEBUG",# 打日志的等级可以换的，下面的同理
#     #         "handlers": ["error_file"], # 对应下面的键
#     #         "propagate": 1,
#     #         "qualname": "gunicorn.error"
#     #     },
#     #
#     #     "gunicorn.access": {
#     #         "level": "DEBUG",
#     #         "handlers": ["access_file"],
#     #         "propagate": 0,
#     #         "qualname": "gunicorn.access"
#     #     }
#     # },
#     'handlers':{
#         "error_file": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "maxBytes": 1024*1024*1024,# 打日志的大小，我这种写法是1个G
#             "backupCount": 1,# 备份多少份，经过测试，最少也要写1，不然控制不住大小
#             "formatter": "generic",# 对应下面的键
#             # 'mode': 'w+',
#             "filename": "/www/wwwroot/ctguswzl.cn/logs/gunicorn.erro1r.log"# 打日志的路径
#         },
#         "access_file": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "maxBytes": 1024*1024*1024,
#             "backupCount": 1,
#             "formatter": "generic",
#             "filename": "/www/wwwroot/ctguswzl.cn/logs/gunicorn.access1.log",
#         }
#     },
#     'formatters':{
#         "generic": {
#             "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'", # 打日志的格式
#             "datefmt": "[%Y-%m-%d %H:%M:%S %z]",# 时间显示方法
#             "class": "logging.Formatter"
#         },
#         "access": {
#             "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",
#             "class": "logging.Formatter"
#         }
#     }
# }
#
