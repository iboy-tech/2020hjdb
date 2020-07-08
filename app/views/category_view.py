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
from flask_login import login_required

from app import db, cache
from app.decorators import super_admin_required
from app.models.category_model import Category
from app.page import category
from app.utils import restful


@category.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
@cache.cached(timeout=3600 * 24, key_prefix="category")  # 缓存5分钟 默认为300s
@login_required
def get_all():
    # logger.info('category页面收到请求', data)
    categorys = Category.query.all()
    list = [c.to_dict() for c in categorys]
    data = {
        "list": list
    }
    return restful.success(data=data)


@category.route('/', methods=['POST'])
@login_required
@super_admin_required
def add_category():
    req = request.json
    c = Category(name=req['name'], about=req['about'])
    try:
        db.session.add(c)
        db.session.commit()
    except Exception as e:
        # logger.info("添加分类："+str(e))
        db.session.rollback()
        return restful.error("类别名称已存在")
    cache.delete("category")
    return restful.success(msg="添加成功")


@category.route('/<int:id>', methods=['DELETE'])
@login_required
@super_admin_required
def delete_category(id=-1):
    if id == -1:
        return restful.error()
    temp = Category.query.get(id)
    db.session.delete(temp)
    db.session.commit()
    cache.delete("category")
    return restful.success()
    cache.delete("category")
    return restful.success(msg='删除成功')
