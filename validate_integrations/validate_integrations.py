"""Validate the structure of an integration file."""
import json
from pathlib import Path
from typing import List, Set
import voluptuous as vol
import sys


def owner(value):
    """Validate owner"""
    if not isinstance(value, list):
        raise AssertionError("The owner key is not a list")

    if not value:
        raise AssertionError("The owner list is empty")

    for entry in value:
        if not entry.startswith("@"):
            raise AssertionError(f"The entry {entry} does not start with @")
    return value


def manifest(value):
    """Validate manifest URL."""
    if "github" in value and not "raw.githubusercontent.com" in value:
        raise AssertionError("The URL for the manifest key is not a raw URL")
    return value


INTEGRATION = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("owner"): owner,
        vol.Required("manifest"): manifest,
        vol.Required("url"): str,
    }
)


def validate():
    """Run the validation."""
    piped_input = sys.stdin.read()
    input_files = piped_input.split("\n")
    for filepath in collect_integration_files(input_files):
        print(f"Validating {filepath.as_posix().split('/')[-1]}")
        with open(filepath) as integration_file:
            INTEGRATION(json.loads(integration_file.read()))


def collect_integration_files(input_files: List[str]) -> Set[Path]:
    """Collect integration files from changed files in the pull request."""
    integration_dir = Path("/validate", "components")
    integration_files = set(integration_dir.glob("**/*.json"))
    changed_integration_files = set(
        [
            integration_dir / fil.split("/")[-1]
            for fil in input_files
            if "components" in fil
        ]
    ).intersection(integration_files)
    return changed_integration_files


validate()
