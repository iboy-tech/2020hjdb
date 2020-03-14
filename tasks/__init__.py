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
from kombu import Queue, Exchange

from .config import broker_url
celery = Celery(__name__,
                broker=broker_url
            )
# celery.conf.task_default_queue = 'default'
celery.config_from_object('tasks.config')

celery.conf.update(
    CELERYBEAT_SCHEDULE={
        "compress_imgs": {
            "task": "app.views.found_view.compress_imgs_in_freetime",
            "schedule": crontab(minute="*/60"),
            "args": ()
        },
    },
    CELERY_QUEUES=(
    Queue("default", Exchange("default"), routing_key = "default"),
    Queue('sendmail', Exchange('sendmail',type='topic'), routing_key='web.#'),
    Queue('img_compress', Exchange('img_compress'),routing_key='img_compress'),
    Queue('send_wechat_msg', Exchange('send_wechat_msg'), routing_key='send_wechat_msg'),
),
CELERY_ROUTES  = {
    "app.utils.mail_sender.send_mail": {'queue': 'sendmail', 'routing_key': 'web.sendmail'},
    "app.utils.tinify_tool.tinypng": {'queue': 'img_compress', 'routing_key': 'img_compress'},
    'app.views.found_view.send_message_by_pusher': {'queue': 'send_wechat_msg', 'routing_key': 'send_wechat_msg'},
    # '*': {'queue': 'default', 'routing_key': 'default'},
}
)



