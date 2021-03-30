#!/bin/env bash

export $(grep -v '^#' .env | xargs)

docker-compose up -d --build --force-recreate
# docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate
# cat user.sql | docker-compose exec -i mysql mysql -uroot -pa2FzZGoxMjk4N2R5NzhuZHNpamZoamhld2lmdTg ${APP_NAME}
docker-compose exec php rm /bin/nc /bin/perl

echo "Setup ${APP_NAME} on port ${PORT}"
