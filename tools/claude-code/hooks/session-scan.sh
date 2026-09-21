#!/bin/bash
# List the other live, interactive Claude Code sessions on this machine.
#
#   session-scan.sh <own_session_id> <own_cwd>
#
# One line per session, tab-separated:
#   relation  label  status  session_id  cwd
# relation: clash   = same checkout (same git toplevel) as <own_cwd>
#           sibling = same repository, other worktree
#           other   = anything else
# status:   arbeitet | wartet | <raw status>
#
# Source: ~/.claude/sessions/<pid>.json, written by Claude Code for every
# running session. A file whose process is gone, or whose pid now belongs to a
# different process (start time differs), is skipped. Used by the status line
# and by the parallel-sessions hook, so both see the same answer.

own_sid=$1
own_cwd=$2
sdir="$HOME/.claude/sessions"
[ -d "$sdir" ] || exit 0

gq() { git --no-optional-locks -C "$1" "${@:2}" 2>/dev/null; }
own_top=""; own_common=""
if [ -n "$own_cwd" ]; then
  own_top=$(gq "$own_cwd" rev-parse --show-toplevel)
  own_common=$(gq "$own_cwd" rev-parse --path-format=absolute --git-common-dir)
fi

for f in "$sdir"/*.json; do
  [ -e "$f" ] || continue
  IFS=$'\t' read -r opid osid ocwd oname ostatus okind ostart < <(
    jq -r '[.pid, .sessionId, .cwd, (.name // ""), (.status // ""), (.kind // ""), (.procStart // "")] | @tsv' "$f" 2>/dev/null)
  [ -z "$opid" ] || [ "$osid" = "$own_sid" ] || [ "$okind" != "interactive" ] && continue
  kill -0 "$opid" 2>/dev/null || continue
  if [ -n "$ostart" ]; then
    # The registry stores the start time in UTC and English; ps localises both.
    live=$(TZ=UTC LC_ALL=C ps -o lstart= -p "$opid" 2>/dev/null | tr -s ' ' | sed 's/^ //; s/ $//')
    [ "$live" != "$(printf '%s' "$ostart" | tr -s ' ')" ] && continue
  fi
  label=${oname:-$(basename "$ocwd")}
  case "$ostatus" in busy) st="arbeitet" ;; idle) st="wartet" ;; *) st=$ostatus ;; esac
  rel="other"
  if [ -n "$own_top" ]; then
    otop=$(gq "$ocwd" rev-parse --show-toplevel)
    ocommon=$(gq "$ocwd" rev-parse --path-format=absolute --git-common-dir)
    if [ -n "$otop" ] && [ "$otop" = "$own_top" ]; then rel="clash"
    elif [ -n "$ocommon" ] && [ "$ocommon" = "$own_common" ]; then rel="sibling"
    fi
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$rel" "$label" "$st" "$osid" "$ocwd"
done
exit 0
