#!/bin/env bash

export $(grep -v '^#' .env | xargs)

docker-compose up -d --build --force-recreate
cat user.sql | docker-compose exec -i mysql mysql -u root -p a2FzZGoxMjk4N2R5NzhuZHNpamZoamhld2lmdTg ${APP_NAME}

echo "Setup ${APP_NAME} on port ${PORT}"
