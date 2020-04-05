# coding: utf-8
from datetime import datetime

from sqlalchemy import text, desc

from app import db


class LostFound(db.Model):
    __tablename__ = 't_lost_found'

    __table_args__ = {'mysql_charset': 'utf8mb4','mysql_collate': 'utf8mb4_unicode_ci'}
    id = db.Column(db.Integer, primary_key=True, info='主键')
    kind = db.Column(db.Integer, nullable=False, info='类型失物或招领01')
    category_id = db.Column(db.Integer, db.ForeignKey('t_category.id', ondelete='CASCADE'), nullable=False,index = True, info='外键')
    about = db.Column(db.String(400), nullable=False,info='详情')
    title = db.Column(db.String(40), nullable=False,index = True, info='帖子标题')
    images = db.Column(db.String(150), info='图片', default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id', ondelete='CASCADE'),index = True, nullable=False, info='创建者id')
    claimant_id = db.Column(db.Integer, info='索要者ID',index = True, default=None)
    create_time = db.Column(db.DateTime, default=datetime.now,index = True, nullable=False, info='创建时间')
    deal_time = db.Column(db.DateTime, info='领取的时间', default=None)
    # fix_top = db.Column(db.Integer, nullable=False, server_default=text('0'), info='置顶')
    location = db.Column(db.String(30), info='位置')
    look_count = db.Column(db.Integer, nullable=False, server_default=text('0'))
    status = db.Column(db.Integer, nullable=False, info='物品的状态01是否被领取', server_default=text('0'))
    # 帖子评论-一对多，删除帖子要删除评论
    comments = db.relationship('Comment', backref='post_comment', order_by=(desc('create_time')),cascade='all, delete-orphan', passive_deletes=True)

    def to_dict(self):
        dict = {
            'id': self.id,
            'user_id':self.user_id,
            'title': self.title,
            'about': self.about,
        }
        return dict

    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<LostFound %r>' % self.title
