# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : img_compress.py
@Time    : 2020/3/9 23:30
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
# -*- coding:UTF-8 -*-
# !/usr/bin/python
import re

"""
@File    : img_3c.py
@Time    : 2020/3/9 23:04
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import os

from PIL import Image
from PIL import ImageFile
from app.config import PostConfig
ImageFile.LOAD_TRUNCATED_IMAGES = True


# resize_images(r"..\\app\\static\\upload", r"..\\app\\static\\upload", 140000)
def change_all_img_scale():
    dir = PostConfig.IMG_UPLOAD_PATH
    min_dir = PostConfig.MINI_IMG_PATH
    allFile = os.listdir(dir)
    for file in allFile:
        print(file, type(file))
        img = Image.open(dir + file)
        w, h = img.size
        newWidth = 100
        # 四舍五入
        newHeight = round(newWidth / w * h)
        img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
        try:
            img.save(min_dir + file, optimize=True, quality=85)
            print(min_dir + file)
        except Exception as e:
            print("错误",str(e),file)


# 传入文件名称
def change_img_scale(file):
    dir = PostConfig.IMG_UPLOAD_PATH
    min_dir = PostConfig.MINI_IMG_PATH
    print(os.path.join(dir, file))
    img = Image.open(os.path.join(dir, file))
    w, h = img.size
    newWidth = 100
    newHeight = round(newWidth / w * h)
    img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
    print(file, type(file))
    print(os.path.join(min_dir, file))
    img.save(os.path.join(min_dir, file), optimize=True, quality=10)


# file = "1559b6de23e34c4a8e44d9e1e29a05df.png"
# change_img_scale(file)

# change_all_img_scale()
