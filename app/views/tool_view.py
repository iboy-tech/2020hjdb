# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : tool_view.py
@Time    : 2020/3/12 23:02
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import re

from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required

from app import redis_client
from app.config import PostConfig
from app.decorators import admin_required
from app.page import tool
# 通过接口进行无损压缩
from app.utils import restful
from app.utils.img_compress import find_big_img
from app.utils.tinify_tool import tinypng


@tool.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
@cross_origin()
def index():
    return render_template('tool.html')


@tool.route('/addKey', methods=['GET', 'POST'])
@login_required
@admin_required
@cross_origin()
def add():
    req = request.args.get('key');
    print(req)
    if not re.match(r"^[a-z0-9A-Z]+$", req):
        return restful.success(False, msg="秘钥格式错误")
    key = PostConfig.TINYPNG_REDIS_KEY
    mapping = {req: 500}
    res = redis_client.zadd(key,mapping)
    print("添加结果", res)
    if res != 0:
        return restful.success(msg="添加成功")
    else:
        return restful.success(False, msg="秘钥已存在")


@tool.route('/deleteKey', methods=['GET', 'POST'])
@login_required
@admin_required
@cross_origin()
def delete():
    id = request.args.get("key")
    key = PostConfig.TINYPNG_REDIS_KEY
    res = redis_client.zrem(key, id)
    if res != 0:
        return restful.success(msg="删除成功")
    else:
        return restful.params_error()


@tool.route('/compress', methods=['GET', 'POST'])
@login_required
@admin_required
@cross_origin()
def compress():
    big_img=find_big_img()
    if big_img:
        tinypng.delay(big_img)
        return restful.success(msg="异步压缩任务已启动,共有 "+str(len(big_img))+" 张图片需要压缩")
    else:
        return restful.success(msg="恭喜，所有图片都达到要求了")



# 通过接口进行无损压缩
@tool.route('/getall', methods=['GET', 'POST'])
@login_required
@admin_required
@cross_origin()
def getall():
    req = request.args.get('key');
    print(req)
    key = PostConfig.TINYPNG_REDIS_KEY
    keys = redis_client.zrange(key, 0, -1, desc=True, withscores=True)
    # max = redis_client.bzpopmax(key)
    list = []
    if keys:
        for k in keys:
            dict = {
                'key': bytes.decode(k[0]),
                'count': int(k[1])
            }
            list.append(dict)
            print(keys, type(keys), type(keys[0]), bytes.decode(keys[0][0]))
    data = {
        'list': list
    }
    return restful.success(data=data)



