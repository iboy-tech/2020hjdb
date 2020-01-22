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


from app.main import auth
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


@auth.route('/recognize',methods=['POST'])
def recognize():
    data=request.json
    print(data)
    usr=data['username']
    pwd=data['password']
    qq=data['qq']
    # code=data['code']
    from app.untils.jwc import user_verify
    user=user_verify(usr,pwd)
    if user is not  None:
        print(user,'验证成功')
    else:
        print('用户名或密码有误')
    data={
          "success" : True,
          "code" : 1000,
          "msg" : "处理成功",
          "data" : {
              "user": {
                  "studentNum": "201520180508",
                  "realName": "cpwu",
                  "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(qq),
                  "email": qq+'@qq.com',
                  "schoolName": "东华理工大学",
                  "gender": 1,
                  "createTime": "2019-04-10 19:06:10",
                  "lastLogin": "2019-04-10 19:06:10",
                  "kind": 0
              }
          }
          # "ext" : None
        }
    return data

