#!/bin/sh

set -e

# тут вызывать код для миграции
python /var/app/manage.py makemigrations
python /var/app/manage.py migrate

# код для тестов
# python3 /app/manage.py test excelMaster
exec $@
