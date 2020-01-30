# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : mial_test.py
@Time    : 2020/1/30 16:26
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import sendgrid
sg = sendgrid.SendGridClient('apikey', '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')
message = sendgrid.Mail()
message.add_to('547142436@qq.com')
message.set_subject('My Test Email')
message.add_substitution('customer_link', 'http://my-domain.com/customer-id')
message.add_filter('templates', 'enable', '1')
message.add_filter('templates', 'template_id', '<alphanumeric-template-id>')
message.add_from('<from-email-address>')
message.set_html('')
message.set_text('')
status, msg = sg.send(message)