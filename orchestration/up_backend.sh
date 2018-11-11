#!/bin/sh

docker build -t esblng/base/python ../base/python
docker build -t esblng/base/mysql ../base/mysql
docker-compose -f backend.yml up -d