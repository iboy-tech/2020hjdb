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
from datetime import datetime, timedelta
from random import randint

from flask import render_template, request, url_for, session, send_from_directory, current_app
from flask_cors import cross_origin
from flask_login import logout_user, login_user, login_required, current_user

from app import db, OpenID, redis_client, cache, limiter
from app.config import LoginConfig, PostConfig
from app.decorators import wechat_required, unfreeze_user
from app.models.user_model import User
from app.page import auth
from app.utils import restful
from app.utils.auth_token import generate_token, validate_token
from app.utils.check_data import check_qq, check_username
from app.utils.log_utils import get_login_info
from app.utils.mail_sender import send_email


# 隐私协议
@auth.route('/policy')
@limiter.limit(limit_value="10/minute")
@cache.cached(timeout=3600 * 24 * 7, query_string=True, key_prefix="policy-html")  # 缓存10分钟 默认为300s
def private():
    return render_template('policy.html')


@auth.route('/favicon.ico')
# @cache.cached(timeout=60, query_string=True)  # 缓存10分钟 默认为300s
def favicon():
    return send_from_directory(
        os.path.join(
            current_app.root_path,
            'static/images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@auth.route('/', methods=['POST', 'OPTIONS', 'GET'])
# @limiter.limit(limit_value="10/minute")
@cross_origin()
@unfreeze_user  # 微信自助解封
@cache.cached(timeout=3600 * 24 * 7, key_prefix="user-html")  # 缓存10分钟 默认为300s
@login_required
@wechat_required
def index():
    return render_template('user.html')  # 所有参数都要


def login_user_longtime(user):
    session.permanent = True
    app = current_app._get_current_object()
    # session持久化，免登陆
    app.permanent_session_lifetime = timedelta(days=365)
    login_user(user, remember=True)
    user.last_login = datetime.now()
    print(user)
    db.session.add(user)
    db.session.commit()
    print('更新用户登陆时间')


@auth.route('/login', methods=['GET', 'POST', 'OPTIONS'])
@limiter.limit(limit_value="20/hour")
@cross_origin()
def login():
    socket_id = request.args.get('token')
    print("我是登录的token", socket_id)
    if socket_id:
        try:
            key = socket_id + PostConfig.PUSHER_REDIS_PREFIX
            op = redis_client.get(key)
            if op != 'null':
                # redies中为byte类型
                op = op.decode()
                data = eval(op)
                op = OpenID.query.filter_by(wx_id=data['uid']).first()
                if op:
                    print(op, op.user)
                    # 用户免登陆
                    login_user_longtime(op.user)
                    # 删除redis中的数据
                    redis_client.delete(key)
                    return restful.success(msg="密码重置成功，新密码已发送到您的微信", data=op.user.auth_to_dict())
                else:
                    return restful.success(False, msg="此微信尚未绑定")
        except Exception as e:
            print("扫码登录异常："+str(e))
            pass
    data = request.json
    print("next的值", request.args.get('next'))
    print('请求成功', type(data))
    if request.method == 'POST':
        print('请求的全路径：', request.full_path, session.get('next'))
        user = User.query.filter_by(username=data['username']).first()
        if user is None:
            return restful.success(success=False, msg='用户名或密码错误')
        else:
            # 密码错误次数判断
            key = user.username + LoginConfig.LOGIN_REDIS_PREFIX
            cnt = redis_client.get(key)
            if cnt is not None:
                cntint = int(bytes.decode(cnt))
                print("达到6次提醒锁定，但不发送通知")
                if cntint >= LoginConfig.LOGIN_ERROR_MAX_TIMES:
                    # 管理员不冻结只提醒
                    if user.kind == 1:
                        return restful.success(success=False, msg='您的账户已被冻结，请1小时后重试')
                    else:
                        redis_client.delete(key)
            # 用户状态判断
            if user.status == 0:
                return restful.success(
                    success=False, msg='您的账户因违规已被冻结，请联系管理员申诉')
            elif user.status == 1:
                return restful.success(
                    success=False,
                    msg='您的账户还未完成认证，请认证后登录，若之前填写的QQ有误，可以在认证界面填写新的QQ重新进行认证')
            elif user is not None and user.verify_password(data['password']):
                # 登录并保存cookie
                login_user_longtime(user)
                op = OpenID.query.filter_by(user_id=current_user.id).first()
                print('我是查询的登录页面查询的OPIN', op, datetime.now())
                if op is None:
                    data = user.auth_to_dict()
                    return restful.success(success=True, msg='登录成功，请绑定微信', data=data, ext='wx')
                print('当前登录的用户', current_user.real_name)
                print(
                    'current_user.is_authenticated',
                    current_user.is_authenticated)
                # print('Flask-Login自动添加', session['user_id'])
                # print(session.get('uid'))
                data = user.auth_to_dict()
                if session.get('next') is not None:
                    print(session.get("next的值"))
                    if "getQRcode" not in session['next']:
                        return restful.success(msg='登录成功', data=data, ext=session.get('next'))
                return restful.success(msg='登录成功', data=data)
            # 状态判断完毕

            # 用户存在但是密码错误
            else:
                key = user.username + LoginConfig.LOGIN_REDIS_PREFIX
                cnt = redis_client.get(key)
                if cnt is not None:
                    redis_client.incr(key)
                    cnt = int(bytes.decode(redis_client.get(key)))

                    left_times = LoginConfig.LOGIN_ERROR_MAX_TIMES - cnt
                    print('计算剩余错误次数', cnt, left_times)
                    if user.kind == 1:
                        if left_times == 0:
                            # 只在刚好达到阈值的时候提醒
                            get_login_info(user, 0)
                            return restful.success(success=False, msg="您的账户已被冻结，请1小时后重试")
                        else:
                            return restful.success(success=False, msg="用户名或密码错误,您还能尝试 %s 次" % str(left_times))
                    else:
                        if cnt == LoginConfig.LOGIN_ERROR_MAX_TIMES:
                            # 只在刚好达到阈值的时候提醒
                            get_login_info(user, 0)
                        return restful.success(success=False, msg="用户名或密码错误")
                else:
                    redis_client.incr(key)  # 把数据存入redis
                    redis_client.expire(key, LoginConfig.LOGIN_FAIL_KEY_EXPIRED)
                    if user.kind == 1:
                        return restful.success(success=False,
                                               msg="用户名或密码错误,您还能尝试 %s 次" % str(LoginConfig.LOGIN_ERROR_MAX_TIMES - 1))
                    else:
                        return restful.success(success=False, msg="用户名或密码错误")
    if request.args.get('next'):
        session['next'] = request.args.get('next')
    # login_html = cache.get("login-html")
    # if not login_html:
    #     cache.set('login-html', render_template('login.html.bak'), timeout=3600 * 24 * 7)
    #     login_html = cache.get("login-html")
    # return login_html
    return render_template('login.html')


@auth.route('/logout', methods=['POST'])
def logout():
    print(session.get('uid'))
    print('用户登出成功')
    logout_user()
    return restful.success(success=True, msg="登出成功")


@auth.route('/recognize', methods=['POST', 'OPTIONS'])
@limiter.limit(limit_value="5/hour")
@check_qq
@check_username
@cross_origin()
def recognize():
    data = request.json
    print(data)
    qq = data['qq']
    # 校验QQ号
    # 判断用户是否存在
    user_db = User.query.filter_by(username=data['username']).first()
    # 用户存在对状态进行校验
    if user_db:
        if user_db.status > 1:
            data = {"user": {}}
            return restful.success(success=False, msg="您的账户已认证，请直接登录", data=data)
        # 被冻结
        elif user_db.status == 0:
            data = {"user": {}}
            return restful.success(
                success=False,
                msg="您的账户已被冻结，请联系管理员申诉",
                data=data)
        # 需要更改认证QQ
        elif user_db.status == 1:
            try:
                user_db.qq = qq
                # 发送验证邮件
                token = str(generate_token(id=user_db.id, operation='confirm-qq', qq=user_db.qq), encoding="utf-8")
                messages = {
                    'real_name': user_db.real_name,
                    'token': url_for('auth.confirm', token=token, _external=True)
                }
                send_email.apply_async(args=(qq, '身份认证', 'confirm', messages), countdown=randint(10, 30))
                db.session.add(user_db)
                db.session.commit()
                return restful.success(
                    msg="验证邮件已重新发送到您的QQ邮箱，可能在垃圾信箱中，请尽快认证",
                    data=data,
                    ext="reg")
            except:
                db.session.rollback()
                return restful.success(success=False, msg="QQ号已被他人使用", data=data)
    else:  # 新用户进行认证
        from app.utils.jwc import user_verify
        usr, pwd = data["username"], data["password"]
        user_jwc = user_verify(usr, pwd)
        # 查询到用户信息
        if user_jwc:
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
            db.session.add(user)
            db.session.commit()
            # 发送验证邮件
            token = str(generate_token(id=user.id, operation='confirm-qq', qq=user.qq), encoding="utf-8")
            messages = {
                'real_name': user.real_name,
                'token': url_for('auth.confirm', token=token, _external=True)
            }
            print('我是生成的认证链接', messages)
            send_email.apply_async(args=(user.qq, '身份认证', 'confirm', messages), countdown=randint(10, 30))
            # 发送验证邮件
            return restful.success(
                success=True,
                msg='验证邮件已发送到您的QQ邮箱，可能在垃圾箱中，请尽快认证',
                data=data)
        # 没有找到用户信息
        else:
            return restful.success(
                success=False,
                msg='学号或密码错误',
                data=data)
    return restful.params_error(msg="认证失败，请重新认证")


# token验证入口
@auth.route('/confirm.html', methods=['GET'])
@limiter.limit(limit_value="5/day")
@cross_origin()
def confirm():
    token = request.args.get('token')
    print(token)
    data = validate_token(token)
    messages = {
        'msg': json.loads(data)['msg'],
        'success': json.loads(data)['success']
    }
    print(messages)
    return render_template('mails/go.html', messages=messages)
