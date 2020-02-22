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
from flask_mail import Message

from app import mail
from tasks import celery


# from flask_mail_sendgrid import Message


# def send_async_email(app, msg):
#     with app.app_context():
#         print('异步发送邮件调用了', msg)
#         mail.send(msg)
#         # print(response.status_code)
#         # print(response.body)
#         # print(response.headers)


@celery.task
def send_email(to, subject, template, messages):
    app = current_app._get_current_object()
    print('这是发送邮件的函数')
    print('MAIL_USERNAME', os.getenv('MAIL_USERNAME'))
    print('MAIL_PASSWORD', os.getenv('MAIL_PASSWORD'))
    print('默认发件人MAIL_DEFAULT_SENDER',app.config['MAIL_DEFAULT_SENDER'])
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, recipients=[to+ '@qq.com'])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template('mails/' + template + '.html', messages=messages)
    # 动态模板使用
    # msg.template_id = 'my-template-id'
    # msg.dynamic_template_data = {'first_name': 'John', 'last_name': 'Doe'}
    # msg.add_filter
    mail.send(msg)
    # thr = Thread(target=send_async_email, args=[app,msg])
    # thr.start()
    print('发送邮件调用了', messages)
    # return thr
