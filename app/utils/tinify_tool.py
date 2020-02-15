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


# https://temp-mail.org/zh/接码免费申请apikey
from datetime import datetime

from celery_app import celery



# 图片异步压缩队列
@celery.task(time_limit=10)
def tinypng(files):
    import os
    import tinify
    from datetime import datetime
    key = 'mmnYWFKXVlkxsKtFbdx17FSqFj5YhWq0'  # 登录后去主页就可以查看到key
    tinify.key = key
    path = os.getenv('PATH_OF_UPLOAD')
    start_time = datetime.now()
    for file in files:
        file = os.path.join(path, file)
        print('我是压缩函数中图片的路径', file)
        # 图片原始大小
        original_size = os.path.getsize(file) / 1000
        if original_size < 500:
            # 小于500kb不压缩
            continue
        try:
            source = tinify.from_file(file)
            source.to_file(file)
        except tinify.AccountError as e:
            print("The error message is: %s" % e.message)
            # Verify your API key and account limit.
        except tinify.ClientError as e:
            print("The error message is: %s" % e.message)
            # Check your source image and request options.
        except tinify.ServerError as e:
            print("The error message is: %s" % e.message)
            # Temporary issue with the Tinify API.
        except tinify.ConnectionError as e:
            print("The error message is: %s" % e.message)
            # A network connection error occurred.
        except Exception as e:
            print("The error message is: %s" % e.message)
            # Something else went wrong, unrelated to the Tinify API.
        # 压缩后大小
        mini_size = os.path.getsize(file) / 1000
        # 减少体积
        compressions_this_month = tinify.compression_count
        remove_size = round(original_size - mini_size)
        print('压缩前：', original_size, '压缩后：', mini_size, '减少：', remove_size)
        print('剩余的压缩次数', 500 - compressions_this_month)
    end_time = datetime.now()
    print('压缩用时', end_time - start_time)
    return 'Compress Finished!'


if __name__ == '__main__':
    # p = Pool(4)
    # for path in imgs:
    #     p.apply_async(tinypng, args=(path,))
    # p.close()
    # p.join()
    img = ['8438ba8e6ac641048316217c47cae372.png']
    file = 'O:\\Python\\Flask-WC\\app\\static\\upload\\8438ba8e6ac641048316217c47cae372.png'
    print(file)
    start_time = datetime.now()
    tinypng(file)
