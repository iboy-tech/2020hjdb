# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : user_view.py
@Time    : 2020/1/19 22:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template, request, g, current_app
from flask_cors import cross_origin

from app.main import user


@user.route('/', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
def index():
    data=request.json
    print('user页面收到请求',data)
    print(g)
    print(current_app)
    user = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
                "studentNum": "201520180508",
                "realName": "cpwu",
                "icon": "www.baidu.com/icon.png",
                "email": "cpwu@foxmail.com",
                "phoneNumber": "15911112222",
                "schoolName": "东华理工大学",
                # "gender": 1,
                "createTime": "2019-04-10 19:06:10",
                "lastLogin": "2019-04-10 19:06:10",
                "kind": 0
            }
        # "ext": None
    }
    user={
            "studentNum": "201520180508",
            "realName": "cpwu",
            "icon": "www.baidu.com/icon.png",
            "email": "cpwu@foxmail.com",
            "phoneNumber": "15911112222",
            "schoolName": "东华理工大学",
            # "gender": 1,
            "createTime": "2019-04-10 19:06:10",
            "lastLogin": "2019-04-10 19:06:10",
            "kind": 0
            }
    item={
          "success" : True,
          "code" : 1000,
          "msg" : "处理成功",
          "data" : {
            "page" : {
              "total" : 1,
              "totalPage" : 1,
              "pageNum" : 0,
              "pageSize" : 10,
              "list" : [ {
                "id" : "00000000001",
                # "icon" : null,
                "kind" : 0,
                "username" : "201520180508",
                "realName": "赵大海",
                "time" : "2019-04-16 03:55:56",
                "location" : "y1",
                "title" : "i lost a book",
                "about" : "about",
                "images" : [ ],
                "category" : "电子数码",
                "lookCount" : 0,
                "commentCount" : 0
              } ]
            }
          },
          # "ext" : null
        }
    notice={
      "success" : True,
      "code" : 1000,
      "msg" : "处理成功",
      "data" : {
        "list" : [ {
          "id" : "3091171d88de43319253c5d03bf267e1",
          "title" : "公告标题",
          "content" : "公告详情",
          "time" : "2020-01-21 13:44",
          "fixTop" : 1
        }, {
          "id" : "2629cced6e5a4da78fb430f4a59765ee",
          "title" : "大家好吗？",
          "content" : "我是管理员，有事随时联系哈",
          "time" : "2019-04-22 09:06",
          "fixTop" : 0
        }, {
          "id" : "38eea82e7bcb4703aed81a5aa34a0317",
          "title" : "搭建成功",
          "content" : "测试",
          "time" : "2020-01-15 19:45",
          "fixTop" : 0
        }, {
          "id" : "6520c1aaa750465cb419ce8498c09fee",
          "title" : "系统开发试用通知",
          "content" : "系统开发进入尾声工作，大家可以进行试用了，首先认证并激活邮箱，再登录既可以发表和查看别人发的东西，自己也可以发东西，快来玩玩吧！",
          "time" : "2019-04-22 07:41",
          "fixTop" : 0
        }, {
          "id" : "e8f8b8558e3642d1a6d5633048703997",
          "title" : "做完了哈",
          "content" : "差不多这样了哦",
          "time" : "2019-04-22 20:29",
          "fixTop" : 0
        } ]
    },
    "ext" : None
    }
    notice =[ {
          "id" : "3091171d88de43319253c5d03bf267e1",
          "title" : "公告标题",
          "content" : "公告详情",
          "time" : "2020-01-21 13:44",
          "fixTop" : 1
        }, {
          "id" : "2629cced6e5a4da78fb430f4a59765ee",
          "title" : "大家好吗？",
          "content" : "我是管理员，有事随时联系哈",
          "time" : "2019-04-22 09:06",
          "fixTop" : 0
        }, {
          "id" : "38eea82e7bcb4703aed81a5aa34a0317",
          "title" : "搭建成功",
          "content" : "测试",
          "time" : "2020-01-15 19:45",
          "fixTop" : 0
        }, {
          "id" : "6520c1aaa750465cb419ce8498c09fee",
          "title" : "系统开发试用通知",
          "content" : "系统开发进入尾声工作，大家可以进行试用了，首先认证并激活邮箱，再登录既可以发表和查看别人发的东西，自己也可以发东西，快来玩玩吧！",
          "time" : "2019-04-22 07:41",
          "fixTop" : 0
        }, {
          "id" : "e8f8b8558e3642d1a6d5633048703997",
          "title" : "做完了哈",
          "content" : "差不多这样了哦",
          "time" : "2019-04-22 20:29",
          "fixTop" : 0
        } ]
    return render_template('user.html', user=user,item=item,notice=notice)
    # return render_template('user.html', user=user)错误了


def logout():
    pass
