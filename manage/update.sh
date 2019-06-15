#!/bin/bash

# Updates an existing setup.

CMD="manage/cmd.sh"
MANAGE="manage/manage.sh"

set -eu # Exit on error and undefined var is error

echo "Updating requirements ..."
$CMD pip3 install -r requirements/development.txt | egrep -v "^Requirement already satisfied" || true

echo
echo "Collecting static ..."
# Ignore admin app, use theme instead
$MANAGE collectstatic -i admin --noinput --clear | egrep -v "^Deleting" || true

echo
echo "Running migrations ..."
$MANAGE migrate --fake-initial
