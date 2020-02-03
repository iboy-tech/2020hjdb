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
# -*- coding：utf-8 -*-
import tinify
import glob
import os
from datetime import datetime
from multiprocessing import Pool

start_time = datetime.now
# https://temp-mail.org/zh/接码免费申请apikey
key = 'mmnYWFKXVlkxsKtFbdx17FSqFj5YhWq0'  # 登录后去主页就可以查看到key
tinify.key = key
PATH_OF_IMAGES_DIR = os.getenv('PATH_OF_IMAGES_DIR')
PATH_OF_IMAGES_DIR = '..\\static\\upload'
# print(os.listdir(PATH_OF_IMAGES_DIR))

imgs = glob.glob(PATH_OF_IMAGES_DIR + '/*.[jp][pn]g')


def tinypng(path):
    # 图片原始大小
    original_size = os.path.getsize(path) / 1000
    source = tinify.from_file(path)
    source.to_file(path)
    # 压缩后大小
    mini_size = os.path.getsize(path) / 1000
    # 减少体积
    remove_size = round(original_size - mini_size, 3)
    print(
        f'图片：\x1b[1;34m{path}\x1b[0m, 压缩前：\x1b[1;34m{str(original_size)}kb\x1b[0m, 压缩后：\x1b[1;34m{str(mini_size)}kb\x1b[0m, 减少：\x1b[1;34m{str(remove_size)}kb\x1b[0m'
    )


if __name__ == '__main__':
    p = Pool(4)
    for path in imgs:
        p.apply_async(tinypng, args=(path,))
    p.close()
    p.join()
    end_time = datetime.now
    total_seconds = (end_time - start_time).total_seconds()
    print('一共用了 %f s' % total_seconds)
