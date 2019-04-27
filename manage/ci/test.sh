#!/bin/bash

MANAGE="python3 manage.py"

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

set -eu # Exit on error and undefined var is error

# Setup files and dirs
cp dev-setup/test/env.original env
mkdir -p log

# Run Django tests
$MANAGE test
