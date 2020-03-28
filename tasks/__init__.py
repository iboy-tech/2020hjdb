# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : __init__.py.py
@Time    : 2020/2/15 9:04
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from celery import Celery

from .config import broker_url

celery = Celery(__name__,broker=broker_url)
celery.config_from_object('tasks.config')

