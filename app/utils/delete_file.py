# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : delete_file.py
@Time    : 2020/3/21 22:33
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 文件删除模块
@Software: PyCharm
"""
import os

from tasks import celery


# 删除文件列表
@celery.task
def remove_files(filenames, kind):
    file_path = {
        0: os.getenv("PATH_OF_UPLOAD"),  # 大图片
        1: os.getenv("MINI_IMG_PATH"),  # 小图片
        2: os.getenv("PATH_OF_REPORT")  # 报表
    }
    if filenames:
        for file in filenames:
            try:
                if kind != 2:
                    os.remove(os.path.join(file_path.get(0), file))
                    os.remove(os.path.join(file_path.get(1), file))
                else:
                    os.remove(os.path.join(file_path.get(2), file))
            except Exception as e:
                print('删除文件', str(e))
