# coding: utf-8
from datetime import datetime

from app import db


class Comment(db.Model):
    __tablename__ = 't_comment'
    id = db.Column(db.Integer, primary_key=True, info='主键')
    lost_found_id = db.Column(db.Integer,db.ForeignKey('t_lost_found.id',ondelete='CASCADE'),nullable=False,index=True,info='失物外键')
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.id',ondelete='CASCADE'),nullable=False,index=True,info='用户外键')
    content = db.Column(db.String(1024), nullable=False, info='评论内容')
    create_time = db.Column(db.DateTime, default=datetime.now, info='时间')

    def __repr__(self):
        return '<Comment %r>' % self.content
