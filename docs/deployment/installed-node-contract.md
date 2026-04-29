# Installed Node Contract

This document defines how ARK_GENESIS maps into an installed `/opt/ark` node.

## Boundaries

- ARK_GENESIS is source.
- `/opt/ark` is deployed runtime state and code target.
- ARKlinux owns the host substrate, packages, permissions, services, and release mechanics.

## Required installed roots

```text
/opt/ark
/opt/ark/runtime
/opt/ark/graveyard
/opt/ark/scripts
/opt/ark/ui/static
/opt/ark/bus
/opt/ark/evidence
/opt/ark/memory
/opt/ark/docs
/var/log/ark
```

## Mutable versus immutable

Mutable state:

- `/opt/ark/bus`
- `/opt/ark/evidence`
- `/opt/ark/memory`
- `/var/log/ark`

Source-controlled runtime/docctrine/UI material should be treated as deployment-owned and non-mutable during normal runtime operation.

## Legacy path policy

`/opt/ark` is canonical. `/opt/ARK` is legacy only and should not be used by new code, manifests, packages, or service units.

## Validation

```bash
python scripts/validate_deployment_manifest.py
python scripts/smoke_check_runtime_contract.py
```
