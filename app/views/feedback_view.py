# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : feedback_view.py
@Time    : 2020/1/23 15:38
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from datetime import datetime

from flask import render_template, request
from flask_login import current_user, login_required

from app import db
from app.config import AdminConfig
from app.decorators import admin_required, wechat_required
from app.models.feedback_model import Feedback
from app.models.user_model import User
from app.page import feedback
from app.utils import restful
from app.utils.mail_sender import send_email


@feedback.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
@wechat_required
@admin_required
def index():
    return render_template('feedback.html')


@feedback.route('/getall', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def get_all():
    feedbacks = Feedback.query.all()
    list = []
    if feedbacks:
        for f in feedbacks:
            admin = None
            if f.handler_id is not None:
                admin = User.query.get(int(f.handler_id))
            user = User.query.get(int(f.user_id))
            dict = {
                "id": f.id,
                "userId": user.id,
                "username": user.username,
                "realName": user.real_name,
                "subject": f.subject,
                "content": f.content,
                "createTime": f.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": f.status,
                "handlerId": f.handler_id,
                "handlerName": admin.real_name if admin is not None else None,
                "handlerEmail": admin.qq + '@qq.com' if admin is not None else None,
                "answer": f.answer,
                "handlerTime": f.handler_time.strftime('%Y-%m-%d %H:%M:%S') if f.handler_time is not None else None,
            }
            list.append(dict)
    data = {
        "list": list,
    }
    return restful.success(data=data)


# 获取未处理的反馈
def get_new_feedback():
    new_count = Feedback.query.filter(Feedback.handler_id == None).count()
    if new_count >= 10:
        new_count = str(new_count)
    elif new_count > 0:
        new_count = "0" + str(new_count)
    else:
        new_count = 0
    return new_count


def checkFeedback(data):
    if data['subject'] == "" or data['content'] == "":
        return True
    else:
        return False


@feedback.route('/add', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
def feedback_add():
    req = request.json
    print('req', req)
    if checkFeedback(req):
        return restful.params_error()  # 表单内容为空
    # 表单过滤
    f = Feedback(subject=req['subject'].replace('/(<（[^>]+）>)/script', ''),
                 content=req['content'].replace('<', '&lt;').replace('>', '&gt;'), user_id=current_user.id)
    messages = {
        "username": current_user.username,
        "real_name": current_user.real_name,
        "subject": f.subject,
        "content": f.content,
        'feedbackTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        db.session.add(f)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return restful.success(success=False, msg=str(e))
    send_email.delay(AdminConfig.SUPER_ADMIN_QQ, '反馈通知', 'feedbackNotice', messages)
    return restful.success(msg="感谢您的反馈")


@feedback.route('/delete', methods=['POST', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def feedback_delete():
    req = request.args.get('id')
    print('request.args.get(\'id\')', req)
    f = Feedback.query.get(int(req))
    db.session.delete(f)
    db.session.commit()
    return restful.success()


@feedback.route('/reply', methods=['POST', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def feedback_replay():
    req = request.json
    print(req)
    id = int(req['id'])
    f = Feedback.query.get(id)
    f.handler_id = current_user.id
    f.status = 1
    f.handler_time = datetime.now()
    u = User.query.get(f.user_id)
    f.answer = req['content']
    db.session.commit()
    messages = {
        'subject': f.subject,
        'content': f.content,
        'createTime': f.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'realName': u.real_name,
        'answer': req['content'],
        'handlerTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'handlerName': current_user.real_name,
        'handlerEmail': current_user.qq + '@qq.com',
    }
    send_email.delay(u.qq, '反馈回复', 'feedbackReply', messages)
    print('要给用户发送提醒邮件')
    return restful.success()


@feedback.route('/mark', methods=['POST', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def feedback_mark():
    req = request.args.get('id')
    print('request.args.get(\'id\')', req)
    f = Feedback.query.get(int(req))
    f.status = 1
    f.handler_time = datetime.now()
    f.handler_id = current_user.id
    db.session.commit()
    return restful.success()
