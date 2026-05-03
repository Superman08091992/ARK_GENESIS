# Combined Runtime Review — 2026-05-03

## Verdict

The uploaded runtime bundles are combinable, but they must be combined as a layered ARK monorepo rather than flattened into one package or one authority surface.

## Uploaded inputs reviewed

1. `ARK_GENESIS_INCORPORATED_PATCHED.zip`
   - Umbrella ARK Genesis source tree.
   - Includes ARKlinux substrate material, runtime/control-plane scaffolding, UI material, Graveyard/doctrine material, package scaffolds, manifests, and a root launcher.

2. `ark_gleaned_project.zip`
   - Clean Python ARK runtime seed.
   - Best candidate for canonical runtime package.
   - Preserves the intended governance flow: Kyle -> quarantine -> Aletheia -> Joey -> HRM -> Kenny dry-run -> memory/audit.

3. `ID_COB_Runtime_v0_1.zip`
   - Independent Python ID / Inner Desire C.O.B. runtime.
   - Contains consent, C.O.B., affect, severity, inflection, store, contracts, CLI, config, examples, and tests.
   - Should remain subordinate to ARK governance and must not become an execution authority.

## Recommended target layout

```text
ARK_GENESIS/
  os/
    arklinux/
  packages/
    ark-runtime/
    id-cob-runtime/
    ark-cli/
  apps/
    operator-ui/
    control-plane-ts/
  modules/
    finance/
      tradeanalyzer/
  graveyard/
    doctrine/
  schemas/
  scripts/
    start.py
    validate.py
```

## Authority model to preserve

```text
Kyle -> quarantine -> Aletheia -> Joey -> HRM -> Kenny
```

Rules:

- Kyle acquires/perceives; Kyle does not approve execution.
- Aletheia verifies/adjudicates truth; Aletheia does not execute.
- Joey analyzes trusted memory; Joey does not fetch raw external data.
- HRM validates policy/governance.
- Kenny executes only bounded, approved, audited actions.
- ID learns/reflects only from curated evidence-linked traces; ID does not authorize or execute.
- UI/control-plane surfaces observe and submit requests; they do not become source of truth.

## Direct combination status

Compatible:

- Python package names do not collide: `ark_runtime`, `id_runtime`, and `ark_cli` are distinct.
- The ARK runtime and ID C.O.B. runtime can coexist as sibling packages.
- ARKlinux material can live under `os/arklinux` or remain in its own repo and be referenced as a substrate component.

Needs adapters:

- ID C.O.B. outputs should be translated into ARK memory/evidence artifacts.
- Trade/finance signals should enter as policy-gated feature modules, not direct broker authority.
- TypeScript/React UI and control plane should call a runtime gateway, not read/write truth state directly.

Do not merge blindly:

- Do not flatten all files into repo root.
- Do not treat old scaffold claims like “production” or “complete” as validated runtime truth.
- Do not let Tradeanalyzer, ID, UI, or the TypeScript server bypass HRM/Kenny boundaries.
- Do not put generated caches, demo state, secrets, tokens, or pyc files into source control.

## Recommended next implementation sequence

1. Create `packages/ark-runtime` from `ark_gleaned_project`.
2. Create `packages/id-cob-runtime` from `ID_COB_Runtime_v0_1`, excluding `__pycache__`, `*.pyc`, and generated demo state unless intentionally preserved as examples.
3. Move ARKlinux material into `os/arklinux` only if this repo is intended to vendor the substrate; otherwise keep it in `Superman08091992/ARKlinux` and reference it.
4. Add an ID-to-memory adapter that emits evidence-linked reflective artifacts.
5. Add finance module boundaries before importing Tradeanalyzer into runtime.
6. Add CI for both Python packages.
7. Keep `start.py` as the memorable human entrypoint, but have it invoke the canonical `ark-runtime` package.

## Storage note

A combined source bundle was built locally in this session as `ARK_GENESIS_COMBINED_RUNTIME_BUNDLE.zip`. The GitHub connector available here can write text files and create PRs, but it does not expose release-asset upload or direct binary artifact upload. Therefore this branch records the integration review and exact merge plan. The actual source bundle should be pushed from a local clone or uploaded as a GitHub release artifact from the destination machine.
