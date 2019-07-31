#!/bin/bash

LOCAL_DIR=".local/venv"
CONFIG_FILE="$LOCAL_DIR/config.env"
LOG_DIR="$LOCAL_DIR/log"
CONFIG_TEMPLATE_FILE="setup/venv/config.template.env"
MANAGE="python src/manage.py"

# Used by app
export CONFIG_FILE

set -eu

# Activate venv and deactivate on exit
# Allow undefined vars
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate.sh"
trap deactivate EXIT
set -u

mkdir -p $LOCAL_DIR
mkdir -p $LOG_DIR

echo "Installing requirements ..."
pip install -r requirements/development.txt

# Add config file and exit if missing
if [[ ! -e $CONFIG_FILE ]]; then
    echo
    echo "Creating new config file ..."
    cp $CONFIG_TEMPLATE_FILE $CONFIG_FILE

    echo
    echo "ATTENTION!"
    echo "A new config file has been created: $CONFIG_FILE"
    echo "Please configure it and then re-run this script."
    exit 0
fi

echo
echo "Collecting static files ..."
# Ignore admin app, use theme instead
$MANAGE collectstatic -i admin --noinput --clear

echo
echo "Running migration ..."
$MANAGE migrate --fake-initial
