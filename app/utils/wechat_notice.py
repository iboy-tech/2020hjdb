# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : wechat_notice.py
@Time    : 2020/3/21 22:36
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 微信通知模块
@Software: PyCharm
"""
import datetime
import os
from random import randint

from app.utils.mail_sender import send_email
from flask import render_template

from app import OpenID, User
from app.utils.wxpusher import WxPusher
from tasks import celery


@celery.task  # 删除帖子给用户发送通知
def delete_post_notice(kind, id, l):
    # 管理删除的和自己删除的不通知
    if kind > 1 and l['user_id'] != id:
        u = User.query.get_or_404(l['user_id'])
        op = OpenID.query.filter_by(user_id=u.id).first_or_404()
        if op is not None:
            dict = {
                'post_user': u.real_name,
                'post_title': l['title'],
                'post_content': l['about'],
                'handle_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'qq_group': '878579883',
                'url': os.getenv('SITE_URL')
            }
            print('删除帖子要发送的消息', dict)
            print('管理员删帖发送消息')
            uids = [op.wx_id]
            send_message_by_pusher(msg=dict, uid=uids, kind=2)


@celery.task
def send_message_by_pusher(msg, uid, kind):
    print('即将要发送的消息', msg)
    msg_template = {
        0: 'WXLostNotice.txt',  # 寻物认领
        1: "WXFoundNotice.txt",  # 招领认领
        2: 'WXDeleteNotice.txt',  # 删除通知
        3: 'WXNotice.txt',  # 发布招领匹配
        4: "WXCommentNotice.txt",  # 评论提醒
        5: 'WXPasswordNotice.txt',  # 重置密码的消息
        6: "WXLoginNotice.txt",  # 异常登录提醒
        7: "WXImportantNotice.txt"  # 群发重要通知
    }
    content = render_template('msgs/' + msg_template[kind], messages=msg)
    print(content)
    if msg.get("url") is None:
        notice_url = os.getenv("SITE_URL")
    else:
        notice_url = msg['url']
    msg_ids = WxPusher.send_message(content=u'' + str(content), uids=uid, content_type=1, url=notice_url)
    print(msg_ids)
    for msg_id in msg_ids["data"]:
        print(msg_id, msg_id["status"])
        if "关闭" in msg_id["status"]:
            print("用户关闭了通知，发送邮件提醒")
            op = OpenID.query.filter(OpenID.wx_id == msg_id["uid"]).first()
            print(op)
            real_name = {
                "realName": op.user.real_name
            }
            send_email.apply_async(args=(op.user.qq, '系统通知', 'importantNotice', real_name), countdown=randint(10, 30))
