# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : oauth_view.py
@Time    : 2020/2/8 19:26
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import datetime
import os

from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, current_user, login_user

from app import db, OpenID, redis_client
from app.page import oauth
from app.utils import restful, mail_sender
from app.utils.auth_token import generate_password
from app.utils.wxpusher import WxPusher
from app.views.found_view import send_message_by_pusher


@oauth.route('/wx.html', methods=['GET'], strict_slashes=False)
@oauth.route('/wx', methods=['POST'], strict_slashes=False)
def index():
    # print('SECRET_KEY', os.getenv('SECRET_KEY'))
    # print('request.sid',request.sid)
    print("用户要绑定位置")
    if current_user.is_authenticated and request.method == 'GET':
        op = OpenID.query.filter_by(user_id=current_user.id).first()
        if op is not None:
            return redirect(url_for('auth.index')), 301
        data = (WxPusher.create_qrcode(extra=current_user.id, valid_time=180))
        # print(type(data), data)
        if data['success']:
            data = data['data']
            # print('user_id', data['extra'])
            # print('qr_code', data['url'])
            data = {
                'url': data['url'],
                'site': os.getenv('SITE_URL')
            }
            return render_template('pusher.html', data=data)
    elif request.method == 'GET' and current_user.is_authenticated == False:
        return redirect(url_for('auth.login')), 301
    elif request.method == 'POST':
        data = request.json['data']
        wx_open_id = data['uid']
        user_id = data['extra']
        # print('用户的ID', user_id,type(user_id))
        # 如果是数字说明是初始扫码绑定
        if user_id.isnumeric():
            op = OpenID(user_id=user_id, wx_id=wx_open_id)
            db.session.add(op)
            db.session.commit()
            db.session.close()
            """
            redis_store = FlaskReis()
            redis_store.get(key)
            get函数接受一个键，通过此键如果有缓存就返回缓存，没有就返回None,常配合条件语句使用
            redis_store.set(key,value)
            set函数接受一个键和值,主要作用是写入缓存
            redis_store.expire(key,time)
            expire函数接受一个键，一个时间（格式可以类似3600*24），设置缓存的期限
            """
        else:
            print("我是找回密码")
            data = request.json['data']
            wx_open_id = data['uid']
            op = OpenID.query.filter_by(wx_id=wx_open_id).first()
            if op:
                print(op, op.user)
                print('用户的OPEN-ID', wx_open_id)
                password = generate_password()
                op.user.password = password
                # 新密码发送到微信
                msg = {
                    'real_name': op.user.real_name,
                    'username': op.user.username,
                    'password': password,
                    'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': os.getenv('SITE_URL') + 'login'
                }
                print("我是新的密码", password)
                mail_sender.send_email.delay(op.user.qq, '密码重置', 'findPassword', msg)
                send_message_by_pusher(msg, [op.wx_id], 5)
                db.session.add(op)
                db.session.commit()
                db.session.close()
    print('我是key的后缀', os.getenv('QR_CODE_SUFFIX'))
    key = '{}-pusher-post-data'.format(user_id)
    redis_client.setrange(key, 0, str(data))  # 把数据存入redis
    print('key的过期时间：', os.getenv('QR_CODE_VALID_TIME'))
    print('redis中的值', redis_client.get('key'), type(redis_client.get('key')))
    return "ok"


@oauth.route('/qq')
@login_required
def open_qq():
    pass



