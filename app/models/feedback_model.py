# coding: utf-8
from datetime import datetime

from sqlalchemy import text

from app import db


class Feedback(db.Model):
    __tablename__ = 't_feedback'
    id = db.Column(db.Integer, primary_key=True, info='主键')
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.id'),nullable=False,info='创建人ID')
    subject = db.Column(db.String(256), nullable=False, info='反馈的主题')
    content = db.Column(db.String(1024), nullable=False, info='反馈的内容')
    create_time = db.Column(db.DateTime,default=datetime.now,nullable=False,info='反馈创建时间')
    handler_id = db.Column(db.Integer,db.ForeignKey('t_user.id'),default=None,info='回复者ID')
    answer = db.Column(db.String(1024), default=None, info='管理人员的回复内容')
    handler_time = db.Column(db.DateTime, default=None, info='处理的时间')
    status = db.Column(db.Integer,nullable=False,server_default=text('0'),info='0/1已读未读')

    def __repr__(self):
        return '<Feedback %r>' % self.subject
