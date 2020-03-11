# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : img_c2.py
@Time    : 2020/3/9 22:57
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import os
from PIL import Image
import glob

DIR = r'../app/static/upload'


class Compress_Picture(object):
    def __init__(self):
        # 图片格式，可以换成.bpm等
        self.file = '.JPG'

    # 图片压缩批处理

    def compressImage(self):

        for filename in glob.glob('%s%s%s' % (DIR, '*', self.file)):
            # print(filename)
            # 打开原图片压缩
            sImg = Image.open(filename)
            w, h = sImg.size
            print(w, h)
            dImg = sImg.resize((1280, 1080), Image.ANTIALIAS)  # 设置压缩尺寸和选项，注意尺寸要用括号
            # 小米6: 1008 * 754
            # 320*240  640*480 800*600 1024*768 1152*864 1280*960 1400*1050 1600*1200 2048*1536
            # 如果不存在目的目录则创建一个
            comdic = "%scompress/" % DIR
            if not os.path.exists(comdic):
                os.makedirs(comdic)

                # 压缩图片路径名称
            f1 = filename.split('/')
            f1 = f1[-1].split('\\')
            f2 = f1[-1].split('.')
            f2 = '%s%s1%s' % (comdic, f2[0], self.file)
            # print(f2)
            dImg.save(f2)  # save这个函数后面可以加压缩编码选项JPEG之类的
            print("%s compressed succeeded" % f1[-1])


obj = Compress_Picture()

obj.compressImage()
