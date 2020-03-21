# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : config.py
@Time    : 2020/2/14 15:03
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : https://www.zhihu.com/topic/20203769/hot
@Software: PyCharm
"""
# 消息代理的连接Celery 从 4.0 开始启用新的小写配置名
from datetime import timedelta

from celery.schedules import crontab
from kombu import Queue, Exchange

broker_url = 'redis://localhost:6379/2'
# result_backend = 'redis://localhost:6379/3'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True
# 设置结果的保存时间
# 最长的确认时间，防止延迟任务被不同的worker重复执行
# https://yabzhang.github.io/2018/10/08/celery%E5%BB%B6%E6%97%B6%E4%BB%BB%E5%8A%A1%E8%B8%A9%E5%9D%91/
visibility_timeout=43200
task_ignore_result= True
task_default_queue='default'
# result_expires = 3600
beat_schedule = {
    "compress_imgs": {
        "task": "app.views.found_view.compress_imgs_in_freetime",
        "schedule": timedelta(seconds=10),# # 每周一至周五早上8点执行任务函数
        # 'schedule': crontab(minute=50, hour=18, day_of_week=[1, 2, 3, 4, 5]),
        'schedule': crontab(minute=3, hour=19),
        "args": ()
    },
}
task_queues = (
    Queue('send_mail', Exchange('send_mail'), routing_key='send_mail'),
    Queue('img_compress', Exchange('img_compress'), routing_key='img_compress'),
    Queue('send_wechat_msg', Exchange('send_wechat_msg'), routing_key='send_wechat_msg'),
    Queue("default", Exchange("default"), routing_key="default"),
)
task_routes= {
    "app.utils.mail_sender.send_mail": {'queue': 'send_mail', 'routing_key': 'send_mail'},
    "app.utils.tinify_tool.tinypng": {'queue': 'img_compress', 'routing_key': 'img_compress'},
    'app.views.found_view.send_message_by_pusher': {'queue': 'send_wechat_msg', 'routing_key': 'send_wechat_msg'},
    '*': {'queue': 'default', 'routing_key': 'default'},
}