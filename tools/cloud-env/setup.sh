#!/usr/bin/env bash
# Setup script for the Claude Code cloud environment (lakeswitch-ai, adhd-relief,
# coding-harness). Pasted into the environment's "Setup script" field; it runs
# outside any checkout, so it carries the bd checksum itself. See README.md.
# Idempotent. Global tools always; per-repo steps only where the repo is checked out.
set -uo pipefail

export PATH="$HOME/.local/bin:$PATH"
BD_VERSION=1.3.0
BD_SHA256=2f92b904ecf35b607e44dc5c39229173af69c54f1183e8d709f1773540cdcf3b  # = tools/beads/checksums/beads_1.3.0_linux_amd64.tar.gz.sha256
BD_DEST="$HOME/.local/bin/bd-$BD_VERSION"

# 1. Python 3.11 (lakeswitch-ai requires >=3.11,<3.12) and 3.12 (coding-harness requires >=3.12)
uv python install 3.11 3.12

# 2. bd, pinned and checksum-verified (fail closed)
if ! { [ -x "$BD_DEST" ] && "$BD_DEST" version 2>/dev/null | grep -q "$BD_VERSION"; }; then
  TMP="$(mktemp -d)"
  TARBALL="beads_${BD_VERSION}_linux_amd64.tar.gz"
  curl -fsSL -o "$TMP/$TARBALL" \
    "https://github.com/steveyegge/beads/releases/download/v${BD_VERSION}/${TARBALL}"
  if [ "$(sha256sum "$TMP/$TARBALL" | awk '{print $1}')" = "$BD_SHA256" ]; then
    tar -xzf "$TMP/$TARBALL" -C "$TMP"
    mkdir -p "$(dirname "$BD_DEST")"
    install -m 0755 "$(find "$TMP" -type f -name bd -perm -u+x | head -1)" "$BD_DEST"
  else
    echo "bd checksum mismatch, not installed" >&2
  fi
  rm -rf "$TMP"
fi

# 3. PATH for later shells
grep -q 'lakeswitch-ai/.venv/bin' "$HOME/.bashrc" 2>/dev/null || \
  echo 'export PATH="/home/user/lakeswitch-ai/.venv/bin:$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"

# 4. Per-repo steps, only if the repo is already cloned
R=/home/user/lakeswitch-ai
if [ -f "$R/requirements-ci.txt" ]; then
  uv venv --allow-existing --python 3.11 "$R/.venv"
  uv pip install --python "$R/.venv/bin/python" -r "$R/requirements-ci.txt"
  uv pip install --python "$R/.venv/bin/python" -e "$R"
fi

R=/home/user/coding-harness
if [ -f "$R/requirements-ci.txt" ]; then
  uv venv --allow-existing --python 3.12 "$R/.venv"
  uv pip install --python "$R/.venv/bin/python" --require-hashes -r "$R/requirements-ci.txt"
fi

# Tracker databases: read-only clone from refs/dolt/data; bootstrap touches two
# tracked files under .beads/, which are restored afterwards.
for R in /home/user/adhd-relief /home/user/coding-harness; do
  if [ -x "$R/tools/bd" ] && [ -x "$BD_DEST" ]; then
    chmod 700 "$R/.beads"
    (cd "$R" && BD_NON_INTERACTIVE=1 tools/bd bootstrap --yes) || echo "bd bootstrap failed in $R" >&2
    git -C "$R" checkout -- .beads/.gitignore .beads/config.yaml 2>/dev/null
  fi
done

exit 0
