#!/bin/bash
# Install the maintainer's Claude Code session display into ~/.claude.
#
#   tools/claude-code/install.sh           copy the files, merge settings.json
#   tools/claude-code/install.sh --check   say what differs; change nothing
#
# This directory is the source. Change a file here, then reinstall; a file
# edited only in ~/.claude is overwritten by the next install. --check shows
# that first, and every file an install replaces is kept beside it as
# <name>.bak-<timestamp>.
#
# settings.json is merged, not replaced: statusLine is set, and each hook of
# ./settings.json is added unless a hook with the same command is there
# already. Everything else in the file is left as it is.

set -euo pipefail

src=$(cd "$(dirname "$0")" && pwd)
dst="$HOME/.claude"
stamp=$(date +%Y%m%d-%H%M%S)
files=(
  statusline.sh
  hooks/recap.sh
  hooks/handover.sh
  hooks/parallel-sessions.sh
  hooks/session-scan.sh
  skills/handover/SKILL.md
)

for tool in jq git perl; do
  command -v "$tool" >/dev/null || { echo "missing: $tool (required)" >&2; exit 2; }
done
command -v claude >/dev/null || echo "note: 'claude' not on PATH — the rolling recap and the session note stay empty"
command -v bd >/dev/null || echo "note: 'bd' not on PATH — the beads line stays hidden"

# The settings as they would be after an install.
merged_settings() {
  { if [ -s "$dst/settings.json" ]; then cat "$dst/settings.json"; else echo '{}'; fi; } \
  | jq --slurpfile frag "$src/settings.json" '
    def commands($groups): [ $groups[]?.hooks[]?.command ];
    $frag[0] as $f
    | .statusLine = $f.statusLine
    | .hooks = reduce ($f.hooks | to_entries[]) as $e ((.hooks // {});
        (.[$e.key] // []) as $have
        | .[$e.key] = $have + [ $e.value[]
            | select(.hooks[0].command as $c | commands($have) | any(.[]; . == $c) | not) ])
  '
}

if [ "${1:-}" = "--check" ]; then
  drift=0
  for f in "${files[@]}"; do
    if [ ! -e "$dst/$f" ]; then echo "missing    ~/.claude/$f"; drift=1
    elif ! cmp -s "$src/$f" "$dst/$f"; then echo "differs    ~/.claude/$f"; drift=1
    fi
  done
  if ! diff -q <(jq -S . "$dst/settings.json" 2>/dev/null || echo '{}') <(merged_settings | jq -S .) >/dev/null; then
    echo "differs    ~/.claude/settings.json (status line or hooks)"; drift=1
  fi
  [ "$drift" -eq 0 ] && echo "in sync with $src"
  exit "$drift"
fi

for f in "${files[@]}"; do
  mkdir -p "$(dirname "$dst/$f")"
  if [ -e "$dst/$f" ] && ! cmp -s "$src/$f" "$dst/$f"; then
    cp -p "$dst/$f" "$dst/$f.bak-$stamp"
    echo "kept       ~/.claude/$f.bak-$stamp"
  fi
  cp "$src/$f" "$dst/$f"
  case "$f" in *.sh) chmod +x "$dst/$f" ;; esac
  echo "installed  ~/.claude/$f"
done

new=$(merged_settings)
if [ ! -s "$dst/settings.json" ] || ! diff -q <(jq -S . "$dst/settings.json") <(printf '%s' "$new" | jq -S .) >/dev/null; then
  [ -s "$dst/settings.json" ] && cp -p "$dst/settings.json" "$dst/settings.json.bak-$stamp" \
    && echo "kept       ~/.claude/settings.json.bak-$stamp"
  printf '%s\n' "$new" > "$dst/settings.json.tmp" && mv "$dst/settings.json.tmp" "$dst/settings.json"
  echo "merged     ~/.claude/settings.json"
else
  echo "unchanged  ~/.claude/settings.json"
fi
echo "Restart Claude Code (or open /hooks) for the hooks to take effect."
