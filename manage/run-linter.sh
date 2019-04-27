#!/bin/bash

set -eu # Exit on error and undefined var is error

MANAGE="python manage.py"

# Activate venv and deactivate on exit
source manage/activate-venv.sh
trap deactivate EXIT

# Run flake8 static code analysis
# Uses settings from .flake8
flake8
