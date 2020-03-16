# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : test_date.py
@Time    : 2020/2/13 21:33
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import datetime


def get_current_monday():
    monday = datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    # 返回当前的星期一
    # print('本周的周一：',monday,type(monday))
    return monday - datetime.timedelta(days=1)  # 上一个周的周日


def my():
    for i in range(0, 11):
        file = []
        # print(i)
        file.append(i)
        if i > 3:
            file.remove(i)
            return []
    return file


if __name__ == '__main__':
    str = '2020-01-01'
    today = datetime.date.today()
    day = (today - datetime.timedelta(days=0))
    print("我是查询的时间", day)
    mydate = datetime.datetime.strptime(str, '%Y-%m-%d')
    print((mydate - datetime.timedelta(days=1)).strftime('%m/%d'))
    print("周一日期", get_current_monday())
    print("周一日期", get_current_monday().date())
    print(datetime.date.today())
    print((datetime.date.today() - get_current_monday().date()).days)
    print(my())
