# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : found_view.py
@Time    : 2020/1/24 20:35
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import base64

from flask import render_template, request, current_app
from flask_login import current_user
from sqlalchemy import desc

from app import db
from app.main import found
from app.models.category_model import Category
from app.models.lostfound_model import LostFound
from app.models.user_model import User


@found.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    return render_template('found.html')


@found.route('/getall', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def get_all():

    req = request.json
    print(req)
    print('get_users收到请求')
    page=int(req['pageNum'])
    pagination =LostFound.query.order_by(desc('create_time')).paginate(page+1, per_page=current_app.config[
        'ARTISAN_POSTS_PER_PAGE'], error_out=False)
    losts = pagination.items
    print(losts)
    datalist=[]
    for l in losts:
        print(l.images,type(l.images))
        l.images=l.images.replace('[','').replace(']','').replace(' \'','').replace('\'','')
        print(l.images, type(l.images))
        imglist=l.images.strip().split(',')
        print(imglist,type(imglist))
        user=User.query.get(l.user_id)
        dict={
                "id": l.id,
                "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                "kind": l.kind,
                "status": l.status,
                "claimantId": l.claimant_id,
                "userId": l.user_id,
                "username": user.username,
                "realName": user.real_name,
                "time": l.create_time.strftime( '%Y-%m-%d %H:%M:%S'),
                "location": l.location,
                "title": l.title,
                "about": l.about,
                "images": imglist,
                "category": Category.query.get(l.category_id).name,
                "lookCount": l.look_count,
                "commentCount": 0
            }
        datalist.append(dict)
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "page": {
                "total": pagination.total,
                "totalPage": pagination.pages,
                "pageNum": req['pageNum'],
                "pageSize": current_app.config['ARTISAN_POSTS_PER_PAGE'],
                "list": datalist
            }
        },
        "ext": None
    }
    return data


@found.route('/pub', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def pub():
    data = request.json
    print(data)
    print(data['images'], type(data['images']))
    imgstr=str(data['images'])
    print(type(imgstr),imgstr)
    lost=LostFound(kind=data['applyKind'],category_id=data['categoryId'],
    images=imgstr,location =data['location'] ,
    title=data['title'],about=data['about'],user_id=current_user.id)
    db.session.add(lost)
    db.session.commit()
    # print(data['images'][0],len(data['images']))
    # strs=data['images'][0]
    # with open('test.jpeg', 'wb') as f:
    #     f.write(base64.b64decode(strs))
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {},
        "ext": None
    }
    return data
