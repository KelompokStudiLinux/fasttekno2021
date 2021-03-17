#!/bin/bash

NAME="web_lolot"

[[ -n `docker ps -aqf name=$NAME` ]] && docker stop $NAME
docker build . -t $NAME
docker run -tidp 3000:3000 --rm --name $NAME $NAME
