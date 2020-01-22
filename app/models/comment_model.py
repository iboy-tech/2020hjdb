# coding: utf-8

from app import  db





class TComment(db.Model):
    __tablename__ = 't_comment'
    id = db.Column(db.String(64), primary_key=True, info='??')
    lost_found_id = db.Column(db.String(64), nullable=False, index=True, info='?????')
    user_id = db.Column(db.String(64), nullable=False, index=True, info='???ID')
    content = db.Column(db.String(128), nullable=False, info='??')
    create_time = db.Column(db.DateTime, nullable=False, info='????')
    def __repr__(self):
        return '<TComment %r>' % self.name
