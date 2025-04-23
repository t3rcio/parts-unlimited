#!/bin/sh
python /code/app/manage.py migrate --noinput
exec "$@"
