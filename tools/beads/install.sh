#!/usr/bin/env bash
# install.sh — the pinned bd binary, checksum-verified.
#
# The tracker is shared infrastructure (refs/dolt/data on origin), so the
# binary that writes it is not fetched off the wire unverified: the sha256 of
# each release tarball this repository pins lives in tools/beads/checksums/,
# and a mismatch refuses the install — fail closed (bead coding-harness-4t8,
# staged toward coding-harness-1jg.3: "installs the pinned bd with a
# checksum").
#
#   bash tools/beads/install.sh            # -> $HOME/.local/bin/bd-<version>
#
# The versioned file name is deliberate: tools/bd looks there FIRST, so this
# never touches a global bd another repository on this machine may need.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$REPO_ROOT/tools/beads/VERSION")"

case "$(uname -s)" in
  Linux)  OS=linux  ;;
  Darwin) OS=darwin ;;
  *) echo "Unsupported OS: $(uname -s) — install bd $VERSION by hand." >&2; exit 1 ;;
esac
case "$(uname -m)" in
  x86_64|amd64)  ARCH=amd64 ;;
  arm64|aarch64) ARCH=arm64 ;;
  *) echo "Unsupported architecture: $(uname -m) — install bd $VERSION by hand." >&2; exit 1 ;;
esac

TARBALL="beads_${VERSION}_${OS}_${ARCH}.tar.gz"
SUMS_FILE="$REPO_ROOT/tools/beads/checksums/${TARBALL}.sha256"
[ -f "$SUMS_FILE" ] || {
  echo "kein gepinnter Checksum fuer $TARBALL (tools/beads/checksums/) — Installation verweigert (fail closed)." >&2
  exit 1
}

DEST="${HOME}/.local/bin/bd-${VERSION}"
if [ -x "$DEST" ] && "$DEST" version 2>/dev/null | grep -q "$VERSION"; then
  echo "bd $VERSION already installed at $DEST — skipping the download."
  exit 0
fi

URL="https://github.com/steveyegge/beads/releases/download/v${VERSION}/${TARBALL}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Fetching bd $VERSION ($OS/$ARCH)…"
curl -fsSL -o "$TMP/$TARBALL" "$URL"

ERWARTET="$(awk '{print $1}' "$SUMS_FILE")"
case "$(uname -s)" in
  Darwin) IST="$(shasum -a 256 "$TMP/$TARBALL" | awk '{print $1}')" ;;
  *)      IST="$(sha256sum "$TMP/$TARBALL" | awk '{print $1}')" ;;
esac
if [ "$IST" != "$ERWARTET" ]; then
  echo "Checksum-MISMATCH fuer $TARBALL:" >&2
  echo "  erwartet: $ERWARTET" >&2
  echo "  erhalten: $IST" >&2
  echo "Installation abgebrochen — der Tarball wird nicht ausgefuehrt." >&2
  exit 1
fi

tar -xzf "$TMP/$TARBALL" -C "$TMP"
SRC="$(find "$TMP" -type f -name bd -perm -u+x | head -1)"
[ -n "$SRC" ] || { echo "No bd binary in $TARBALL" >&2; exit 1; }

mkdir -p "$(dirname "$DEST")"
install -m 0755 "$SRC" "$DEST"
echo "Installed: $DEST"