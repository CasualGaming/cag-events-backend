#!/bin/bash

# Checks if updates are available for pip requirements/dependencies.

CUSTOM_COMPILE_COMMAND="manage/deps-upgrade.sh"
DC_FILE="setup/simple/docker-compose.yml"
CMD="docker-compose -f $DC_FILE run --rm -e CUSTOM_COMPILE_COMMAND=$CUSTOM_COMPILE_COMMAND app"

set -eu # Exit on error and undefined var is error

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Temporarily updating requirements files ..."
$CMD pip-compile --quiet --upgrade --output-file requirements/all.tmp.txt requirements/all.in

echo "Available dependency updates:"
diff requirements/all.old.txt requirements/all.tmp.txt || true

rm -f requirements/all.old.txt
rm -f requirements/all.tmp.txt
