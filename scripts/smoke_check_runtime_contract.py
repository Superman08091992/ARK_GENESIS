#!/usr/bin/env python3
from pathlib import Path

from scripts.validate_deployment_manifest import validate_deployment
from opt.ark.scripts.validate_graveyard import validate_graveyard


def smoke_check(root: Path):
    deployment_ok, deployment_errors = validate_deployment(root)
    graveyard = validate_graveyard(root)
    errors = list(deployment_errors) + list(graveyard.errors)
    return deployment_ok and graveyard.ok, tuple(errors)


def main():
    ok, errors = smoke_check(Path.cwd())
    if ok:
        print('runtime contract smoke check ok')
        return 0
    for error in errors:
        print(error)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
