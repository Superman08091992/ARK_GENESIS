#!/usr/bin/env python3
"""Stable dispatcher for ARK_GENESIS repository helper scripts.

Use:
  python -m scripts validate-deployment
  python -m scripts smoke-contract
  python -m scripts render-runtime-tree
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_deployment_manifest import main as validate_deployment_main
from scripts.render_runtime_tree import main as render_runtime_tree_main
from scripts.smoke_check_runtime_contract import main as smoke_contract_main

COMMANDS = {
    'validate-deployment': validate_deployment_main,
    'smoke-contract': smoke_contract_main,
    'render-runtime-tree': render_runtime_tree_main,
}


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {'-h', '--help', 'help'}:
        print('usage: python -m scripts <command> [args]')
        print('commands:')
        for command in sorted(COMMANDS):
            print(f'  {command}')
        return 0 if args else 2

    command = args.pop(0)
    handler = COMMANDS.get(command)
    if handler is None:
        print(f'unknown command: {command}', file=sys.stderr)
        print('run: python -m scripts --help', file=sys.stderr)
        return 2
    return handler(args)


if __name__ == '__main__':
    raise SystemExit(main())
