#!/bin/bash

export C_FORCE_ROOT="True"
#source venv/bin/activate
#pkill -f "celery"

rm -rf *.pid
rm -rf *.log
celery multi start celery worker -B -A run.celery  DEBUG -E -P eventlet -Q default
celery multi start celery worker -A run.celery -l   DEBUG -E -P eventlet -Q default --logfile=logs/celery/default.log --pidfile=logs/celery/default.pid

celery multi start celery worker -A run.celery -n send_mail -l  DEBUG -E -P eventlet -Q send_mail --logfile=logs/celery/send_mail.log --pidfile=logs/celery/send_mail.pid

celery multi start celery worker -A run.celery  -n img_compress -l  DEBUG -E -P eventlet -Q img_compress --logfile=logs/celery/img_compress.log --pidfile=logs/celery/img_compress.pid

celery multi start celery worker -A run.celery -n send_wechat_msg -l  DEBUG -E -P eventlet -Q send_wechat_msg --logfile=logs/celery/send_wechat_msg.log  --pidfile=logs/celery/send_wechat_msg.pid

celery worker -A app.utils.mail_sender.send_mail -n send_mail -l  DEBUG -E -P eventlet -Q send_mail
celery worker -A  run.celery    -l info -n worker.%h  -E -Q sendmail
celery worker -A  run.celery  -n send_mail -l  DEBUG -E -P eventlet -Q send_mail