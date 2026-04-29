#!/usr/bin/env python3
"""Smoke-check ARK runtime contracts.

This file supports both invocation styles:
  python scripts/smoke_check_runtime_contract.py
  python -m scripts smoke-contract
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_function(module_path: Path, module_name: str, function_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'cannot load module from {module_path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


validate_deployment = _load_function(
    ROOT / 'scripts' / 'validate_deployment_manifest.py',
    'ark_validate_deployment_manifest',
    'validate_deployment',
)
validate_graveyard = _load_function(
    ROOT / 'opt' / 'ark' / 'scripts' / 'validate_graveyard.py',
    'ark_validate_graveyard',
    'validate_graveyard',
)


def smoke_check(root: Path):
    deployment_ok, deployment_errors = validate_deployment(root)
    graveyard = validate_graveyard(root)
    errors = list(deployment_errors) + list(graveyard.errors)
    return deployment_ok and graveyard.ok, tuple(errors)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path(args[0]).resolve() if args else ROOT
    ok, errors = smoke_check(root)
    if ok:
        print('runtime contract smoke check ok')
        return 0
    for error in errors:
        print(error, file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
