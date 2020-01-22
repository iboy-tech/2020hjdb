# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : auth_view.py
@Time    : 2020/1/19 21:21
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import datetime
import json


from main import auth
from flask import render_template, request
from flask_cors import cross_origin
from flask import json


@auth.route('/', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
    data=request.json
    print('请求成功',type(data))
    # print(request.args)
    # print(request.json_module)
    if request.method == 'POST':
        # data = request.get_data(as_text=True)
        print(data, type(data))
        # print(aws)
        # data = json.loads(data)
        # print(data)
        print(data['username'])
        item = {
            "success": True,
            "code": 1000,
            "msg": "处理成功",
            "data": {
                "schools": [
                    {
                        "schoolId": "12345678123456781234567812345678",
                        "schoolName": "东华理工大学"
                    },
                    {
                        "schoolId": "12345678123456781234567812345677",
                        "schoolName": "南昌大学"
                    },
                    {
                        "schoolId": "12345678123456781234567812345676",
                        "schoolName": "江西财经大学"
                    }
                ]
            },
            "ext": None
        }
    print('登录请求成功！', datetime.datetime.now())
    return render_template('login.html')


@auth.route('/recognize')
def recognize():
    print('我是认证模块')
    print(request.json)
    pass
