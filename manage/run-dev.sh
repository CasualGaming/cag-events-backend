#!/bin/bash

set -eu # Exit on error and undefined var is error

MANAGE="python manage.py"

# Check if settings exist
APP_SETTINGS_FILE=core/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "App settings not found: $APP_SETTINGS_FILE" 1>&2
    exit 1
fi

# Activate venv and deactivate on exit
machine="$(uname -s)"
case "${machine}" in
    MINGW*) source .venv/Scripts/activate;;
    *) source .venv/bin/activate;;
esac
trap deactivate EXIT

export DJANGO_SETTINGS_MODULE=core.settings.local

#exec uwsgi --ini uwsgi.ini
${MANAGE} runserver

