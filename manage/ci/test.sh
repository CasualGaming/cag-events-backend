#!/bin/bash

CONFIG_TEMPLATE_FILE="setup/ci/config.template.env"
MANAGE="python3 src/manage.py"

set -eu # Exit on error and undefined var is error

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

# Setup files and dirs
cp $CONFIG_TEMPLATE_FILE config.env
mkdir -p log

# Run Django tests
$MANAGE test
