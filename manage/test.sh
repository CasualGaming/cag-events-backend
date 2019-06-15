#!/bin/bash

# Run Django tests.

MANAGE="manage/manage.sh"

set -eu # Exit on error and undefined var is error

# Run Django tests
$MANAGE test
