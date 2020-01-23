# coding: utf-8
from datetime import datetime

from sqlalchemy import Index, text

from app import db


class LostFound(db.Model):
    __tablename__ = 't_lost_found'
    __table_args__ = (
        Index('INDEX_LF', 'title', 'category_id'),  # 索引名称
    )
    # category_id = db.Column(db.Integer, )  # 定义外键

    id = db.Column(db.Integer, primary_key=True, info='主键')
    kind = db.Column(db.Integer, nullable=False, info='类型失物或招领')
    category_id = db.Column(db.Integer, db.ForeignKey('t_category.id'),nullable=False, info='外键')#定义外键
    about = db.Column(db.String(512), nullable=False, info='详情')
    title = db.Column(db.String(128), nullable=False, info='帖子标题')
    images = db.Column(db.String(1024), info='?????')
    claimant_id = db.Column(db.String(64), info='???ID')
    create_time = db.Column(db.DateTime,default=datetime.utcnow(), nullable=False, info='????')
    deal_time = db.Column(db.DateTime, info='?????')
    fix_top = db.Column(db.Integer, nullable=False, server_default=text('0'), info='????')
    location = db.Column(db.String(512), info='????')
    look_count = db.Column(db.Integer, nullable=False,server_default=text('0'))
    record_status = db.Column(db.Integer, nullable=False,server_default=text('0'))
    status = db.Column(db.Integer, nullable=False, info='??????????0??1??')
    user_id = db.Column(db.String(64), nullable=False, info='???id')

    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TLostFound %r>' % self.name
