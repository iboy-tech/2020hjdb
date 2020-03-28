# # -*- coding:UTF-8 -*-
# #!/usr/bin/python
# """
# @File    : access_token.py
# @Time    : 2020/1/16 13:34
# @Author  : iBoy
# @Email   : iboy@iboy.tech
# @Software: PyCharm
# """
# # from __future__ import  print_function
# import ast
# import redis
# import requests
# from idna import unicode
#
#
# r=redis.Redis(host='127.0.0.1',port=6379)
# obj=r.get("...")
# print(unicode(obj,encoding="utf-8"))
# # print(*obj)
# # print(repr(obj).encode('utf-8'))
# def refresh_token():
#     resp=requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}').__format__(APPID,APPSECRET)
#     # print(resp,type(resp))
#     # print(resp.text,type(resp.text))
#     # obj=json.load(resp.text)
#     data=ast.literal_eval(resp.text)
#     print(data,type(data))
#     data.get('access_token')