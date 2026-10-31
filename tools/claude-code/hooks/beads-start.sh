#!/bin/bash
# The repository's SessionStart hook: merged completion trailers close before
# the prime context is built (bead coding-harness-l1if).
#
# .claude/settings.json wires THIS script in place of the old direct
# `tools/bd prime --hook-json`. The order matters: the starting session is the
# tracker writer (house rule 4), so it reconciles first and the prime context
# already reflects the closures. This is a repository hook, not part of the
# user-level installed set — tools/claude-code/install.sh does not wire it.
#
# Writer eligibility is conservative, on purpose (decisions.md, "Only the
# tracker writer runs it"):
#   - a recap child never writes (CLAUDE_RECAP_CHILD, as in every hook here),
#   - a start after compaction never writes,
#   - a missing session identity, a missing jq or a failed session scan can
#     never mean "sole writer" — the write is skipped,
#   - another live session in the same checkout or a sibling worktree skips
#     the write (hooks/session-scan.sh, relations clash and sibling; sessions
#     in unrelated repositories are not this tracker's writers).
# The designated writer can still reconcile in its merge step. Skips and
# failures stay visible in German; a successful no-op run is quiet. The prime
# context is emitted in every case that can produce one, with the skip or
# failure note folded into the JSON — never as plain stdout around it, and a
# reconciliation failure never reads as "nothing pending".

hook_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$hook_dir/../../.." && pwd)
cd "$repo_root" || exit 1

RECONCILE_TIMEOUT=${BEADS_START_RECONCILE_TIMEOUT:-180}
SCAN_TIMEOUT=${BEADS_START_SCAN_TIMEOUT:-20}
PRIME_TIMEOUT=${BEADS_START_PRIME_TIMEOUT:-30}

