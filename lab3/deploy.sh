#!/bin/sh
set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

. ./my_env/bin/activate
cd ./lab3
export BUILD_ID=dontKillMe
export JENKINS_NODE_COOKIE=dontKillMe
path_model=$(cat best_model.txt)
mlflow models serve -m "$path_model" -p 5003 --no-conda &
