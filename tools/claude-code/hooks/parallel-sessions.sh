#!/bin/bash
# Tell Claude when another session works in the same checkout.
#
#   parallel-sessions.sh start    SessionStart: always report a clash
#   parallel-sessions.sh prompt   UserPromptSubmit: report only when the set of
#                                 clashing sessions changed since last reported
#
# Silent when there is no clash. Two sessions editing one working tree
# overwrite each other without either noticing; the model is asked to warn the
# person before changing files, not to refuse.

[ -n "$CLAUDE_RECAP_CHILD" ] && exit 0

mode=$1
input=$(cat)
sid=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "$sid" ] || [ -z "$cwd" ] && exit 0

clashes=$("$HOME/.claude/hooks/session-scan.sh" "$sid" "$cwd" | awk -F'\t' '$1 == "clash"')
state="$HOME/.claude/recaps/$sid.clash"
mkdir -p "$(dirname "$state")"

if [ -z "$clashes" ]; then
  rm -f "$state"
  exit 0
fi

key=$(printf '%s' "$clashes" | cut -f4 | sort | tr '\n' ' ')
if [ "$mode" = "prompt" ] && [ "$(cat "$state" 2>/dev/null)" = "$key" ]; then
  exit 0                                         # already told, nothing changed
fi
printf '%s' "$key" > "$state"

top=$(git --no-optional-locks -C "$cwd" rev-parse --show-toplevel 2>/dev/null)
list=$(printf '%s\n' "$clashes" | awk -F'\t' '{ printf "%s- %s (Status: %s)", (NR > 1 ? "\n" : ""), $2, $3 }')
event="UserPromptSubmit"; [ "$mode" = "start" ] && event="SessionStart"

msg="Parallele Sessions im selben Checkout (${top:-$cwd}):
${list}

Diese Session teilt sich das Arbeitsverzeichnis mit der oder den Sessions oben. Zwei Sessions im selben Checkout können sich Änderungen gegenseitig überschreiben, ohne es zu merken.
Bevor du in diesem Checkout Dateien änderst, Commits machst oder den Branch wechselst: Weise die Person kurz und deutlich darauf hin, nenne die andere Session beim Namen und frage, ob du fortfahren sollst. Schlage bei Bedarf einen eigenen Worktree vor. Reines Lesen ist unbedenklich."

jq -n --arg e "$event" --arg m "$msg" '{hookSpecificOutput: {hookEventName: $e, additionalContext: $m}}'
exit 0
