#!/bin/bash
# Install this repository's Omnigent default policy into the machine's Omnigent config.
#
#   tools/omnigent/install.sh            merge policy.yaml into the global config
#   tools/omnigent/install.sh --check    say whether the installed policies equal the repository's
#   tools/omnigent/install.sh --remove   take the coding_harness__* policies out again
#
# The maintainer runs this in a terminal - not an agent, not CI. Install and
# remove refuse without a terminal (exit 2); --check works without one.
#
# The target is $OMNIGENT_CONFIG_HOME/config.yaml, else ~/.omnigent/config.yaml.
# Every key and every policy not named coding_harness__* is kept, the
# coding_harness__* policies are replaced as a set, and the old file is kept as
# config.yaml.bak-<timestamp> before any change. The result is validated with
# Omnigent's own parser and CEL compiler first; on failure nothing is written.
# --remove validates nothing: it deletes only our own policies, and a foreign
# policy Omnigent rejects must not keep them in.
#
# It never starts or stops Omnigent. Omnigent reads `policies:` only when its
# server starts - a run that changed the file says what to do about that.
#
# The merge itself is scripts/omnigent_policy.py, run with Omnigent's own
# Python ($OMNIGENT_PYTHON, else the interpreter the `omnigent` launcher names;
# `omnigent_policy.py --print-python` decides), because it needs Omnigent to validate.

set -euo pipefail

src=$(cd "$(dirname "$0")" && pwd)
tool="$src/../../scripts/omnigent_policy.py"
mode=install
case "${1:-}" in
  "") ;;
  --check) mode=check ;;
  --remove) mode=remove ;;
  *) echo "usage: $0 [--check | --remove]" >&2; exit 2 ;;
esac

if [ "$mode" != check ] && [ ! -t 0 ]; then
  echo "run this yourself in a terminal - not from an agent or CI" >&2
  exit 2
fi

# One resolution, in the module: any python3 can ask it (it needs only the
# standard library); the tests use the same function.
boot=$(command -v python3 || true)
if [ -z "$boot" ]; then
  echo "python3 not found on the PATH - it is needed to locate Omnigent's Python" >&2
  exit 2
fi
py=$("$boot" "$tool" --print-python) || py=""
if [ -z "$py" ]; then
  echo "Omnigent not found: no \$OMNIGENT_PYTHON and no usable 'omnigent' launcher on the PATH" >&2
  exit 2
fi

target="${OMNIGENT_CONFIG_HOME:-$HOME/.omnigent}/config.yaml"

case "$mode" in
  check) exec "$py" "$tool" --installed "$target" ;;
  remove) exec "$py" "$tool" --merge-config "$target" --remove ;;
  *) exec "$py" "$tool" --merge-config "$target" ;;
esac
