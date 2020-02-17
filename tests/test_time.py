# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : test_time.py
@Time    : 2020/2/17 20:13
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import time
from datetime import datetime


def get_time_str(create_time):
    now_utc = datetime.now()
    print('当前时间', now_utc)
    minute = (now_utc - create_time).seconds / 3600
    print(minute, '获取分钟')
    if minute <= 60:
        return '%d分钟前' % minute
    elif minute <= 60 * 24:
        return u'%d小时前' % int(minute / 60)
    elif minute <= 60 * 24 * 2:
        return '昨天'
    elif minute <= 60 * 24 * 30:
        return '%d天前' % (minute / 60 / 24)
    else:
        return create_time.strftime('%Y-%m-%d %H:%M:%S')


def test_my(create_time_utc):
    now_utc = time.mktime(datetime.now().timetuple())

    minute = int((now_utc - create_time_utc) / 60)
    if minute <= 60:
        return '%d分钟前' % (minute / 60)
    elif minute <= 60 * 24:
        return u'%d小时前' % (minute / 60)
    elif minute <= 60 * 24 * 2:
        return '昨天'
    elif minute <= 60 * 24 * 30:
        return '%d天前' % (minute / 60 / 24)
    else:
        return create_time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    str = '2020-01-01 20:48:00'
    create_time = datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    print(create_time, type(create_time))
    print(test_my(time.mktime(create_time.timetuple())))
