#!/usr/bin/env bash

set -euo pipefail

BASEDIR=$(dirname $PWD/..)

echo "==> Starting Initialization"

echo "==> Creating Virtualenv"
cd $BASEDIR
python3 -m venv ./venv
source venv/bin/activate

echo "==> Insalling dependencies"
cd $BASEDIR
pip install -r requirements.txt

echo "==> Initialization finished"
