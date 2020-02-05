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

from dotenv import load_dotenv

dotenv_path1 = os.path.join(os.path.dirname(__file__), '.env')
dotenv_path2 = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path1 and dotenv_path2):
    load_dotenv(dotenv_path1, dotenv_path2)
    print('环境变量配置文件加载成功')
    print(os.getenv('APPID'))

print('当前的环境变量配置', os.getenv('FLASK_CONFIG'))

app = create_app(os.getenv('FlASK_CONFIG') or 'default')

# print('FLASK_APP:'+os.getenv('FLASK_APP'))
#
#

#
#


#


# def init_env():
#     print('导入环境变量')
#     print(os.path.realpath)
#     if os.path.exists('.env'):
#         print('Importing environment from .env...')
#         for line in open('../.env'):
#             var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]
#     if os.path.exists('../.flaskenv'):
#         print('Importing environment from .flaskenv...')
#         for line in open('../.flaskenv'):
#             var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]


# if __name__ == '__main__':
#     manager.run()
#     print(os.getenv('APPID'))
