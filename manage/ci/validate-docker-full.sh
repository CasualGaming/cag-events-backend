#!/bin/bash

set -eu # Exit on error and undefined var is error

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

manage/setup-docker-full.sh
manage/run-docker-full.sh
