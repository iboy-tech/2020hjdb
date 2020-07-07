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

from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import db, OpenID, redis_client, PostConfig, logger
from app.page import oauth
from app.utils import mail_sender
from app.utils.auth_token import generate_password
from app.utils.wxpusher import WxPusher
from app.views.found_view import send_message_by_pusher


@oauth.route('/wx.html', methods=['GET'], strict_slashes=False)
@oauth.route('/wx', methods=['POST'], strict_slashes=False)
def index():
    if current_user.is_authenticated and request.method == 'GET':
        op = OpenID.query.filter_by(user_id=current_user.id).first()
        if op:  # 已经绑定过了
            return redirect(url_for('auth.index')), 301
        data = (WxPusher.create_qrcode(extra=current_user.id, valid_time=180))
        # logger.info(type(data), data)
        if data['success']:
            data = data['data']
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
        # logger.info('用户的ID', user_id,type(user_id))
        # 如果是数字说明是初始扫码绑定
        if user_id.isnumeric():
            try:
                op = OpenID(user_id=user_id, wx_id=wx_open_id)
                db.session.add(op)
                db.session.commit()
                db.session.close()
            except:
                key = '{}'.format(user_id) + PostConfig.PUSHER_REDIS_PREFIX
                redis_client.setrange(key, 0, "exist")  # 不是系统用户重置密码
                return "false"
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
            logger.info("用户：%s 找回密码" % current_user.real_name)
            data = request.json['data']
            wx_open_id = data['uid']
            op = OpenID.query.filter_by(wx_id=wx_open_id).first()
            if op:
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
                mail_sender.send_email.delay(op.user.qq, '密码重置', 'findPassword', msg)
                send_message_by_pusher(msg, [op.wx_id], 5)
                db.session.add(op)
                db.session.commit()
                db.session.close()
            else:
                key = '{}'.format(user_id) + PostConfig.PUSHER_REDIS_PREFIX
                redis_client.setrange(key, 0, "guest")  # 不是系统用户重置密码
                return "false"
    key = '{}'.format(user_id) + PostConfig.PUSHER_REDIS_PREFIX
    redis_client.setrange(key, 0, str(data))  # 把数据存入redis
    return "ok"


@oauth.route('/qq')
@login_required
def open_qq():
    pass
