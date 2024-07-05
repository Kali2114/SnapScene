#!/bin/sh

set -e


mkdir -p /app/media
mkdir -p /app/static
chown -R django-user:django-user /app/media /app/static
chmod -R 755 /app/media /app/static

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi