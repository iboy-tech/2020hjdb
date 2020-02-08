# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : manage.py
@Time    : 2020/1/10 16:58
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 顶级文件夹中的 manage.py 文件用于启动程序
@Software: PyCharm
"""
import os
from app import create_app

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('.env'))
load_dotenv(find_dotenv('.flaskenv'))

# if os.path.exists('.env'):
#         print('Importing environment from .env...')
#         for line in open('../.env'):
#             var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]
# if os.path.exists('../.flaskenv'):
#     print('Importing environment from .flaskenv...')
#     for line in open('../.flaskenv'):
#         var = line.strip().split('=')
#     if len(var) == 2:
#         os.environ[var[0]] = var[1]

app = create_app(os.getenv('FlASK_CONFIG') or 'default')
