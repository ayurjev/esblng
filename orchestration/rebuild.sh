#!/bin/sh

docker-compose -f services.yml up -d --build $1
docker-compose -f workers.yml up -d --build $1