# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : log_view.py
@Time    : 2020/3/23 21:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from functools import cmp_to_key

from flask import render_template, request
from flask_login import login_required

from app import redis_client, LogConfig
from app.decorators import super_admin_required
from app.page import log
from app.utils import restful
from app.utils.log_utils import custom_sort


@log.route('/', strict_slashes=False)
@login_required
@super_admin_required
def index():
    type_map = {
        "admin": render_template('log-admin.html'),
        "error": render_template('log-error.html'),
        "info": render_template('log-info.html'),
    }
    try:
        log_type = request.args.get("type")
        # print("需要"+log_type)
        if log_type not  in type_map.keys():
            return restful.params_error()
    except:
        return  restful.params_error()
    return type_map.get(log_type)


def get_admin_log():
    keys = redis_client.keys(pattern='*{}*'.format(LogConfig.REDIS_ADMIN_LOG_KEY))
    list = []
    for key in keys:
        res = eval(redis_client.get(key.decode()))
        # print(res, type(res))
        list.append(res)
    # 按时间排序
    list.sort(key=cmp_to_key(custom_sort(lambda x: x["time"])))
    return list


def get_error_log():
    keys = redis_client.keys(pattern='*{}*'.format(LogConfig.REDIS_ERROR_LOG_KEY))
    list = []
    for key in keys:
        res = eval(redis_client.get(key.decode()))
        # print(res, type(res))
        list.append(res)
    # 按时间排序
    list.sort(key=cmp_to_key(custom_sort(lambda x: x["time"])))
    return list


def get_info_log():
    keys = redis_client.keys(pattern='*{}*'.format(LogConfig.REDIS_INFO_LOG_KEY))
    list = []
    for key in keys:
        res = eval(redis_client.get(key.decode()))
        # print(res, type(res))
        list.append(res)
    # 按时间排序
    list.sort(key=cmp_to_key(custom_sort(lambda x: x["time"])))
    return list


@log.route('/getall', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@super_admin_required
def get_all():
    log_type = request.args.get("type")
    # print("我是日志类型", log_type)
    type_map = {
        "admin": get_admin_log(),
        "error": get_error_log(),
        "info": get_info_log()
    }
    data = {
        'list': type_map.get(log_type)
    }
    # print(data)
    return restful.success(data=data)


@log.route('/delete', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@super_admin_required
def delete_all():
    log_type = request.args.get("type")
    # print("我是日志类型", log_type)
    type_map = {
        "admin": LogConfig.REDIS_ADMIN_LOG_KEY,
        "error": LogConfig.REDIS_ERROR_LOG_KEY,
        "info": LogConfig.REDIS_INFO_LOG_KEY
    }
    # print("键值" + type_map.get(log_type))
    keys = redis_client.keys(pattern='*{}*'.format(type_map.get(log_type)))
    for key in keys:
        redis_client.delete(key.decode())
    return restful.success(msg='删除成功')
