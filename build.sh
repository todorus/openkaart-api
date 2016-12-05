# get the local directory to convert relative paths to absolute ones
LOCAL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# build and push the images for the api
docker-compose -f $LOCAL_DIR/deployment/production.yaml build --no-cache
docker-compose -f $LOCAL_DIR/deployment/production.yaml push

# build and push the images for certbot
docker-compose -f $LOCAL_DIR/deployment/certbot.yaml build --no-cache
docker-compose -f $LOCAL_DIR/deployment/certbot.yaml push
