#!/bin/bash

# Runs Django manage.py with the specified command in the container.

$(dirname $BASH_SOURCE[0])/cmd.sh python3 src/manage.py $@
