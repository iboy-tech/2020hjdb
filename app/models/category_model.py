# coding: utf-8

from app import db


class TCategory(db.Model):
    __tablename__ = 't_category'

    id = db.Column(db.Integer, primary_key=True, nullable=False, info='???ID')
    name = db.Column(db.String(128), primary_key=True, nullable=False, info='?????')
    about = db.Column(db.String(256), info='?????')
    create_time = db.Column(db.DateTime, nullable=False, info='???????')
    user_id = db.Column(db.String(256), nullable=False, info='???id')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TCategory %r>' % self.name
