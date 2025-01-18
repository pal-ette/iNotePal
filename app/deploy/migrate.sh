#!/bin/sh

PYTHON_PATH=$(which python3.10)
CURRENT_PATH=$(pwd)/.venv/bin/python3.10
if [ ${PYTHON_PATH} = ${CURRENT_PATH} ] ; then
    echo "Already inside virtual environment. skip activate"
else
    . $(pwd)/.venv/bin/activate
fi;

reflex db migrate
