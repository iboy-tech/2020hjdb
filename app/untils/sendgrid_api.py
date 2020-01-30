# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : sendgrid_api.py
@Time    : 2020/1/30 15:31
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import sendgrid
from sendgrid.helpers.mail import *

apikey = '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'  #API密钥
sg = sendgrid.SendGridAPIClient(apikey)
# apikey=os.getenv('SENDGRID_API_KEY')     #从环境变量获取密钥

from_email = "ctgu@iboy.tech"
to_email = "547142436@qq.com"
subject = '账户冻结通知'
content = "I love Python"
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": to_email
        }
      ],
      "subject": subject
    }
  ],
  "from": {
    "email": from_email
  },
  "content": [
    {
      "type": "text/plain",
      "value": content
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)


