# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y git python python-dev python-distribute python-pip libpq-dev

# Install Python requirements
COPY regions/.docker/requirements.txt /deployment/requirements.txt
RUN pip install -r /deployment/requirements.txt

# Copy app code
COPY    regions/code   /frame/app
COPY    lib            /frame/app/lib 
RUN mv  /frame/app/start_server.py /frame

# Start server
WORKDIR /frame
CMD python start_server.py
