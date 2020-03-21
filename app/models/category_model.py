# coding: utf-8
from datetime import datetime

from app import db
from app.models.lostfound_model import LostFound


class Category(db.Model):
    __tablename__ = 't_category'
    id = db.Column(db.Integer, primary_key=True, info='主键')
    name = db.Column(db.String(128), nullable=False,index=True,info='分类名称', unique=True)
    about = db.Column(db.String(256), info='分类说明')
    create_time = db.Column(db.DateTime,default=datetime.now,nullable=False,info='创建时间')
    #一对多
    posts= db.relationship('LostFound', backref='post_category', cascade='all, delete-orphan', passive_deletes=True)

    def to_dict(self):
        dict = {
            "name": self.name,
            "about": self.about,
            "categoryId": self.id,
            "createTime": self.create_time,
            "count": LostFound.query.filter_by(category_id=self.id).count()
        }
        return dict

    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<Category %r>' % self.name
