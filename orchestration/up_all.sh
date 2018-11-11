#!/bin/sh

docker-compose -f services.yml up -d --build
sleep 5
docker-compose -f orchestration.yml up -d --build
docker-compose -f orchestration.yml exec orchestration python3 tests/utils.py