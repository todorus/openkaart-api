# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y git python python-dev python-distribute python-pip libpq-dev

# Install Python requirements
COPY app/regions/.docker/requirements.txt /deployment/requirements.txt
RUN pip install -r /deployment/requirements.txt
COPY app/regions/.docker/test-requirements.txt /deployment/test-requirements.txt
RUN pip install -r /deployment/test-requirements.txt

# Install tests
COPY app/lib /frame/app/lib
RUN touch /frame/app/__init__.py
COPY app/regions/tests /frame/tests
COPY test_lib /frame/tools

# Start tests
WORKDIR /frame
CMD nose2
