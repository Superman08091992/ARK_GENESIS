# ARKlinux Release Procedure — Maintainer Reference

Version: v1.0  
Document date: March 2026  
Last updated in ARK_GENESIS: April 2026

This document links the ARKlinux release lifecycle to ARK_GENESIS without collapsing the two systems.

Canonical separation:

- `ARK_GENESIS` is the source-of-truth build repository for ARK runtime doctrine, staged runtime code, UI surfaces, policy, evidence, and tests.
- `/opt/ark` is the installed runtime target on a node.
- `ARKlinux` is the Arch-based host/substrate that builds, mounts, signs, publishes, and runs the installed node environment.

## 1. Release scope

ARKlinux releases cover the operating system substrate and installable artifact set, including packages, ISO image, release signatures, checksums, build manifest, SBOM files, and GitHub Release assets.

The ARK runtime may be packaged into ARKlinux, but ARKlinux is not the runtime itself.

## 2. Versioning

ARKlinux uses Semantic Versioning.

| Type | Format | Meaning | Example |
| --- | --- | --- | --- |
| Patch | `vX.Y.Z+1` | Bug fixes and security patches | `v1.0.1` |
| Minor | `vX.Y+1.0` | Backward-compatible feature release | `v1.1.0` |
| Major | `vX+1.0.0` | Breaking substrate, architecture, or governance change | `v2.0.0` |

## 3. Build host dependencies

A local validation builder should run on Arch Linux or an Arch-compatible build container.

Required packages:

- `archiso`
- `base-devel`
- `git`
- `gnupg`
- `libisoburn`
- `squashfs-tools`
- `docker` optional for local containerized builds
- `github-cli` optional for GitHub release inspection

Bootstrap target:

```bash
./scripts/install-build-deps.sh
```

## 4. GitHub Actions secrets

The release pipeline expects these repository secrets to exist in GitHub Actions settings:

| Secret | Purpose |
| --- | --- |
| `ARK_GPG_PRIVATE_KEY` | Base64-encoded ASCII-armored private GPG key for package signing |
| `ARK_GPG_KEY_ID` | Long fingerprint of the signing key |
| `ARK_GPG_PASSPHRASE` | Passphrase for the signing key |
| `GITHUB_TOKEN` | Automatically provided by GitHub Actions for release publishing |

Never commit private keys, passphrases, tokens, or secret values to the repository. Only the public release key belongs in the repo.

## 5. Signing key setup

Generate a release key only on a trusted maintainer machine:

```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format LONG
```

Export the private key for GitHub Secrets:

```bash
gpg --export-secret-keys YOUR_KEY_ID | base64 -w0
```

Export the public key for repository verification:

```bash
gpg --export --armor YOUR_KEY_ID > keys/arklinux-release.asc
```

## 6. Pre-release checklist

Before tagging a release:

- All release pull requests are merged to `main`.
- `CHANGELOG.md` contains the target version.
- Version strings are aligned across PKGBUILDs and archiso profile metadata.
- Database migration scripts are reviewed.
- CI is passing on `main`.
- No open critical/high severity issues block the milestone.
- GPG secrets are present in repository settings.
- The public signing key is committed under `keys/`.

## 7. Local validation build

Expected local validation flow:

```bash
make deps
make packages
make repo
make iso
make vm ISO=out/arklinux-1.0.0-x86_64.iso
```

Success criteria:

- `out/` contains a bootable `.iso`.
- `out/` contains `SHA256SUMS.txt`.
- Package repository database exists.
- VM boot test reaches installer or expected live environment.

## 8. Tagging release

