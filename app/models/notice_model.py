# coding: utf-8
from datetime import datetime

from sqlalchemy import text

from app import db


class Notice(db.Model):
    __tablename__ = 't_notice'
    __table_args__ = {'mysql_charset': 'utf8mb4','mysql_collate': 'utf8mb4_unicode_ci'}
    id = db.Column(db.Integer, primary_key=True, info='主键')
    title = db.Column(db.String(128), nullable=False, info='标题')
    content = db.Column(db.String(1024), nullable=False, info='内容')
    fix_top = db.Column(db.Integer, nullable=False, server_default=text('0'), info='是否置顶')
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False, info='创建时间')

    def to_dict(self):
        dict = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "fixTop": self.fix_top,
            "isNew": (datetime.now()-self.create_time).days<=7
        }
        return dict

    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<Notice %r>' % self.title
