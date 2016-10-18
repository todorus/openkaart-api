# get the local directory to convert relative paths to absolute ones
LOCAL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# make sure we use the latest builds
docker-compose -f $LOCAL_DIR/.docker/docker-compose-production.yaml build
docker-compose -f $LOCAL_DIR/.docker/docker-compose-test.yaml build

# run the production container
docker-compose -f $LOCAL_DIR/.docker/docker-compose-production.yaml up

# give the databse time to start
sleep 10s

# run the tests
docker-compose -f $LOCAL_DIR/.docker/docker-compose-test.yaml up
