#!/bin/sh

set -e

# тут вызывать код для миграции
python /var/app/manage.py makemigrations
python /var/app/manage.py migrate

# код для тестов
python /var/app/manage.py test film_api
exec $@
