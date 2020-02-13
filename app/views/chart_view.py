# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : chart_view.py
@Time    : 2020/1/19 21:21
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import datetime

from flask import render_template
from flask_login import login_required

from app import db, User
from app.decorators import admin_required
from app.main import chart
from app.models.lostfound_model import LostFound
from app.untils import restful

print('视图文件加载')


# https://blog.csdn.net/yannanxiu/article/details/53816567

@chart.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    print('蓝图请求成功！')

    data = get_data()
    # {
    #     # //数据总览
    #     # //今日和总计
    #     'lost': [1, 11],
    #     'found': [2, 22],
    #     'solve': [3, 33],
    #     # //近期数据
    #     # 'barChartData1': {
    #     'labels1': ["01/13", "04/14", "04/15", "04/16", "04/17", "04/18", "04/13"],
    #     # //柱状图
    #     'data1': [[1111, 70, 55, 20, 45, 0, 60], [65, 59, 90, 81, 56, 0, 40], [65, 1, 90, 81, 56, 1, 300]],
    #     # },
    #     # //面积图
    #     # 'lineChartData1': {
    #     'labels2': ["Jan", "Feb", "March", "April", "May", "June", "July"],
    #     'data2': [[22, 31, 2, 40, 555, 65, 68], [1, 31, 2, 40, 55, 0, 68], [1, 1, 39, 1, 55, 65, 68]],
    #     # },
    #     # //饼状图
    #     # 'pieData1': {
    #     # //拾取，丢失，找到
    #     'data3': [10, 20, 88],
    #     # },
    #     # //用户数量变化图
    #     # 'lineChartData2': {
    #     'labels4': ["11/13", "04/14", "04/15", "04/17", "04/17", "04/18", "04/13"],
    #     'data4': [1, 31, 39, 100, 55, 65, 1],
    #     # },
    #     # //用户活跃量
    #     # 'lineChartData3': {
    #     'lables5': ["Jan", "Feb", "March", "April", "May", "June", "July"],
    #     'data5': [[22, 31, 39, 40, 55, 65, 68], [12, 15, 23, 34, 36, 44, 51]],
    #     # },
    #     # //性别比例
    #     # 'pieData2': {
    #     'data6': [10000, 50000]
    #     # }
    # }
    return render_template('chart.html', data=data)


def get_data():
    today = datetime.date.today()
    print(today)
    # 0=lost 1 found
    # losts_today = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == today,LostFound.kind==1).all()
    # founds_today = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == today, LostFound.kind == 1).all()
    today_lost = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == today, LostFound.kind == 0).count()
    today_found = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == today, LostFound.kind == 1).count()
    today_solve = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == today,
                                         LostFound.status == 1).count()
    total_lost = LostFound.query.filter(LostFound.kind == 0).count()
    total_found = LostFound.query.filter(LostFound.kind == 1).count()
    total_solve = LostFound.query.filter(LostFound.status == 1).count()
    boy_users = User.query.filter(User.gender == 0).count()
    girl_users = User.query.filter(User.gender == 1).count()
    # list1, list2, list3, list4 = get_week_data()
    mylist=get_week_data()
    data = {
        # //数据总览
        # //今日和总计
        'lost': [today_lost, total_lost],
        'found': [today_found, total_found],
        'solve': [today_solve, total_solve],
        # //近期数据
        # 'barChartData1': {
        # 'labels1':  ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        # //柱状图
        # 'data1': [[1111, 70, 55, 20, 45, 0, 60], [65, 59, 90, 81, 56, 0, 40], [65, 1, 90, 81, 56, 1, 300]],
        'data1': [mylist[0], mylist[1],mylist[2]],
        # },
        # //面积图
        # 'lineChartData1': {
        # 'labels2': ["Jan", "Feb", "March", "April", "May", "June", "July"],
        # 'data2': [[22, 31, 2, 40, 555, 65, 68], [1, 31, 2, 40, 55, 0, 68], [1, 1, 39, 1, 55, 65, 68]],
        'data2': [mylist[0], mylist[1],mylist[2]],
        # },
        # //饼状图
        # 'pieData1': {
        # //拾取，丢失，找到
        'data3': [total_lost, total_found, total_solve],
        # },
        # //用户数量变化图
        # 'lineChartData2': {
        # 'labels4':["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        # 'data4': list4,
        'data4':mylist[3],
        # },
        # //用户活跃量
        # 'lineChartData3': {
        # 'lables5': ["Jan", "Feb", "March", "April", "May", "June", "July"],
        'data5': [mylist[4], mylist[5]],
        # },
        # //性别比例
        # 'pieData2': {
        'data6': [boy_users, girl_users]
        # }
    }
    return data


def get_en_month(n):
    month = "JanFebMarAprMayJunJulAugSepOctNovDec"  # 将所有月份简写存到month中
    pos = ((int(n) - 1) * 3)  # 输入的数字为n,将(n-1)*3,即为当前月份所在索引位置
    en_month = month[pos:pos + 3]
    return en_month


# 获取本周的周一
def get_last_sunday():
    monday = datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    # 返回当前的星期一
    # print('本周的周一：',monday,type(monday))
    return monday - datetime.timedelta(days=1)  # 上一个周的周日


def get_week_data():
    last_sunday = get_last_sunday()
    print('last_sunday', last_sunday)
    today = datetime.date.today()
    print('today', today)
    time_len = (today - last_sunday.date()).days  # 获取当前与上周相差的天数
    print("time——len", time_len)
    # list1 = [], list2 = [], list3 = [], list4 = []
    mylist=[[],[],[],[],[],[]]
    # datetime.timedelta(days=1)加上一个天数
    for i in range(1, time_len + 1):
        print(i)
        day = (last_sunday + datetime.timedelta(days=i)).date()
        print("我是查询的时间",day)
        today_lost = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == day, LostFound.kind == 0).count()
        mylist[0].append(today_lost)
        today_found = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == day,
                                             LostFound.kind == 1).count()
        mylist[1].append(today_found)
        today_solve = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == day,
                                             LostFound.status == 1).count()
        mylist[2].append(today_solve)
        today_user = User.query.filter(db.cast(User.create_time, db.DATE) == day).count()
        mylist[3].append(today_user)
        active_boy = User.query.filter(db.cast(User.last_login, db.DATE) == day, User.gender ==0).count()
        mylist[4].append(active_boy)
        active_girl=User.query.filter(db.cast(User.last_login, db.DATE) == day,User.gender==1).count()
        mylist[5].append(active_girl)

    # print(list1,list2,list3,list4)
    print('每周的结果',mylist)
    return mylist
