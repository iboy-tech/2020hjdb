# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : check_data.py
@Time    : 2020/3/21 9:34
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 对用户请求内容做合法性校验
@Software: PyCharm
"""
import re
from functools import wraps

from flask import request

from app import PostConfig
from app.utils import restful


# 评论表单检查
def check_comment(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        if req is not None:
            print("添加评论")
            print(req['content'])
            if req['content'] == "":
                return restful.success(False, msg="评论内容不能为空")
            if len(req['content']) > PostConfig.MAX_COMMENT_LENGTH:
                return restful.success(False, msg="评论字数大于" + PostConfig.MAX_COMMENT_LENGTH)
            if req["content"].isspace():  # 全部是空格
                return restful.success(False, msg="评论内容无效")
            return func(*args, **kwargs)
        print("查看评论")
        return func(*args, **kwargs)

    return decorated_view


# 反馈表单检查
def check_feedback(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        try:
            if req['subject'] == "" or req['content'] == "":
                return restful.params_error(msg="反馈标题或内容不能为空")
            if req["subject"].isspace() or req['content'].isspace():  # 全部是空格
                return restful.params_error(msg="请认真填写反馈信息")
        except:
            return restful.params_error()
        return func(*args, **kwargs)

    return decorated_view


# 检查学号格式
def check_username(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        try:
            username = req['username']
            if not username.isnumeric():
                return restful.params_error(msg="学号格式错误")
            else:
                return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return restful.params_error()
    return decorated_view


# 注册表单检查
def check_qq(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        try:
            qq = req['qq']
            # 正则表达式
            pattern = "^[1-9]\\d{4,10}$"
            res = re.findall(pattern, qq)
            print(res, "验证QQ", qq)
            if res:
                return func(*args, **kwargs)
            else:
                return restful.params_error(msg="QQ号格式错误")
        except Exception as e:
            print(str(e))
            return restful.params_error()

    return decorated_view


# 发帖表单检查
def check_post(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        try:
            if req['applyKind'] not in [0, 1]:
                return restful.params_error(msg="类型有误")
            if req['title'] == "" or req['about'] == "":
                return restful.params_error(msg="标题或详情不能为空")
            if req["title"].isspace() or req['about'].isspace():  # 全部是空格
                return restful.success(False, msg="内容或标题无效")
            if len(req['images']) > PostConfig.MAX_UPLOAD_IMG_NUM:
                return restful.params_error(msg="最多上传{}张图片".format(PostConfig.MAX_UPLOAD_IMG_NUM))
        except:
            return restful.params_error()
        return func(*args, **kwargs)

    return decorated_view
