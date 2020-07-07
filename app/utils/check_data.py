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

from app import PostConfig, logger
from app.utils import restful


# 评论表单检查
def check_comment(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        if req is not None:
            if req['content'] == "":
                return restful.error("评论内容不能为空")
            if len(req['content']) > PostConfig.MAX_COMMENT_LENGTH:
                return restful.error("评论字数大于" + PostConfig.MAX_COMMENT_LENGTH)
            if req["content"].isspace():  # 全部是空格
                return restful.error("评论内容无效")
            return func(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view


# 反馈表单检查
def check_feedback(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        try:
            if req['subject'] == "" or req['content'] == "":
                return restful.error("反馈标题或内容不能为空")
            if req["subject"].isspace() or req['content'].isspace():  # 全部是空格
                return restful.error("请认真填写反馈信息")
        except:
            return restful.error()
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
                return restful.error("学号格式错误")
            else:
                return func(*args, **kwargs)
        except Exception as e:
            logger.info(str(e))
            return restful.error()

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
            if res:
                return func(*args, **kwargs)
            else:
                return restful.error("QQ号格式错误")
        except Exception as e:
            logger.info(str(e))
            return restful.error()

    return decorated_view


# 发帖表单检查
def check_post(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        req = request.json
        try:
            if req['applyKind'] not in [0, 1]:
                return restful.error("类型有误")
            if req['title'] == "" or req['about'] == "":
                return restful.error("标题或详情不能为空")
            if req["title"].isspace() or req['about'].isspace():  # 全部是空格
                return restful.error("内容或标题无效")
            if len(req['images']) > PostConfig.MAX_UPLOAD_IMG_NUM:
                return restful.error("最多上传{}张图片".format(PostConfig.MAX_UPLOAD_IMG_NUM))
            if req['images']:  # 对文件类型进行判断
                for imgbs4 in req['images']:
                    file_type = imgbs4.split(";")[0].split(":")[1].split("/")
                    if file_type[1] not in PostConfig.ALLOW_UPLOAD_FILE_TYPE:
                        return restful.error("只能上传JPG或PNG格式的图片")
        except:
            return restful.error()
        return func(*args, **kwargs)

    return decorated_view
