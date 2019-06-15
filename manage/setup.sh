#!/bin/bash

# Configures the container, including building the image, creating the container,
# installing extra deps, collecting static files, migrating the DB, etc.

LOCAL_DIR=".local/simple"
CONFIG_FILE="$LOCAL_DIR/config.env"
DB_FILE="$LOCAL_DIR/db.sqlite3"
CONFIG_TEMPLATE_FILE="setup/simple/config.template.env"
DC_FILE="setup/simple/docker-compose.yml"
DC="docker-compose -f $DC_FILE"

set -eu # Exit on error and undefined var is error

mkdir -p $LOCAL_DIR

# Add config file and exit if missing
if [[ ! -e $CONFIG_FILE ]]; then
    echo "Creating new config file ..."
    cp $CONFIG_TEMPLATE_FILE $CONFIG_FILE

    echo
    echo "ATTENTION!"
    echo "A new config file has been created: $CONFIG_FILE"
    echo "Please configure it and then re-run this script."
    exit 0
fi

# Create DB file (so Docker doesn't make it a directory)
if [[ ! -e $DB_FILE ]]; then
    echo "Creating DB file ..."
    touch $DB_FILE
fi

echo
echo "Removing any previous Docker Compose setup ..."
$DC down

echo
echo "Building image ..."
$DC build app

echo
echo "Creating containers ..."
$DC up --no-start

echo
manage/update.sh
