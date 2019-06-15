#!/bin/bash

set -e # No -u because of source below

# Activate venv and deactivate on exit
source "$(dirname "$BASH_SOURCE[0]")/activate.sh"
trap deactivate EXIT

set -eu

echo
echo "Installing requirements ..."
pip install --quiet -r requirements/development.txt
