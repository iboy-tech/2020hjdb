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

from app import db, cache
from app.decorators import admin_required, super_admin_required, wechat_required
from app.page import category
from app.models.category_model import Category
from app.utils import restful


@category.route('/', methods=['GET'], strict_slashes=False)
@cache.cached(timeout=3600*24*7,key_prefix="category-html")  # 缓存5分钟 默认为300s
@login_required
@wechat_required
@admin_required
def index():
    return render_template('category.html')


@category.route('/getall', methods=['POST', 'OPTIONS'], strict_slashes=False)
@cache.cached(timeout=3600*24,key_prefix="category")  # 缓存5分钟 默认为300s
@login_required
def get_all():
    # print('category页面收到请求', data)
    categorys=Category.query.all()
    list=[c.to_dict() for c in categorys]
    data={
            "list":list
        }
    return restful.success(data=data)


@category.route('/add', methods=['POST'])
@login_required
@super_admin_required
def add_category():
    req = request.json
    c = Category(name=req['name'], about=req['about'])
    try:
        db.session.add(c)
        db.session.commit()
    except Exception as e:
        print("添加分类："+str(e))
        db.session.rollback()
        return restful.success(success=False, msg="类别名称已存在")
    cache.delete("category")
    return restful.success()


@category.route('/delete', methods=['POST'])
@login_required
@super_admin_required
def delete_category():
    req = request.args.get('name')
    print('delete_category', req)
    temp = Category.query.filter_by(name=req).first()
    print(temp)
    if temp is not None:
        db.session.delete(temp)
        db.session.commit()
        cache.delete("category")
        return restful.success()
    cache.delete("category")
    return restful.success(success=False,msg='删除失败')
