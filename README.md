# ARK_GENESIS

ARK_GENESIS is the source-of-truth build repository for the ARK scaffold. It is not the installed runtime root and it is not the ARKlinux OS substrate.

Canonical separation:

- `ARK_GENESIS` = source repository, doctrine, staged runtime contracts, tests.
- `/opt/ark` = installed runtime target on the official node.
- `ARKlinux` = Arch-based host substrate that mounts and runs `/opt/ark`.

Current v0.1 scope:

- Graveyard doctrine scaffold and validator.
- Runtime kernel contracts: Cube, ODA, OperationEnvelope, Checkpoint, lifecycle.
- Policy preconditions: Aletheia ref, Joey plan ref, HRM approval ref, checkpoint ref, operator/request identity, dry-run-only enforcement.
- AEM translator-only layer.
- ExecutionBroker stub-only mediation layer.
- Local event bus using append-only JSONL records.
- Evidence writer using canonical JSON payload hashing, per-kind evidence records, and append manifest.
- End-to-end dry-run pipeline tests, including recorded bus/evidence path.

Critical authority rule:

A.R.K. owns authorization, policy, state, and safety. AEM does not authorize. ExecutionBroker mediates final tool execution. Aletheia owns truth verification only.

Validation:

```bash
python -m py_compile \
  opt/ark/scripts/validate_graveyard.py \
  opt/ark/runtime/kernel/*.py \
  opt/ark/runtime/policy/*.py \
  opt/ark/runtime/action_model/*.py \
  opt/ark/runtime/execution_broker/*.py \
  opt/ark/runtime/bus/*.py \
  opt/ark/runtime/evidence/*.py \
  tests/test_graveyard_contracts.py \
  tests/test_kernel_contracts.py \
  tests/test_action_authorization_flow.py \
  tests/test_action_model.py \
  tests/test_execution_broker.py \
  tests/test_end_to_end_dry_run_pipeline.py \
  tests/test_event_bus.py \
  tests/test_evidence_writer.py \
  tests/test_end_to_end_recorded_pipeline.py

python -m unittest \
  tests/test_graveyard_contracts.py \
  tests/test_kernel_contracts.py \
  tests/test_action_authorization_flow.py \
  tests/test_action_model.py \
  tests/test_execution_broker.py \
  tests/test_end_to_end_dry_run_pipeline.py \
  tests/test_event_bus.py \
  tests/test_evidence_writer.py \
  tests/test_end_to_end_recorded_pipeline.py
```
