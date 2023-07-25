#!/bin/bash
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd katplan; python manage.py createsuperuser --no-input)
fi
(cd katplan; gunicorn app.wsgi:application --user www-data --bind 0.0.0.0:8000 --workers 3) &
nginx -g "daemon off;"
