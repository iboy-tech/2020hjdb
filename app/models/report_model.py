# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : report_model.py
@Time    : 2020/2/27 20:45
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from datetime import datetime

from app import db


# 报表模型
class Report(db.Model):
    __tablename__ = 't_report'
    id = db.Column(db.String(100), primary_key=True)
    file_name = db.Column(db.String(200), default=None)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.id', ondelete='CASCADE'),nullable=False,index=True,info='创建人ID')
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)


def __repr__(self):
    return '<Report %r>' % self.file_name
