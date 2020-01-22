# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : admin_view.py
@Time    : 2020/1/19 21:21
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from datetime import datetime
from flask import render_template, url_for, session, redirect

from main import admin

# from .. import db
# from .forms import NameForm
# from ..models import User

print('视图文件加载')


@admin.route('/admin', methods=['GET', 'POST'])
def index():
    print('蓝图请求成功！')
    # form = NameForm()
    # if form:
    #     return redirect(url_for('.index'))
    user = {
        'schoolName':'三峡大学',
        'email':'547142436@qq.com'
    }
    return render_template('admin.html',user=user)
    # return render_template('admin.html', form=form, name=session.get('name'),
    #                        know=session.get('know', False),
    #                        current_time=datetime.utcnow())