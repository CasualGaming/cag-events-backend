#!/bin/bash

# Runs linter.

CMD="manage/cmd.sh"
SRC_DIR="src"

set -eu # Exit on error and undefined var is error

# Run flake8 static code analysis
# Uses settings from .flake8
$CMD flake8 $SRC_DIR
