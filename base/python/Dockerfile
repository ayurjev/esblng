FROM python:alpine3.6

#https://gitlab.com/gitlab-org/gitlab-runner/issues/1682
ENV PYTHONDONTWRITEBYTECODE 1
#https://oncletom.io/2015/docker-encoding/
ENV LANG=C.UTF-8

RUN apk add --no-cache bash openssl openssl-dev

RUN pip3 install --cache-dir /tmp/mysql http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.1.7.tar.gz \
      && rm -rf /tmp/mysql

RUN set -ex \
      && apk add --no-cache --virtual .build-deps \
        git \
        gcc \
        libc-dev \
        linux-headers \
      \
      && pip3 install uwsgi -I --no-cache-dir \
      && pip3 install --no-cache-dir requests redis clickhouse-driver python-dateutil \
      && pip3 install --no-cache-dir bottle pika==0.11.2 \
      && pip3 install --no-cache-dir git+https://git@github.com/ayurjev/mapex.git \
      && pip3 install --no-cache-dir git+https://git@github.com/ayurjev/envi.git \
      \
      && apk del .build-deps

COPY migrate.py /usr/local/lib/python3.6/site-packages/migrate.py

COPY uwsgi.ini /uwsgi.ini
COPY start.sh /start.sh
RUN chmod a+x /start.sh
COPY start_daemon.sh /start_daemon.sh
RUN chmod a+x /start_daemon.sh

RUN echo '#!/bin/bash' >> /usr/local/bin/runtests && \
    echo 'python3 -m unittest discover /var/www/' >> /usr/local/bin/runtests && \
    chmod a+x /usr/local/bin/runtests

EXPOSE 80

WORKDIR /var/www/
CMD ["/start.sh"]
