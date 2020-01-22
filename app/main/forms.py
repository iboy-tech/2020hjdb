# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : forms.py
@Time    : 2020/1/18 13:00
@Author  : iBoy
@Email   : iboy@iboy.tech
@Software: PyCharm
"""
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
class NameForm(Form):
    name = StringField('你的姓名是什么？',validators=[DataRequired()])
    submit=SubmitField('Submit')
    # def __init__(self,x):
    #     self.x=x

