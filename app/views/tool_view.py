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
import os
import re

from flask import render_template, request

from flask_login import login_required

from app import redis_client, cache, logger
from app.config import PostConfig, LoginConfig
from app.decorators import admin_required, super_admin_required
from app.models.lostfound_model import LostFound
from app.page import tool
# 通过接口进行无损压缩
from app.utils import restful
from app.utils.delete_file import remove_files
from app.utils.img_process import find_big_img, change_all_img_scale
from app.utils.tinypng_util import tinypng


@tool.route('/<key>', methods=['POST'])
@login_required
@admin_required
def add(key):
    if not re.match(r"^[a-z0-9A-Z]+$", key):
        return restful.error("秘钥格式错误")
    key_pre = PostConfig.TINYPNG_REDIS_KEY
    mapping = {key: 500}
    res = redis_client.zadd(key_pre, mapping)
    if res != 0:
        return restful.success(msg="添加成功")
    else:
        return restful.error("秘钥已存在")


@tool.route('/<key>', methods=['DELETE'])
@login_required
@super_admin_required
def delete(key):
    key_pre = PostConfig.TINYPNG_REDIS_KEY
    res = redis_client.zrem(key_pre, key)
    if res != 0:
        return restful.success(msg="删除成功")
    else:
        return restful.error()


@tool.route('/import', methods=['GET'])
@login_required
@admin_required
def import_keys():
    cnt = 0
    try:
        with open("app/static/temp/tiny_keys.txt") as f:
            for api_key in f:
                api_key = api_key[:-1]  # 去掉换行符
                key = PostConfig.TINYPNG_REDIS_KEY
                mapping = {api_key: 500}
                res = redis_client.zadd(key, mapping)
                if res is not 0:
                    cnt = cnt + 1
        f.close()
    except Exception as e:
        logger.info(str(e))
        return restful.error("请把秘钥文件(tiny_keys.txt)放在app/static/temp/目录下")
    return restful.success(msg="恭喜，成功导入" + str(cnt) + "个秘钥")


@tool.route('/compress', methods=['GET'])
@login_required
@super_admin_required
def compress():
    big_img = find_big_img()
    if big_img:
        tinypng.delay(big_img)
        return restful.success(msg="异步压缩任务已启动,共有 " + str(len(big_img)) + " 张图片需要压缩")
    else:
        return restful.success(msg="恭喜，所有图片都达到要求了")


@tool.route('/clear', methods=['GET'])
@login_required
@super_admin_required
def clear():
    dir_path1 = os.getenv("PATH_OF_UPLOAD")
    dir_path2 = os.getenv("MINI_IMG_PATH")
    file_names1 = os.listdir(dir_path1)
    file_names2 = os.listdir(dir_path2)
    scan_list = file_names1 if len(file_names1) >= len(file_names2) else file_names2
    delete_list = []
    # 清理redis垃圾数据
    keys1 = redis_client.keys(pattern='*{}*'.format(PostConfig.PUSHER_REDIS_PREFIX))
    if keys1:
        for key in keys1:
            redis_client.delete(key.decode())
    # 清理redis垃圾数据
    keys2 = redis_client.keys(pattern='*{}*'.format(LoginConfig.LOGIN_REDIS_PREFIX))
    if keys2:
        for key in keys2:
            redis_client.delete(key.decode())
    # 查询数据库
    for file in scan_list:
        res = LostFound.query.filter(LostFound.images.like("%" + file + "%")).first()
        if not res:
            delete_list.append(file)
    # 缩略图与上传的文件夹相互比较
    remove_files(delete_list, 0)
    return restful.success(msg="恭喜，脏数据清理完成")


@tool.route('/', methods=['GET'],strict_slashes=False)
@login_required
@admin_required
def getall():
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
            # logger.info(keys, type(keys), type(keys[0]), bytes.decode(keys[0][0]))
    data = {
        'list': list
    }
    return restful.success(data=data)


# 对之前的图片进行批量裁剪
@tool.route('/resize', methods=['GET'])
@login_required
@super_admin_required
def resize():
    # 转化所有png图片为jpg
    # change_all_img_to_jpg()
    # 裁剪upload文件夹下的图片生成缩略图
    change_all_img_scale()
    return restful.success(msg="裁剪成功")
