#!/bin/bash

# Syntax: ./cmd.sh <cmd>
# Runs the specified command in the container.

DC_FILE="setup/simple/docker-compose.yml"
DC="docker-compose -f $DC_FILE"

$DC run --rm app $@
