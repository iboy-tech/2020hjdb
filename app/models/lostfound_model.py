# coding: utf-8
from datetime import datetime
from sqlalchemy import Index, text, desc
from sqlalchemy.orm import relationship

from app import db, User


class LostFound(db.Model):
    __tablename__ = 't_lost_found'
    __table_args__ = (
        Index('INDEX_LF', 'title', 'category_id'),  # 索引名称
    )
    id = db.Column(db.Integer, primary_key=True, info='主键')
    comments = db.relationship('Comment', order_by=(desc('create_time')), backref='t_lost_found', lazy="select",
                               cascade='all', passive_deletes=True)
    kind = db.Column(db.Integer, nullable=False, info='类型失物或招领01')
    category_id = db.Column(db.Integer, db.ForeignKey('t_category.id', ondelete='CASCADE'), nullable=False, info='外键')
    about = db.Column(db.String(1024), nullable=False, info='详情')
    title = db.Column(db.String(128), nullable=False, info='帖子标题')
    images = db.Column(db.String(1024), info='图片', default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id', ondelete='CASCADE'), nullable=False, info='创建者id')
    claimant_id = db.Column(db.Integer, info='索要者ID', default=None)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False, info='创建时间')
    deal_time = db.Column(db.DateTime, info='领取的时间', default=None)
    # fix_top = db.Column(db.Integer, nullable=False, server_default=text('0'), info='置顶')
    location = db.Column(db.String(512), info='位置')
    look_count = db.Column(db.Integer, nullable=False, server_default=text('0'))
    status = db.Column(db.Integer, nullable=False, info='物品的状态01是否被领取', server_default=text('0'))
    # 帖子评论-一对多，删除帖子要删除评论
    comments=db.relationship('Comment', backref='post_comment', cascade='all, delete-orphan', passive_deletes=True)


    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<LostFound %r>' % self.title
