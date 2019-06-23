#!/bin/bash

# Run Django tests.

MODULE_PARENTS="src src/apps"
MANAGE="manage/manage.sh"

set -eu # Exit on error and undefined var is error

# Run all Django tests
$MANAGE test --no-input $MODULE_PARENTS
