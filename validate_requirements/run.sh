#!/bin/sh
set -e
cat /validate/files.json | jq -r '.[]' | /validate/validate_requirements.py