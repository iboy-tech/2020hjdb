# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : config.py
@Time    : 2020/2/14 15:03
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : https://www.zhihu.com/topic/20203769/hot
@Software: PyCharm
"""
# 消息代理的连接Celery 从 4.0 开始启用新的小写配置名
broker_url = 'redis://localhost:6379/2'
result_backend = 'redis://localhost:6379/3'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = False
# 设置结果的保存时间
result_expires= 3600
