#!/bin/bash
docker-compose -f production.yaml pull
docker-compose -f production.yaml up --force-recreate -d

docker-compose -f certbot-update.yaml pull
docker-compose -f certbot-update.yaml up --force-recreate
