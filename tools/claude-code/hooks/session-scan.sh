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
strict=${3:-}
if [ "$strict" = "--strict" ]; then
  # Startup may trust an empty scan only after all registry reads succeeded.
  [ -d "$sdir" ] && [ -r "$sdir" ] && [ -x "$sdir" ] || exit 1
else
  [ -d "$sdir" ] || exit 0
fi

gq() { git --no-optional-locks -C "$1" "${@:2}" 2>/dev/null; }
own_top=""; own_common=""
if [ -n "$own_cwd" ]; then
  own_top=$(gq "$own_cwd" rev-parse --show-toplevel)
  own_common=$(gq "$own_cwd" rev-parse --path-format=absolute --git-common-dir)
fi
if [ "$strict" = "--strict" ]; then
  [ -n "$own_top" ] && [ -n "$own_common" ] || exit 1
fi

for f in "$sdir"/*.json; do
  if [ "$strict" = "--strict" ] && { [ -e "$f" ] || [ -L "$f" ]; }; then
    jq -e 'type == "object" and
      (.pid | type == "number" and . > 0 and . == floor) and
      (.sessionId | type == "string" and length > 0) and
      (.cwd | type == "string" and length > 0) and
      (.kind | type == "string" and length > 0)' "$f" >/dev/null 2>&1 || exit 1
  fi
  [ -e "$f" ] || continue
  # Feldtrennung ohne Kollaps (bead hit): `IFS=$'\t' read` liess leere Felder
  # (Session ohne Namen oder Status) auf die Nachbarn rutschen — die Session
  # galt dann als nicht-interaktiv und wurde nie als Clash gemeldet. NUL
  # ueberlebt jedes Feld, und `read -d ''` (nicht mapfile: bash 3.2 auf macOS
  # hat keins) bricht an jedem einzelnen. Alle Felder vorher leeren, damit
  # ein kurzer Datensatz nicht vom Vorgaenger erbt.
  opid=""; osid=""; ocwd=""; oname=""; ostatus=""; okind=""; ostart=""
  i=0
  while IFS= read -r -d '' feld; do
    case $i in
      0) opid=$feld ;;   1) osid=$feld ;;   2) ocwd=$feld ;;
      3) oname=$feld ;;  4) ostatus=$feld ;; 5) okind=$feld ;;
      6) ostart=$feld ;;
    esac
    i=$((i + 1))
  done < <(
    jq -j '[.pid, .sessionId, .cwd, (.name // ""), (.status // ""), (.kind // ""), (.procStart // "")]
           | map(tostring) | join("\u0000") + "\u0000"' "$f" 2>/dev/null)
  if [ "$strict" = "--strict" ] && [ "$i" -ne 7 ]; then exit 1; fi
  [ -z "$opid" ] || [ "$osid" = "$own_sid" ] || [ "$okind" != "interactive" ] && continue
  kill -0 "$opid" 2>/dev/null || continue
  if [ -n "$ostart" ]; then
    # The registry stores the start time in UTC and English; ps localises both.
    live=$(TZ=UTC LC_ALL=C ps -o lstart= -p "$opid" 2>/dev/null | tr -s ' ' | sed 's/^ //; s/ $//')
    [ "$live" != "$(printf '%s' "$ostart" | tr -s ' ')" ] && continue
  fi
  label=${oname:-$(basename "$ocwd")}
  # Das Zeilenformat ist tab-separiert: Tabs und Zeilenenden im Namen wuerden
  # Zellen verschieben. Der alte @tsv-Pfad entkam ihnen, also entkommt der
  # neue sie genauso — sichtbar als \\t, nicht als Formatbruch.
  label=${label//$'\t'/\\t}
  label=${label//$'\n'/ }
  case "$ostatus" in busy) st="arbeitet" ;; idle) st="wartet" ;; *) st=$ostatus ;; esac
  st=${st//$'\t'/\\t}
  st=${st//$'\n'/ }
  rel="other"
  if [ -n "$own_top" ]; then
    outside_git=false
    if [ "$strict" = "--strict" ]; then
      # A removed working directory cannot belong to a current checkout.
      # Otherwise only Git's explicit non-repository diagnostic establishes
      # that the peer is unrelated; all other failures remain uncertain.
      if [ ! -e "$ocwd" ]; then
        outside_git=true
        otop=""; top_rc=0
      else
        otop=$(LC_ALL=C git --no-optional-locks -C "$ocwd" rev-parse --show-toplevel 2>&1)
        top_rc=$?
        if [ "$top_rc" -ne 0 ] &&
          [ "$otop" = "fatal: not a git repository (or any of the parent directories): .git" ]; then
          outside_git=true
          otop=""; top_rc=0
        fi
      fi
    else
      otop=$(gq "$ocwd" rev-parse --show-toplevel)
      top_rc=$?
    fi
    if [ "$outside_git" = true ]; then
      ocommon=""; common_rc=0
    else
      ocommon=$(gq "$ocwd" rev-parse --path-format=absolute --git-common-dir)
      common_rc=$?
    fi
    if [ "$strict" = "--strict" ]; then
      # A live peer with unreadable Git metadata has unknown ownership.
      # Failed commands can emit output; require success as well as a value.
      if [ "$outside_git" != true ]; then
        [ "$top_rc" -eq 0 ] && [ "$common_rc" -eq 0 ] &&
          [ -n "$otop" ] && [ -n "$ocommon" ] || exit 1
      fi
    fi
    if [ -n "$otop" ] && [ "$otop" = "$own_top" ]; then rel="clash"
    elif [ -n "$ocommon" ] && [ "$ocommon" = "$own_common" ]; then rel="sibling"
    fi
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$rel" "$label" "$st" "$osid" "$ocwd"
done
exit 0
