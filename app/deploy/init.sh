#!/bin/sh

asdf local python 3.10.12

python3.10 -m venv .venv

. $(pwd)/.venv/bin/activate

pip install -r requirements.txt
