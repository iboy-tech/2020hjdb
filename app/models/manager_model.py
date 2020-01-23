# coding: utf-8
from datetime import datetime

from app import  db




class Manager(db.Model):
    __tablename__ = 't_manager'

    id = db.Column(db.Integer, primary_key=True, info='??')
    create_time = db.Column(db.DateTime, default=datetime.utcnow(),nullable=False)
    creator_id = db.Column(db.DateTime, nullable=False)
    qq = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.String(64), nullable=False, unique=True, info='??ID')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TManager %r>' % self.name
