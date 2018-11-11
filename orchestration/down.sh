#!/bin/sh

docker-compose -f orchestration.yml down -v
docker-compose -f services.yml down -v
docker-compose -f backend.yml down -v