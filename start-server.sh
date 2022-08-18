#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd banking_battle; python manage.py createsuperuser --no-input)
fi
echo
echo "CREATED SUPERUSER"
echo
(cd banking_battle; gunicorn banking_battle.wsgi --bind 0.0.0.0:8010 --workers 3)