#!/usr/bin/env bash
set -euo pipefail

# Reconstructs the full combined runtime bundle after the source archives are available locally.
# Expected default input location: ./incoming

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INCOMING="${ARK_INCOMING:-$ROOT/incoming}"
OUT="${ARK_OUT:-$ROOT/build/combined-runtime}"

ARK_GENESIS_ZIP="${ARK_GENESIS_ZIP:-$INCOMING/ARK_GENESIS_INCORPORATED_PATCHED.zip}"
ARK_RUNTIME_ZIP="${ARK_RUNTIME_ZIP:-$INCOMING/ark_gleaned_project.zip}"
ID_COB_ZIP="${ID_COB_ZIP:-$INCOMING/ID_COB_Runtime_v0_1.zip}"

for f in "$ARK_GENESIS_ZIP" "$ARK_RUNTIME_ZIP" "$ID_COB_ZIP"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing required archive: $f" >&2
    exit 1
  fi
done

rm -rf "$OUT"
mkdir -p "$OUT/sources" "$OUT/ARK_GENESIS_COMBINED_RUNTIME"

unzip -q "$ARK_GENESIS_ZIP" -d "$OUT/sources"
unzip -q "$ARK_RUNTIME_ZIP" -d "$OUT/sources"
unzip -q "$ID_COB_ZIP" -d "$OUT/sources"

COMBINED="$OUT/ARK_GENESIS_COMBINED_RUNTIME"
mkdir -p "$COMBINED/packages/ark-runtime" \
         "$COMBINED/packages/id-cob-runtime" \
         "$COMBINED/os" \
         "$COMBINED/artifacts/source-archives" \
         "$COMBINED/docs" \
         "$COMBINED/scripts"

rsync -a --exclude='__pycache__' --exclude='*.pyc' \
  "$OUT/sources/ark_gleaned_project/" \
  "$COMBINED/packages/ark-runtime/"

rsync -a --exclude='__pycache__' --exclude='*.pyc' \
  "$OUT/sources/ID_COB_Runtime_v0_1/" \
  "$COMBINED/packages/id-cob-runtime/"

if [[ -d "$OUT/sources/ARK_GENESIS_UNIFIED_FULL" ]]; then
  rsync -a --exclude='__pycache__' --exclude='*.pyc' \
    "$OUT/sources/ARK_GENESIS_UNIFIED_FULL/" \
    "$COMBINED/umbrella-source/"
elif [[ -d "$OUT/sources/ARK_GENESIS_INCORPORATED_PATCHED" ]]; then
  rsync -a --exclude='__pycache__' --exclude='*.pyc' \
    "$OUT/sources/ARK_GENESIS_INCORPORATED_PATCHED/" \
    "$COMBINED/umbrella-source/"
else
  echo "Could not find extracted ARK Genesis source root under $OUT/sources" >&2
  find "$OUT/sources" -maxdepth 2 -type d >&2
  exit 1
fi

if [[ -d "$COMBINED/umbrella-source/arklinux" ]]; then
  rsync -a "$COMBINED/umbrella-source/arklinux/" "$COMBINED/os/arklinux/"
fi

cp "$ARK_GENESIS_ZIP" "$COMBINED/artifacts/source-archives/"
cp "$ARK_RUNTIME_ZIP" "$COMBINED/artifacts/source-archives/"
cp "$ID_COB_ZIP" "$COMBINED/artifacts/source-archives/"

cat > "$COMBINED/README.md" <<'EOF'
# ARK Genesis Combined Runtime Bundle

Layered combination of ARK Genesis, the clean Python ARK runtime seed, and the ID C.O.B. runtime.

Canonical authority remains:

`Kyle -> quarantine -> Aletheia -> Joey -> HRM -> Kenny`

ID is reflective/identity modeling only. It is not an execution authority.
EOF

(
  cd "$COMBINED"
  find . -type f | sort | sed 's#^./##' > MANIFEST.txt
  find . -type f | sort -print0 | xargs -0 sha256sum > SHA256SUMS.txt
)

(
  cd "$OUT"
  zip -qr "$ROOT/ARK_GENESIS_COMBINED_RUNTIME_BUNDLE.zip" ARK_GENESIS_COMBINED_RUNTIME
)

echo "Built: $ROOT/ARK_GENESIS_COMBINED_RUNTIME_BUNDLE.zip"
