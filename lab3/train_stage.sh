#!/bin/sh
set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

. ./my_env/bin/activate
cd ./lab3
python3 train_model.py > best_model.txt
