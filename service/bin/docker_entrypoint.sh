#!/bin/sh

set -e

# Call the code for migration here
python /var/app/manage.py makemigrations
python /var/app/manage.py migrate

# call tests
python /var/app/manage.py test film_api
exec $@
