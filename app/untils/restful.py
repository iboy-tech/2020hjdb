# encoding:utf-8
from flask import jsonify


class HttpCode(object):
    Ok = 200
    ParamerError = 400
    Unauth = 401
    ServerError = 500
    Forbidden = 403


def RestfulResult(success, code, msg, data, ext=None):
    data = jsonify({'success': success, 'code': code, 'msg': msg, 'data': data, 'ext': ext})
    print("生成消息类",str(data))
    return data


def success(success=True, msg="处理成功", data={"user": {}}, ext=None):
    return RestfulResult(success, HttpCode.Ok, msg=msg+"！", data=data, ext=ext)


def params_error(success=False, msg="参数错误", data={}, ext=None):
    return RestfulResult(success, HttpCode.ParamerError, msg=msg+"！", data=data, ext=ext)


def unauth_error(success=False, msg="请登录后操作", data={}, ext=None):
    return RestfulResult(success, HttpCode.Unauth, msg=msg+"！", data=data, ext=ext)


def server_error(success=False, msg="服务器繁忙", data={}, ext=None):
    return RestfulResult(success, HttpCode.ServerError, msg=msg+"！", data=data, ext=ext)


def forbidden_error(success=False, msg="权限不足！", data={}, ext=None):
    return RestfulResult(success, HttpCode.Forbidden, msg=msg+"！", data=data, ext=ext)
