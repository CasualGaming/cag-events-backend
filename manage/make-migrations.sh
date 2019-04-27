#!/bin/bash

set -eu # Exit on error and undefined var is error

SETTINGS_FILE="env"
MANAGE="python manage.py"

# Check if settings exist
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "App settings not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

echo "Making migrations ..."
$MANAGE makemigrations
