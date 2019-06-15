#!/bin/bash

CONFIG_TEMPLATE_FILE="setup/config.template.env"
MANAGE="python3 src/manage.py"

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

set -eu # Exit on error and undefined var is error

# Setup files and dirs
cp $CONFIG_TEMPLATE_FILE config.env
mkdir -p log

# Run Django tests
$MANAGE test
