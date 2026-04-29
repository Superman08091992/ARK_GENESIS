# Runtime Promotion Policy

Runtime promotion is the controlled movement from ARK_GENESIS source into an installed `/opt/ark` node.

## Rule

Promotion is deny-by-default and operator-approved.

## Required gates

Before promotion:

```bash
make compile
make test
make validate-packaging
python opt/ark/scripts/validate_graveyard.py
python scripts/validate_deployment_manifest.py
python scripts/smoke_check_runtime_contract.py
```

## Promotion phases

1. Validate source and contracts.
2. Snapshot the target node.
3. Stage the package set.
4. Install approved packages.
5. Restart only registered services.
6. Verify health, status, bus, and evidence paths.
7. Record promotion evidence.

## Operator approval

Operator approval is required for installation, service restart, capability expansion, network binding changes, service identity changes, and Graveyard changes.

## Blocked categories

The promotion policy blocks unbounded host actions, external account actions, public network binding, and private machine material in source unless a later formal policy explicitly permits a bounded version.
