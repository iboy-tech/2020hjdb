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

from flask import request
from flask_cors import cross_origin
from flask_login import current_user, login_required
from sqlalchemy import desc

from app import db
from app.decorators import wechat_required
from app.page import comment
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User
from app.utils import restful


@comment.route('/', methods=['GET', 'POST', 'OPTIONS'],strict_slashes=False)
@login_required
@wechat_required
def index():
    id=request.args.get('id')
    print('评论的ID',id)
    req = request.json
    if req is not None:
        print('添加评论',req)
        comment = Comment(lost_found_id=req['targetId'], user_id=current_user.id, content=req['content'])
        db.session.add(comment)
        db.session.commit()
        return restful.success()
    else:
        comments=Comment.query.order_by(desc('create_time')).filter_by(lost_found_id=int(id)).all()
        # print("我是帖子的评论：",comments)
        if not comments:
            data={
                    "comments": []
                }
            return restful.success(data=data)
        else:
            list=[]
            for c in comments:
                user =User.query.get(c.user_id)
                dict={
                        "id": c.id,
                        "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                        "username": user.username,
                        "time": c.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "content": c.content
                }
                list.append(dict)
            data= {
                "comments": list
            }
            # print("评论参数data：",data)
            return restful.success(data=data)


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
            return restful.success(msg='删除成功')
        else:
            return restful.params_error()
