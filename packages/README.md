# ARK Packaging Scaffold

This directory bridges ARK_GENESIS into future ARKlinux packaging.

Canonical separation remains:

- `ARK_GENESIS` owns source, doctrine, runtime contracts, tests, and UI source.
- `/opt/ark` is the installed runtime target.
- `ARKlinux` owns OS substrate packaging, signing, ISO build, services, permissions, and release publication.

Packages:

| Package | Purpose |
| --- | --- |
| `ark-runtime` | Installs runtime contracts, Graveyard scaffold, and support scripts into `/opt/ark`. |
| `ark-ui` | Installs the static operator console into `/opt/ark/ui/static`. |
| `ark-services` | Installs service wrappers, systemd units, sysusers, and tmpfiles rules. |

This is a packaging scaffold, not a full released ARKlinux ISO pipeline.

The current Python module namespace is `opt.ark.*`, so the bootstrap service wrapper sets `PYTHONPATH=/` after installation. A later packaging hardening pass should move runtime Python modules into a conventional package layout or install a dedicated wheel into `/opt/ark/venvs/ark-runtime`.
