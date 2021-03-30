#!/bin/env bash

export $(grep -v '^#' .env | xargs)

[[ -n `docker ps -aqf name=$APP_NAME` ]] && docker stop $APP_NAME && docker container rm $APP_NAME
docker build . -t $APP_NAME
docker run -tidp $PORT:3000 --restart always --name $APP_NAME $APP_NAME

echo "Setup ${APP_NAME} on port ${PORT}"
