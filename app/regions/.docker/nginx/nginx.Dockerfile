FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY api.conf /etc/nginx/conf.d/api.conf