# run_bounded <seconds> <stdin-file|-> <stdout-file> <stderr-file> <command...>
# Runs <command> with its streams bound to files and a watchdog; sets RUN_RC
# (124 = the watchdog ended it). A hook must never hang a session start.
run_bounded() {
  local secs=$1 sin=$2 sout=$3 serr=$4
  shift 4
  local flag pid watchdog
  flag=$(mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX")
  rm -f "$flag"
  if [ "$sin" = "-" ]; then
    "$@" >"$sout" 2>"$serr" &
  else
    "$@" <"$sin" >"$sout" 2>"$serr" &
  fi
  pid=$!
  # The watchdog's stdio stays away from the caller's: when it is killed, its
  # `sleep` is left orphaned, and an inherited stdout would keep the session's
  # pipe open after this hook has exited — the reader waits for an EOF that
  # never comes.
  ( sleep "$secs"; if kill -0 "$pid" 2>/dev/null; then kill "$pid" 2>/dev/null; : >"$flag"; fi ) \
    >/dev/null 2>&1 </dev/null &
  watchdog=$!
  wait "$pid" 2>/dev/null
  RUN_RC=$?
  kill "$watchdog" 2>/dev/null
  wait "$watchdog" 2>/dev/null
  [ -e "$flag" ] && RUN_RC=124
  rm -f "$flag"
  return 0
}

input=$(cat)

jq_pick() { printf '%s' "$input" | jq -r "$1 // empty" 2>/dev/null; }

sid=$(jq_pick '.session_id')
cwd=$(jq_pick '.cwd')
source=$(jq_pick '.source')
[ -z "$source" ] && source=startup

# ── may this session write? Conservative: only a clear yes writes. ──────────
grund=""
[ -n "$CLAUDE_RECAP_CHILD" ] && grund="Kindprozess des Recaps"
[ -z "$grund" ] && [ "$source" = "compact" ] && grund="Start nach der Kompaktierung"
if [ -z "$grund" ] && { [ -z "$sid" ] || [ -z "$cwd" ]; }; then
  grund="Sitzungs-Identität unvollständig (session_id/cwd fehlen in der Hook-Eingabe)"
fi
if [ -z "$grund" ] && ! command -v jq >/dev/null 2>&1; then
  grund="jq fehlt — das Ergebnis des Sitzungs-Scans wäre nicht lesbar"
fi
if [ -z "$grund" ] && [ ! -x "$hook_dir/session-scan.sh" ]; then
  grund="Sitzungs-Scan fehlt oder ist nicht ausführbar"
fi
if [ -z "$grund" ]; then
  scan_out=$(mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX")
  # session-scan.sh reports its lines on stdout: they land in scan_out; the
  # scan's own chatter goes to /dev/null.
  run_bounded "$SCAN_TIMEOUT" - "$scan_out" /dev/null "$hook_dir/session-scan.sh" "$sid" "$cwd"
  if [ "$RUN_RC" -ne 0 ]; then
    grund="Sitzungs-Scan fehlgeschlagen (Exit $RUN_RC)"
  elif grep -Eq $'^clash\t|^sibling\t' "$scan_out" 2>/dev/null; then
    grund="weitere Sitzung im selben Repository aktiv"
  fi
  rm -f "$scan_out"
fi
if [ -z "$grund" ] && [ ! -f "$repo_root/scripts/close_merged_beads.py" ]; then
  grund="der Abgleich fehlt: scripts/close_merged_beads.py"
fi
if [ -z "$grund" ] && ! command -v python3 >/dev/null 2>&1; then
  grund="python3 fehlt"
fi

hinweis=""
if [ -n "$grund" ]; then
  hinweis="Hinweis: Beads-Abgleich übersprungen ($grund) — diese Session schreibt den Tracker nicht; die erste Sitzung im Repository gleicht beim Start ab."
fi

# ── the reconciliation itself, synchronously and before prime ───────────────
if [ -z "$grund" ]; then
  recon_out=$(mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX")
  recon_err=$(mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX")
  run_bounded "$RECONCILE_TIMEOUT" - "$recon_out" "$recon_err" \
    python3 "$repo_root/scripts/close_merged_beads.py" --write
  recon_rc=$RUN_RC
  if [ "$recon_rc" -ne 0 ]; then
    if [ "$recon_rc" -eq 124 ]; then
      hinweis="⚠ Beads-Abgleich nach ${RECONCILE_TIMEOUT}s abgebrochen — es ist offen, ob mergede Abschlüsse ausstehen. Nicht als „nichts offen“ lesen. Bericht: make close-merged · Schreiben: make close-merged ARGS=--write"
    else
      hinweis="⚠ Beads-Abgleich fehlgeschlagen (Exit $recon_rc) — es ist offen, ob mergede Abschlüsse ausstehen. Nicht als „nichts offen“ lesen. Bericht: make close-merged · Schreiben: make close-merged ARGS=--write"
    fi
    details=$(head -c 2000 "$recon_out" 2>/dev/null; head -c 2000 "$recon_err" 2>/dev/null)
    [ -n "$details" ] && hinweis="$hinweis
$details"
  fi
  rm -f "$recon_out" "$recon_err"
fi

# ── the prime context, in every case that can produce one ───────────────────
p_in=$(mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX")
p_out=$(mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX")
p_err=$(mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX")
trap 'rm -f "$p_in" "$p_out" "$p_err"' EXIT
printf '%s' "$input" >"$p_in"
if [ ! -x "$repo_root/tools/bd" ]; then
  echo "⚠ Beads-Start-Hook: das gepinnte tools/bd fehlt ($repo_root/tools/bd) — kein Prime-Kontext." >&2
  exit 1
fi
run_bounded "$PRIME_TIMEOUT" "$p_in" "$p_out" "$p_err" "$repo_root/tools/bd" prime --hook-json
if [ "$RUN_RC" -ne 0 ]; then
  echo "⚠ Beads-Start-Hook: tools/bd prime --hook-json fehlgeschlagen (Exit $RUN_RC) — kein Prime-Kontext." >&2
  exit 1
fi
# Without jq the old behaviour holds: prime's stdout passes through untouched.
if command -v jq >/dev/null 2>&1 && ! jq -e . "$p_out" >/dev/null 2>&1; then
  echo "⚠ Beads-Start-Hook: tools/bd prime --hook-json lieferte kein gültiges JSON — kein Prime-Kontext." >&2
  exit 1
fi
if [ -n "$hinweis" ]; then
  printf '%s\n' "$hinweis" >&2
  if command -v jq >/dev/null 2>&1; then
    jq --arg n "$hinweis" \
      '.hookSpecificOutput.additionalContext = ((.hookSpecificOutput.additionalContext // "") + "\n\n" + $n)' "$p_out"
    exit 0
  fi
fi
cat "$p_out"
exit 0
