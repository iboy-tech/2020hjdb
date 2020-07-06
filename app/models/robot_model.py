# coding: utf-8
from datetime import datetime

from sqlalchemy import text

from app import db


class Robot(db.Model):
    __tablename__ = 't_robot'
    id = db.Column(db.Integer, primary_key=True, info='主键')
    group_num = db.Column(db.String(12), nullable=False, index=True, info='QQ群号', unique=True)
    group_name = db.Column(db.String(40), nullable=False, info='群名称')
    key = db.Column(db.String(40), nullable=False, info='Key值', unique=True)
    type = db.Column(db.Integer, nullable=False, server_default=text('0'), info='0/1群发私发')
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False, info='创建时间')

    def to_dict(self):
        dict = {
            "Id": self.id,
            "groupNum": self.group_num,
            "groupName": self.group_name,
            "Key": self.key,
            "createTime": self.create_time
        }
        return dict

    # 返回一个具有可读性的字符串模型  方便调试
    def __repr__(self):
        return '<Robot %r>' % self.group_name
