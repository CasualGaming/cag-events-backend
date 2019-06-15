#!/bin/bash

# Runs the Django dev server in the container.

DC_FILE="setup/simple/docker-compose.yml"
DC="docker-compose -f $DC_FILE"

$DC up --no-recreate
