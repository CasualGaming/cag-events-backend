#!/bin/bash

# Run some checks ...

CMD="manage/cmd.sh"
MANAGE="manage/manage.sh"

set -eu # Exit on error and undefined var is error

echo "Running some checks. This will stop on the first error, or print \"success\" if no errors were caught."

echo
echo "Running linter ..."
manage/lint.sh

echo
echo "Checking migrations ..."
$MANAGE makemigrations --check --no-input --dry-run
$MANAGE migrate --fake-initial --no-input --fake --plan

echo
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR

echo
echo "Running tests ..."
manage/test.sh

echo
echo "Collecting static files ..."
# Ignore admin app, use theme instead
$MANAGE collectstatic -i admin --no-input --clear | egrep -v "^Deleting" || true

echo
echo "Success!"
