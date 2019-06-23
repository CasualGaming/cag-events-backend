#!/bin/bash

# Runs Django manage.py with the specified command in the container.

LOCAL_DIR=".local/simple"
CONFIG_FILE="$LOCAL_DIR/config.env"
DB_FILE="$LOCAL_DIR/db.sqlite3"

# Check if config file exists
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

# Create DB file so Docker doesn't make it a directory
if [[ ! -e $DB_FILE ]]; then
    echo "Creating DB file ..."
    touch $DB_FILE
fi

manage/cmd.sh python3 src/manage.py $@
