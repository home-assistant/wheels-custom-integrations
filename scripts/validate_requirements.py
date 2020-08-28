#!/usr/bin/env python3
"""Validate custom wheels package requirements."""
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List, Set
import urllib.request

from stdlib_list import stdlib_list

SUPPORTED_PYTHON_VERSIONS = ["3.8"]
STD_LIBS = {version: set(stdlib_list(version)) for version in SUPPORTED_PYTHON_VERSIONS}


def main() -> int:
    """Run main function."""
    return 0 if validate() else 1


def validate() -> bool:
    """Do the validation."""
    print("Validating requirements")
    print()
    piped_input = sys.stdin.read()
    changed_files = piped_input.split("\n")
    changed_component_files = collect_component_files(changed_files)
    validated_ok = True
    print("Integrations to validate:", len(changed_component_files))

    for fil in changed_component_files:
        manifest = get_manifest(fil)
        print()
        print(f"Validating {manifest['domain']}:")
        requirements = set(manifest["requirements"])
        requirements_ok = validate_requirements(requirements)
        if requirements_ok:
            print("OK!")
        validated_ok = requirements_ok

    return validated_ok


def collect_component_files(changed_files: List[str]) -> Set[Path]:
    """Collect component files from changed files in the pull request."""
    project_dir = Path(__file__).parent.parent
    component_dir = project_dir / "components"
    component_files = set(component_dir.glob("**/*.json"))
    changed_component_files = set([Path(fil) for fil in changed_files]).intersection(
        component_files
    )
    return changed_component_files


def get_manifest(component_file: Path) -> Dict[str, Any]:
    """Return the integration manifest."""
    component_data = json.loads(component_file.read_text())
    manifest_address = component_data["manifest"]
    with urllib.request.urlopen(manifest_address) as url:
        manifest = json.loads(url.read().decode())

    return manifest


def validate_requirements(requirements: Set[str]) -> bool:
    """Validate requirements."""
    install_ok = install_requirements(requirements)

    if not install_ok:
        return False

    all_integration_requirements = get_requirements(requirements)

    if requirements and not all_integration_requirements:
        print(f"Failed to resolve requirements {requirements}")
        return False

    validated_ok = True

    # Check for requirements incompatible with standard library.
    for version, std_libs in STD_LIBS.items():
        for req in all_integration_requirements:
            if req in std_libs:
                print(
                    f"Package {req} is not compatible "
                    f"with Python {version} standard library",
                )
                validated_ok = False

    return validated_ok


def get_requirements(requirements: Set[str]) -> Set[str]:
    """Return all (recursively) requirements for an integration."""
    all_requirements = set()

    for req in requirements:
        package = normalize_package_name(req)
        try:
            result = subprocess.run(
                ["pipdeptree", "-w", "silence", "--packages", package],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.SubprocessError:
            print(f"Failed to resolve requirements for {req}")
            continue

        # parse output to get a set of package names
        output = result.stdout
        lines = output.split("\n")
        parent = lines[0].split("==")[0]  # the first line is the parent package
        if parent:
            all_requirements.add(parent)

        for line in lines[1:]:  # skip the first line which we already processed
            line = line.strip()
            line = line.lstrip("- ")
            package = line.split("[")[0]
            package = package.strip()
            if not package:
                continue
            all_requirements.add(package)

    return all_requirements


def install_requirements(requirements: Set[str]) -> bool:
    """Install integration requirements.

    Return True if successful.
    """
    install_ok = True

    for req in requirements:
        requirement_args = req.split(" ")
        args = [sys.executable, "-m", "pip", "install", "--quiet"]
        args.extend(requirement_args)
        try:
            subprocess.run(args, check=True)
        except subprocess.SubprocessError:
            print(f"Requirement {req} failed to install")
            install_ok = False

    return install_ok


def normalize_package_name(requirement: str) -> str:
    """Return a normalized package name from a requirement string."""
    requirement = requirement.split(" ")[-1]  # remove potential pip argument
    package = requirement.split("==")[0]  # remove version pinning
    package = package.split("[")[0]  # remove potential require extras
    # replace underscore with dash to work with pipdeptree
    package = package.replace("_", "-")
    package = package.lower()  # normalize casing

    return package


if __name__ == "__main__":
    sys.exit(main())
