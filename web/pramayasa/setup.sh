#!/bin/env bash

export $(grep -v '^#' .env | xargs)

docker build . -t pramayasa
[[ `docker ps -qf name=${APP_NAME}` ]] && docker stop ${APP_NAME}
docker run -tid --rm --name ${APP_NAME} -p ${PORT}:80 pramayasa

echo "Setup ${APP_NAME} on port ${PORT}"
