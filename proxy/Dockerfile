FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="snapscene.com"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN mkdir -p /app/static && \
    mkdir -p /app/media && \
    chmod 755 /app/static && \
    chmod 755 /app/media && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod 644 /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /app/static
VOLUME /app/media

USER nginx

CMD ["/run.sh"]