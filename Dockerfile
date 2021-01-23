FROM python:3.6-alpine

LABEL author="iBoy<547142436@qq.com>" version="1.0" description="ctguswzl.cn"

ENV C_FORCE_ROOT True

WORKDIR /www/wwwroot/ctguswzl.cn

COPY requirements.txt docker-entrypoint.sh ./

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    &&  chmod +x docker-entrypoint.sh\
    &&  apk --update  add --no-cache --virtual build-dependencies g++ gcc  libxslt-dev  zlib-dev python3-dev openssl-dev \
    &&  apk add jpeg-dev mysql-dev freetype-dev \
    &&  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    &&  pip install -U pip \
    &&  pip install --no-cache-dir -r requirements.txt \
    &&  apk del build-dependencies \
    &&  rm -rf /var/cache/apk/* \
    &&  rm -rf /root/.cache \
    &&  rm -rf /tmp/*
    
EXPOSE 8888

ENTRYPOINT [ "./docker-entrypoint.sh" ]