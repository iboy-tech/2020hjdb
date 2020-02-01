# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : detail_view.py
@Time    : 2020/1/25 22:30
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template, request
from flask_login import current_user

from app import db
from app.main import detail
from app.models.category_model import Category
from app.models.lostfound_model import LostFound
from app.models.user_model import User


@detail.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def index():
    req=request.args.get('id')
    if not req:
        lost = LostFound.query.get(int(request.json))
        if lost is not None:
            user = User.query.get(lost.user_id)
            lost.images = lost.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
            lost.look_count = lost.look_count + 1
            db.session.add(lost)
            db.session.commit()
            imglist = lost.images.strip().split(',')
            data = {
                "success": True,
                "code": 1000,
                "msg": "处理成功",
                "data": {
                    "item": {
                        "id": lost.id,
                        "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                        "kind": lost.kind,
                        "userId": lost.user_id,
                        "username": user.username,
                        "realName": user.real_name,
                        "time": lost.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "location": lost.location,
                        "title": lost.title,
                        "about": lost.about,
                        "images": imglist,
                        "category": (Category.query.get(lost.category_id)).name,
                        "lookCount": lost.look_count,
                        "status": lost.status,
                        "dealTime": None if lost.deal_time is None else lost.deal_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "isSelf": current_user.id == lost.user_id,
                        "email": user.qq + '@qq.com',
                        "QQ": user.qq
                    }
                },
                "ext": None
            }
            return data

    return render_template('detail.html')


@detail.route('/get', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def get_detail():
    req=request.args.get('id')
    print('我是详情页面：',req)


