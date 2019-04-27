#!/bin/bash

SETTINGS_FILE="env"
MANAGE="python manage.py"

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

set -eu # Exit on error and undefined var is error

# Check if settings exist
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "App settings not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

echo "Making migrations ..."
$MANAGE makemigrations
