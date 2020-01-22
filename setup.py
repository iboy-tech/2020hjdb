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
from app import creat_app, db
from app.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

print('导入环境变量')
print(os.path.realpath)
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
    if len(var) == 2:
        os.environ[var[0]] = var[1]
if os.path.exists('.flaskenv'):
    print('Importing environment from .flaskenv...')
    for line in open('.flaskenv'):
        var = line.strip().split('=')
    if len(var) == 2:
        os.environ[var[0]] = var[1]

print('当前的环境变量配置',os.getenv('FLASK_CONFIG'))

app = creat_app(os.getenv('FlASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


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
    # init_env()
    manager.run()
