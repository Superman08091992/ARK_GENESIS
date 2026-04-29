#!/usr/bin/env python3
import sys
from pathlib import Path

REQUIRED_FILES = (
    'deployment/runtime-manifest.yaml',
    'deployment/filesystem-contract.yaml',
    'deployment/service-registry.yaml',
    'deployment/promotion-policy.yaml',
)

REQUIRED_RUNTIME_TARGETS = (
    '/opt/ark/runtime',
    '/opt/ark/graveyard',
    '/opt/ark/ui/static',
    '/opt/ark/bus',
    '/opt/ark/evidence',
    '/var/log/ark',
)

REQUIRED_SERVICES = ('ark-local-api',)


def read_text(root: Path, rel: str) -> str:
    path = root / rel
    if not path.exists():
        raise ValueError(f'missing required deployment file: {rel}')
    text = path.read_text(encoding='utf-8')
    if not text.strip():
        raise ValueError(f'empty required deployment file: {rel}')
    return text


def require_contains(text: str, expected: str, rel: str) -> None:
    if expected not in text:
        raise ValueError(f'{rel}: missing expected value {expected!r}')


def validate_deployment(root: Path):
    errors = []
    texts = {}
    for rel in REQUIRED_FILES:
        try:
            texts[rel] = read_text(root, rel)
        except Exception as exc:
            errors.append(str(exc))

    if errors:
        return False, tuple(errors)

    runtime = texts['deployment/runtime-manifest.yaml']
    filesystem = texts['deployment/filesystem-contract.yaml']
    services = texts['deployment/service-registry.yaml']
    policy = texts['deployment/promotion-policy.yaml']

    for rel, text in texts.items():
        for required in ('schema_version:', '"0.1"'):
            try:
                require_contains(text, required, rel)
            except Exception as exc:
                errors.append(str(exc))

    for target in REQUIRED_RUNTIME_TARGETS:
        try:
            require_contains(runtime + filesystem, target, 'deployment contracts')
        except Exception as exc:
            errors.append(str(exc))

    for service in REQUIRED_SERVICES:
        try:
            require_contains(services, service, 'deployment/service-registry.yaml')
        except Exception as exc:
            errors.append(str(exc))

    for required in ('operator_approved', 'default_decision: "deny"', 'required_prechecks:', 'promotion_steps:'):
        try:
            require_contains(policy, required, 'deployment/promotion-policy.yaml')
        except Exception as exc:
            errors.append(str(exc))

    return not errors, tuple(errors)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path(args[0]).resolve() if args else Path.cwd()
    ok, errors = validate_deployment(root)
    if ok:
        print('deployment contracts validation ok')
        return 0
    for error in errors:
        print(error, file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
