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
from flask import request, render_template, session
from flask_login import current_user

from app import db
from app.main import category
from app.models.category_model import Category
from app.models.lostfound_model import LostFound


@category.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def index():
    return render_template('category.html')


@category.route('/getall', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def get_all():
    data = request.json
    print('category页面收到请求', data)
    categorys=Category.query.all()
    print('categorys:',categorys)
    list=[]
    for c in categorys:
        dict={
            "name":c.name,
            "about":c.about,
            # "image": None,
            "categoryId": c.id,
            "createTime": c.create_time,
            # "level": 1,
            # "targetId": "000",
            "count": LostFound.query.filter_by(category_id=c.id).count()
        }
        print(dict)
        list.append(dict)
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data":{
            "list":list
        },
        "ext": None
    }
    return data


@category.route('/add', methods=['POST'])
def add_category():
    req = request.json
    print('category', session['user_id'])
    print(current_user)
    if Category.query.filter_by(name=req['name']).first() is None:
        c = Category(name=req['name'], about=req['about'], user_id=current_user.id)
        db.session.add(c)
        db.session.commit()
        data = {
            "success": True,
            "code": 1000,
            "msg": "处理成功",
            "data": {},
            "ext": None
        }
        return data
    data = {
        "success": False,
        "code": 2201,
        "msg": "类别身份证已存在",
        "data": {},
        "ext": None
    }
    return data


@category.route('/delete', methods=['POST'])
def delete_category():
    req = request.json
    req = request.args.get('name')
    print('delete_category', req)
    temp = Category.query.filter_by(name=req).first()
    print(temp)
    if temp is not None:
        db.session.delete(temp)
        db.session.commit()
        data = {
            "success": True,
            "code": 1000,
            "msg": "处理成功",
            "data": {},
            "ext": None
        }
        return data
    data = {
        "success": False,
        "code": 1000,
        "msg": "删除失败",
        "data": {},
        "ext": None
    }
    return data
