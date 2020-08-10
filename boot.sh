#!/bin/sh
gunicorn -c config.py run:app

celery worker -A run.celery --loglevel=info  --logfile=logs/celery/worker.log --pool=eventlet  -E
