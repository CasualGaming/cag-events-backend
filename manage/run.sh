#!/bin/bash

# Runs the Django dev server in the container.

LOCAL_DIR=".local/simple"
CONFIG_FILE="$LOCAL_DIR/config.env"
DB_FILE="$LOCAL_DIR/db.sqlite3"
DC_FILE="setup/simple/docker-compose.yml"
DC="docker-compose -f $DC_FILE"

# Check if config file exists
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

# Check if DB file exists
if [[ ! -e $DB_FILE ]]; then
    echo "DB file not found: $DB_FILE" 1>&2
    exit -1
fi

$DC up --no-recreate
