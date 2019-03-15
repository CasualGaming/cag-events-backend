#!/bin/bash

set -eu # Exit on error and undefined var is error

PYTHON_PATH=

case "$OSTYPE" in
  darwin*)  PYTHON_PATH=$(which python3) ;; 
  *)        PYTHON_PATH=$(which python) ;;
esac

# Setup virtual environment to install packages and stuff inside
if [[ ! -d .venv ]]; then
    echo "Creating venv ..."
    # Don't use symlinks if in VirtualBox shared folder
    if ( df -t vboxsf . 1>/dev/null 2>/dev/null ); then
        echo "VirtualBox shared folder detected"
        virtualenv -p $PYTHON_PATH --always-copy .venv
    else
        virtualenv -p $PYTHON_PATH .venv
    fi
fi

# Create empty required files and directories
[[ ! -e studlan.db ]] && touch studlan.db
[[ ! -e log ]] && mkdir -p log

# Add dev app settings
APP_SETTINGS_FILE=fearlessFred/settings/local.py

DEV_APP_SETTINGS_FILE=sample-configs/local-dev.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "Using sample local.py ..."
    cp $DEV_APP_SETTINGS_FILE $APP_SETTINGS_FILE
fi