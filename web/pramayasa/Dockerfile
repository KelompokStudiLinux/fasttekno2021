FROM php:fpm-alpine

COPY flag.txt /flag.txt

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

RUN rm -rf /tmp/*
