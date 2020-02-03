# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : role_model.py
@Time    : 2020/2/3 20:46
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from app import db

# 关联表
roles_permissions = db.Table('roles_permissions',
                             # db.Model.metadata,
                             db.Column('role_id', db.Integer, db.ForeignKey('t_role.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('t_permission.id'))
                             )


class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30), unique=True,nullable = False)
    permissions = db.relationship('Permission', secondary='roles_permissions', back_populates='roles')
    users = db.relationship('User', back_populates='role')