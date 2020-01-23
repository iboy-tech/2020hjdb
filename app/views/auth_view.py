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

from flask import render_template, request, redirect, url_for, g, session
from flask_cors import cross_origin

from app import db
from app.main import auth
from app.models.user_model import User


@auth.route('/', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
    data=request.json
    print(data, type(data))
    print('请求成功',type(data))
    # print(request.args)
    # print(request.json_module)
    if request.method == 'POST':
        user = User.query.filter_by(username=data['username']).first()
        if user is not None and user.verify_password(data['password']):
            # session['user'] = user
            print(session.get('user'))
            data = {
                "success": True,
                "code": 1000,
                "msg": "处理成功",
                "data": {
                    "user": {
                        "studentNum": user.username,
                        "realName": user.real_name,
                        "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                        "email": user.qq + '@qq.com',
                        # "schoolName": "东华理工大学",
                        # "gender": 1,
                        "createTime": user.create_time,
                        "lastLogin": user.last_login,
                        "kind": user.kind
                    }
                }
                # "ext" : None
            }
            print(data)
            return data
        # data = request.get_data(as_text=True)

        # print(aws)
        # data = json.loads(data)
        # print(data)
        print(data['username'])

    print('登录请求成功！', datetime.datetime.now())
    return render_template('login.html')


@auth.route('/recognize',methods=['POST','OPTIONS','GET'])
@cross_origin()
def recognize():
    data=request.json
    print(data)
    usr=data['username']
    pwd=data['password']
    qq=data['qq']
    # code=data['code']
    from app.untils.jwc import user_verify
    user_jwc=user_verify(usr,pwd)
    if user_jwc is not  None:
        print(user_jwc,'验证成功')
        u=User(username=user_jwc['username'],password=pwd,real_name=user_jwc['real_name'],
               academy=user_jwc['academy'],class_id=user_jwc['class_id'],major=user_jwc['major'],
               qq=qq,sex=user_jwc['sex'],create_time=datetime.datetime.now())
        print(u)
        # g.user=u
        db.session.add(u)
        db.session.commit()
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
                  "kind": 2
              }
          }
          # "ext" : None
        }
    return data

