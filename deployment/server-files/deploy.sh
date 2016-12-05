#!/bin/bash
docker-compose -f certbot.yaml pull
docker-compose -f certbot.yaml up --force-recreate

docker-compose -f production.yaml pull
docker-compose -f production.yaml up --force-recreate -d
