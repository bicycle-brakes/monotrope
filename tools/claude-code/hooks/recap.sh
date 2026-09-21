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
# no tools, no session persistence, from /tmp.

[ -n "$CLAUDE_RECAP_CHILD" ] && exit 0          # never recurse from the child

mode=$1
input=$(cat)
sid=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
[ -z "$sid" ] && exit 0
dir="$HOME/.claude/recaps"
ndir="$HOME/.claude/session-notes"
mkdir -p "$dir"

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

    # One update at a time per session; a lock older than five minutes is dead.
    lock="$dir/$sid.lock"
    [ -d "$lock" ] && [ $(( $(date +%s) - $(stat -f %m "$lock" 2>/dev/null || echo 0) )) -gt 300 ] && rmdir "$lock"
    for _ in $(seq 1 90); do mkdir "$lock" 2>/dev/null && break; sleep 1; done
    trap 'rmdir "$lock" 2>/dev/null' EXIT

    t0=$(stat -f %m "$dir/$sid.now" 2>/dev/null || echo 0)
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

    out=$(cd /tmp && printf '%s' "$prompt" \
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
