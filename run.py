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

from dotenv import load_dotenv, find_dotenv
from flask import request
from flask_cors import CORS
from flask_login import current_user
from flask_socketio import emit, SocketIO

from app import create_app, create_celery, redis_client, PostConfig, logger
from app.utils.wxpusher import WxPusher

# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

async_mode = 'eventlet'
load_dotenv(find_dotenv('.env'), override=True)
load_dotenv(find_dotenv('.flaskenv'), override=True)

# logger.info('当前环境' + os.getenv('FlASK_ENV'))
# logger.info('MAIL_USERNAME', os.getenv('MAIL_USERNAME'))
# logger.info('MAIL_PASSWORD', os.getenv('MAIL_PASSWORD'))
# logger.info('SECRET_KEY', os.getenv('SECRET_KEY'))
# logger.info('PATH_OF_IMAGES_DIR', os.getenv('PATH_OF_IMAGES_DIR'))
# logger.info('MAIL_SENDGRID_API_KEY', os.getenv('MAIL_SENDGRID_API_KEY'))
logger.info('站点地址：%s' % os.getenv('SITE_URL'))
# print('站点地址：'+os.getenv('SITE_URL'))

app = create_app(os.getenv('FlASK_ENV') or 'production')
CORS(app, supports_credentials=True, resources=r'/*')  # 允许所有域名跨域

socketio = SocketIO(app=app, async_mode=async_mode, cors_allowed_origins="*", manage_session=False)
celery = create_celery(app)

res = None


@socketio.on('server')
def server(data):
    msg = data.get("msg")
    if msg == 'login':
        client_id = request.sid
        key = PostConfig.PUSHER_REDIS_PREFIX+client_id
        redis_client.set(key, 'null')  # 把数据存入redis
        redis_client.expire(key, 180)
    elif msg == 'wx':
        key = PostConfig.PUSHER_REDIS_PREFIX+str(current_user.id)
        redis_client.set(key, 'null')  # 把数据存入redis
        redis_client.expire(key, 180)
    else:
        res = {
            'success': 'false',
            'data': {'msg': '参数错误'},
        }
        emit('server', res)
    while True:
        op = redis_client.get(key)
        if op is not None:
            op = op.decode()
            # logger.info('当前用户姓名', current_user.real_name)
            # db.session.remove()
            if op != 'null':
                if op == "guest":  # 找回密码的扫码的不是系统用户
                    res = {
                        'success': 'false',
                        'data': {'msg': '此微信尚未绑定',
                                 'bg': '0'
                                 }
                    }
                    redis_client.delete(key)  # 删除key
                    emit('server', res)
                    break
                if op == "exist":
                    res = {
                        'success': 'false',
                        'data': {'msg': '此微信已被其他用户绑定',
                                 'bg': '0'
                                 }
                    }
                    redis_client.delete(key)  # 删除key
                    emit('server', res)
                    break

                data = eval(op)
                res = {
                    'success': 'true',
                    'data': {'msg': '绑定成功！即将回到主页',
                             'head': data['userHeadImg'].replace('http', 'https')
                             },
                    'token': request.sid
                }
                emit('server', res)
                break
            else:
                res = {
                    'success': 'false',
                    'data': {'msg': '二维码还有 ' + str(redis_client.ttl(key)) + 's 失效',
                             'bg': '1'
                             }
                }
                print(res)
                socketio.emit('server', res)
        else:
            res = {
                'success': 'false',
                'data': {'msg': '二维码已失效，请重新获取', 'bg': '0'}
            }
            socketio.emit('server', res)
            break;
        socketio.sleep(5)


@socketio.on('qrcode')
def get_qrcode():
    client_id = request.sid
    data = (WxPusher.create_qrcode(extra=client_id, valid_time=180))
    if data['success']:
        data = data['data']
        res = {
            'success': 'true',
            'url': data['url'],
        }
        # res =
        socketio.emit("qrcode", res)
    else:
        res = {
            'success': 'false',
        }
        socketio.emit("qrcode", res)


@socketio.on('connect')
def connect():
    pass


if __name__ == '__main__':
    """
    启动 Web server:
    https://www.jianshu.com/p/cdee367b77d3
    python run.py  --host=0.0.0.0 --port=8888 --no-reload
    启动 Celery worker:
    sudo apt-get --purge remove gunicorn
    source venv/bin/activate && nohup gunicorn -c config.py run:app   &> log.log
   celery multi start  celery worker -A run.celery -l  DEBUG -E -P eventlet
   celery  -A run.celery  beat
      gunicorn -c config.py run:app  --daemon
    celery worker -A run.celery -l  DEBUG -E -P eventlet -Q default 
    celery worker -A run.celery -l  DEBUG -E -P solo -Q default
   ps auxww | grep 'celery worker'
   pkill -f "celery"
   celery worker
   pkill -f " celery worker"
   celery multi start celery worker -B -A run.celery 
   celery worker -A run.celery --loglevel=debug  --logfile=worker.log --pool=eventlet  -E
   ln -s /usr/local/python3/bin/celery /usr/bin/celery
  https://blog.wpjam.com/m/weixin-emotions/ 
  http://www.oicqzone.com/tool/emoji/ #表情地址
  http://www.oicqzone.com/qqjiqiao/2014123020663.html
   ln -s  /usr/local/bin/celery /usr/bin/celery
   export C_FORCE_ROOT="True"
   pkill -9 -f 'celery worker'

   source venv/bin/activate && gunicorn -c config.py run:app 
   set ff=unix
   celery worker -E -l INFO -A run.celery -n send_mail -Q send_mail -P eventlet
    celery worker -E -l INFO -A run.celery -n img_compress -Q img_compress -P eventlet
   celery beat -A run.celery -l INFO -f logs/schedule_tasks.log --detach

 celery worker -E -l INFO -n worker_compute -Q for_task_compute
celery -A 项目名 worker -loglevel=info ： 前台启动命令
celery multi start w1 -A 项目名 -l info ： 后台启动命令
celery multi restart img_compress -A run.celery -l info ： 后台重启命令
celery multi stop w1 -A 项目名 -l info ： 后台停止命令
   重启celery multi restart 1 --pidfile=%n.pid


    """
    socketio.run(app=app, host='0.0.0.0', port='8888')
