# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : detail_view.py
@Time    : 2020/1/25 22:30
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template

from app.main import detail

@detail.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def index():
    item={
          "success" : True,
          "code" : 1000,
          "msg" : "处理成功",
          "data" : {
            "item" : {
              "id" : "b8a3d60480fd45308fd16c1fcfe77caa",
              "icon" : "upload_6720338131142720698.jpg",
              "kind" : 0,
              "userId" : "6529d0739c344ccba3f4f0f820edcc98",
              "username" : "201520180508",
              "realName" : "普通用户",
              "time" : "2020-01-21 13:12",
              "location" : "欣苑",
              "title" : "手机掉了",
              "about" : "手机掉了啊啊啊详情",
              "images" : [ "upload_8124810867403574170.jpg" ],
              "category" : "手机",
              "lookCount" : 14,
              "status" : 1,
              "dealTime" : None,
              "isSelf" : True,
              "email" : "547142436@qq.com",
              "phoneNumber" : "123456 "
            }
          },
          "ext" : None
        }
    comments={
      "success" : True,
      "code" : 1000,
      "msg" : "处理成功",
      "data" : {
        "comments" : [ {
          "id" : "b659546fb35b465e839ed91989fed40c",
          "icon" : "upload_6720338131142720698.jpg",
          "username" : "201520180508",
          "time" : "2020-01-21 13:13",
          "content" : "哈哈"
        } ]
      },
      "ext" : None
    }
    return render_template('detail.html',item=item,comments=comments)