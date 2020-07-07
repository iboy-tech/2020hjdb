# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : tinify_tool.py
@Time    : 2020/2/1 11:40
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""

# https://temp-mail.org/zh/接码免费申请apikey
from __future__ import absolute_import
import os
from datetime import datetime
from threading import Thread

import tinify


def get_max_key():
    key = PostConfig.TINYPNG_REDIS_KEY
    keys = redis_client.zrange(key, 0, -1, desc=True, withscores=True)
    if keys:
        return bytes.decode(keys[0][0])
    else:
        return "R5gzXY2WKQrCZBhgSvCZRNRgJ2n5MQZQ"


# key = 'mmnYWFKXVlkxsKtFbdx17FSqFj5YhWq0'  # 登录后去主页就可以查看到key
# tinify.key = key
from app import redis_client, logger
from app.config import PostConfig

path = os.getenv('PATH_OF_UPLOAD')
from tasks import celery


def async_compress_imgs(m, n, files):
    images = files[m:n]
    for file in images:
        file = os.path.join(os.getenv("PATH_OF_UPLOAD"), file)
        # 图片原始大小
        original_size = os.path.getsize(file) / 1024
        if original_size < PostConfig.MAX_IMG_SIZE:
            # 小于500kb不压缩
            continue
        try:
            source = tinify.from_file(file)
            source.to_file(file)
        except tinify.AccountError as e:
            logger.info("The error message is: %s" % e.message)
            # Verify your API key and account limit.
        except tinify.ClientError as e:
            logger.info("The error message is: %s" % e.message)
            # Check your source image and request options.
        except tinify.ServerError as e:
            logger.info("The error message is: %s" % e.message)
            # Temporary issue with the Tinify API.
        except tinify.ConnectionError as e:
            logger.info("The error message is: %s" % e.message)
            # A network connection error occurred.
        except Exception as e:
            logger.info("The error message is: %s" % e.message)
            # Something else went wrong, unrelated to the Tinify API.
        # 压缩后大小
        mini_size = os.path.getsize(file) / 1024
        # 减少体积
        compressions_this_month = tinify.compression_count
        left_times = 500 - compressions_this_month
        key = PostConfig.TINYPNG_REDIS_KEY
        mapping = {tinify.key: left_times}
        redis_client.zadd(key, mapping)


# 图片异步压缩队列
@celery.task
def tinypng(files):
    max_key = get_max_key()
    tinify.key = max_key
    start = datetime.now()
    total_imgs = len(files)
    # logger.info("线程的分组", total_imgs // PostConfig.IMG_NUM_IN_THREAD, total_imgs / PostConfig.IMG_NUM_IN_THREAD)
    for i in range(total_imgs // PostConfig.IMG_NUM_IN_THREAD):
        s = Thread(target=async_compress_imgs,
                   args=(i * PostConfig.IMG_NUM_IN_THREAD, (1 + i) * PostConfig.IMG_NUM_IN_THREAD, files))
        # logger.info(i * 5, (1 + i) *5)
        s.start()
        # s.join()
        if total_imgs % PostConfig.IMG_NUM_IN_THREAD != 0 and i == total_imgs // PostConfig.IMG_NUM_IN_THREAD - 1:
            s = Thread(target=async_compress_imgs, args=((i + 1) * PostConfig.IMG_NUM_IN_THREAD, (
                    1 + i) * PostConfig.IMG_NUM_IN_THREAD + total_imgs % PostConfig.IMG_NUM_IN_THREAD, files))
            # logger.info((i+1)* 5, (1 + i) * 5+urllen % 5)
            s.start()
            # s.join()
            # logger.info('线程【', i + 2, '】已启动')

    # thr = Thread(target=send_async_email, args=[app,msg])
    # thr.start()
    # return thr

    # return 'Compress Finished!'


def get_count(data):
    tinify.key = data
    resp = tinify.from_url("https://tinypng.com/web/output/tu2zvxe80hh79f7x40emeg9ueewb2d13/tick.png")
    compressions_this_month = tinify.compression_count
    return 500 - compressions_this_month



