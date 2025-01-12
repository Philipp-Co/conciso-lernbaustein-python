#!/bin/sh

python /labyrinth_server/manage.py makemigrations
python /labyrinth_server/manage.py migrate
cd labyrinth_server && \
    gunicorn labyrinth_server.wsgi:application \
        --name server \
        --bind :8000 \
        --timeout=300 \
        --workers=4
