#!/bin/bash

SETTINGS_FILE="env"
MANAGE="python src/manage.py"

set -e # Exit on error

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

set -eu # Exit on error and undefined var is error

# Check if settings exist
if [[ ! -e $SETTINGS_FILE ]]; then
    echo "App settings not found: $SETTINGS_FILE" 1>&2
    exit -1
fi

echo
echo "Collecting static files ..."
$MANAGE collectstatic --no-input --clear | egrep -v "^Deleting" || true

echo
echo "Checking migrations ..."
$MANAGE makemigrations --check --no-input --dry-run
$MANAGE migrate --fake-initial --no-input --plan

echo
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR

echo
echo "Running tests ..."
$MANAGE test --no-input

echo
echo "Running linter ..."
flake8

echo
echo "Success!"
