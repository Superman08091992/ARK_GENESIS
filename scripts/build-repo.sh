#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PKGDIR="${ROOT}/out/packages"
REPODIR="${ROOT}/repo/os/x86_64"
DBNAME="arklinux"

mkdir -p "$REPODIR"
cp "$PKGDIR"/*.pkg.tar.* "$REPODIR"/
cd "$REPODIR"
repo-add "${DBNAME}.db.tar.gz" ./*.pkg.tar.*

echo "Repository database written to ${REPODIR}/${DBNAME}.db.tar.gz"
