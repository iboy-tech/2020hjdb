# coding: utf-8
from sqlalchemy.schema import FetchedValue

from app import  db




class TNotice(db.Model):
    __tablename__ = 't_notice'

    id = db.Column(db.String(64), primary_key=True, info='??')
    title = db.Column(db.String(128), nullable=False, info='????')
    content = db.Column(db.String(1024), nullable=False, info='????')
    fix_top = db.Column(db.Integer, nullable=False, server_default=FetchedValue(), info='????')
    create_time = db.Column(db.DateTime, nullable=False, info='????')
    creator_id = db.Column(db.String(64), nullable=False, info='???ID')
    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<TNotice %r>' % self.name
