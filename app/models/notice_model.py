# coding: utf-8
from datetime import datetime

from sqlalchemy import text

from app import  db




class Notice(db.Model):
    __tablename__ = 't_notice'

    id = db.Column(db.Integer, primary_key=True, info='主键')
    title = db.Column(db.String(128), nullable=False, info='标题')
    content = db.Column(db.String(1024), nullable=False, info='内容')
    fix_top = db.Column(db.Integer, nullable=False,server_default=text('0'), info='是否置顶')
    create_time = db.Column(db.DateTime,default=datetime.utcnow(), nullable=False, info='创建时间')
    creator_id = db.Column(db.String(64), nullable=False, info='创建者')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TNotice %r>' % self.name
