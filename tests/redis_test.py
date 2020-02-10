# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : redis_test.py
@Time    : 2020/2/10 15:31
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import unittest

from app import redis_client
from app import create_app


def test():
    redis_client.set('name', '杨豪')
    print(redis_client.get('name'))

class RedisTestCase(unittest.TestCase):
    # 创建测试环境
    def setUp(self):
        self.app = create_app('testing')
        # 激活应用程序上下文
        self.app_context = self.app.app_context()
        # test()
        self.app_context.pop()
        # db.create_all()

    pass
