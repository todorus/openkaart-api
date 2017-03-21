# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

# Install Certbot
RUN apt-get install -y letsencrypt

VOLUME /webroot
VOLUME /etc/letsencrypt

CMD letsencrypt certonly \
    --webroot -w /webroot \
    -d api.waarregelikzorg.nl -d staging.waarregelikzorg.nl \
    --renew-by-default \
    --text --non-interactive \
    --agree-tos --email todorus@todorus.com
