# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : app.py.py
@Time    : 2020/1/16 16:32
@Author  : iBoy
@Email   : iboy@iboy.tech
@Software: PyCharm
"""
from flask import Flask

app = Flask(__name__)

app.route('/',defaults={'name':'我是默认值'})
app.route('/get/<name>')
def index(name):
    return "<h1>你好,%s!</h1>"%name
if __name__=='__main__':
    app.run()

