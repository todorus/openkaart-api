# make sure we use the latest build
docker build . -f development.Dockerfile -t todorus/openkaart-resources-regions:development

# get the local directory to convert relative paths to absolute ones
LOCAL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# run the development container
docker run -it -v $LOCAL_DIR:/app todorus/openkaart-resources-regions:development /bin/bash
