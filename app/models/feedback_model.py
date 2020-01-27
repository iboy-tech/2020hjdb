# coding: utf-8
from datetime import datetime

from sqlalchemy import text

from app import db


class Feedback(db.Model):
    __tablename__ = 't_feedback'

    id = db.Column(db.Integer, primary_key=True, info='主键')
    answer = db.Column(db.String(1024), info='?????')
    content = db.Column(db.String(1024), nullable=False, info='?????')
    create_time = db.Column(db.DateTime, default=datetime.now(),nullable=False, info='????')
    handler_name = db.Column(db.String(256), info='??????')
    real_name = db.Column(db.String(256), nullable=False, info='????????')
    record_status = db.Column(db.Integer, nullable=False,server_default=text('0'), info='????0/1 0????')
    subject = db.Column(db.String(256), nullable=False, info='?????')
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.id'),nullable=False, info='创建人ID')
    username = db.Column(db.String(64), nullable=False, info='?????')
    def __repr__(self):
        return '<TFeedback %r>' % self.name
