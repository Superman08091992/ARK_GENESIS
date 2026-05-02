#!/usr/bin/env python3
"""Simple ARK_GENESIS runtime entrypoint.

Memorable command:
    python start.py

Safe defaults:
- validates contracts
- prints runtime status
- starts only the local read-only status API when requested
- does not execute shell/browser/account/file tools
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from opt.ark.runtime.api import RuntimeStatusReader, make_server
from scripts.smoke_check_runtime_contract import smoke_check
from scripts.render_runtime_tree import render_tree


def validate() -> int:
    ok, errors = smoke_check(ROOT)
    if ok:
        print('ARK validation: OK')
        return 0
    print('ARK validation: FAILED', file=sys.stderr)
    for error in errors:
        print(f'- {error}', file=sys.stderr)
    return 1


def status(runtime_root: Path) -> int:
    data = RuntimeStatusReader(runtime_root).read_status()
    print('ARK runtime status')
    print(f"  runtime_root: {data['runtime_root']}")
    print(f"  authority_mode: {data['authority']['mode']}")
    print(f"  bus_events: {data['bus']['event_count']}")
    print(f"  evidence_records: {data['evidence']['record_count']}")
    print('  real_tool_execution: disabled')
    return 0


def serve_api(runtime_root: Path, host: str, port: int) -> int:
    server = make_server(host, port, runtime_root)
    print(f'ARK local status API: http://{host}:{port}')
    print(f'Runtime root: {runtime_root}')
    print('Mode: read-only / dry-run-only')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nARK local status API stopped')
    finally:
        server.server_close()
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Start or inspect ARK_GENESIS runtime scaffold')
    parser.add_argument('command', nargs='?', default='status', choices=['status', 'validate', 'api', 'tree'], help='command to run')
    parser.add_argument('--runtime-root', default=str(ROOT), help='runtime root to inspect; use /opt/ark after deployment')
    parser.add_argument('--host', default='127.0.0.1', help='API bind host')
    parser.add_argument('--port', type=int, default=8081, help='API bind port')
    args = parser.parse_args(argv)

    runtime_root = Path(args.runtime_root).resolve()
    if args.command == 'validate':
        return validate()
    if args.command == 'api':
        rc = validate()
        if rc != 0:
            return rc
        return serve_api(runtime_root, args.host, args.port)
    if args.command == 'tree':
        print(render_tree(), end='')
        return 0
    return status(runtime_root)


if __name__ == '__main__':
    raise SystemExit(main())
