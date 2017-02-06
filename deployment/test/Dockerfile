# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y git python python-dev python-distribute python-pip libpq-dev
# Install BCrypt dependencies
RUN apt-get install -y build-essential libffi-dev
# Install Shapely dependencies
RUN apt-get install -y libgeos-dev

# Install Python requirements
COPY deployment/api/requirements.txt /deployment/requirements.txt
RUN pip install -r /deployment/requirements.txt
COPY deployment/test/requirements.txt /deployment/test-requirements.txt
RUN pip install -r /deployment/test-requirements.txt

# Install tests
COPY app /frame/app
COPY tests /frame/tests

# Start tests
WORKDIR /frame
CMD nose2
