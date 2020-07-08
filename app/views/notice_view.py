# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : notice_view.py
@Time    : 2020/1/23 15:37
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import datetime

from flask import request, render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import db, OpenID, cache, logger
from app.decorators import admin_required, wechat_required
from app.page import notice
from app.models.notice_model import Notice
from app.utils import restful
from app.views.found_view import send_message_by_pusher
from tasks import celery


@notice.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
@cache.cached(timeout=3600 * 24 * 7, key_prefix="notice")  # 缓存5分钟 默认为300s
@login_required
def get_all():
    notices = Notice.query.order_by(desc('fix_top'), desc('create_time')).limit(10)
    list = [n.to_dict() for n in notices]
    data = {
        "list": list
    }
    return restful.success(data=data)


@notice.route('/', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def notice_add():
    req = request.json
    n = Notice(title=req['title'].replace('<', '&lt;').replace('>', '&gt;'),
               content=req['content'].replace('<', '&lt;').replace('>', '&gt;'),
               fix_top=1 if req['fixTop'] == True else 0)
    if req['pusher']:
        if current_user.kind == 3:
            logger.info("超级管理向所有用户推送微信消息")
            msg = {
                "title": n.title,
                "content": n.content,
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            noticeAll.delay(msg)
    db.session.add(n)
    db.session.commit()
    cache.delete("notice")
    return restful.success(msg="发布成功")


# 向所有用户异步发送通知
@celery.task
def noticeAll(msg):
    uids = []
    wx_opens = db.session.query(OpenID)
    for wx in wx_opens:
        if wx.wx_id:
            uids.append(wx.wx_id)
    send_message_by_pusher(msg=msg, uid=uids, kind=7)


@notice.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@login_required
@admin_required
def notice_delete(id=-1):
    if id == -1:
        return restful.error()
    n = Notice.query.get(id)
    db.session.delete(n)
    db.session.commit()
    cache.delete("notice")
    return restful.success(msg="删除成功")


@notice.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@login_required
@admin_required
def notice_switch(id=-1):
    if id == -1:
        return restful.error()
    n = Notice.query.get(id)
    n.fix_top = 1 if n.fix_top == 0 else 0
    db.session.commit()
    cache.delete("notice")
    return restful.success()
