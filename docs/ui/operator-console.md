# ARK Operator Console

The operator console is a transitional local UI for observing the ARK runtime without granting the UI direct authority over tools, accounts, shell access, or runtime mutation.

## Placement

Source path in ARK_GENESIS:

```text
opt/ark/ui/static/
```

Installed target path:

```text
/opt/ark/ui/static/
```

The UI is intentionally static. It reads the local API and displays status. It does not authorize actions.

## Local API

Source path:

```text
opt/ark/runtime/api/
```

Default bind:

```text
127.0.0.1:8081
```

Endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/health` | local API liveness |
| `/status` | bus count, evidence count, last event, last evidence record, and authority mode |

Run command after deployment or in repo root:

```bash
python -m opt.ark.runtime.api.server --host 127.0.0.1 --port 8081 --runtime-root /opt/ark
```

For development without installed `/opt/ark`, point `--runtime-root` at a temporary directory or repository fixture.

## Authority boundary

The UI is read-oriented in v0.1.

It may display:

- dry-run authority mode
- event count
- evidence count
- last event
- last evidence record
- local runtime root

It must not directly perform:

- shell execution
- browser automation
- account access
- file mutation
- HRM approval
- policy override
- AEM authorization

Future action buttons must call a policy-gated local API route that creates an OperationEnvelope and records evidence before any brokered execution.

## Relationship to ARKlinux

ARKlinux should package the static UI and local API as part of the installed runtime package once packaging exists.

ARKlinux owns:

- service unit installation
- loopback binding
- filesystem placement
- permissions
- logs
- firewall posture

ARK_GENESIS owns:

- UI source files
- API source contracts
- tests
- doctrine and runtime semantics

## Relationship to `/opt/ark`

After deployment:

```text
/opt/ark/runtime/api/        local status API source/runtime package
/opt/ark/ui/static/          static operator console
/opt/ark/bus/events.jsonl    append-only local event records
/opt/ark/evidence/           evidence records and manifest
```

The console reads from the API, and the API reads bus/evidence state from the selected runtime root.
