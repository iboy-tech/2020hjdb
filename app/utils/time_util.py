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
from datetime import datetime, timedelta
import time

def get_action_time():
    # 获取当前时间 此时间为东八区时间
    ctime = time.time()
    # 将当前的东八区时间改为 UTC时间 注意这里一定是UTC时间,没有其他说法
    utc_time = datetime.utcfromtimestamp(ctime)
    # 为当前时间增加 10 秒
    add_time = timedelta(seconds=int(os.getenv('SEND_MAIL_DELAY_TIME')))
    action_time = utc_time + add_time
    # action_time 就是当前时间未来10秒之后的时间
    # 现在我们使用apply_async定时执行
    return action_time

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
