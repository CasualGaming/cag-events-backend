#!/bin/bash

set -eu

# Activate venv and deactivate on exit
# Allow undefined vars
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate.sh"
trap deactivate EXIT
set -u

echo
echo "Installing requirements ..."
pip install --quiet -r requirements/development.txt
