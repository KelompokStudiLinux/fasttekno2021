#!/bin/env bash

export $(grep -v '^#' .env | xargs)

[[ -n `docker ps -aqf name=$APP_NAME` ]] && docker stop $APP_NAME && docker container rm $APP_NAME
docker build . -t $APP_NAME
docker run -tidp $PORT:80 --restart unless-stopped --name $APP_NAME $APP_NAME

echo "Setup ${APP_NAME} on port ${PORT}"
