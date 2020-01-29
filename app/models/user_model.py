# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index, text
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from app import login_manager
from app import db

Base = declarative_base()
metadata = Base.metadata


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
    kind = db.Column(db.Integer, nullable=False, server_default=text('1'), info='是否为管理员')
    gender = db.Column(db.Integer, server_default=text('0'), info='0男1女')
    status = db.Column(db.Integer, nullable=False, default=1, info='用户状态01')
    create_time = db.Column(db.DateTime, default=datetime.now(), info='时间')
    last_login = db.Column(db.DateTime, default=datetime.now(), info='最后登录时间')

    # @property是让这个更简洁
    # ，既保持直接对属性赋值的方便，又对条件做了限制：
    # 调用的时候仍然是方便快捷的直接赋值：
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # 生成密码散列
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # 验证密码
        return check_password_hash(self.password_hash, password)

    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TUser %r>' % self.real_name
        #     return '新建用户'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
