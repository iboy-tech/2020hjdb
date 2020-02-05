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

"""
权限分析：
通知；
ADD_NOTICE （超级）管理员
DEL_NOTICE  （超级）管理员
MOD_NOTICE  （超级）管理员
GET_NOTICE  所有
失物招领：
ADD_LOST_FOUND 所有
DEL_LOST_FOUND 所有
MOD_LOST_FOUND 所有
GET_LOST_FOUND 所有
反馈：
ADD_FEEDBACK 用户
DEL_FEEDBACK （超级）管理员
MOD_FEEDBACK  (超级）管理员
GET_FEEDBACK   用户
评论：
ADD_COMMENT 所有
DEL_COMMENT 用户和超管
MOD_COMMENT  没有
GET_COMMENT  所有
目录:
ADD_CATEGORY  超级管理员
DEL_CATEGORY  超级管理员
MOD_CATEGORY  超级管理员
GET_CATEGORY  (超级)管理员

用户：
LOCK_USER (超级)管理员
SET_SUPER_ADMIN 超管
SET_ADMIN  超管
DEL_USER    (超级)管理员
GET_USER_DETAIL (超级)管理员
GET_OWN_INFO  所有
RESET_PASSWORD (超级)管理员
"""
"""
SUPER_ADMIN
ADMIN
"""
from app.models.permission_model import Permission


class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary='roles_permissions', back_populates='roles')
    users = db.relationship('User', back_populates='role')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'User': ['USER'],
            'Admin': ['ADMIN'],
            'SuperAdmin': ['ADMIN', 'SUPER_ADMIN']
        }
        for role_name in roles_permissions_map:  # 添加角色
            print('角色名称：' + role_name)
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []  # 这会取消该角色对象和相关的权限对象之间的关联
            for permission_name in roles_permissions_map[role_name]:  # 重新更新权限列表
                print('权限名称：' + permission_name)
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
            db.session.commit()
