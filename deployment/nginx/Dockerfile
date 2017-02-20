FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY deployment/nginx/api.conf /etc/nginx/conf.d/api.conf
COPY docs/html /var/www/docs

VOLUME /var/www
VOLUME /certificates
