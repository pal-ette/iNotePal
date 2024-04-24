#!/bin/sh

PYTHON_PATH=$(which python)
CURRENT_PATH=$(pwd)/.venv/bin/python
if [ ${PYTHON_PATH} != ${CURRENT_PATH} ] ; then
    echo "Already inside virtual environment."
else
    . $(pwd)/.venv/bin/activate
fi;

mkdir -p logs

nohup time reflex run --env=prod --backend-only | ts '[%Y-%m-%d %H:%M:%S]' > logs/log-"`date +"%Y-%m-%d-%H:%M:%S"`".log &
