#!/bin/bash

DEV_SETTINGS_FILE="dev-setup/docker-simple/env.original"
SETTINGS_FILE="dev-setup/docker-simple/env"
DB_FILE="db.sqlite"
DC_FILE="dev-setup/docker-simple/docker-compose.yml"
DC="docker-compose -f $DC_FILE"
DC_MANAGE="$DC run app python manage.py"

set -eu # Exit on error and undefined var is error

# Add settings file
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "Adding sample settings file ..."
    mkdir -p $(dirname $SETTINGS_FILE)
    cp $DEV_SETTINGS_FILE $SETTINGS_FILE
fi

# Add DB file
if [[ ! -e $DB_FILE ]]; then
    echo "Adding DB file ..."
    touch $DB_FILE
fi

echo
echo "Removing previous instances ..."
$DC down

echo
echo "Building ..."
$DC build app

echo
echo "Creating containers ..."
$DC up --no-start

echo
echo "Installing dependencies ..."
$DC run --no-deps app pip3 install --quiet -r requirements/development.txt

echo
echo "Collecting static files ..."
$DC_MANAGE collectstatic --noinput --clear | egrep -v "^Deleting" || true

echo
echo "Stopping ..."
$DC stop
