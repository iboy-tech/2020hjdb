# -*- coding:UTF-8 -*-
# !/usr/bin/python
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
# timezone = 'Asia/Shanghai'
# enable_utc = True
# 设置结果的保存时间
# 最长的确认时间，防止延迟任务被不同的worker重复执行
# https://yabzhang.github.io/2018/10/08/celery%E5%BB%B6%E6%97%B6%E4%BB%BB%E5%8A%A1%E8%B8%A9%E5%9D%91/
visibility_timeout=43200
# result_expires = 3600
