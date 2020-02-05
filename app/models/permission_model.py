# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : permission_model.py
@Time    : 2020/2/3 20:43
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from app import db


class Permission(db.Model):
    __tablename__ = 't_permission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    roles = db.relationship('Role', secondary='roles_permissions', back_populates='permissions')
