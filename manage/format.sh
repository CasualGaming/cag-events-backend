#!/bin/bash

# Runs code formatter and import sorter.

SRC_DIRS="src"
CMD="manage/cmd.sh"

set -eu # Exit on error and undefined var is error

# Sort imports
#$CMD isort -rc $SRC_DIRS

# Format code
$CMD black $SRC_DIRS
