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
from celery.schedules import crontab

celery = Celery('celery_app',
                broker='redis://localhost:6379/2',
                backend='redis://localhost:6379/3',
                include=['app.views.user_view', 'app.utils.tinify_tool', 'app.utils.mail_sender'],
                )
celery.config_from_object('celery_app.celeryconfig')
celery.conf.update(
    CELERYBEAT_SCHEDULE={
        'add-every-minute': {
            'task': 'app.scheduled.tasks.scheduled_task',
            'schedule': crontab(minute='*'),
        }
    },
    CELERY_TIMEZONE='Asia/Shanghai'
)
