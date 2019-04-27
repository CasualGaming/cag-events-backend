#!/bin/bash

# Docker
if command -v docker-compose 1>/dev/null 2>&1; then
    docker-compose -f dev-setup/docker-simple/docker-compose.yml down
    docker-compose -f dev-setup/docker-full/docker-compose.yml down
fi

# Data
rm -rf env
rm -rf db.sqlite
rm -rf static
rm -rf log
rm -rf dev-setup/docker-simple/env
rm -rf dev-setup/docker-full/env
rm -rf /tmp/cag-events-backend

# Venv
rm -rf .venv

# Python
find . -name "__pycache__" -exec rm -rf {} \; -prune
#find . -name "*.pyc" -exec rm -rf {} \;

# Other
rm -f requirements/*.old.txt
