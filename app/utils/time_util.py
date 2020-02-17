# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : time_util.py
@Time    : 2020/2/17 21:42
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from datetime import datetime
import time


def get_time_str(create_time):
    create_time_utc = time.mktime(create_time.timetuple())
    now_utc = time.mktime(datetime.now().timetuple())
    minute = int((now_utc - create_time_utc) / 60)
    if minute <= 60:
        mytime = minute / 60
        print('我是mytime',mytime)
        if mytime == 0:
            return '刚刚'
        else:
            return '%d分钟前' % minute
    elif minute <= 60 * 24:
        return u'%d小时前' % (minute / 60)
    elif minute <= 60 * 24 * 2:
        return '昨天'
    elif minute <= 60 * 24 * 30:
        return '%d天前' % (minute / 60 / 24)
    else:
        return create_time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    pass
