# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : create_data.py
@Time    : 2020/3/17 19:02
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import base64
import json
import os
import random

import requests
from faker.factory import Factory

Faker = Factory().create('zh_CN')


def get_detail():
    return Faker.paragraph()


def get_title():
    return Faker.sentence()


def get_name():
    return Faker.name()


def get_address():
    return Faker.street_address()


def get_phone_number():
    return Faker.phone_number()


print(get_address(), get_name(), get_phone_number())

path = "C:\\Users\\Default Account\\Desktop\\Weibo-Album-Crawler\\downloads\\images"


def to_base64(file):
    if files:
        list = []
        str = "data:image/jpg;base64,"
        for mf in file:
            with open(os.path.join(path, mf), "rb") as f:
                base64_data = base64.b64encode(f.read())
                list.append(str + base64_data.decode("utf-8"))
        return list
    else:
        print("没有照片啦")


files = os.listdir(path)

category = [1, 6, 15, 16, 17, 18, 19, 21, 24]
def get_images():
    print(files)
    print(len(files)//3)
    for i in range(0, len(files)//3):
        print(i+3*i, i+3*i+3,files[i+3*i:i+3*i+3])
        data = {
            "applyKind": random.randint(0, 1),
            "categoryIndex": random.randint(0, 1),
            "categoryId": category[random.randint(0, len(category)-1)],
            "title": get_title(),
            "about": "姓名：" + get_name() + "，联系电话：" + get_phone_number() + " 内容：" + get_detail(),
            "location": get_address(),
            "images": to_base64(files[i+3*i:i+3*i+3]),
            "info": "",
        }
        url = "https://ctguswzl.cn/found.html/pub"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
            "Content-Type": "application/json;charset=UTF-8",
            "Cookie": "shipyard=MTU4MzY1ODA1MXxEdi1CQkFFQ180SUFBUkFCRUFBQUpfLUNBQUVHYzNSeWFXNW5EQW9BQ0hWelpYSnVZVzFsQm5OMGNtbHVad3dIQUFWaFpHMXBiZz09fHPM8aHdsBftc8GJJTcBxz_sSM8wOoSHp3nR0esBDwAB; remember_token=5|67c4a6b0f939f9db3fb2d564e3c54ae9ab441b3fb30b2fda5c7eca3f7167167f720b659cdc46e273cdfe55b2aa6bb52fd78062a0d23671e484999d957633b2f8; Hm_lvt_cadc146ea11d785cac889d32e36f336b=1584405977,1584421365,1584423862,1584427921; Hm_lpvt_cadc146ea11d785cac889d32e36f336b=1584441909; session=.eJztUkFuxCAM_ErFOQdwAEO-UlYrA6a7UhNVIUiVVvv3Olr1Dz30MgzYnhkkP9S1fVK_cVfL-0O9HXKolXunD1aTSsM2r9Nwrbg0YsCcBvoTo7de3q3mNDzYmkbQ7cScm1Qd88n5NXUielCX5_Tv8ac8LpMswM79ppZjHyy3e1WLQg5kqcYQnQZrcmVGyBhNaNYYADbYLKGLfi6z2GmoFsA41KLrCpVCswXviLQJQE4EIhI2cJJKG8plhmC0jVhIekpjnN1sRDJUiW3kq9cv3lfaeDt-o238LVxRXe-bNIzO-yutU88fNt3YUg.XnCyBA.qRRE9jmFYmUjLF__tbFCxLb4G6A",
        }
        resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        print(resp)

get_images()



