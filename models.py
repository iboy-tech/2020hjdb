# coding: utf-8
from sqlalchemy import Column, DateTime, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TCategory(Base):
    __tablename__ = 't_category'

    id = Column(INTEGER(11), primary_key=True, nullable=False, comment='???ID')
    name = Column(String(128), primary_key=True, nullable=False, comment='?????')
    about = Column(String(256), comment='?????')
    create_time = Column(DateTime, nullable=False, comment='???????')
    user_id = Column(String(256), nullable=False, comment='???id')


class TComment(Base):
    __tablename__ = 't_comment'

    id = Column(String(64), primary_key=True, comment='??')
    lost_found_id = Column(String(64), nullable=False, index=True, comment='?????')
    user_id = Column(String(64), nullable=False, index=True, comment='???ID')
    content = Column(String(128), nullable=False, comment='??')
    create_time = Column(DateTime, nullable=False, comment='????')


class TFeedback(Base):
    __tablename__ = 't_feedback'

    id = Column(String(64), primary_key=True, comment='??')
    answer = Column(String(1024), comment='?????')
    content = Column(String(1024), nullable=False, comment='?????')
    create_time = Column(DateTime, nullable=False, comment='????')
    handler_name = Column(String(256), comment='??????')
    real_name = Column(String(256), nullable=False, comment='????????')
    record_status = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='????0/1 0????')
    subject = Column(String(256), nullable=False, comment='?????')
    user_id = Column(String(64), nullable=False, comment='???ID')
    username = Column(String(64), nullable=False, comment='?????')


class TLostFound(Base):
    __tablename__ = 't_lost_found'
    __table_args__ = (
        Index('INDEX_LF', 'title', 'category_id'),
    )

    id = Column(String(64), primary_key=True, comment='??')
    kind = Column(INTEGER(11), nullable=False, comment='?????????')
    category_id = Column(String(128), nullable=False, comment='?????')
    about = Column(String(512), nullable=False, comment='????')
    title = Column(String(128), nullable=False, comment='?????')
    images = Column(String(1024), comment='?????')
    claimant_id = Column(String(64), comment='???ID')
    create_time = Column(DateTime, nullable=False, comment='????')
    deal_time = Column(DateTime, comment='?????')
    fix_top = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='????')
    location = Column(String(512), comment='????')
    look_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    record_status = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    status = Column(INTEGER(11), nullable=False, comment='??????????0??1??')
    user_id = Column(String(64), nullable=False, comment='???id')


class TManager(Base):
    __tablename__ = 't_manager'

    id = Column(String(64), primary_key=True, comment='??')
    create_time = Column(DateTime, nullable=False)
    creator_id = Column(DateTime, nullable=False)
    qq = Column(String(256), nullable=False)
    user_id = Column(String(64), nullable=False, unique=True, comment='??ID')


class TNotice(Base):
    __tablename__ = 't_notice'

    id = Column(String(64), primary_key=True, comment='??')
    title = Column(String(128), nullable=False, comment='????')
    content = Column(String(1024), nullable=False, comment='????')
    fix_top = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='????')
    create_time = Column(DateTime, nullable=False, comment='????')
    creator_id = Column(String(64), nullable=False, comment='???ID')


class TUser(Base):
    __tablename__ = 't_user'
    __table_args__ = (
        Index('UNIQUE_USER', 'username', 'qq', unique=True),
    )

    id = Column(String(64), primary_key=True, comment='?????')
    username = Column(String(64), nullable=False, comment='??')
    password = Column(String(64), nullable=False, comment='????')
    id_card = Column(String(64), nullable=False, comment='?????')
    real_name = Column(String(256), nullable=False, comment='????')
    tel = Column(String(16), comment='??')
    academy = Column(String(128), nullable=False, comment='??')
    class_id = Column(String(128), nullable=False, comment='??')
    major = Column(String(30), nullable=False, comment='??')
    area = Column(String(20), nullable=False, comment='??')
    qq = Column(String(16), nullable=False, comment='QQ?')
    avatar = Column(String(256), comment='??')
    kind = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='??/0????/2???/1??????')
    sex = Column(TINYINT(3), server_default=text("'0'"), comment='??,1???,2???,0???')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='????')
    last_login = Column(DateTime, comment='??????')
