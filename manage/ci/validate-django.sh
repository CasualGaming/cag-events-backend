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

# Collect static files
echo "Collecting static files ..."
# Ignore admin app, use theme instead
$MANAGE collectstatic -i admin --no-input --clear

# Run migration, but skip initial if matching table names already exist
echo "Running migration ..."
$MANAGE migrate --fake-initial --no-input

# Check if new migrations can be made
$MANAGE makemigrations --dry-run --check --no-input

# Validate
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR
