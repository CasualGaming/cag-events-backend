#!/bin/bash

# Runs the Django dev server in the container.

LOCAL_DIR=".local/simple"
CONFIG_FILE="$LOCAL_DIR/config.env"
DC_FILE="setup/simple/docker-compose.yml"
DC="docker-compose -f $DC_FILE"

# Check if config file exist
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

$DC up --no-recreate
