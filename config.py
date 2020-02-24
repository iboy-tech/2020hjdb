# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : gunicorn.py
@Time    : 2020/1/18 13:07
@Author  : iBoy
@Email   : iboy@iboy.tech
@Software: PyCharm
"""
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

# 监听本地8889端口(端口自己指定,喜欢哪个就哪个) 
bind = '0.0.0.0:8888'

# 证书
#certfile = '/www/server/panel/vhost/cert/swzl.iboy.tech/fullchain.pem'

# 秘钥
#keyfile = '/www/server/panel/vhost/cert/swzl.iboy.tech/privkey.pem'

# 协程运行
worker_class = 'eventlet'  # 使用eventlet模式，还可以使用sync 模式，默认的是sync模式

backlog = 2048               #即等待服务的客户的数量

chdir = '/www/wwwroot/swzl.iboy.tech'  # gunicorn要切换到的目的工作目录

timeout = 30  # 超时

workers = multiprocessing.cpu_count()  # 进程数

threads = 1  # 指定每个进程开启的线程数

loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置

access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误

accesslog = "/www/wwwroot/swzl.iboy.tech/gunicorn_access.log"  # 访问日志文件

errorlog = "/www/wwwroot/swzl.iboy.tech/gunicorn_error.log"  # 错误日志文件
