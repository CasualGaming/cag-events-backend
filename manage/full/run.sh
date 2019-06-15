#!/bin/bash

LOCAL_DIR=".local/full"
CONFIG_FILE="$LOCAL_DIR/config.env"
DC_FILE="setup/full/docker-compose.yml"
DC="docker-compose -f $DC_FILE"

# Check if config exist
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $CONFIG_FILE" 1>&2
    exit -1
fi

$DC up
$DC down
