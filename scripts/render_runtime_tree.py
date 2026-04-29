#!/usr/bin/env python3
from pathlib import Path

RUNTIME_TREE = (
    '/opt/ark',
    '/opt/ark/runtime',
    '/opt/ark/graveyard',
    '/opt/ark/scripts',
    '/opt/ark/ui/static',
    '/opt/ark/bus',
    '/opt/ark/evidence',
    '/opt/ark/memory',
    '/opt/ark/docs',
    '/var/log/ark',
)


def render_tree() -> str:
    return '\n'.join(RUNTIME_TREE) + '\n'


def main():
    print(render_tree(), end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
