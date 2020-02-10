# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : test_01.py
@Time    : 2020/1/18 13:08
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 单元测试
@Software: PyCharm
"""
import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    # 创建测试环境
    def setUp(self):
        self.app = create_app('testing')
        # 激活应用程序上下文
        self.app_context = self.app.app_context()
        self.app_context.pop()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
