#!/bin/bash

LOCAL_DIR=".local/venv"
CONFIG_FILE="$LOCAL_DIR/config.env"
LOG_DIR="$LOCAL_DIR/log"
CONFIG_TEMPLATE_FILE="setup/venv/config.template.env"
MANAGE="python src/manage.py"

export CONFIG_FILE

set -e # No -u because of source below

# Activate venv and deactivate on exit
source "$(dirname "$BASH_SOURCE[0]")/activate.sh"
trap deactivate EXIT

set -eu

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

# Add other dirs and files
[[ ! -e $LOG_DIR ]] && mkdir -p $LOG_DIR

echo
echo "Installing requirements ..."
pip install --quiet -r requirements/development.txt

echo
echo "Collecting static files ..."
# Ignore admin app, use theme instead
$MANAGE collectstatic -i admin --noinput --clear | egrep -v "^Deleting" || true

echo
echo "Running migration ..."
$MANAGE migrate --fake-initial
