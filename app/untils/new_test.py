# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : new_test.py
@Time    : 2020/1/30 16:45
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='ctgu@iboy.tech',
    to_emails='yang.hao@aliyun.com',
    subject='账户冻结通知',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    apikey = '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'  # API密钥
    sg = SendGridAPIClient(apikey)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)