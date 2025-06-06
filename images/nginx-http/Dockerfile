ARG NGINX_TAG=1.25.5-alpine-slim

FROM nginx:${NGINX_TAG}

USER root

RUN apk update && \
    mkdir -p /nginx/files && \
    cd /nginx/files && \
    chmod  775 /nginx/files

WORKDIR /nginx/files
COPY nginx.conf /etc/nginx
COPY test.txt /nginx/files
