#!/bin/bash

# Added to .txt headers
export CUSTOM_COMPILE_COMMAND="manage/update-deps.sh"

set -e # Exit on error

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
