# coding: utf-8
from sqlalchemy import FetchedValue

from app import db


class TFeedback(db.Model):
    __tablename__ = 't_feedback'

    id = db.Column(db.String(64), primary_key=True, info='??')
    answer = db.Column(db.String(1024), info='?????')
    content = db.Column(db.String(1024), nullable=False, info='?????')
    create_time = db.Column(db.DateTime, nullable=False, info='????')
    handler_name = db.Column(db.String(256), info='??????')
    real_name = db.Column(db.String(256), nullable=False, info='????????')
    record_status = db.Column(db.Integer, nullable=False, server_default=FetchedValue(), info='????0/1 0????')
    subject = db.Column(db.String(256), nullable=False, info='?????')
    user_id = db.Column(db.String(64), nullable=False, info='???ID')
    username = db.Column(db.String(64), nullable=False, info='?????')
    def __repr__(self):
        return '<TFeedback %r>' % self.name
