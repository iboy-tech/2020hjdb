# coding: utf-8
from sqlalchemy import Index
from sqlalchemy.schema import FetchedValue

from app import db


class TLostFound(db.Model):
    __tablename__ = 't_lost_found'
    __table_args__ = (
        Index('INDEX_LF', 'title', 'category_id'),
    )

    id = db.Column(db.String(64), primary_key=True, info='??')
    kind = db.Column(db.Integer, nullable=False, info='?????????')
    category_id = db.Column(db.String(128), nullable=False, info='?????')
    about = db.Column(db.String(512), nullable=False, info='????')
    title = db.Column(db.String(128), nullable=False, info='?????')
    images = db.Column(db.String(1024), info='?????')
    claimant_id = db.Column(db.String(64), info='???ID')
    create_time = db.Column(db.DateTime, nullable=False, info='????')
    deal_time = db.Column(db.DateTime, info='?????')
    fix_top = db.Column(db.Integer, nullable=False, server_default=FetchedValue(), info='????')
    location = db.Column(db.String(512), info='????')
    look_count = db.Column(db.Integer, nullable=False, server_default=FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=FetchedValue())
    status = db.Column(db.Integer, nullable=False, info='??????????0??1??')
    user_id = db.Column(db.String(64), nullable=False, info='???id')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TLostFound %r>' % self.name
