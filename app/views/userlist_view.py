# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : userlist_view.py
@Time    : 2020/1/23 22:41
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template, request, current_app

from app.main import userlist


@userlist.route('/', methods=['POST', 'GET', 'OPTIONS'], strict_slashes=False)
def index():
    print('userlist请求成功', request.json)
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "page": {
                "total": 2,
                "totalPage": 1,
                "pageNum": 0,
                "pageSize": 10,
                "list": [{
                    "userId": "316a62ea3a444711927d872609296dbf",
                    "name": "赵大海",
                    "username": "201520180517",
                    "gender": "男",
                    "email": "admin",
                    "phoneNumber": "13511112222",
                    "classNum": "1521805",
                    "major": "软件工程",
                    "academy": "软件学院",
                    "campus": "南昌校区",
                    "lastLogin": "2020-01-21 14:04",
                    "status": "正常",
                    "kind": 2
                }, {
                    "userId": "6529d0739c344ccba3f4f0f820edcc98",
                    "name": "钱二喜",
                    "username": "201520180508",
                    "gender": "男",
                    "email": "547142436@qq.com",
                    "phoneNumber": "123456 ",
                    "classNum": "1521805",
                    "major": "软件工程",
                    "academy": "软件学院",
                    "campus": "南昌校区",
                    "lastLogin": "2020-01-23 22:49",
                    "status": "正常",
                    "kind": 0
                }]
            }
        },
        "ext": None
    }
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
    items=[{
                    "userId": "316a62ea3a444711927d872609296dbf",
                    "name": "赵大海",
                    "username": "201520180517",
                    "gender": "男",
                    "email": "admin",
                    "phoneNumber": "13511112222",
                    "classNum": "1521805",
                    "major": "软件工程",
                    "academy": "软件学院",
                    "campus": "南昌校区",
                    "lastLogin": "2020-01-21 14:04",
                    "status": "正常",
                    "kind": 2
                }, {
                    "userId": "6529d0739c344ccba3f4f0f820edcc98",
                    "name": "钱二喜",
                    "username": "201520180508",
                    "gender": "男",
                    "email": "547142436@qq.com",
                    "phoneNumber": "123456 ",
                    "classNum": "1521805",
                    "major": "软件工程",
                    "academy": "软件学院",
                    "campus": "南昌校区",
                    "lastLogin": "2020-01-23 22:49",
                    "status": "正常",
                    "kind": 0
                }]
    # data = [{
    #     "userId": "316a62ea3a444711927d872609296dbf",
    #     "name": "赵大海",
    #     "username": "201520180517",
    #     "gender": "男",
    #     "email": "admin",
    #     "phoneNumber": "13511112222",
    #     "classNum": "1521805",
    #     "major": "软件工程",
    #     "academy": "软件学院",
    #     "campus": "南昌校区",
    #     "lastLogin": "2020-01-21 14:04",
    #     "status": "正常",
    #     "kind": 2
    # }, {
    #     "userId": "6529d0739c344ccba3f4f0f820edcc98",
    #     "name": "钱二喜",
    #     "username": "201520180508",
    #     "gender": "男",
    #     "email": "547142436@qq.com",
    #     "phoneNumber": "123456 ",
    #     "classNum": "1521805",
    #     "major": "软件工程",
    #     "academy": "软件学院",
    #     "campus": "南昌校区",
    #     "lastLogin": "2020-01-23 22:49",
    #     "status": "正常",
    #     "kind": 0
    # }]
    return render_template('userlist.html',user=user,result=data,items=items)
    # return data


@userlist.route('/test', methods=['POST', 'GET', 'OPTIONS'], strict_slashes=False)
def test():
    return current_app.send_static_file('userlist.html')
