#!/bin/bash

exec bash --init-file <(echo "source manage/activate.venv.sh; trap deactivate EXIT") -i
