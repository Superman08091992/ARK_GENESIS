#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${ROOT}/out/packages"
mkdir -p "$OUT"

for pkg in ark-runtime ark-ui ark-services; do
  echo "==> Building ${pkg}"
  (
    cd "${ROOT}/packages/${pkg}"
    makepkg --force --cleanbuild --syncdeps --noconfirm
    cp ./*.pkg.tar.* "$OUT"/
  )
done

echo "Packages copied to ${OUT}"
