#!/bin/sh

PYTHON_PATH=$(which python3.10)
CURRENT_PATH=$(pwd)/.venv/bin/python3.10
if [ ${PYTHON_PATH} = ${CURRENT_PATH} ] ; then
    echo "Already inside virtual environment. skip activate"
else
    . $(pwd)/.venv/bin/activate
fi;

mkdir -p logs

nohup time reflex run --env=prod --backend-only | ts '[%Y-%m-%d %H:%M:%S]' > logs/log-"`date +"%Y-%m-%d-%H:%M:%S"`".log &
