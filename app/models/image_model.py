# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : image_model.py
@Time    : 2020/2/3 12:40
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from datetime import datetime

from sqlalchemy.engine import default

from app import db


class ImageAPI(db.Model):
    __tablename__ = 't_image'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=False)
    is_active = db.Column(db.int, default=False)
    create_time = db.Column(db.DateTime(), default=datetime.now)
