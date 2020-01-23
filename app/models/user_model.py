# coding: utf-8
from datetime import datetime

from sqlalchemy import Index,text
from sqlalchemy.ext.declarative import declarative_base


from app import db

Base = declarative_base()
metadata = Base.metadata


class User(db.Model):
    __tablename__ = 't_user'
    __table_args__ = (
        Index('UNIQUE_USER', 'username', 'qq'),
    )
    id = db.Column(db.Integer, primary_key=True, info='主键')
    username = db.Column(db.String(25), nullable=False, info='学号')
    password = db.Column(db.String(64), nullable=False, info='密码')
    real_name = db.Column(db.String(100), nullable=False, info='真名')
    academy = db.Column(db.String(150), nullable=False, info='学院')
    class_id = db.Column(db.String(30), nullable=False, info='班级')
    major = db.Column(db.String(50), nullable=False, info='专业')
    qq = db.Column(db.String(16), nullable=False, info='QQ')
    # avatar = db.Column(db.String(256), info='??')
    kind = db.Column(db.Integer, nullable=False, server_default=text('0'), info='是否为管理员')
    sex = db.Column(db.Integer, server_default=text('0'), info='0男1女')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(), info='时间')
    last_login = db.Column(db.DateTime, default=datetime.utcnow(),nullable=True,info='最后登录时间')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TUser %r>' % self.name
