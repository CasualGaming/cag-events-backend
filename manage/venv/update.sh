#!/bin/bash

LOCAL_DIR=".local/venv"
CONFIG_FILE="$LOCAL_DIR/config.env"
LOG_DIR="$LOCAL_DIR/log"
MANAGE="python src/manage.py"

export CONFIG_FILE

set -e # No -u because of source below

# Activate venv and deactivate on exit
source manage/venv/activate.sh
trap deactivate EXIT

set -eu

# Check if config file exists
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

# Add other dirs and files
[[ ! -e $LOG_DIR ]] && mkdir -p $LOG_DIR

echo
echo "Running migration ..."
$MANAGE migrate --fake-initial
