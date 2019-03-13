#!/bin/bash

set -eu # Exit on error and undefined var is error

MANAGE="python manage.py"

manage/setup-base.sh
# Activate venv and deactivate on exit
machine="$(uname -s)"
case "${machine}" in
    Linux*) source .venv/bin/activate;;
    MINGW*) source .venv/Scripts/activate;;
esac

export DJANGO_SETTINGS_MODULE=fearlessFred.settings.local

#source .venv/bin/activate
trap deactivate EXIT

# Install requirements inside venv, and check for outdated packages
echo "Installing requirements ..."
pip install pip-tools
pip-compile requirements/development.in
pip install --upgrade -r requirements/development.txt
#pip-review

# Collect static files
echo "Collecting static files ..."
$MANAGE collectstatic --noinput --clear

# Run migration, but skip initial if matching table names already exist
echo "Running migration ..."
$MANAGE migrate --fake-initial

# Add superuser
echo "Adding superuser ..."
echo "Press CTRL+C to cancel"
$MANAGE createsuperuser
