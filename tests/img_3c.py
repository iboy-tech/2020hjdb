# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : img_3c.py
@Time    : 2020/3/9 23:04
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import math
import os
from glob import glob

from PIL import Image


def resize_images(source_dir, target_dir, threshold):
    filenames = glob('{}/*'.format(source_dir))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for filename in filenames:
        filesize = os.path.getsize(filename)
        if filesize >= threshold:
            print(filename)
            with Image.open(filename) as im:
                width, height = im.size
                if width >= height:
                    new_width = int(math.sqrt(threshold / 2))
                    new_height = int(new_width * height * 1.0 / width)
                else:
                    new_height = int(math.sqrt(threshold / 2))
                    new_width = int(new_height * width * 1.0 / height)
                resized_im = im.resize((new_width, new_height))
                output_filename = filename.replace(source_dir, target_dir)
                resized_im.save(output_filename)


resize_images(r"..\\app\\static\\upload", r"..\\app\\static\\upload", 140000)
