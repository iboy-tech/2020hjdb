# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : comment_view.py
@Time    : 2020/1/23 15:37
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import datetime
import os

from flask import request
from flask_cors import cross_origin
from flask_login import current_user, login_required
from sqlalchemy import desc

from app import db, OpenID, PostConfig, cache
from app.decorators import wechat_required
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.page import comment
from app.utils import restful
from app.utils.check_data import check_comment
from app.views.found_view import send_message_by_pusher


@comment.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
@wechat_required
@check_comment
def index():
    id = request.args.get('id')
    req = request.json
    if req is not None:
        lost = LostFound.query.get(req['targetId'])
        if lost:
            user = User.query.get(lost.user_id)
            comment = Comment(lost_found_id=req['targetId'], user_id=current_user.id,
                              content=req['content'].replace('/(<（[^>]+）>)/script', ''))
            dict = {
                'post_user': user.real_name,
                'comment_user': current_user.real_name,
                'comment_content': comment.content,
                'connect_way': current_user.qq,
                'comment_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': os.getenv('SITE_URL') + 'detail.html?id=' + str(lost.id)
            }
            op = OpenID.query.filter_by(user_id=user.id).first()
            if op is not None and user.id != current_user.id:
                print('发送消息')
                uids = [op.wx_id]
                send_message_by_pusher(dict, uids, 4)
            try:
                db.session.add(comment)
                db.session.commit()
                return restful.success(msg='评论成功')
            except Exception as e:
                return restful.success(False, str(e))
        else:
            return restful.params_error()
    else:
        comments = Comment.query.order_by(desc('create_time')).filter_by(lost_found_id=int(id)).all()
        post=LostFound.query.get(int(id))
        if post:
            post_user=User.query.get(post.user_id)
            # print("我是帖子的评论：",comments)
            if not comments:
                data = {
                    "comments": [],
                    "wxReward": "" if post_user.wx_reward_url is None else post_user.wx_reward_url
                }
                return restful.success(data=data)
            else:
                list = []
                for c in comments:
                    user = User.query.get(c.user_id)
                    dict = {
                        "id": c.id,
                        "icon": PostConfig.AVATER_API.replace("{}", user.qq),
                        "realName": user.real_name,
                        "time": c.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "content": c.content
                    }
                    list.append(dict)
                data = {
                    "comments": list,
                    "wxReward": "" if post_user.wx_reward_url is None else post_user.wx_reward_url
                }
                # print("评论参数data：",data)
                return restful.success(data=data)
        else:
            return restful.params_error()


@comment.route('/delete', methods=['POST'])
@login_required
@cross_origin()
def delete_comment():
    refer = request.referrer
    print(refer)
    req = request.args.get('id')
    print('删除评论：', req, type(req))
    if not req:
        return restful.params_error()
    else:
        c = Comment.query.get(int(req))
        if c is not None and (
                LostFound.query.get(c.lost_found_id).user_id == current_user.id or current_user.kind >= 2):
            db.session.delete(c)
            db.session.commit()
            # 删除消息缓存
            # res=cache.delete("messages")
            # print("消息缓存删除结果：",res)
            return restful.success(msg='删除成功')
        else:
            return restful.params_error()
