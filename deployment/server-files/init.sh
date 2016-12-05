#!/bin/bash
docker-compose -f certbot-init.yaml pull
docker-compose -f certbot-init.yaml up --force-recreate
