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
from app import redis_client
from app.config import PostConfig

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

ImageFile.LOAD_TRUNCATED_IMAGES = True


def change_all_img_to_jpg():
    dir = os.getenv("PATH_OF_UPLOAD")
    # dir = "O:\\Python\\Flask-WC\\app\\static\\upload\\"
    allFile = os.listdir(dir)
    print(len(allFile))
    for file in allFile:
        # print(file, type(file))
        try:
            image = Image.open(dir + file)
            print(image.mode)
            if image.mode != "RGB" or file.endswith("png"):
                image = image.convert('RGB')
                new_name = file.replace("png", "jpg")
                print(new_name)
                image.save(dir + new_name)
                os.remove(dir+file)
        except Exception as e:
            print("出现意外错误", str(e))


# resize_images(r"..\\app\\static\\upload", r"..\\app\\static\\upload", 140000)
def change_all_img_scale():
    dir = os.getenv("PATH_OF_UPLOAD")
    min_dir = os.getenv("MINI_IMG_PATH")
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
            print("错误", str(e), file)

def find_big_img():
    dir = os.getenv("PATH_OF_UPLOAD")
    allFile = os.listdir(dir)
    fileMap = {}
    print(len(allFile))
    for file in allFile:
        print(file, type(file))
        # 字节数转换为kb数
        size = (os.path.getsize(dir + file) / 1024)
        print(size)
        if size < PostConfig.MAX_IMG_SIZE:
            print("<200kb,无需压缩")
        else:
            fileMap.setdefault(file, size)
    filelist = sorted(fileMap.items(), key=lambda d: d[1], reverse=True)
    big_img = []
    for filename, size in filelist:
        print("filename is %s , and size is %d" % (filename, size))
        big_img.append(filename)
    print("需要压缩的图片", big_img, len(big_img))
    return big_img
# 传入文件名称
def change_img_scale(file):
    dir = os.getenv("PATH_OF_UPLOAD")
    min_dir = os.getenv("MINI_IMG_PATH")
    print(os.path.join(dir, file))
    img = Image.open(os.path.join(dir, file))
    w, h = img.size
    newWidth = 100
    newHeight = round(newWidth / w * h)
    img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
    print(file, type(file))
    print(os.path.join(min_dir, file))
    try:
        img.save(os.path.join(min_dir, file), optimize=True, quality=10)
    except Exception as e:
        print("出现错误",str(e))


# file = "1559b6de23e34c4a8e44d9e1e29a05df.png"
# change_img_scale(file)
# change_all_img_to_jpg()
# change_all_img_scale()
def get_max_key():
    key = PostConfig.TINYPNG_REDIS_KEY
    keys = redis_client.zrange(key, 0, -1, desc=True, withscores=True)
    if keys:
        return bytes.decode(keys[0][0])
    else:
        return "R5gzXY2WKQrCZBhgSvCZRNRgJ2n5MQZQ"
