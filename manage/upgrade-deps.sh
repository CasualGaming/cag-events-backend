#!/bin/bash

# Added to .txt headers
export CUSTOM_COMPILE_COMMAND="manage/update-deps.sh"

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

set -eu # Exit on error and undefined var is error

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Updating requirements files ..."
pip-compile --quiet --upgrade requirements/base.in
pip-compile --quiet --upgrade requirements/development.in
pip-compile --quiet --upgrade requirements/production.in
pip-compile --quiet --upgrade requirements/testing.in
pip-compile --quiet --upgrade requirements/all.in

echo
echo "Dependency changes (if any):"
diff requirements/all.old.txt requirements/all.txt || true
rm -f requirements/all.old.txt

echo
echo "Done. Now check the changelogs for updated deps and make sure they didn't break anything."