Tag pushes matching `v*` trigger the release pipeline.

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "ARKlinux v1.0.0 — Initial Release"
git push origin v1.0.0
```

The tag version should match package and profile versions.

## 9. CI/CD pipeline stages

Expected pipeline structure:

1. Checkout repository.
2. Restore build caches.
3. Prepare `out/` and pacman repo workspace.
4. Enter privileged Arch build container.
5. Build packages.
6. Build pacman repository database.
7. GPG-sign packages and repository metadata.
8. Build installer ISO with `mkarchiso`.
9. Generate build manifest and checksums.
10. Generate SBOM files.
11. Sign release assets.
12. Upload artifacts.
13. Publish GitHub Release on tag pushes.

## 10. Trigger matrix

| Trigger | ISO | Package signing | Asset signing | Publish release |
| --- | --- | --- | --- | --- |
| Push to `main` | yes | yes if secrets present | yes | no |
| Pull request | yes | no | no | no |
| Tag `v*` | yes | yes | yes | yes |
| Manual dispatch | yes | yes if secrets present | yes | no |

## 11. Artifact inventory

A successful release should contain:

- `arklinux-<version>.iso`
- `SHA256SUMS.txt`
- `SHA256SUMS.txt.asc`
- `build-manifest.txt`
- pacman repository database files
- package files and detached signatures
- SBOM files in CycloneDX JSON format
- asset signatures and certificates where applicable

## 12. Verification commands

```bash
gpg --import keys/arklinux-release.asc
gpg --verify SHA256SUMS.txt.asc SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt --ignore-missing
```

For keyless Sigstore/Cosign artifacts:

```bash
cosign verify-blob --signature arklinux-1.0.0.iso.sig --certificate arklinux-1.0.0.iso.pem arklinux-1.0.0.iso
```

## 13. Post-release tasks

After publishing:

- Announce the release with URL, hash, and changelog summary.
- Update download links and documentation.
- Close the milestone.
- Create the next milestone.
- Add a new blank `Unreleased` section to `CHANGELOG.md`.
- Archive SBOMs to the compliance store.
- For major releases, file a governance proposal.

## 14. Hotfix procedure

For critical fixes:

```bash
git checkout -b hotfix/v1.0.1 v1.0.0
# apply minimal fix
git add -p
git commit -m "fix: describe the security or bug fix"
git push origin hotfix/v1.0.1
```

After review and merge:

```bash
git checkout main
git pull origin main
git tag -a v1.0.1 -m "Hotfix v1.0.1 — fix description"
git push origin v1.0.1
```

Branch hotfixes from the affected release tag, not from unrelated future development.

## 15. Rollback procedure

Do not delete a published GitHub Release. Preserve the audit trail.

Rollback path:

1. Mark defective release as pre-release.
2. Communicate incident status.
3. Review manifest and CI logs.
4. Apply minimal fix through expedited PR.
5. Publish corrected patch release.
6. File governance proposal if governance behavior was affected.

Installed systems should rely on Btrfs snapshots for local rollback independent of ISO publication.

## 16. Secret rotation

Rotate immediately when a signing key is compromised, expired, or maintainer trust changes.

Rotation path:

1. Generate new key pair.
2. Update GitHub Actions secrets.
3. Commit new public key.
4. Revoke old key.
5. Re-sign and republish current release artifacts through a patch release.
6. Announce the rotation.

## 17. Troubleshooting table

| Issue | Symptom | Resolution |
| --- | --- | --- |
| GPG signing fails | `no secret key` | Verify secret encoding and key import path |
| `mkarchiso` missing | command not found | Ensure `archiso` is installed in the build container |
| `repo-add` fails | package add error | Verify package files exist and PKGBUILDs are valid |
| Release not published | GitHub 422 or existing release | Remove draft or retag cleanly |
| ISO too large | media/write failure | Review packages and compression settings |
| Pacman keyring failure | keyring not writable | Verify privileged container mode and writable workspace |

## 18. Integration checkpoint with ARK_GENESIS

Before ARKlinux packages ARK runtime components from ARK_GENESIS, the following must pass:

```bash
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

The ARKlinux release pipeline should treat failed ARK_GENESIS runtime tests as a packaging blocker once ARK runtime packaging is enabled.
