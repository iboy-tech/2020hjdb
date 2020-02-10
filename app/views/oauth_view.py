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
import os

from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import db, OpenID, redis_client
from app.main import oauth
from app.wxpusher import WxPusher


@oauth.route('/wx', methods=['GET', 'POST'], strict_slashes=False)
def index():
    # print('SECRET_KEY', os.getenv('SECRET_KEY'))
    # print('request.sid',request.sid)

    if current_user.is_authenticated and request.method == 'GET':
        op = OpenID.query.filter_by(user_id=current_user.id)
        if op is not None:
            return redirect(url_for('user.index'))
        data = (WxPusher.create_qrcode(extra=current_user.id,valid_time=180))
        # print(type(data), data)
        if data['success']:
            data = data['data']
            # print('user_id', data['extra'])
            # print('qr_code', data['url'])
            data = {
                'url': data['url']
            }
            return render_template('pusher.html', data=data)
    elif request.method == 'GET':
        return redirect(url_for('auth.login')),301
    elif request.method == 'POST':
        data = request.json['data']
        wx_open_id = data['uid']
        # print('用户的OPEN-ID', wx_open_id)
        user_id = data['extra']
        # print('用户的ID', user_id)
        op = OpenID(user_id=user_id, wx_id=wx_open_id)
        db.session.add(op)
        db.session.commit()
        """
        redis_store = FlaskReis()
        redis_store.get(key)
        get函数接受一个键，通过此键如果有缓存就返回缓存，没有就返回None,常配合条件语句使用
        redis_store.set(key,value)
        set函数接受一个键和值,主要作用是写入缓存
        redis_store.expire(key,time)
        expire函数接受一个键，一个时间（格式可以类似3600*24），设置缓存的期限
        """
        print('我是key的后缀',os.getenv('QR_CODE_SUFFIX'))
        key=str(user_id)+'-pusher-post-data'
        redis_client.setrange(key,0,str(data)) # 把数据存入redis
        print('key的过期时间：',os.getenv('QR_CODE_VALID_TIME'))
        print('redis中的值',redis_client.get('key'),type(redis_client.get('key')))
        return data


@oauth.route('/qq')
@login_required
def open_qq():
    pass
