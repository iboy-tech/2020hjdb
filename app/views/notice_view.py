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
from flask import request, render_template
from flask_login import current_user, login_required
from sqlalchemy import desc

from app import db
from app.decorators import admin_required
from app.main import notice
from app.models.notice_model import Notice
from app.untils import restful


@notice.route('/', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
@admin_required
def index():
    data = request.json
    print('notice页面收到请求', data)
    return render_template('notice.html')


@notice.route('/getall', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
@login_required
def get_all():
    # notices=Notice.query.limit(10).order_by(Notice.create_time.desc()).all()
    # notices = Notice.query.all().order_by(Notice.create_time.desc())
    # notices = Notice.query.limit(10).order_by(desc('create_time')).all()
    notices = Notice.query.order_by(desc('fix_top'),desc('create_time')).limit(10)
    cnt = len(Notice.query.all())
    print('cnt:',cnt)
    print('notices:',notices)
    list=[]
    for n in notices:
        dict=n.to_dict()
        list.append(dict)
        data={
            "list": list
        }
    return restful.success(data=data)


@notice.route('/add', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def notice_add():
    req = request.json
    print(req)
    n = Notice(title=req['title'].replace('<','&lt;').replace('>','&gt;'), content=req['content'].replace('<','&lt;').replace('>','&gt;'), fix_top=1 if req['fixTop'] == True else 0)
    db.session.add(n)
    db.session.commit()
    return restful.success()


@notice.route('/delete', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def notice_delete():
    req=request.args.get('id')
    print('request.args.get(\'id\')',req)
    n=Notice.query.get(int(req))
    db.session.delete(n)
    db.session.commit()
    return restful.success()


@notice.route('/switch', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def notice_switch():
    req=request.args.get('id')
    print('request.args.get(\'id\')',req)
    n=Notice.query.get(int(req))
    n.fix_top=1 if n.fix_top==0 else 0
    db.session.commit()
    return restful.success()
