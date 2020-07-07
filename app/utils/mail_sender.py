# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : mail_sender.py
@Time    : 2020/1/18 15:03
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 电子邮件支持
@Software: PyCharm
"""
import os

from flask import current_app, render_template
from flask_mail import Message  # 用QQ邮箱发邮件

from app import mail, logger
from tasks import celery


# from flask_mail_sendgrid import Message

# def send_async_email(app, msg):
#     with app.app_context():
#         logger.info('异步发送邮件调用了', msg)
#         mail.send(msg)
#         # logger.info(response.status_code)
#         # logger.info(response.body)
#         # logger.info(response.headers)


@celery.task
def send_email(to, subject, template, messages):
    app = current_app._get_current_object()
    # logger.info('这是发送邮件的函数')
    # logger.info('邮箱用户名MAIL_USERNAME', os.getenv('MAIL_USERNAME'))
    # logger.info('密码MAIL_PASSWORD', os.getenv('MAIL_PASSWORD'))
    # logger.info('默认发件人MAIL_DEFAULT_SENDER', app.config['MAIL_DEFAULT_SENDER'])
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, recipients=[to+'@qq.com'])
    msg.html = render_template('mails/' + template + '.html', messages=messages)
    mail.send(msg)
