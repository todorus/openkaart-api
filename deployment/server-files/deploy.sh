docker-compose -f production.yaml pull
docker-compose -f production.yaml up --force-recreate -d

sleep 15
docker-compose -f certbot.yaml pull
docker-compose -f certbot.yaml up --force-recreate

#force a restart of nginx
docker-compose -f production.yaml up --force-recreate -d
