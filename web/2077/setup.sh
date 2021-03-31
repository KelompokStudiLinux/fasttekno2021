#!/bin/env bash

export $(grep -v '^#' .env | xargs)

if [[ ${APP_NAME} == 'production' ]]; then
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate
else
	docker-compose up -d --build --force-recreate
fi

echo "Setup ${APP_NAME} on port ${PORT} for ${APP_ENV}"
