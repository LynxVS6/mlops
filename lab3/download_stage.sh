#!/bin/sh
set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

python3 -m venv ./my_env
. ./my_env/bin/activate
cd ./lab3
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip setuptools
pip3 install -r requirements.txt
python3 download.py
