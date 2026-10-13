# Cloud environment setup script

`setup.sh` prepares a Claude Code cloud session (claude.ai/code, the Claude
app, the Desktop app's cloud mode) for the three repositories the maintainer
works in: `coding-harness`, `lakeswitch-ai` and `adhd-relief`.

**Where it runs.** Not from this checkout. Its text is pasted into the cloud
environment's **Setup script** field (environment selector → Cloud → the
settings icon on the environment; editable at claude.ai/code or in the Desktop
app, not in the iOS app). It runs as root before Claude Code starts. When it
finishes in about five minutes the platform snapshots the result, and later
sessions start from that snapshot; it runs again when the script changes or the
snapshot expires (about seven days).

## What it does

- **Python 3.11 and 3.12** via `uv python install 3.11 3.12`: `lakeswitch-ai`
  requires `>=3.11,<3.12`, `coding-harness` requires `>=3.12`, and the image
  ships 3.13.
- **bd 1.3.0** to `~/.local/bin/bd-1.3.0`, checksum-verified: `tools/bd`
  looks there first; a mismatch skips the install (fail closed).
- **`lakeswitch-ai/.venv`** from `requirements-ci.txt`, plus an editable
  install of the package: the same pins CI installs.
- **`coding-harness/.venv`** on Python 3.12 with `--require-hashes`: what
  `make venv` builds.
- **Tracker** via `tools/bd bootstrap --yes` in `adhd-relief` and
  `coding-harness`: clones from `refs/dolt/data`, reads only, pushes nothing.
  Bootstrap rewrites `.beads/.gitignore` and `.beads/config.yaml`; the script
  restores both, so the tree stays clean.
- **`PATH`** in `~/.bashrc` gains the lakeswitch venv and `~/.local/bin`, so
  `lakeswitch verify` works without activating the venv.

Every step is idempotent. A repository that is not checked out when the script
runs is skipped without an error; Python and bd are installed regardless.

## Known limits

- The bd checksum is a copy of
  `tools/beads/checksums/beads_1.3.0_linux_amd64.tar.gz.sha256`, because the
  script runs outside any checkout. A bd version bump has to change both; no
  check holds them together yet.
- Whether the repositories are already cloned when the setup script runs has
  not been observed in a fresh environment.
- Tested 2026-10-09 in a running cloud session (bd removed first to force the
  download and checksum path): exit 0, all three working trees unchanged.
