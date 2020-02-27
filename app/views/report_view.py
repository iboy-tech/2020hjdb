# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : report_view.py
@Time    : 2020/2/27 14:22
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from datetime import datetime

from flask import render_template, request
from flask_login import login_required
from sqlalchemy import and_, func

from app import db
from app.decorators import wechat_required, admin_required
from app.models.category_model import Category
from app.models.lostfound_model import LostFound
from app.page import report
from app.utils import restful
from uuid import uuid4


@report.route('/', methods=['POST', 'GET'], strict_slashes=False)
@login_required
@wechat_required
@admin_required
def get_report():
    # start_time = '2020-01-02'
    # end_time = '2020-02-27'
    # found_list = db.session.query(LostFound).filter(LostFound.create_time.between(start_time, end_time),
    #                                                 LostFound.kind == 1) \
    #     .order_by(LostFound.create_time).all()
    """
    捡到物品
    """
    start_time = '2020-01-27'
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = '2020-02-28'

    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    found_list = db.session.query(LostFound).filter(
        and_(LostFound.create_time.between(start_time, end_time), LostFound.kind == 1)) \
        .order_by(LostFound.create_time).all()
    print('我是查询的报表', found_list)
    if found_list:
        for f in found_list:
            print(f.post_user.real_name, f.post_user.qq, f.post_category.name, f.location, f.about, f.create_time)
    """
    丢失物品
    失主	失物	失物详情	遗失地点	遗失时间	失主联系方式
    """
    found_list = db.session.query(LostFound).filter(
        and_(LostFound.create_time.between(start_time, end_time), LostFound.kind == 0)) \
        .order_by(LostFound.create_time).all()
    print('我是查询的报表', found_list)
    if found_list:
        for f in found_list:
            print(f.post_user.real_name, f.post_category.name,f.post_user.qq, f.about , f.location, f.create_time,f.post_user.qq)
    """
    (归还统计)
    类型	失物数量	找回数量	拾取数量	归还数量
    """
    categories=db.session.query(Category).all()
    for c in categories:
        found_list = db.session.query(LostFound).filter(
            and_(LostFound.category_id==c.id, LostFound.kind == 0,LostFound.status==0,LostFound.create_time.between(start_time, end_time))).count()
        print(start_time,end_time,'失物数量查询',found_list)
        found_list = db.session.query(LostFound).filter(
            and_(LostFound.category_id==c.id, LostFound.kind == 0,LostFound.status==1,LostFound.create_time.between(start_time, end_time))).count()
        print(start_time,end_time,'找回数量查询',found_list)

        found_list = db.session.query(LostFound).filter(
            and_(LostFound.category_id==c.id, LostFound.kind == 1,LostFound.status==0,LostFound.create_time.between(start_time, end_time))).count()
        print(start_time,end_time,'拾取数量查询',found_list)

        found_list = db.session.query(LostFound).filter(
            and_(LostFound.category_id==c.id, LostFound.kind == 1,LostFound.status==1,LostFound.create_time.between(start_time, end_time))).count()
        print(start_time,end_time,'归还数量查询',found_list)
    """
    (失物统计)
    失主/拾主	物品	拾取/丢失地点	所属学院
    """
    found_list = db.session.query(LostFound).filter(
        and_(LostFound.create_time.between(start_time, end_time))) \
        .order_by(LostFound.create_time).all()
    print('我是查询的报表', found_list)
    if found_list:
        for f in found_list:
            print(f.post_user.real_name, f.post_category.name, f.location,f.post_user.academy)

    return render_template('report.html')


@report.route('/getall', methods=['POST'], strict_slashes=False)
@login_required
@wechat_required
@admin_required
def get_file():
    list = []
    data = {"list": list}
    return restful.success(data=data)


@report.route('/add', methods=['POST'], strict_slashes=False)
@login_required
@wechat_required
@admin_required
def create_report():
    req = request.json
    print('生成数据的条件', req)
    list = []
    data = {"list": list}
    start_time = '2020-02-27'
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = '2020-02-28'
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    found_list = db.session.query(LostFound).filter(
        and_(LostFound.create_time.between(start_time, end_time), LostFound.kind == 1)) \
        .order_by(LostFound.create_time).all()
    print('我是查询的报表', found_list)
    return restful.success(data=data, msg="报表正在生成，请耐心等待")


# 失物统计表（归还统计,失物统计）
def get_lost_summary():
    start_time = '2020-01-02'
    end_time = '2020-02-27'
    """
    (归还统计)
    类型	失物数量	找回数量	拾取数量	归还数量
    (失物统计)
    失主/拾主	物品	拾取/丢失地点	所属学院
    :return:
    """
    pass


# 失物登记表（拾物采集表，失物上报表）
def get_lost_record():
    start_time = '2020-01-02'
    end_time = '2020-02-27'
    """
    拾物采集kind=1
    """
    found_list = db.session.query(LostFound).filter(LostFound.create_time.between(start_time, end_time),
                                                    LostFound.kind == 1) \
        .order_by(LostFound.create_time).all()

    """
    (拾物采集表)
    物品	详情	拾取地点	拾取时间	领取方式
    (失物上报表)
    失主	失物	失物详情	遗失地点	遗失时间	失主联系方式
    :return:
    """
    pass
