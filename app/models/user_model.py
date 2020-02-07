# coding: utf-8
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.role_model import Role
from app import login_manager, db
from app.models.permission_model import Permission


class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    @property
    def is_super_admin(self):
        return False


class User(db.Model, UserMixin):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, info='主键')
    username = db.Column(db.String(25), nullable=False, info='学号', unique=True)
    password_hash = db.Column(db.String(128), info='密码散列')
    real_name = db.Column(db.String(100), nullable=False, info='真名')
    academy = db.Column(db.String(150), nullable=False, info='学院')
    class_name = db.Column(db.String(30), nullable=False, info='班级')
    major = db.Column(db.String(50), nullable=False, info='专业')
    qq = db.Column(db.String(16), nullable=False, info='QQ', unique=True)
    kind = db.Column(db.Integer, db.ForeignKey('t_role.id'), nullable=False, server_default=text('1'), info='是否为管理员')
    role = db.relationship('Role', back_populates='users')
    gender = db.Column(db.Integer, nullable=False, server_default=text('0'), info='0男1女')
    status = db.Column(db.Integer, nullable=False, server_default=text('1'), info='用户状态01')
    create_time = db.Column(db.DateTime, default=datetime.now, info='时间')
    last_login = db.Column(db.DateTime, default=datetime.now, info='最后登录时间')
    lost_founds = db.relationship('LostFound', backref='t_lost_founds', lazy="select")  # 关联评论表
    comments = db.relationship('Comment', backref='t_comment', lazy="select")  # 关联评论表

    # @property是让这个更简洁
    # ，既保持直接对属性赋值的方便，又对条件做了限制：
    # 调用的时候仍然是方便快捷的直接赋值：
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # 生成密码散列
        self.password_hash = generate_password_hash(password)

    # generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    def verify_password(self, password):  # 验证密码
        return check_password_hash(self.password_hash, password)

    def set_role(self):  # 权限初始化
        if self.role is None:
            if self.username == current_app.config['SUPER_ADMIN_USERNAME']:
                self.role = Role.query.filter_by(name='SuperAdmin').first()
        else:
            self.role = Role.query.filter_by(name='User').first()
            db.session.commit()

    @staticmethod
    def init_role_permission():  # 为已注册用户添加权限
        for user in User.query.all():  # 迭代User模型中的所有记录
            if user.role is None:
                if user.username == current_app.config['SUPER_ADMIN_USERNAME']:
                    user.role = Role.query.filter_by(name='SuperAdmin').first()
        else:
            user.role = Role.query.filter_by(name='User').first()
            db.session.add(user)
            db.session.commit()

    def to_dict(self):
        dict = {
            "userId": self.id,
            "name": self.real_name,
            "username": self.username,
            "gender": '男' if self.gender == 0 else '女',
            "qq": self.qq,
            "classNum": self.class_name,
            "major": self.major,
            "academy": self.academy,
            "lastLogin": self.last_login.strftime('%Y-%m-%d %H:%M:%S'),
            "status": "正常" if self.status == 1 else '已冻结',
            "kind": self.kind
        }
        return dict

    @property
    def is_admin(self):
        return self.role.name == 'Admin'

    @property
    def is_super_admin(self):
        return self.role.name == 'SuperAdmin'

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and \
               permission in self.role.permissions

    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<User %r>' % self.real_name
        #     return '新建用户'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))