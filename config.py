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
bind = '127.0.0.1:8888'

# 证书
# certfile = '/www/server/panel/vhost/cert/ctguswzl.cn/fullchain.pem'

# 秘钥
# keyfile = '/www/server/panel/vhost/cert/ctguswzl.cn/privkey.pem'

# 协程运行
worker_class = 'eventlet'  # 使用eventlet模式，还可以使用sync 模式，默认的是sync模式

backlog = 2048  # 即等待服务的客户的数量

chdir = '/www/wwwroot/ctguswzl.cn'  # gunicorn要切换到的目的工作目录

timeout = 30  # 超时
#只能设置成这个值，不然websocket无法使用
workers = multiprocessing.cpu_count()  # 进程数

threads = 8  # 指定每个进程开启的线程数

loglevel = 'debug'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置


logging.basicConfig(level=logging.DEBUG,
                    filename='/www/wwwroot/ctguswzl.cn/logs/output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
file_run_log=logging.handlers.TimedRotatingFileHandler(
        "/www/wwwroot/ctguswzl.cn/logs/gunicorn.log", when="D", interval=1, backupCount=30,
        encoding="UTF-8", delay=False, utc=True)
file_run_log.setLevel(level=logging.INFO)
LOG_FORMAT = "%(asctime)s------%(levelname)s[:%(lineno)d]-------%(message)s"
file_run_log.setFormatter(logging.Formatter(LOG_FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(file_run_log)
# logging.handlers.TimedRotatingFileHandler(run_log, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))

daemon = True  #后台运行


# 设置gunicorn访问日志格式，错误
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = "/www/wwwroot/ctguswzl.cn/logs/gunicorn_access.log"  # 访问日志文件

errorlog = "/www/wwwroot/ctguswzl.cn/logs/gunicorn_error.log"  # 错误日志文件
#maxbytes: 1024*1024
