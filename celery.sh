#!/bin/sh

celery beat -A run.celery -l INFO -f logs/celery/schedule_tasks.log --detach --pidfile=logs/celery/pid/schedule_tasks.pid  -s logs/celery/pid/celerybeat-schedule 

celery multi start celery worker -A run.celery  -n img_compress -l  DEBUG -E -P eventlet -Q img_compress --logfile=logs/celery/img_compress.log --pidfile=logs/celery/pid/img_compress.pid

celery multi start celery worker -A run.celery -l   DEBUG -E -P eventlet -Q default --logfile=logs/celery/default.log --pidfile=logs/celery/pid/default.pid

celery multi start celery worker -A run.celery -n send_wechat_msg -l  DEBUG -E -P eventlet -Q send_wechat_msg --logfile=logs/celery/send_wechat_msg.log  --pidfile=logs/celery/pid/send_wechat_msg.pid

celery multi start celery worker -A run.celery -n send_qq_group_notice -l  DEBUG -E -P eventlet -Q send_qq_group_notice --logfile=logs/celery/send_qq_group_notice.log  --pidfile=logs/celery/pid/send_qq_group_notice.pid




