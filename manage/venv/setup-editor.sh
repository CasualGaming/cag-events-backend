#!/bin/bash

set -e # No -u because of source below

# Activate venv and deactivate on exit
source manage/venv/activate.sh
trap deactivate EXIT

set -eu

echo
echo "Installing requirements ..."
pip install -r requirements/development.txt
