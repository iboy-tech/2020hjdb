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
from flask import render_template
from flask_login import login_required

from app.decorators import admin_required
from app.main import chart
from app.untils import restful

print('视图文件加载')


@chart.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    print('蓝图请求成功！')
    return render_template('chart.html')


@chart.route('/get', methods=['GET', 'POST'])
@login_required
@admin_required
def get_data():
    print('图标蓝图请求成功！')
    data = {
        # //数据总览
        # //今日和总计
        'lost': [1, 21110],
        'found': [2, 1110],
        'solve': [10, 11100],
        'item':[  # //近期数据
        {
            'labels': ["01/10", "04/14", "04/15", "04/16", "04/17", "04/18", "04/13"],
            # //柱状图
            'data': [[1111, 70, 55, 20, 45, 0, 60], [65, 59, 90, 81, 56, 0, 40], [65, 1, 90, 81, 56, 1, 1]]
        },
        # //面积图
        {
            'labels': ["Jan", "Feb", "March", "April", "May", "June", "July"],
            'data': [[22, 31, 2, 40, 555, 65, 68], [1, 31, 2, 40, 55, 0, 68], [1, 1, 39, 1, 55, 65, 68]]
        },
        # //饼状图
       {
            # //拾取，丢失，找到
            'data': [10, 20, 88]
        },
        # //用户数量变化图
        {
            'labels': ["11/13", "04/14", "04/15", "04/17", "04/17", "04/18", "04/13"],
            'data': [1, 31, 39, 100, 55, 65, 1]
        },
        # //用户活跃量
         {
            'lables': ["Jan", "Feb", "March", "April", "May", "June", "July"],
            'data': [[22, 31, 39, 40, 55, 65, 68], [12, 15, 23, 34, 36, 44, 51]]
        },
        # //性别比例
        {
            'data': [10000,10000]
        }]
    }
    print('表格数据',restful.success(data=data))
    return restful.success(data=data)
