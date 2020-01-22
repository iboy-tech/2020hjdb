# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : errors.py
@Time    : 2020/1/18 13:00
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 错误处理文件
@Software: PyCharm
"""
from flask import  render_template
from . import  auth
#注册全局
@auth.app_errorhandler(404)
def page_not_found():
    return render_template('404.html'),404

@auth.app_errorhandler(500)
def internal_server_error():
    return  render_template('500.html'),500