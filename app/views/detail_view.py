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
from flask_login import current_user, login_required

from app import db
from app.decorators import wechat_required
from app.page import detail
from app.models.category_model import Category
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.utils import restful


# @detail.route("/?id=<int:lost_id>",defaults = {"lost_id":1})
@detail.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
@wechat_required
def index():
    print('我是前端的ID')
    print('这是详情页面request.json', request.json)
    if request.method == 'GET':
        print("我是获取的ID", request.args.get('id'))
        id = request.args.get('id')
        try:
            lost = LostFound.query.get_or_404(int(id))
        except:
            return restful.success(success=False,msg='警告,非法注入，后台已记录')
        if lost is not None:
            user = User.query.get_or_404(lost.user_id)
            if lost.images == "":
                imglist = []
            else:
                lost.images = lost.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                imglist = lost.images.strip().split(',')
            lost.look_count = lost.look_count + 1
            db.session.add(lost)
            db.session.commit()
            item = {
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
            return render_template('detail.html', item=item)

    else:
        """
        # print('查找详情', type(request.json))
        id = request.args.get('id')
        # req = request.json
        # print('我是详情ID', id)
        lost = LostFound.query.get_or_404(int(id))
        if lost is not None:
            user = User.query.get_or_404(lost.user_id)
            if lost.images == "":
                imglist = []
            else:
                lost.images = lost.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                imglist = lost.images.strip().split(',')
            lost.look_count = lost.look_count + 1
            db.session.add(lost)
            db.session.commit()
            data = {
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
            }
            """
        return restful.success()

