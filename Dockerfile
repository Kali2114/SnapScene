FROM python:3.12.3-alpine3.19
LABEL maintainer="snapscene.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /app/static && \
    mkdir -p /app/media && \
    chown -R django-user:django-user /app/static && \
    chown -R django-user:django-user /app/media && \
    chmod -R 755 /app/static && \
    chmod -R 755 /app/media && \
    chmod +x /scripts/run.sh

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["sh", "/scripts/run.sh"]