#!/bin/bash

export CUSTOM_COMPILE_COMMAND="manage/update-deps.sh"

set -e # Exit on error

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

set -eu # Exit on error and undefined var is error

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Temporarily updating requirements files ..."
pip-compile --quiet --upgrade --output-file requirements/all.tmp.txt requirements/all.in

echo "Dependency updates:"
diff requirements/all.old.txt requirements/all.tmp.txt || true

rm -f requirements/all.old.txt
rm -f requirements/all.tmp.txt
