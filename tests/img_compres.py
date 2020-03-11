# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : img_compres.py
@Time    : 2020/3/9 22:17
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import os

from PIL import Image


def compress_image(infile, outfile='', mb=0.1, step=10, quality=0):
    print("执行了")
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    print("图片大小",o_size)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality,subsampling=0)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)


def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024



print("执行了")
path = "..\\app\\static\\upload\\d119013dca4a43978fb84de2a53f2209.png"
compress_image(path,"..\\app\\static\\d119013dca4a43978fb84de2a53f2209.png", mb=300, step=10, quality=80)
print(os.path.getsize(path)/1024)
