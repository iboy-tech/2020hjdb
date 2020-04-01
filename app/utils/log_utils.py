# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : log_utils.py
@Time    : 2020/3/27 12:07
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import json
import os
import uuid
from datetime import datetime

import requests
from flask import request
from flask_login import current_user

from app import redis_client
from app.config import LoginConfig, LogConfig
from app.utils.wechat_notice import send_message_by_pusher


def get_log():
    data = get_login_info(current_user, 1)  # 仅仅获取IP信息
    print(request.url)
    print(request.query_string)
    print(data)
    data.pop("is_admin")
    data.pop("real_name")
    ext = {
        "url": request.url.replace(os.getenv("SITE_URL").replace("https", "http"), ""),
        "username": current_user.username
    }
    data.update(ext)
    return data


def add_log(type_id, data, expire_time=LogConfig.REDIS_EXPIRE_TIME):
    type_map = {
        0: "数据删除",
        1: "管理登录",
    }
    key = {
        0: uuid.uuid4().hex,  # redis的前缀
        1: current_user.username,
    }
    if type_id == 0:
        detail = "删除 {} 篇帖子".format(data["num"])
    elif type_id == 1:
        detail = "IP:{},地址:{}".format(data["ip"], data["addr"])
    info = {
        "real_name": current_user.real_name,
        "type": type_map.get(type_id),
        "detail": detail,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    key = key.get(type_id) + LogConfig.REDIS_ADMIN_LOG_KEY
    redis_client.set(key, json.dumps(info))
    redis_client.expire(key, expire_time)


def custom_sort(preprocess_func=lambda x: x):
    def cmp_datetime(a, b):
        a = preprocess_func(a)
        b = preprocess_func(b)
        a_datetime = datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
        b_datetime = datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
        if a_datetime > b_datetime:
            return -1
        elif a_datetime < b_datetime:
            return 1
        else:
            return 0

    return cmp_datetime


def get_login_info(user, kind):
    ip = request.remote_addr
    print("我是转发的ip", ip)
    try:
        _ip = request.headers.get("X-Real-IP")
        print("X-Real-IP", _ip)
        if _ip is not None:
            ip = _ip
    except Exception as e:
        print(e)
    print("我是最终的ip", ip)
    data = requests.get(LoginConfig.LOGIN_INFO_API.replace("{}", ip)).text
    data = eval(data)
    print(data)
    info = {
        "real_name": user.real_name,
        "ip": data.get("ip"),
        "addr": data.get("addr"),
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "is_admin": user.kind > 1,
    }
    if kind == 0:  # 登录异常检测，需要发送信息
        send_message_by_pusher(info, [user.wx_open.wx_id], 6)
        print(info)
    else:
        return info
