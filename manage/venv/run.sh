#!/bin/bash

LOCAL_DIR=".local/venv"
CONFIG_FILE="$LOCAL_DIR/config.env"
MANAGE="python src/manage.py"
ENDPOINT="localhost:8000"

# Used by app
export CONFIG_FILE

set -eu

# Activate venv and deactivate on exit
# Allow undefined vars
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate.sh"
trap deactivate EXIT
set -u

$MANAGE runserver $ENDPOINT
