# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : detail_view.py
@Time    : 2020/1/25 22:30
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import os

from flask import render_template, request, abort, current_app
from flask_login import current_user, login_required

from app import db, redis_client, limiter, logger
from app.config import PostConfig
from app.decorators import wechat_required
from app.models.category_model import Category
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.page import detail
from app.utils import restful


@detail.route('/<int:id>.html', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@limiter.limit(limit_value="30/minute")
@login_required
@wechat_required
def index(id=-1):
    if id == -1:
        return restful.error("参数缺失")
    if request.method == 'GET':
        # logger.info("我是获取的ID", request.args.get('id'))
        # id = request.args.get('id')
        # if id is None:
        #     return restful.error('提示：参数缺失')
        lost = LostFound.query.get(id)
        if lost is not None:
            return render_template('detail.html')
        else:
            abort(404)
    else:
        try:
            lost = LostFound.query.get(id)
        except Exception as e:
            logger.info(str(e))
            return restful.error('警告,检测到用户 {} 尝试非法字符注入，后台已记录'.format(current_user.real_name))
        if lost is not None:
            key = PostConfig.POST_REDIS_PREFIX+str(lost.id)
            redis_client.incr(key)
            intcnt = int(bytes.decode(redis_client.get(key)))
            # 超过一定程度吧浏览量存入数据库
            if intcnt - lost.look_count >= PostConfig.REDIS_MAX_VIEW:
                lost.look_count = lost.look_count + (intcnt - lost.look_count)
                db.session.add(lost)
                db.session.commit()
            user = User.query.get_or_404(lost.user_id)
            if lost.images == "":
                imglist = []
            else:
                # lost.images = lost.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                imglist = lost.images.strip().split(',')
            item = {
                "id": lost.id,
                "icon": PostConfig.AVATER_API.replace("{}", user.qq),
                "kind": lost.kind,
                "userId": lost.user_id,
                "username": user.username,
                "realName": user.real_name,
                "time": lost.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "location": lost.location,
                "title": lost.title,
                "about": lost.about,
                "images": imglist,
                "category": (Category.query.get(lost.category_id)).name,
                "lookCount": intcnt,
                "status": lost.status,
                "dealTime": None if lost.deal_time is None else lost.deal_time.strftime('%Y-%m-%d %H:%M:%S'),
                "isSelf": current_user.id == lost.user_id,
                "isAdmin": current_user.kind > user.kind,
                "email": user.qq + '@qq.com',
                "QQ": user.qq,
                "site": os.getenv('SITE_URL')
            }
            data = {"item": item}
            return restful.success(data=data)
        else:
            abort(404)
