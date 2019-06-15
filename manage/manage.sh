#!/bin/bash

# Runs Django manage.py with the specified command in the container.

LOCAL_DIR=".local/simple"
CONFIG_FILE="$LOCAL_DIR/config.env"

# Check if config file exist
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

manage/cmd.sh python3 src/manage.py $@
