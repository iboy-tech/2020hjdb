# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : test_app.py
@Time    : 2020/1/18 20:58
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 测试用实例
@Software: PyCharm
"""
from flask import  Flask
from flask_script import  Manager
from flask import render_template

from main.forms import NameForm


app=Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
manage=Manager(app)
@app.route('/',methods=['GET','POST'])
def index():
    user={
        'name':'杨豪',
        'sex':'男'
    }
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
    form.name.data = ''
    return render_template('admin.html', form=form, name=name)
if __name__=='__main__':
    manage.run()