#!/bin/bash

VENV_DIR=".venv"

set -eu

if ! [[ -e $VENV_DIR ]]; then
    echo "Virtualenv not found, creating it ..."

    # The essentials
    # Make sure the user bin dir is added to PATH
    pip3 install --user --quiet --upgrade pip virtualenv setuptools wheel pip-tools

    # Windows uses Python 3 as "python", and has no "python3" or "python2"
    # Linux uses Python 2 as "python", but has "python3" and "python2"
    case "$(uname -s)" in
        MINGW*) PYTHON_PATH="$(which python)" ;;
        *) PYTHON_PATH="$(which python3)" ;;
    esac

    if [[ ! -d .venv ]]; then
        echo "Creating venv ..."
        # Don't use symlinks if in VirtualBox shared folder
        if ( df -t vboxsf . 1>/dev/null 2>/dev/null ); then
            echo "VirtualBox shared folder detected"
            virtualenv -p $PYTHON_PATH --always-copy $VENV_DIR
        else
            virtualenv -p $PYTHON_PATH $VENV_DIR
        fi
    fi
fi

case "$(uname -s)" in
    MINGW*) source $VENV_DIR/Scripts/activate ;;
    *) source $VENV_DIR/bin/activate ;;
esac
