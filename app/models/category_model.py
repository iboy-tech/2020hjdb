# coding: utf-8
from datetime import datetime

from app import db


class Category(db.Model):
    __tablename__ = 't_category'
    #一对多关系
    lostfounds=db.relationship('LostFound', backref='t_category')

    id = db.Column(db.Integer, primary_key=True, nullable=False, info='主键')
    name = db.Column(db.String(128), primary_key=True, nullable=False, info='分类名称')
    about = db.Column(db.String(256), info='分类说明')
    create_time = db.Column(db.DateTime,default=datetime.utcnow(),nullable=False, info='创建时间')
    user_id = db.Column(db.Integer, nullable=False, info='创建人ID')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TCategory %r>' % self.name
