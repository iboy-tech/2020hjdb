FROM python:3.6-alpine

LABEL author="iBoy<547142436@qq.com>" version="1.0" description="CTGU SWZL"

WORKDIR /www/wwwroot/ctguswzl.cn

COPY requirements.txt \
	 boot.sh \
	 celery.sh \
	 . /

RUN echo "https://mirrors.aliyun.com/alpine/v3.12/main/" > /etc/apk/repositories \
    &&  apk --update  add --no-cache --virtual build-dependencies g++ gcc  libxslt-dev python-dev zlib-dev python3-dev openssl-dev \
    &&  apk add jpeg-dev mysql-dev \
    &&  pip config set global.index-url https://mirrors.aliyun.com/simple \
    &&  pip install  --upgrade pip \
    &&  pip install -r requirements.txt \
    &&  apk del build-dependencies
    
ENV C_FORCE_ROOT True

EXPOSE 8888
