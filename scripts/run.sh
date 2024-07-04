#!/bin/sh

set -e

mkdir -p /vol/web/static
mkdir -p /vol/web/media
mkdir -p /vol/static
mkdir -p /app/static
mkdir -p /app/vol

chown -R django-user:django-user /vol/web/static /vol/web/media /app/static /vol/static /app/vol /app/media
chmod -R 755 /vol/web/static /vol/web/media /app/static /vol/static /app/vol /app/media

python manage.py wait_for_db
python manage.py collectstatic --noinput

python manage.py migrate

echo "Przed uruchomieniem uWSGI"
ls -la /vol/web/static
ls -la /vol/web/media
ls -la /vol/static

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi