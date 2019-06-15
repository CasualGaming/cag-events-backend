#!/bin/bash

# Upgrades pip requirements/dependencies.

CUSTOM_COMPILE_COMMAND="manage/deps-upgrade.sh"
DC_FILE="setup/simple/docker-compose.yml"
CMD="docker-compose -f $DC_FILE run --rm -e CUSTOM_COMPILE_COMMAND=$CUSTOM_COMPILE_COMMAND app"

set -eu # Exit on error and undefined var is error

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Upgrading requirements for base ..."
$CMD pip-compile --quiet --upgrade requirements/base.in
echo "Upgrading requirements for testing ..."
$CMD pip-compile --quiet --upgrade requirements/testing.in
echo "Upgrading requirements for development ..."
$CMD pip-compile --quiet --upgrade requirements/development.in
echo "Upgrading requirements for production ..."
$CMD pip-compile --quiet --upgrade requirements/production.in
echo "Upgrading requirements for all ..."
$CMD pip-compile --quiet --upgrade requirements/all.in

# Create requirements.txt for dependency analyzers etc.
echo "#" > requirements.txt
echo "# This file contains all requirements and is meant for dependency analyzers etc." >> requirements.txt
echo "# Do not use this file to install requirements, use one of the \"requirements/*.txt\" files instead." >> requirements.txt
cat requirements/all.txt >> requirements.txt

echo
echo "Dependency changes (if any):"
diff requirements/all.old.txt requirements/all.txt || true
rm -f requirements/all.old.txt

echo
echo "Done. Now check the changelogs for updated deps and make sure they didn't break anything."
