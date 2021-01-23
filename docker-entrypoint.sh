#!/bin/sh

celery beat -A run.celery -l INFO -f logs/celery/schedule_tasks.log --detach --pidfile=/tmp/schedule_tasks.pid  --pidfile=/tmp/celerybeat-schedule

celery multi start w1 -A run.celery -n img_compress -l  ERROR -E -P eventlet -Q img_compress --logfile=logs/celery/img_compress.log --pidfile=/tmp/img_compress.pid

celery multi start w2 -A run.celery -n send_mail -l  ERROR -E -P eventlet -Q send_mail --logfile=logs/celery/send_mail.log --pidfile=/tmp/send_mail.pid

celery multi start w3 -A run.celery -n default -l   ERROR -E -P eventlet -Q default --logfile=logs/celery/default.log --pidfile=/tmp/default.pid

gunicorn -c config.py run:app
















