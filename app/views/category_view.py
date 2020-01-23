# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : category_view.py
@Time    : 2020/1/19 22:11
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import request

from app.main import category


@category.route('/',methods=['GET','POST','OPTIONS'])
def index():
    data=request.json
    print('category页面收到请求',data)
    data = {
      "success" : None,
      "code" : 1000,
      "msg" : "处理成功",
      "data" : {
        "list" : [ {
          "name" : "哈哈",
          "about" : "哈哈爱是擦好吃吧唧",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-21 13:27",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "手机",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:34",
          "level" : 1,
          "targetId" : "000",
          "count" : 2
        }, {
          "name" : "充电线或充电器",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "水杯",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "其他",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "教材",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "雨伞",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "书籍",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "宠物",
          "about" : "宠物",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "银行卡",
          "about" : "银行卡",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:32",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "身份证",
          "about" : "身份证",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:32",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "校园卡",
          "about" : "校园卡",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:32",
          "level" : 1,
          "targetId" : "000",
          "count" : 1
        } ]
      },
      "ext" : None
    }
    data=[ {
          "name" : "哈哈",
          "about" : "哈哈爱是擦好吃吧唧",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-21 13:27",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "手机",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:34",
          "level" : 1,
          "targetId" : "000",
          "count" : 2
        }, {
          "name" : "充电线或充电器",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "水杯",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "其他",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "教材",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "雨伞",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "书籍",
          "about" : "",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "宠物",
          "about" : "宠物",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:33",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "银行卡",
          "about" : "银行卡",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:32",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "身份证",
          "about" : "身份证",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:32",
          "level" : 1,
          "targetId" : "000",
          "count" : 0
        }, {
          "name" : "校园卡",
          "about" : "校园卡",
          "image" : None,
          "creatorId" : "316a62ea3a444711927d872609296dbf",
          "createTime" : "2020-01-15 20:32",
          "level" : 1,
          "targetId" : "000",
          "count" : 1
        } ]
    return data


def logout():
    pass
