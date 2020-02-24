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
import json
import os
import re
from datetime import datetime

from flask import render_template, request, redirect, url_for, session, send_from_directory, current_app
from flask_cors import cross_origin
from flask_login import logout_user, login_user, login_required, current_user

from app import db, OpenID, redis_client, cache
from app.decorators import wechat_required
from app.page import auth
from app.models.user_model import User
from app.utils import restful
from app.utils.auth_token import generate_token, validate_token
from app.utils.mail_sender import send_email


@auth.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(
            current_app.root_path,
            'static/images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@auth.route('/', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
@login_required
@wechat_required
@cache.cached(timeout=60, query_string=True)  # 缓存10分钟 默认为300s
def index():
    data = request.json
    print('user页面收到请求', data)
    return render_template('user.html')  # 所有参数都要


def checkQQ(str):
    # 正则表达式
    pattern = r"qq:[1-9]\d{4,10}"
    res = re.findall(pattern, str, re.I)
    if not res:
        return True
    else:
        return False


@auth.route('/login', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
    data = request.json
    print("next的值", request.args.get('next'))
    print('请求成功', type(data))
    if request.method == 'POST':
        print('请求的全路径：', request.full_path, session.get('next'))
        user = User.query.filter_by(username=data['username']).first()
        if user is None:
            restful.success(success=False, msg='账户名或密码错误')
        else:
            if user.status == 0:
                return restful.success(
                    success=False, msg='您的账户因违规已被冻结，请联系管理员申诉')
            elif user.status == 1:
                return restful.success(
                    success=False,
                    msg='您的账户还未完成认证，请认证后登录，若之前填写的QQ有误，可以在认证界面填写新的QQ重新进行认证')
            elif user is not None and user.verify_password(data['password']):
                login_user(user, remember=True)
                user.last_login = datetime.now()
                print(user)
                db.session.add(user)
                db.session.commit()
                print('更新用户登陆时间')
                op = OpenID.query.filter_by(user_id=current_user.id).first()
                print('我是查询的登录页面查询的OPIN', op, datetime.now())
                if op is None:
                    data = user.auth_to_dict()
                    return restful.success(
                        success=True, msg='登录成功，请绑定微信', data=data, ext='wx')
                print('当前登录的用户', current_user.real_name)
                print(
                    'current_user.is_authenticated',
                    current_user.is_authenticated)
                print('Flask-Login自动添加', session['user_id'])
                print(session.get('uid'))
                data = user.auth_to_dict()
                if session.get('next') is not None:
                    print(session.get("next的值"), session['next'])
                    return restful.success(msg='登录成功', data=data, ext=session.get('next'))
                return restful.success(msg='登录成功', data=data)
            else:
                app = current_app._get_current_object()
                key = str(user.id) + '-fail-login-times'
                cnt = redis_client.get(key)
                if cnt != None:
                    redis_client.setrange(key, 0, str(data))
                else:
                    redis_client.incr(key)  # 把数据存入redis
                    redis_client.expire(key, 60 * 60)
                    print('登录错误的次数', redis_client.get(key), type(redis_client.get(key)))
                # redis_client.setrange(key, 0, str(data))  # 把数据存入redis
                # print('key的过期时间：', os.getenv('QR_CODE_VALID_TIME'))
                # print('redis中的值', redis_client.get('key'), type(redis_client.get('key')))
                return restful.success(success=False, msg="用户名或密码错误,您还有能尝试" + str(
                    app.config['LOGIN_FAIL_TIMES'] - int(eval(redis_client.get(key)))))
    if request.args.get('next'):
        session['next'] = request.args.get('next')
    return render_template('login.html')


@auth.route('/logout', methods=['POST'])
def logout():
    print(session.get('uid'))
    print('用户登出成功')
    logout_user()
    return restful.success(success = True,msg = "登出成功")


@auth.route('/recognize', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
def recognize():
    data = request.json
    print(data)
    usr = data['username']
    pwd = data['password']
    qq = data['qq']
    if checkQQ(qq):
        user_db = User.query.filter_by(username=data['username']).first()
        if user_db is not None and user_db.status > 1:
            data = {"user": {}}
            return restful.success(
                success=False, msg="您的账户已认证，请直接登录", data=data)
        elif user_db is not None and user_db.status == 0:
            data = {"user": {}}
            return restful.success(
                success=False,
                msg="您的账户已被冻结，请联系管理员申诉",
                data=data)
        elif user_db is not None and user_db.status == 1:  # 重发验证邮件
            user_db.qq = qq
            db.session.commit()
            # 发送验证邮件
            token = generate_token(
                user=user_db,
                operation='confirm-qq',
                qq=user_db.qq)
            messages = {
                'real_name': user_db.real_name,
                'token': token
            }
            cache.delete('user-getall')  # 删除缓存
            send_email.delay('849764742', '身份认证', 'confirm', messages)
            return restful.success(
                success=False,
                msg="验证邮件已发送到您的QQ邮箱，可能在垃圾信箱中，请尽快认证",
                data=data)
        else:
            from app.utils.jwc import user_verify
            user_jwc = user_verify(usr, pwd)
            if user_jwc is not None:
                print(user_jwc, '验证成功')
                user = User(
                    username=user_jwc['username'],
                    password=pwd,
                    real_name=user_jwc['real_name'],
                    academy=user_jwc['academy'],
                    class_name=user_jwc['class_name'],
                    major=user_jwc['major'],
                    qq=qq,
                    gender=user_jwc['gender'])
                print(user)
                # g.user=u
                db.session.add(user)
                db.session.commit()
                # 发送验证邮件
                token = generate_token(
                    user=user, operation='confirm-qq', qq=user.qq)
                messages = {
                    'real_name': user.real_name,
                    'token': token
                }
                send_email.delay(user.qq, '身份认证', 'confirm', messages)
                # 发送验证邮件
                data = restful.success(
                    success=False,
                    msg='验证邮件已发送到您的QQ邮箱，可能在垃圾信箱中，请尽快认证',
                    data=data)
    else:
        return restful.success(success=False, msg='QQ号格式不正确', data=data)
    return data


@auth.route('/confirm.html', methods=['GET'])
@cross_origin()
def confirm():
    token = request.args.get('token')
    print(token)
    data = validate_token(token)
    messages = {
        'msg': json.loads(data)['msg']
    }
    return render_template('mails/go.html', messages=messages)


@auth.route('/index', methods=['GET'])
@cross_origin()
def demo():
    return render_template('index.html')
