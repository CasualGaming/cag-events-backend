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

# Collect static files
echo "Collecting static files ..."
$MANAGE collectstatic --no-input --clear | egrep -v "^Deleting" || true

# Run migration, but skip initial if matching table names already exist
echo "Running migration ..."
$MANAGE migrate --fake-initial --no-input

# Check if new migrations can be made
$MANAGE makemigrations --dry-run --check --no-input

# Validate
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR

# Run Django tests
$MANAGE test --no-input

# Run flake8 static code analysis
# Uses settings from .flake8
flake8

echo
echo "Success!"
