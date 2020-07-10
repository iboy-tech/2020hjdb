# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : img_process.py
@Time    : 2020/3/9 23:30
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
# -*- coding:UTF-8 -*-
# !/usr/bin/python
import base64
import uuid
from io import BytesIO

from app import logger
from app.config import PostConfig
from app.utils.tinypng_util import tinypng
from tasks import celery

"""
@File    : img_3c.py
@Time    : 2020/3/9 23:04
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 图片处理
@Software: PyCharm
"""
import os

from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


@celery.task
def compress_imgs_in_freetime():
    big_img = find_big_img()
    if big_img:
        tinypng(big_img)



def change_all_img_to_jpg():
    dir = os.getenv("PATH_OF_UPLOAD")
    # dir = "O:\\Python\\Flask-WC\\app\\static\\upload\\"
    allFile = os.listdir(dir)
    # logger.info(len(allFile))
    for file in allFile:
        # logger.info(file, type(file))
        try:
            image = Image.open(dir + file)
            # logger.info(image.mode)
            if image.mode != "RGB" or file.endswith("png"):
                image = image.convert('RGB')
                new_name = file.replace("png", "jpg")
                # logger.info(new_name)
                image.save(dir + new_name)
                os.remove(dir + file)
        except Exception as e:
            logger.info(str(e))


# resize_images(r"..\\app\\static\\upload", r"..\\app\\static\\upload", 140000)
def change_all_img_scale():
    dir = os.getenv("PATH_OF_UPLOAD")
    min_dir = os.getenv("MINI_IMG_PATH")
    allFile = os.listdir(dir)
    for file in allFile:
        # logger.info(file, type(file))
        img = Image.open(dir + file)
        w, h = img.size
        newWidth = 100
        # 四舍五入
        newHeight = round(newWidth / w * h)
        img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
        try:
            img.save(min_dir + file, optimize=True, quality=85)
            # logger.info(min_dir + file)
        except Exception as e:
            logger.info(str(e))


def find_big_img():
    dir = os.getenv("PATH_OF_UPLOAD")
    allFile = os.listdir(dir)
    fileMap = {}
    # logger.info(len(allFile))
    for file in allFile:
        # 字节数转换为kb数
        size = (os.path.getsize(dir + file) / 1024)
        if size > PostConfig.MAX_IMG_SIZE:
            fileMap.setdefault(file, size)
    filelist = sorted(fileMap.items(), key=lambda d: d[1], reverse=True)
    big_img = []
    for filename, size in filelist:
        # logger.info("filename is %s , and size is %d" % (filename, size))
        big_img.append(filename)
    # logger.info("需要压缩的图片", big_img, len(big_img))
    return big_img


# 传入文件名称
def change_img_scale(file):
    dir = os.getenv("PATH_OF_UPLOAD")
    min_dir = os.getenv("MINI_IMG_PATH")
    img = Image.open(os.path.join(dir, file))
    w, h = img.size
    newWidth = 100
    newHeight = round(newWidth / w * h)
    img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
    try:
        img.save(os.path.join(min_dir, file), optimize=True, quality=80)
    except Exception as e:
        logger.info(str(e))


# 对上传图片进行格式转换并裁剪
def change_bs4_to_png(imglist):
    files = []
    for img in imglist:
        bas4_code = img.split(',')
        filename = uuid.uuid4().hex + '.jpg'
        files.append(filename)
        myfile = os.path.join(os.getenv("PATH_OF_UPLOAD"), filename)
        # logger.info("保存的路径", myfile)
        image = base64.b64decode(bas4_code[1])
        image = BytesIO(image)
        image = Image.open(image)
        image = image.convert('RGB')
        image.save(myfile)
        # 生成缩略图
        change_img_scale(filename)
        # 后台检查图片大小
        if os.path.getsize(myfile) / 1024 > PostConfig.UPLOAD_MAX_SIZE:
            try:
                os.remove(myfile)
                os.remove(os.getenv("MINI_IMG_PATH") + filename)
                # 一张图片超过上限返回空值
                return True, ''
            except Exception as e:
                logger.info(str(e))
    if files:
        tinypng.delay(files)
    # logger.info(files, '我是文件名')
    return False,files
