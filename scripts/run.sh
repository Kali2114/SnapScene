#!/bin/sh

set -e

mkdir -p /app/static
mkdir -p /vol/web/static
mkdir -p /vol/web/media
mkdir -p /vol/static

# Ustawienie uprawnień jako root
chown -R django-user:django-user /app/static /vol/web/static /vol/web/media /vol/static
chmod -R 755 /vol/web/static /vol/web/media /vol/static

python manage.py wait_for_db
python manage.py collectstatic --noinput

chown -R django-user:django-user /vol/web/static /vol/web/media
chmod -R 755 /vol/web/static /vol/web/media

cp -r /app/static/* /vol/web/static/

python manage.py migrate

echo "Przed uruchomieniem uWSGI"
ls -la /vol/web/static
ls -la /vol/web/media
ls -la /vol/static

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi