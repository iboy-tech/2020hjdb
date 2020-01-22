# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : models.py
@Time    : 2020/1/18 13:06
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 数据库模型
@Software: PyCharm
"""
from . import  db
# class User(object):
#     #构造函数
#     def __init__(self,usr,pwd):
#         self.usr=usr
#         self.pwd=pwd
#     def save(self):
#         # conn=get_coon()
#         # cur=conn.cursor()
#         sql='insert '
#         # conn.close()
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    def __repr__(self):
        return '<User %r>' % self.username