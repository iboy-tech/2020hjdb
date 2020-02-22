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
from __future__ import absolute_import

import os
from datetime import datetime

# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

from dotenv import load_dotenv, find_dotenv
from flask_login import current_user
from flask_socketio import emit, SocketIO

from app import create_app, create_celery, redis_client


async_mode = 'eventlet'
load_dotenv(find_dotenv('.env'))
load_dotenv(find_dotenv('.flaskenv'))

app = create_app(os.getenv('FlASK_ENV') or 'development')

app.config['SECRET_KEY'] = 'adsdad&*^%^$%#afcsefvdzcssef1212'

socketio = SocketIO(app=app, async_mode=async_mode, cors_allowed_origins="*")
celery = create_celery(app)

res = None


@socketio.on('server')
def server():
    print('server用户连接了', datetime.now())
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)
    key = str(current_user.id) + '-pusher-post-data'
    redis_client.set(key, 'null')  # 把数据存入redis
    redis_client.expire(key, 180)
    while True:
        op = redis_client.get(key)
        print('我是redis中的数据类型', op, type(op))
        if op is not None:
            op = op.decode()
            print('当前用户姓名', current_user.real_name)
            # op = OpenID.query.filter_by(user_id=current_user.id).first()
            # db.session.remove()
            if op != 'null':
                data = eval(op)
                print('data的数据类型', type(data))
                print('我是查询的OP', op)
                print('循环查询OpenID', datetime.now(), op)
                res = {
                    'success': 'true',
                    'data': {'msg': '绑定成功！即将回到主页',
                             'head': data['userHeadImg'].replace('http', 'https')
                             }
                }
                print('background_thread我是查询结果', res)
                emit('server', res)
                # redis_client.delete(key)
                break;
            else:
                res = {
                    'success': 'false',
                    'data': {'msg': '二维码还有 ' + str(redis_client.ttl(key)) + 's 失效',
                             'bg': '1'
                             }
                }
                print('background_thread我是查询结果', res)
                socketio.emit('server', res)
        else:
            res = {
                'success': 'false',
                'data': {'msg': '二维码已过期，请刷新页面重新绑定', 'bg': '0'}
            }
            print('background_thread我是查询结果', res)
            socketio.emit('server', res)
            break;
        socketio.sleep(3)


@socketio.on('connect')
def connect():
    # print('服务端的connect函数',datetime.now())
    emit('connect', {'msg': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    print('server用户连接了', datetime.now())
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)


if __name__ == '__main__':
    """
    启动 Web server:
    https://www.jianshu.com/p/cdee367b77d3
    python run.py  --host=0.0.0.0 --port=8888 --no-reload
    启动 Celery worker:
    celery worker -A app.celery -l  INFO  -n ctgu@celeryd -E --loglevel=info  
    celery worker -A app.utils.mail_sender.celery -l  INFO  -n ctgu@celeryd -E --loglevel=info 
    celery worker -A app.utils.tinify_tool.celery -l  INFO  
    celery worker -A app.views.user_view.celery -l  INFO 
    celery flower --address=127.0.0.1 --port=55555
   celery worker -A app.extensions.celery -l  INFO  
   celery worker -A run.celery -l  DEBUG -E -P eventlet
   gevent
   celery worker -A run.celery -l  beat
   celery worker -A manager.celery -l  DEBUG -E -P eventlet
   celery worker -A run.celery --loglevel=info --pool=eventlet  -E
   celery beat -A run.celery -l info
   celery worker -A tasks.celery -l  INFO -E -P eventlet
   celery -A webapp.main.tasks worker -l info -f celery.log --pool=eventlet

    """
    socketio.run(app=app, host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
