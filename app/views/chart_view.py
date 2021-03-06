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

from flask import render_template, request
from flask_login import login_required, current_user

from app import db, User, redis_client, LogConfig
from app.decorators import admin_required, wechat_required
from app.page import chart, auth
from app.models.lostfound_model import LostFound
from app.utils import restful
from app.utils.log_utils import add_log, get_log
from app.views.feedback_view import get_new_feedback


# https://blog.csdn.net/yannanxiu/article/details/53816567

@chart.route('/', methods=['GET', 'POST'], strict_slashes=False)
@auth.route('/admin')
@login_required
@wechat_required
@admin_required
def index_page():
    if request.method == 'GET':
        return render_template('chart.html')
    key = current_user.username
    log_info = redis_client.get(key)
    if not log_info:
        add_log(1, get_log(), LogConfig.LOGIN_EXPIRE_TIME)  # 7天过期
    res = get_data()
    isSuperAdmin = current_user.kind == 3
    data = {
        "newCount": get_new_feedback(),
        "lost": res.get("lost"),
        "found": res.get("found"),
        "solve": res.get("solve"),
        "item": res.get("item"),
        "isSuperAdmin": isSuperAdmin
    }
    return restful.success(data=data)


def get_data():
    today = datetime.date.today()
    # 今日丢失
    today_lost = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == today, LostFound.kind == 0).count()
    # 今日拾取
    today_found = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == today, LostFound.kind == 1).count()
    # 今日解决
    today_solve = LostFound.query.filter(db.cast(LostFound.deal_time, db.DATE) == today,
                                         LostFound.status == 1).count()
    # 总计丢失
    total_lost = LostFound.query.filter(LostFound.kind == 0).count()
    # 总计拾取
    total_found = LostFound.query.filter(LostFound.kind == 1).count()
    # 总计解决
    total_solve = LostFound.query.filter(LostFound.status == 1).count()
    # 男生
    boy_users = User.query.filter(User.gender == 0).count()
    # 女生
    girl_users = User.query.filter(User.gender == 1).count()
    mylist = get_week_data()
    data = {
        # //数据总览
        # //今日和总计
        'lost': [today_lost, total_lost],
        'found': [today_found, total_found],
        'solve': [today_solve, total_solve],
        # //最近7天
        'item': [mylist[0], [mylist[0], mylist[1], mylist[2]], mylist[3], [mylist[4], mylist[5]],
                 [boy_users, girl_users]],
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
    # logger.info('本周的周一：',monday,type(monday))
    return monday - datetime.timedelta(days=1)  # 上一个周的周日


def get_week_data():
    last_sunday = get_last_sunday()
    # logger.info('last_sunday', last_sunday)
    today = datetime.date.today()
    # logger.info('today', today)
    # time_len = (today - last_sunday.date()).days  # 获取当前与上周相差的天数
    # logger.info("time——len", time_len)
    # list1 = [], list2 = [], list3 = [], list4 = []
    mylist = [[], [], [], [], [], [], []]
    seven_day_ago = today - datetime.timedelta(days=7)
    # datetime.timedelta(days=1)加上一个天数
    for i in range(1, 8):
        # logger.info(i)
        day = seven_day_ago + datetime.timedelta(days=i)
        # logger.info("我是七天前查询的时间", day)
        today_lost = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == day, LostFound.kind == 0).count()
        mylist[0].append(today_lost)
        today_found = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == day,
                                             LostFound.kind == 1).count()
        mylist[1].append(today_found)
        today_solve = LostFound.query.filter(db.cast(LostFound.create_time, db.DATE) == day,
                                             LostFound.status == 1).count()
        mylist[2].append(today_solve)
        today_user = User.query.filter(db.cast(User.create_time, db.DATE) <= day).count()
        mylist[3].append(today_user)
        active_boy = User.query.filter(db.cast(User.last_login, db.DATE) == day, User.gender == 0).count()
        mylist[4].append(active_boy)
        active_girl = User.query.filter(db.cast(User.last_login, db.DATE) == day, User.gender == 1).count()
        mylist[5].append(active_girl)
        mylist[6].append(day.strftime('%m/%d'))

    # logger.info(list1,list2,list3,list4)
    # logger.info('每周的结果', mylist)
    return mylist
