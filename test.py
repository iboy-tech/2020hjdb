# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : test.py
@Time    : 2020/1/13 16:58
@Author  : iBoy
@Email   : iboy@iboy.tech
@Software: PyCharm
"""
import requests
KEY = '0ec0af8b8df84b36ae010fb25be93a89'

def get_response(msg):
    # 这里实现与图灵机器人的交互
    # 构造了要发送给服务器的数据
    apiUrl = 'http://openapi.tuling123.com/openapi/api/v2'
    # data = {
    #     'key' : KEY,
    #   'info' : msg,
    #   'userid' : 'wechat-robot',
    # }
    data={
	"reqType":0,
    "perception": {
        "inputText": {
            "text": "附近的酒店"
        },
        "inputImage": {
            "url": "imageUrl"
        },
        "selfInfo": {
            "location": {
                "city": "北京",
                "province": "北京",
                "street": "信息路"
            }
        }
    },
    "userInfo": {
        "apiKey": KEY,
        "userId": ""
    }
}
    try:
        r = requests.post(apiUrl, data=data).json()
        print(r)
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return