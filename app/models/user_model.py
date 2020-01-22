# coding: utf-8
from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import FetchedValue

from app import db

Base = declarative_base()
metadata = Base.metadata


class TUser(db.Model):
    __tablename__ = 't_user'
    __table_args__ = (
        Index('UNIQUE_USER', 'username', 'qq'),
    )

    id = db.Column(db.String(64), primary_key=True, info='?????')
    username = db.Column(db.String(64), nullable=False, info='??')
    password = db.Column(db.String(64), nullable=False, info='????')
    real_name = db.Column(db.String(256), nullable=False, info='????')
    academy = db.Column(db.String(128), nullable=False, info='??')
    class_id = db.Column(db.String(128), nullable=False, info='??')
    major = db.Column(db.String(30), nullable=False, info='??')
    qq = db.Column(db.String(16), nullable=False, info='QQ?')
    avatar = db.Column(db.String(256), info='??')
    kind = db.Column(db.Integer, nullable=False, server_default=FetchedValue(), info='??/0????/2???/1??????')
    sex = db.Column(db.Integer, server_default=FetchedValue(), info='??,0???,1???')
    create_time = db.Column(db.DateTime, nullable=False, server_default=FetchedValue(), info='????')
    last_login = db.Column(db.DateTime, info='??????')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TUser %r>' % self.name
