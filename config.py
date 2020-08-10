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

bind = '0.0.0.0:8888'


# 协程运行
worker_class = 'eventlet'  # 使用eventlet模式，还可以使用sync 模式，默认的是sync模式

backlog = 2048  # 即等待服务的客户的数量

chdir = '/www/wwwroot/ctguswzl.cn'  # gunicorn要切换到的目的工作目录

timeout = 30  # 超时

# 只能设置成这个值，不然websocket无法使用
workers = multiprocessing.cpu_count()  # 进程数

threads = 8  # 指定每个进程开启的线程数

daemon = True  # 后台运行

logconfig_dict=dict(
        version=1,
        disable_existing_loggers=False,

        root={"level": "INFO", "handlers": ["access_console"]},
        loggers={
            "gunicorn.error": {
                "level": "ERROR",
                "handlers": ["error_console"],
                "propagate": True,
                "qualname": "gunicorn.error"
            },

            "gunicorn.access": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": True,
                "qualname": "gunicorn.access"
            }
        },
        handlers={
            "access_console": {
				"class": "logging.handlers.TimedRotatingFileHandler",
				"filename": "./logs/gunicorn_access.log",
				"when":"D",
				"interval":1,
				"backupCount": 30, #保存近30天的日志
				"utc":True,
				"formatter": "generic"
				},
            "error_console": {
				"class": "logging.handlers.TimedRotatingFileHandler",
				"filename": "./logs/gunicorn_error.log" ,  # 打日志的路径
				"when":"D",
				"interval":1,
				"backupCount": 30,
				"utc":True,
				"formatter": "generic"
            },
        },
		formatters={
			"generic": {
				# 打日志的格式
				"format": "[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
				"datefmt": "[%Y-%m-%d %H:%M:%S %z]",  # 时间显示方法
				"class": "logging.Formatter"
			},
			"access": {
				"format": "[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
				"class": "logging.Formatter"
			}
    }
)