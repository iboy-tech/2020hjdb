# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : __init__.py.py
@Time    : 2020/2/15 9:04
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from celery import Celery
from .config import broker_url,result_backend
celery = Celery(__name__,
                broker=broker_url,
                backend=result_backend,
                include=['app.views.user_view', 'app.utils.tinify_tool', 'app.utils.mail_sender'],
                )
celery.config_from_object('tasks.config')
# celery.conf.update(
#     CELERYBEAT_SCHEDULE={
#         'add-every-minute': {
#             'task': 'app.scheduled.tasks.scheduled_task',
#             'schedule': crontab(minute='*'),
#         }
#     },
#     CELERY_TIMEZONE='Asia/Shanghai'
# )
