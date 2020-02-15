# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File   = fakes.py
@Time   = 2020/1/27 18:58
@Author = iBoy
@Email  = iboy@iboy.tech
@Description= 
@Software: PyCharm
"""

from app.models.user_model import User,db
admin_role=User(username='2018171101',password='123456',real_name='测试',academy='计算机与信息学院',class_name='20181107',major='物联网',qq='3282534296',kind=1,gender=0)
db.session.add(admin_role)
db.session.commit()

from datetime import datetime
from app.models.category_model import  Category,db
category=Category(name='校园卡',about='校园卡',user_id='2',create_time=datetime.now)
db.session.add(category)
db.session.commit()

from app.models.lostfound_model import LostFound,db

lostfound=LostFound(kind= 0,status= 1,claimant_id= None,user_id= 2,location ="西苑足球场",title = "手机掉了",about = "白色苹果手机",images="upload_7702946183392903652.jpg",category_id=1,look_count = 1)
db.session.add(lostfound)
db.session.commit()


from app.models.comment_model import Comment,db
comment=Comment(lost_found_id=1,user_id=1,content='祝你好运')
db.session.add(comment)
db.session.commit()


from  app.models.notice_model import Notice,db
notice=Notice(title='放假通知',content='考试周，失物招领工作暂停，感谢大家的支持！',fix_top=1,user_id=2)
db.session.add(notice)
db.session.commit()

from  app.models.feedback_model import Feedback,db
feed=Feedback(subject='发现BUG',content='考试周，失物招领工作暂停，感谢大家的支持！',user_id='1',handler_id='2',answer='收到谢谢')
db.session.add(feed)
db.session.commit()