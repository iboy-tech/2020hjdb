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
from flask_login import logout_user, login_user, login_required, current_user

from app import db, login_manager
from app.main import auth
from app.models.user_model import User


@auth.route('/', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
    # from app.untils.create_data import create_test_data
    # create_test_data()
    data = request.json
    print(data, type(data))
    print('请求成功', type(data))

    # print(request.args)
    # print(request.json_module)
    # if "user_id" in session:
    #     user=current_user
    #     login_user(user,remember=True)
    #     data = {
    #         "success": True,
    #         "code": 1000,
    #         "msg": "处理成功",
    #         "data": {
    #             "user": {
    #                 "studentNum": user.username,
    #                 "realName": user.real_name,
    #                 "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
    #                 "email": user.qq + '@qq.com',
    #                 "qq": user.qq,
    #                 "gender": user.gender,
    #                 "createTime": user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
    #                 "lastLogin": user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
    #                 "kind": user.kind
    #             }
    #         }
    #         # "ext" : None
    #     }
    #     print(data)
    #     return data
    #     print('已经登录测试')
    if request.method == 'POST':
        user = User.query.filter_by(username=data['username']).first()
        if user is not None and user.verify_password(data['password']):
            login_user(user,remember=True)
            print('当前登录的用户', current_user.real_name)
            print('current_user.is_authenticated',current_user.is_authenticated)
            print('Flask-Login自动添加',session['user_id'])
            # session['uid'] = user.id
            user.last_login = datetime.datetime.now()
            print(user)
            # db.session.add(user)
            db.session.commit()
            print('更新用户登陆时间')

            # print(g.current_user)
            print(session.get('uid'))
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
                        "qq": user.qq,
                        "gender": user.gender,
                        "createTime": user.create_time.strftime( '%Y-%m-%d %H:%M:%S' ),
                        "lastLogin": user.last_login.strftime( '%Y-%m-%d %H:%M:%S' ),
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


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    print(session.get('uid'))
    print('用户登出成功')
    logout_user()
    return redirect(url_for('auth.login')), 301


@auth.route('/recognize', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
def recognize():
    data = request.json
    print(data)
    usr = data['username']
    pwd = data['password']
    qq = data['qq']
    # code=data['code']
    from app.untils.jwc import user_verify
    user_jwc = user_verify(usr, pwd)
    if user_jwc is not None:
        print(user_jwc, '验证成功')
        u = User(username=user_jwc['username'], password=pwd, real_name=user_jwc['real_name'],
                 academy=user_jwc['academy'], class_name=user_jwc['class_name'], major=user_jwc['major'],
                 qq=qq, gender=user_jwc['gender'], create_time=datetime.datetime.now())
        print(u)
        # g.user=u
        db.session.add(u)
        db.session.commit()
    else:
        print('用户名或密码有误')
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "user": {
                "studentNum": "201520180508",
                "realName": "cpwu",
                "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(qq),
                "email": qq + '@qq.com',
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


# 注册全局
@auth.app_errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@auth.app_errorhandler(500)
def internal_server_error():
    return render_template('500.html'), 500


@login_manager.user_loader
def load_user(user_id):
    """加载用户信息回调"""

    return User.query.get(int(user_id))
    # user=User.query.get(int(id))
    # print(user)
    # return User.query.filter_by(id=int(user_id))
