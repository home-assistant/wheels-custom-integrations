#!/bin/sh
set -e
cat /validate/files.json | jq -r '.[]' | python3 /validate/validate_integrations.py