# encoding:utf-8
import datetime
import json

from app.models.robot_model import Robot


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, Robot):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


class HttpCode(object):
    Ok = 200
    ParamerError = 400
    Unauth = 401
    ServerError = 500
    Forbidden = 403


def RestfulResult(success, code, msg, data, ext=None):
    data = json.dumps({'success': success, 'code': code, 'msg': msg, 'data': data, 'ext': ext}, cls=MyEncoder)
    # logger.info("生成消息类", str(data))
    return data


def success(success=True, msg="处理成功", data={"user": {}}, ext=None):
    return RestfulResult(success, HttpCode.Ok, msg=msg + "！", data=data, ext=ext)


def error(msg="参数错误"):
    return RestfulResult(False, -1, msg=msg + "！", data={}, ext=None)


def params_error(success=False, msg="参数错误", data={}, ext=None):
    return RestfulResult(success, HttpCode.ParamerError, msg=msg + "！", data=data, ext=ext)


def unauth_error(success=False, msg="请登录后操作", data={}, ext=None):
    return RestfulResult(success, HttpCode.Unauth, msg=msg + "！", data=data, ext=ext)


def server_error(success=False, msg="服务器繁忙", data={}, ext=None):
    return RestfulResult(success, HttpCode.ServerError, msg=msg + "！", data=data, ext=ext)


def forbidden_error(success=False, msg="权限不足！", data={}, ext=None):
    return RestfulResult(success, HttpCode.Forbidden, msg=msg + "！", data=data, ext=ext)
