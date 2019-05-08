#!/bin/bash

# Configures the container, including building the image, creating the container,
# installing extra deps, collecting static files, migrating the DB, etc.

DEV_SETTINGS_FILE="setup/docker-simple/env.original"
SETTINGS_FILE="setup/docker-simple/env"
DB_FILE="db.sqlite3"
DC_FILE="setup/docker-simple/docker-compose.yml"
DC="docker-compose -f $DC_FILE"
DC_MANAGE="$DC run app python3 src/manage.py"
# Set to true if run by CI
CI=$CI

set -eu # Exit on error and undefined var is error

# Add settings file
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "Adding sample settings file ..."
    mkdir -p $(dirname $SETTINGS_FILE)
    cp $DEV_SETTINGS_FILE $SETTINGS_FILE
fi

# Add DB file (so Docker doesn't make it a directory)
if [[ ! -e $DB_FILE ]]; then
    echo "Adding DB file ..."
    touch $DB_FILE
fi

echo
echo "Removing previous setup ..."
$DC down

echo
echo "Building image ..."
$DC build app

echo
echo "Creating containers ..."
$DC up --no-start

echo
echo "Installing extra dependencies ..."
if [[ $CI != "true" ]]; then
    $DC run --no-deps app pip3 install --quiet -r requirements/development.txt
else
    $DC run --no-deps app pip3 install -r requirements/development.txt
fi

echo
echo "Configuring app ..."
$DC_MANAGE collectstatic --noinput --clear | egrep -v "^Deleting" || true
$DC_MANAGE migrate --fake-initial

echo
echo "Stopping ..."
$DC stop
