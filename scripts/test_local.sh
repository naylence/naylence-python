#!/bin/sh
set -e

STARTERS_PATH=${NAYLENCE_STARTERS_PATH:-../naylence-starters}
export NAYLENCE_STARTERS_PATH="$STARTERS_PATH"

python -m naylence init ./.tmp/test-app --template agent-on-sentinel --flavor ts --from-local

echo "Generated app in ./ .tmp/test-app"
