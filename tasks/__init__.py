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

# from dotenv import load_dotenv, find_dotenv
# 一、自动搜索 .env 文件
# load_dotenv(verbose=True)
# load_dotenv(find_dotenv('.env'), override=True)
# load_dotenv(find_dotenv('.flaskenv'), override=True)

celery = Celery(__name__,broker=broker_url)
celery.config_from_object('tasks.config')

