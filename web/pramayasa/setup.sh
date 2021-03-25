#!/bin/env bash

PHP_INI_DIR="/usr/local/etc/php"

docker-compose up -d --build --force-recreate
docker-compose exec php cp "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
