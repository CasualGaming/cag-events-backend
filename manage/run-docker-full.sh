#!/bin/bash

SETTINGS_FILE="dev-setup/docker-full/env"
DC_FILE="dev-setup/docker-full/docker-compose.yml"
DC="docker-compose -f $DC_FILE"

# Check if settings exist
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "App settings not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

$DC up
