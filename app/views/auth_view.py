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
from datetime import datetime

from flask import render_template, request, redirect, url_for, g, session
from flask_cors import cross_origin
from flask_login import logout_user, login_user, login_required, current_user

from app import db, login_manager
from app.main import auth
from app.models.user_model import User
from app.untils import restful


@auth.route('/', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
    data = request.json
    print(data, type(data))

    print('请求成功', type(data))
    if request.method == 'POST':
        user = User.query.filter_by(username=data['username']).first()
        if user is not None and user.verify_password(data['password']):
            login_user(user, remember=True)
            print('当前登录的用户', current_user.real_name)
            print('current_user.is_authenticated', current_user.is_authenticated)
            print('Flask-Login自动添加', session['user_id'])
            # session['uid'] = user.id
            user.last_login = datetime.now()
            print(user)
            db.session.add(user)
            db.session.commit()
            print('更新用户登陆时间')

            # print(g.current_user)
            print(session.get('uid'))
            login_user(user, remember=True)
            data = {
                "user": {
                    "studentNum": user.username,
                    "realName": user.real_name,
                    "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                    "email": user.qq + '@qq.com',
                    "qq": user.qq,
                    "gender": user.gender,
                    "createTime": user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "lastLogin": user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
                    "kind": user.kind
                }
            }
            return restful.success(msg='登录成功', data=data)
        else:
            return restful.success(success=False, msg="用户名或密码错误")
    time1 = datetime.now
    time2 = datetime.now()
    print('登录请求成功', time1, type(time1))
    print('登录请求成功', time2, type(time2))
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
    user_db = User.query.filter_by(username=data['username']).first()
    if user_db is not None:
        data = {"user": {}}
        return restful.success(msg="您的账户已认证，请直接登录", data=data)
    else:
        from app.untils.jwc import user_verify
        user_jwc = user_verify(usr, pwd)
        if user_jwc is not None:
            print(user_jwc, '验证成功')
            user = User(username=user_jwc['username'], password=pwd, real_name=user_jwc['real_name'],
                        academy=user_jwc['academy'], class_name=user_jwc['class_name'], major=user_jwc['major'],
                        qq=qq, gender=user_jwc['gender'], create_time=datetime.datetime.now)
            print(user)
            # g.user=u
            db.session.add(user)
            db.session.commit()
            data={
                "user": {
                    "studentNum": user.username,
                    "realName": user.real_name,
                    "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                    "email": user.qq + '@qq.com',
                    "qq": user.qq,
                    "gender": user.gender,
                    "createTime": user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "lastLogin": user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
                    "kind": user.kind
                }
            }
            data=restful.success(msg='恭喜验证成功',data=data)
        else:
            data = restful.success(success=False,msg="您的用户名或密码有误，请重新尝试")
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
