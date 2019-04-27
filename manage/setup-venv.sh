#!/bin/bash

DEV_SETTINGS_FILE="dev-setup/venv/env.original"
SETTINGS_FILE="env"
LOG_DIR="log"
MANAGE="python3 manage.py"

set -eu # Exit on error and undefined var is error

# Add settings file
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "Adding sample settings file ..."
    mkdir -p $(dirname $SETTINGS_FILE)
    cp $DEV_SETTINGS_FILE $SETTINGS_FILE
fi

# Add other dirs and files
[[ ! -e $LOG_DIR ]] && mkdir -p $LOG_DIR

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

# Install requirements inside venv, and check for outdated packages
echo
echo "Installing requirements ..."
pip install --quiet -r requirements/development.txt

# Collect static files
echo
echo "Collecting static files ..."
$MANAGE collectstatic --noinput --clear | egrep -v "^Deleting" || true

# Run migration, but skip initial if matching table names already exist
echo
echo "Running migration ..."
$MANAGE migrate --fake-initial

# Add superuser
#echo "Adding superuser ..."
#echo "Press CTRL+C to cancel"
#$MANAGE createsuperuser
