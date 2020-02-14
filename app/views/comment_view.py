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
from flask_login import current_user, login_required
from sqlalchemy import desc

from app import db
from app.decorators import wechat_required
from app.main import comment
from app.models.comment_model import Comment
from app.models.user_model import User
from app.untils import restful


@comment.route('/', methods=['GET', 'POST', 'OPTIONS'],strict_slashes=False)
@login_required
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


@comment.route('/delete', methods=['GET', 'POST', 'OPTIONS'],strict_slashes=False)
@login_required
def delete_comment():
    pass
