#!/bin/bash

# Run some checks ...

CMD="manage/cmd.sh"
MANAGE="manage/manage.sh"

set -eu # Exit on error and undefined var is error

echo
echo "Collecting static files ..."
# Ignore admin app, use theme instead
$MANAGE collectstatic -i admin --no-input --clear | egrep -v "^Deleting" || true

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
$CMD flake8

echo
echo "Success!"
