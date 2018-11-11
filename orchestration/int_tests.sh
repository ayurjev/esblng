#!/bin/sh

docker-compose -f orchestration.yml exec orchestration runtests $1