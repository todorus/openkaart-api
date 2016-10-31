# get the local directory to convert relative paths to absolute ones
LOCAL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# build the images needed
docker-compose -f $LOCAL_DIR/.docker/docker-compose-production.yaml build

# push it to the repository
docker-compose -f $LOCAL_DIR/.docker/docker-compose-production.yaml push

#TODO start rollout
