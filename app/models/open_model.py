# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : open_model.py
@Time    : 2020/2/8 18:50
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from datetime import datetime

from sqlalchemy.orm import relationship

from app import db


class OpenID(db.Model):
    __tablename__ = 'openid'
    id = db.Column(db.Integer, primary_key=True)
    qq_id = db.Column(db.String(50), unique=True, default=None)
    wx_id = db.Column(db.String(50), unique=True,index=True, default=None)
    # 一对一外键关系使用
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id', ondelete='CASCADE'), unique=True)
    user = relationship("User", back_populates="wx_open")
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return '<OpenID %r>' % self.user_id
