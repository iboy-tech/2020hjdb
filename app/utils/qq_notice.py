# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : qq_notice.py
@Time    : 2020/7/7 11:11
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import requests
from flask import render_template

from app import PostConfig
from app.models.robot_model import Robot
from tasks import celery


@celery.task  # 删除帖子给用户发送通知
def qq_group_notice(messages):
    data = render_template('msgs/QQNotice.txt', messages=messages)
    print(data)
    groups = Robot.query.all()
    print(groups)
    for g in groups:
        print(g)
        api = PostConfig.QQ_GROUP_API+g.key
        print(api)
        resp = requests.post(url=api, data=data.encode())
        print(resp)
