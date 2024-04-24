#!/bin/sh

PYTHON_PATH=$(which python)
CURRENT_PATH=$(pwd)/.venv/bin/python
if [ ${PYTHON_PATH} != ${CURRENT_PATH} ] ; then
    echo "Already inside virtual environment."
else
    . $(pwd)/.venv/bin/activate
fi;

nohup reflex run --env=prod --backend-only &
