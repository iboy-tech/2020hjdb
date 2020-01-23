# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : login_form.py
@Time    : 2020/1/23 15:18
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(10, 18),
                                             DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')