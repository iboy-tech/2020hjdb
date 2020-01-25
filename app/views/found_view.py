# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : found_view.py
@Time    : 2020/1/24 20:35
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template

from app.main import found


@found.route('/',methods=['GET','POST'],strict_slashes=False)
def index():
    user = {
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
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "page": {
                "total": 3,
                "totalPage": 1,
                "pageNum": 0,
                "pageSize": 3,
                "list": [{
                    "id": "b8a3d60480fd45308fd16c1fcfe77caa",
                    "icon": "upload_6720338131142720698.jpg",
                    "kind": 0,
                    "status": 1,
                    "claimantId": None,
                    "userId": "6529d0739c344ccba3f4f0f820edcc98",
                    "username": "201520180508",
                    "realName": "普通用户",
                    "time": "2020-01-21 13:12",
                    "location": "欣苑",
                    "title": "手机掉了",
                    "about": "手机掉了啊啊啊详情",
                    "images": ["upload_8124810867403574170.jpg"],
                    "category": "手机",
                    "lookCount": 13,
                    "commentCount": 1
                }, {
                    "id": "390dcac7dec44861a21b8c933fd88eab",
                    "icon": "upload_3606103688582511042.jpg",
                    "kind": 1,
                    "status": 3,
                    "claimantId": "6529d0739c344ccba3f4f0f820edcc98",
                    "userId": "316a62ea3a444711927d872609296dbf",
                    "username": "2018171109",
                    "realName": "管理员",
                    "time": "2020-01-19 16:35",
                    "location": "西苑食堂",
                    "title": "苹果手机",
                    "about": "手机掉了",
                    "images": ["upload_3284452982529621166.jpg"],
                    "category": "手机",
                    "lookCount": 20,
                    "commentCount": 0
                }, {
                    "id": "83b9f303927b4255869280fcf40a009a",
                    "icon": "upload_6720338131142720698.jpg",
                    "kind": 0,
                    "status": 1,
                    "claimantId": None,
                    "userId": "6529d0739c344ccba3f4f0f820edcc98",
                    "username": "201520180508",
                    "realName": "普通用户",
                    "time": "2020-01-15 20:40",
                    "location": "东苑",
                    "title": "我的校园卡掉了",
                    "about": "大概在东苑到图书馆的小路上",
                    "images": ["upload_2180137498044705888.jpg"],
                    "category": "校园卡",
                    "lookCount": 1016,
                    "commentCount": 1
                }]
            }
        },
        "ext": None
    }
    userInfo={
          "success" : True,
          "code" : 1000,
          "msg" : "处理成功",
          "data" : {
            "user" : {
              "userId" : "6529d0739c344ccba3f4f0f820edcc98",
              "name" : "钱二喜",
              "username" : "201520180508",
              "gender" : "男",
              "email" : "547142436@qq.com",
              "phoneNumber" : "123456 ",
              "classNum" : "1521805",
              "major" : "软件工程",
              "academy" : "软件学院",
              "campus" : "南昌校区",
              "lastLogin" : "2020-01-25 21:56",
              "status" : "正常",
              "kind" : None
            }
          },
          "ext" : None
        }
    return render_template('found.html',user=user,index=1,item=item,userInfo=userInfo,result=item)