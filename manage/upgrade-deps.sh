#!/bin/bash

# Added to .txt headers
export CUSTOM_COMPILE_COMMAND="manage/update-deps.sh"

set -eu # Exit on error and undefined var is error

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Updating requirements files ..."
pip-compile --quiet --upgrade requirements/all.in
pip-compile --quiet --upgrade requirements/development.in
pip-compile --quiet --upgrade requirements/production.in
pip-compile --quiet --upgrade requirements/testing.in

echo "Dependency changes (if any):"
diff requirements/all.old.txt requirements/all.txt || true

rm -f requirements/all.old.txt
