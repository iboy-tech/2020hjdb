# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : user_view.py
@Time    : 2020/1/19 22:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template, request, g, current_app, session, redirect, url_for
from flask_cors import cross_origin
from flask_login import current_user

from app import db
from app.main import user, auth
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User


@user.route('/', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
def index():
    data=request.json
    print('user页面收到请求',data)
    return render_template('user.html')#所有参数都要


@user.route('/messages', methods=['POST', 'OPTIONS', 'GET'])
@cross_origin()
def get_message():
    req=request.json
    print('查询消息req',req)
    # commens=Comment.query.join(LostFound,user_id=current_user.id)
    losts=LostFound.query.filter_by(user_id=current_user.id).all()
    print("这是我接受的消息" ,type(losts),losts,losts[0].comments)
    if len(losts)==0:
      data= {
      "success" : True,
      "code" : 1000,
      "msg" : "处理成功",
      "data" : {
        "list" : []
      },
      "ext" : None
    }
    else:
        list=[]
        for l in losts:
            if len(l.comments) !=0:
                for c in  l.comments:
                    user=User.query.get(c.user_id)
                    dict={
                      "id" : c.id,
                      "userId" :user.id,
                      "icon" : 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
                      "username" : user.real_name+' '+user.username,
                      "time" : c.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                      "title" : l.title,
                      "lostFoundId" : l.id,
                      "content" : c.content
                    }
                    list.append(dict)
            data={
              "success" : True,
              "code" : 1000,
              "msg" : "处理成功",
              "data" : {
                "list" : list
              },
              "ext" : None
            }
    return data

@user.route('/setPassword', methods=['POST'])
@cross_origin()
def get_all_user():
    print('用户准备更改密码')
    req=request.json
    print(req)
    u=User.query.get(current_user.id)
    if u.verify_password(req['oldPassword']):
        u.password=req['newPassword']
        db.session.commit()
        data={
                "success":True,
                "code": 1002,
                "msg": "改密成功",
                "data": {},
                "ext": None
            }
        return data
    data = {
        "success": False,
        "code": 1002,
        "msg": "您输入的密码有误",
        "data": {},
        "ext": None
    }
    return data

