# ARK_GENESIS

ARK_GENESIS is the source-of-truth build repository for the ARK scaffold. It is not the installed runtime root and it is not the ARKlinux OS substrate.

Canonical separation:

- `ARK_GENESIS` = source repository, doctrine, staged runtime contracts, UI source, package scaffolds, tests.
- `/opt/ark` = installed runtime target on the official node.
- `ARKlinux` = Arch-based host substrate that mounts, packages, signs, publishes, and runs `/opt/ark`.

Current v0.1 scope:

- Graveyard doctrine scaffold and validator.
- Runtime kernel contracts: Cube, ODA, OperationEnvelope, Checkpoint, lifecycle.
- Policy preconditions: Aletheia ref, Joey plan ref, HRM approval ref, checkpoint ref, operator/request identity, dry-run-only enforcement.
- AEM translator-only layer.
- ExecutionBroker stub-only mediation layer.
- Local event bus using append-only JSONL records.
- Evidence writer using canonical JSON payload hashing, per-kind evidence records, and append manifest.
- Local status API exposing `/health` and `/status` on loopback by default.
- Static operator console under `opt/ark/ui/static/`.
- Arch package scaffolds for `ark-runtime`, `ark-ui`, and `ark-services`.
- Service wrapper, systemd unit, sysusers rule, tmpfiles rule, and environment example.
- End-to-end dry-run pipeline tests, including recorded bus/evidence path.

Critical authority rule:

A.R.K. owns authorization, policy, state, and safety. AEM does not authorize. ExecutionBroker mediates final tool execution. Aletheia owns truth verification only. The UI observes state; it does not approve or execute actions.

Key docs:

- `docs/arklinux/release-procedure.md`
- `docs/ui/operator-console.md`
- `packages/README.md`

Local API development command:

```bash
python -m opt.ark.runtime.api.server --host 127.0.0.1 --port 8081 --runtime-root /opt/ark
```

Validation:

```bash
make compile
make test
```

Packaging scaffold validation:

```bash
make validate-packaging
```

Future Arch packaging commands, once building locally on Arch/ARKlinux:

```bash
make packages
make repo
```
