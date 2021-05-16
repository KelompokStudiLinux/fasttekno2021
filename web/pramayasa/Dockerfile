FROM php:apache

COPY flag.txt /flag.txt
COPY readflag.c /readflag.c
COPY readflag /readflag
COPY public /var/www/html

RUN chmod 400 /flag.txt
RUN chmod u+s /readflag

# clean up
RUN rm /tmp/* -rf
