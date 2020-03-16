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
import os
import datetime
import time


def get_action_time():
    # 获取当前时间 此时间为东八区时间
    ctime = time.time()
    # 将当前的东八区时间改为 UTC时间 注意这里一定是UTC时间,没有其他说法
    utc_time = datetime.utcfromtimestamp(ctime)
    # 为当前时间增加 10 秒
    add_time = datetime.timedelta(seconds=int(os.getenv('SEND_MAIL_DELAY_TIME')))
    action_time = utc_time + add_time
    # action_time 就是当前时间未来10秒之后的时间
    # 现在我们使用apply_async定时执行
    return action_time


def get_time_str(create_time):
    print("时间BUG修复", type(create_time), create_time, create_time.day)
    create_time_utc = time.mktime(create_time.timetuple())
    now = datetime.datetime.now()
    now_utc = time.mktime(now.timetuple())
    day_len = now.day - create_time.day
    minute = int((now_utc - create_time_utc) / 60)
    if minute <= 60:
        mytime = minute / 60
        print('我是mytime', mytime)
        if mytime == 0:
            return '刚刚'
        else:
            return '%d分钟前' % minute
    # 一天之内
    elif minute <= 60 * 24 and day_len == 0:
        return u'%d小时前' % (minute / 60)
    # 超过24小时
    elif minute <= 60 * 24 * 2 and day_len == 1:
        return '昨天'
    # 超过30天显示准确的时间
    elif minute <= 60 * 24 * 30:
        return '%d天前' % (minute / 60 / 24)
    else:
        return create_time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    str = '2020-01-02'
    relday = datetime.datetime.strptime(str, '%Y-%m-%d')
    need_time = datetime.date.today()
    print('查询用的时间格式', datetime.datetime.now(), type(datetime.datetime.now()))
    print(relday, type(relday), "need_time:", need_time, type(need_time))
    print(datetime.datetime.now().day - relday.day)
