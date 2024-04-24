#!/bin/sh

PYTHON_PATH=$(which python)
CURRENT_PATH=$(pwd)/.venv/bin/python
if [ ${PYTHON_PATH} = ${CURRENT_PATH} ] ; then
    echo "Already inside virtual environment. skip activate"
else
    . $(pwd)/.venv/bin/activate
fi;

pip install -r requirements.txt

reflex export
