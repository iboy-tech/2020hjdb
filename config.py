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

# 监听本地8889端口(端口自己指定,喜欢哪个就哪个)

bind = '0.0.0.0:8888'

# 协程运行
worker_class = 'eventlet'  # 使用eventlet模式，还可以使用sync 模式，默认的是sync模式

backlog = 2048  # 即等待服务的客户的数量

chdir = '/www/wwwroot/ctguswzl.cn'  # gunicorn要切换到的目的工作目录

timeout = 30  # 超时

# 只能设置成这个值，不然websocket无法使用
workers = multiprocessing.cpu_count()  # 进程数

threads = 8  # 指定每个进程开启的线程数

# daemon = True  # 后台运行
