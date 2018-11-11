#!/bin/sh

./up_backend.sh

if [ -z "$1" ];
then
    docker-compose -f services.yml up -d --build
    for service_name in `docker-compose -f services.yml ps --services`
    do
        echo "--- Testing \033[1;32m$service_name ---\033[0m"
        docker-compose -f services.yml exec $service_name runtests
        if [ $? != 0 ];
        then
            exit
        fi
    done
else
    for service_name in `docker-compose -f services.yml ps --services`
    do
        if [ $1 = $service_name ];
        then
            echo "--- Testing \033[1;32m$service_name ---\033[0m"
            docker-compose -f services.yml up -d --build $service_name
            docker-compose -f services.yml exec $service_name runtests
            if [ $? != 0 ];
            then
                exit
            fi
        fi
    done
fi