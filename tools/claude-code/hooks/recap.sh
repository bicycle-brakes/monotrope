#!/bin/bash
# A rolling recap of the session, and the automatic note under the handover.
#
#   recap.sh prompt   UserPromptSubmit: note what the session is working on now
#   recap.sh stop     Stop (async): one Haiku call updates both
#                     - the one-line recap, shown by ~/.claude/statusline.sh
#                     - the session note, stored by ~/.claude/hooks/handover.sh
#                       (a safety net for a session that ends without writing
#                       its handover file; never the handover itself)
#
# Files: ~/.claude/recaps/<session_id>.{txt,now,base,entry}, removed after 7
# days. The Haiku call runs with no user settings (so no hooks: no recursion),
# no tools, no session persistence, from a private scratch directory
# (mktemp -d, mode 0700, removed afterwards): a world-writable /tmp would let
# any local process plant project settings the child would happily load
# (bead hit).

[ -n "$CLAUDE_RECAP_CHILD" ] && exit 0          # never recurse from the child

mode=$1
input=$(cat)
sid=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
[ -z "$sid" ] && exit 0
dir="$HOME/.claude/recaps"
ndir="$HOME/.claude/session-notes"
mkdir -p "$dir"

# BSD stat (macOS) vs GNU stat (Linux): nur eine Form gilt je Plattform, und
# GNU liest -f %m als Dateisystem-Status (mehrzeilig, Exit 0) — als mtime
# geisterte hier dieser Dump (bead hit). GNU zuerst, dann BSD; ohne lesbare
# mtime gilt eine Datei als ewig alt.
mtime() {
  stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0
}

case "$mode" in
  prompt)
    p=$(printf '%s' "$input" | jq -r '.prompt // empty' | tr '\n\t' '  ' | cut -c1-1000)
    # Background notices (finished agents, system events) arrive as prompts too;
    # they are not what the person asked for.
    case "$p" in ""|"<task-notification>"*|"<system-reminder>"*|"<agent-message"*) exit 0 ;; esac
    printf '%s' "$p" > "$dir/$sid.now"
    ;;

  stop)
    last=$(printf '%s' "$input" | jq -r '.last_assistant_message // empty' | head -c 6000)
    [ -z "$last" ] && exit 0
    cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')

    # One update at a time per session. A lock older than five minutes is dead
    # (its holder is gone or stuck) and may be removed; a FRESH one is never
    # stolen. The old loop fell through after 90 seconds and wrote anyway —
    # worse, its EXIT trap removed the lock another run then held (bead hit).
    # Without ownership this run drops out instead of writing in parallel.
    # RECAP_LOCK_SEKUNDEN kuerzt die Wartezeit fuer Tests (Produktivwert 90).
    lock="$dir/$sid.lock"
    besitz=""
    for _ in $(seq 1 "${RECAP_LOCK_SEKUNDEN:-90}"); do
      if mkdir "$lock" 2>/dev/null; then besitz=1; break; fi
      [ $(( $(date +%s) - $(mtime "$lock") )) -gt 300 ] && rmdir "$lock" 2>/dev/null
      sleep 1
    done
    [ -n "$besitz" ] || exit 0
    arbeitsplatz=$(mktemp -d)
    trap 'rm -rf "$arbeitsplatz"; rmdir "$lock" 2>/dev/null' EXIT

    t0=$(mtime "$dir/$sid.now")
    prev=$(cat "$dir/$sid.txt" 2>/dev/null)
    asked=$(cat "$dir/$sid.now" 2>/dev/null)
    # The note so far: this session's own, else the one it continues.
    base=$(cat "$dir/$sid.base" 2>/dev/null)
    pnote=$(cat "$ndir/$sid.md" 2>/dev/null)
    [ -z "$pnote" ] && [ -n "$base" ] && pnote=$(cat "$ndir/$base.md" 2>/dev/null)

    prompt="Du pflegst zwei Notizen einer Claude-Code-Session für eine Person mit ADHS.

Bisheriger Recap: ${prev:-(noch keiner)}

Bisherige Notiz:
${pnote:-(noch keine)}

Letzte Anfrage der Person: ${asked:-(unbekannt)}

Letzte Antwort von Claude (gekürzt):
${last}

Aktualisiere beide. Antworte genau in diesem Format, ohne Einleitung, ohne Codeblock:

RECAP: Erledigt: … · Nächstes: …
## Wo wir stehen
Zwei bis drei Sätze: Ziel und Stand.
## Nächster Schritt
Ein Satz: der konkret nächste Schritt.
## Was ich von dir brauche
Eine offene Entscheidung oder Frage an die Person, oder „gerade nichts“.
## Offen
- höchstens fünf Punkte, die ausdrücklich als offen genannt wurden

Regeln:
- Deutsch. Die RECAP-Zeile höchstens 170 Zeichen.
- Keine IDs oder Kürzel ohne kurze Erklärung; Dateinamen und IDs nur in Klammern hinter einer Aussage.
- Nichts erfinden und nichts ergänzen: Jeder Punkt muss wörtlich oder sinngemäß in Notiz, Anfrage oder Antwort stehen. Keine eigenen Ideen, Empfehlungen oder naheliegenden Folgeaufgaben. Lieber weniger Punkte; steht nichts Offenes da, schreibe „- nichts genannt“.
- Zahlen nur mit Stichtag.
- Behalte, was aus der bisherigen Notiz noch gilt; streiche, was erledigt ist."

    # The child runs from the private scratch directory with project settings
    # as the only source — and there are none: the directory is empty and ours.
    out=$(cd "$arbeitsplatz" && printf '%s' "$prompt" \
      | CLAUDE_RECAP_CHILD=1 claude -p --model haiku --no-session-persistence \
          --setting-sources project --tools "" 2>/dev/null | grep -v '^```')

    recap=$(printf '%s\n' "$out" | grep -m1 '^RECAP:' | sed 's/^RECAP:[ ]*//' \
      | tr '\n' ' ' | sed 's/  */ /g; s/^ //; s/ $//' | cut -c1-220)
    if [ -n "$recap" ]; then
      printf '%s' "$recap" > "$dir/$sid.txt.tmp" && mv "$dir/$sid.txt.tmp" "$dir/$sid.txt"
    fi
    printf '%s\n' "$out" | awk '/^## Wo wir stehen/ { p = 1 } p' \
      | "$HOME/.claude/hooks/handover.sh" note "$sid" "$cwd" "$t0"

    rm -f "$dir/$sid.now"
    find "$dir" -type f -mtime +7 -delete 2>/dev/null
    ;;
esac
exit 0
