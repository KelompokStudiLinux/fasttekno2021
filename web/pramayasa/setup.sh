#!/bin/bash

NAME="web_pramayasa"
PORT="3001"
PHP_INI_DIR="/usr/local/etc/php"

env PORT=$PORT docker-compose up -d --build --force-recreate
docker-compose exec php cp "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
