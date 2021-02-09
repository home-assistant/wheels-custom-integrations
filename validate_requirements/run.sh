#!/bin/sh

cat /validate/files.json | jq -r '.[]' | /validate/validate_requirements.py