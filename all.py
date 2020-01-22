# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, MetaData, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)



class TCategory(Base):
    __tablename__ = 't_category'

    id = Column(Integer, primary_key=True, nullable=False, info='???ID')
    name = Column(String(128), primary_key=True, nullable=False, info='?????')
    about = Column(String(256), info='?????')
    create_time = Column(DateTime, nullable=False, info='???????')
    user_id = Column(String(256), nullable=False, info='???id')



class TComment(Base):
    __tablename__ = 't_comment'

    id = Column(String(64), primary_key=True, info='??')
    lost_found_id = Column(String(64), nullable=False, index=True, info='?????')
    user_id = Column(String(64), nullable=False, index=True, info='???ID')
    content = Column(String(128), nullable=False, info='??')
    create_time = Column(DateTime, nullable=False, info='????')



class TFeedback(Base):
    __tablename__ = 't_feedback'

    id = Column(String(64), primary_key=True, info='??')
    answer = Column(String(1024), info='?????')
    content = Column(String(1024), nullable=False, info='?????')
    create_time = Column(DateTime, nullable=False, info='????')
    handler_name = Column(String(256), info='??????')
    real_name = Column(String(256), nullable=False, info='????????')
    record_status = Column(Integer, nullable=False, server_default=FetchedValue(), info='????0/1 0????')
    subject = Column(String(256), nullable=False, info='?????')
    user_id = Column(String(64), nullable=False, info='???ID')
    username = Column(String(64), nullable=False, info='?????')



class TLostFound(Base):
    __tablename__ = 't_lost_found'
    __table_args__ = (
        Index('INDEX_LF', 'title', 'category_id'),
    )

    id = Column(String(64), primary_key=True, info='??')
    kind = Column(Integer, nullable=False, info='?????????')
    category_id = Column(String(128), nullable=False, info='?????')
    about = Column(String(512), nullable=False, info='????')
    title = Column(String(128), nullable=False, info='?????')
    images = Column(String(1024), info='?????')
    claimant_id = Column(String(64), info='???ID')
    create_time = Column(DateTime, nullable=False, info='????')
    deal_time = Column(DateTime, info='?????')
    fix_top = Column(Integer, nullable=False, server_default=FetchedValue(), info='????')
    location = Column(String(512), info='????')
    look_count = Column(Integer, nullable=False, server_default=FetchedValue())
    record_status = Column(Integer, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, info='??????????0??1??')
    user_id = Column(String(64), nullable=False, info='???id')



class TManager(Base):
    __tablename__ = 't_manager'

    id = Column(String(64), primary_key=True, info='??')
    create_time = Column(DateTime, nullable=False)
    creator_id = Column(DateTime, nullable=False)
    qq = Column(String(256), nullable=False)
    user_id = Column(String(64), nullable=False, unique=True, info='??ID')



class TNotice(Base):
    __tablename__ = 't_notice'

    id = Column(String(64), primary_key=True, info='??')
    title = Column(String(128), nullable=False, info='????')
    content = Column(String(1024), nullable=False, info='????')
    fix_top = Column(Integer, nullable=False, server_default=FetchedValue(), info='????')
    create_time = Column(DateTime, nullable=False, info='????')
    creator_id = Column(String(64), nullable=False, info='???ID')



class TUser(Base):
    __tablename__ = 't_user'
    __table_args__ = (
        Index('UNIQUE_USER', 'username', 'qq'),
    )

    id = Column(String(64), primary_key=True, info='?????')
    username = Column(String(64), nullable=False, info='??')
    password = Column(String(64), nullable=False, info='????')
    real_name = Column(String(256), nullable=False, info='????')
    academy = Column(String(128), nullable=False, info='??')
    class_id = Column(String(128), nullable=False, info='??')
    major = Column(String(30), nullable=False, info='??')
    qq = Column(String(16), nullable=False, info='QQ?')
    avatar = Column(String(256), info='??')
    kind = Column(Integer, nullable=False, server_default=FetchedValue(), info='??/0????/2???/1??????')
    sex = Column(Integer, server_default=FetchedValue(), info='??,0???,1???')
    create_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='????')
    last_login = Column(DateTime, info='??????')



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
