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
from flask_login import current_user, login_required

from app import db
from app.decorators import admin_required, super_admin_required
from app.main import category
from app.models.category_model import Category
from app.models.lostfound_model import LostFound
from app.untils import restful


@category.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def index():
    return render_template('category.html')


@category.route('/getall', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
def get_all():
    data = request.json
    # print('category页面收到请求', data)
    categorys=Category.query.all()
    list=[]
    for c in categorys:
        dict={
            "name":c.name,
            "about":c.about,
            "categoryId": c.id,
            "createTime": c.create_time,
            "count": LostFound.query.filter_by(category_id=c.id).count()
        }
        list.append(dict)
    data={
            "list":list
        }
    return restful.success(data=data)


@category.route('/add', methods=['POST'])
@login_required
@super_admin_required
def add_category():
    req = request.json
    print('category', session['user_id'])
    print(current_user)
    if Category.query.filter_by(name=req['name']).first() is None:
        c = Category(name=req['name'], about=req['about'])
        db.session.add(c)
        db.session.commit()
        return restful.success()
    return restful.success(success=False,msg="类别身份证已存在")


@category.route('/delete', methods=['POST'])
@login_required
@super_admin_required
def delete_category():
    req = request.json
    req = request.args.get('name')
    print('delete_category', req)
    temp = Category.query.filter_by(name=req).first()
    print(temp)
    if temp is not None:
        db.session.delete(temp)
        db.session.commit()
        return restful.success()
    return restful.success(success=False,msg='删除失败')
