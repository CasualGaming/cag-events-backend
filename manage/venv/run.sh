#!/bin/bash

LOCAL_DIR=".local/venv"
CONFIG_FILE="$LOCAL_DIR/config.env"
MANAGE="python src/manage.py"

export CONFIG_FILE

set -e # No -u because of source below

# Activate venv and deactivate on exit
source "$(dirname "$BASH_SOURCE[0]")/activate.sh"
trap deactivate EXIT

set -eu

$MANAGE runserver localhost:8000
