# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : manage.py
@Time    : 2020/1/10 16:58
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 顶级文件夹中的 manage.py 文件用于启动程序
@Software: PyCharm
"""
import os,sys
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension
from app.models.feedback_model import Feedback
from app.models.lostfound_model import LostFound
from app.models.notice_model import Notice
from app.models.user_model import User
from app.models.comment_model import Comment
from app.models.category_model import Category


from dotenv import load_dotenv

dotenv_path1 = os.path.join(os.path.dirname(__file__), '.env')
dotenv_path2 = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path1 and dotenv_path2) :
    load_dotenv(dotenv_path1,dotenv_path2)
    print('环境变量配置文件加载成功')
    print(os.getenv('APPID'))

print('当前的环境变量配置',os.getenv('FLASK_CONFIG'))

app = create_app(os.getenv('FlASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)
toolbar = DebugToolbarExtension(app)
# print('FLASK_APP:'+os.getenv('FLASK_APP'))


def make_shell_context():
    return dict(app=app, db=db, User=User,Category=Category,
                Comment=Comment,Notice=Notice,LostFound=LostFound,Feedback=Feedback)


manager.add_command('shell', Shell(make_shell_context()))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# def init_env():
#     print('导入环境变量')
#     print(os.path.realpath)
#     if os.path.exists('.env'):
#         print('Importing environment from .env...')
#         for line in open('../.env'):
#             var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]
#     if os.path.exists('../.flaskenv'):
#         print('Importing environment from .flaskenv...')
#         for line in open('../.flaskenv'):
#             var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]


if __name__ == '__main__':
    manager.run()
    print(os.getenv('APPID'))
