# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : feedback_view.py
@Time    : 2020/1/23 15:38
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template

from app.main import feedback

@feedback.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
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
          "success" : True,
          "code" : 1000,
          "msg" : "处理成功",
          "data" : {
            "list" : [ {
              "id" : "44db1dff514740069714c868422bd3ec",
              "kind" : 0,
              "targetId" : None,
              "schoolId" : "000",
              "userId" : "6529d0739c344ccba3f4f0f820edcc98",
              "username" : "201520180508",
              "realName" : "普通用户",
              "subject" : "反馈的主题",
              "content" : "反馈的详情",
              "createTime" : "2020-01-21 13:35",
              "status" : 0,
              "handlerId" : "316a62ea3a444711927d872609296dbf",
              "handlerName" : "管理员",
              "handlerEmail" : "admin",
              "answer" : "收到answer",
              "handlerTime" : "2020-01-21 13:35",
              "recordStatus" : 1
            }, {
              "id" : "fea99e8f678048dbb65cf5f710378393",
              "kind" : 0,
              "targetId" : None,
              "schoolId" : "000",
              "userId" : "316a62ea3a444711927d872609296dbf",
              "username" : "201520180517",
              "realName" : "赵大海",
              "subject" : "测试",
              "content" : "有BUG",
              "createTime" : "2020-01-15 19:44",
              "status" : 1,
              "handlerId" : "316a62ea3a444711927d872609296dbf",
              "handlerName" : "赵大海",
              "handlerEmail" : "admin@qq.com",
              "answer" : None,
              "handlerTime" : "2020-01-15 19:48",
              "recordStatus" : 1
            } ]
          },
          "ext" : None
        }
    return render_template('feedback.html',user=user,item=item)