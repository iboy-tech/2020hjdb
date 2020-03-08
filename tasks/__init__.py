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
from kombu import Exchange, Queue

from .config import broker_url
celery = Celery(__name__,
                broker=broker_url
                # backend=result_backend,#不存储结果
                # include=['app.views.user_view', 'app.utils.tinify_tool', 'app.utils.mail_sender']
                )

celery.config_from_object('tasks.config')
# 配置队列（settings.py）
CELERY_QUEUES=(
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('send_mail', Exchange('send_mail'), routing_key='send_mail'),
    Queue('img_compress', Exchange('img_compress'), routing_key='img_compress'),
    Queue('send_wechat_msg', Exchange('send_wechat_msg'), routing_key='send_wechat_msg'),
)
# # 路由（哪个任务放入哪个队列）
CELERY_ROUTES  = {
    "app.utils.mail_sender.send_mail": {'queue': 'send_mail', 'routing_key': 'send_mail'},
    "app.utils.tinify_tool.tinypng": {'queue': 'img_compress', 'routing_key': 'img_compress'},
    'app.views.found_view.send_message_by_pusher': {'queue': 'send_wechat_msg', 'routing_key': 'send_wechat_msg'},
    '*': {'queue': 'default', 'routing_key': 'default'},
}
# CELERY_TIMEZONE = 'Asia/Shanghai',

celery.conf.update(CELERY_QUEUES=CELERY_QUEUES, CELERY_ROUTES=CELERY_ROUTES)


