#!/bin/bash
# The entry point of a session, and the safety net under the handover.
#
#   handover.sh start               SessionStart: show the person where things
#                                   stand; give Claude the latest handover
#   handover.sh show [CWD]          print the entry a new session would see
#   handover.sh where [CWD]         print the repository's handover convention
#   handover.sh note SID CWD T0     store the automatic session note (stdin);
#                                   T0 = when the turn began (recap.sh, Stop)
#
# The handover is a file in the repository, never the chat (coding-harness
# AGENTS.md, "Communication and session continuity"). Two conventions exist:
#   docs/journal/handover/   coding-harness, portfolio: dated files with the
#                            schema of scripts/handover_schema.py
#   journal/                 lakeswitch: append-only session notes
# The newest file there is what a session starts from. Writing one is the
# /uebergabe skill's job, not this script's.
#
# The automatic note (~/.claude/session-notes/<sid>.md, Haiku, after every
# answer) is only a safety net for a session that ended without a handover. It
# is shown when the last session kept working after the newest handover, and it
# is never presented as a handover. Git state and beads are measured at start:
# a summary ages, the working tree does not.
#
# Since bead hit: the handover's CONTENT is injected into the session's context
# only for trusted repositories. Whoever controls a clone controls journal/*.md
# — a bare journal/ directory must never pipe its newest file into every
# session starting there. ~/.claude/handover-trust lists one regex per line,
# matched against the origin URL (override the path with $HANDOVER_TRUST).
# Without a hit the session sees metadata only (path, title, age) and reads
# the file itself when it needs it.

[ -n "$CLAUDE_RECAP_CHILD" ] && exit 0

ndir="$HOME/.claude/session-notes"
rdir="$HOME/.claude/recaps"
mkdir -p "$ndir" "$rdir"
now=$(date +%s)

gq() { git --no-optional-locks -C "$1" "${@:2}" 2>/dev/null; }
# BSD stat (macOS) nimmt -f %m als mtime; GNU stat (Linux, CI) liest dasselbe
# als Dateisystem-Status und druckt einen MEHRZEILIGEN Dump — mit Exit 0, so
# dass der Fallback nie greift und der Dump als mtime durch die TSV-Zerlegung
# geisterte (bead hit, CI-Lauf zu PR #28). GNU-Form zuerst, dann BSD.
mtime_of() {
  stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0
}
# One line of at most $1 characters: the first sentence when it fits, else cut
# at a word boundary. Never mid-word — a torn word is harder to read than none.
oneline() {
  MAX=$1 perl -CSD -Mutf8 -0777 -ne '
    s/\*\*//g; s/\s+/ /g; s/^\s+|\s+$//g;
    $_ = $1 if /^(.{20,}?[.!?])(?=\s|$)/;
    if (length > $ENV{MAX}) { $_ = substr($_, 0, $ENV{MAX} - 1); s/\s+\S*$//; $_ .= "…" }
    print'
}

# When a handover was last changed: its commit time when committed and clean,
# since a checkout rewrites the file time; otherwise the file time.
doc_time() {
  local t=""
  [ -z "$(gq "$2" status --porcelain -- "$1")" ] && t=$(gq "$2" log -1 --format=%ct -- "$1")
  printf '%s' "${t:-$(mtime_of "$1")}"
}

answers() { [ "$1" -eq 1 ] && echo "Antwort" || echo "Antworten"; }

ago() {
  local s=$1
  if   [ "$s" -lt 120 ];    then echo "gerade eben"
  elif [ "$s" -lt 3600 ];   then echo "vor $(( s / 60 )) min"
  elif [ "$s" -lt 172800 ]; then echo "vor $(( s / 3600 )) h"
  else                           echo "vor $(( s / 86400 )) Tagen"; fi
}

# ── the repository's handover ────────────────────────────────────────────────
convention() {  # top → "harness <dir>" | "journal <dir>" | nothing
  if   [ -d "$1/docs/journal/handover" ]; then printf 'harness\t%s\n' "$1/docs/journal/handover"
  elif [ -d "$1/journal" ];               then printf 'journal\t%s\n' "$1/journal"
  fi
}

# Handover files, newest first: by the date the file name carries, then mtime.
list_handovers() {
  local f base d m
  for f in "$1"/*.md; do
    [ -e "$f" ] || continue
    base=$(basename "$f")
    case "$base" in _*|README*|INDEX*) continue ;; esac
    m=$(mtime_of "$f")
    d=$(printf '%s' "$base" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}')
    [ -z "$d" ] && d=$(date -r "$m" +%F)
    printf '%s\t%s\t%s\n' "$d" "$m" "$f"
  done | sort -r | cut -f3
}

doc_title() {
  local t
  t=$(awk 'NR == 1 && $0 != "---" { exit } NR > 1 && $0 == "---" { exit }
           /^title:/ { sub(/^title:[ ]*"?/, ""); sub(/"[ ]*$/, ""); print; exit }' "$1")
  [ -z "$t" ] && t=$(grep -m1 '^# ' "$1" | sed 's/^# *//')
  printf '%s' "${t:-$(basename "$1" .md)}"
}

# First paragraph (or first list item) under the last heading that names the
# next step — the last, because an addendum below the original record
# supersedes its plan. The headings in use vary: "Next step", "Beim nächsten
# Mal zuerst", "Empfohlener Einstieg", "What to do first", "How to resume".
next_step() {
  awk '
    function close_para() { if (inn && started) last = para }
    /^#+ / { close_para(); h = tolower($0)
             inn = (h ~ /next step|next action|what to do first|how to resume|resume it|nächste[rn]? schritt|zuerst zu tun|beim nächsten mal|empfohlener einstieg/)
             para = ""; started = 0; next }
    inn && started && /^[ ]*([0-9]+[.)]|[-*]) / { close_para(); inn = 0; next }
    inn { line = $0; sub(/^[ ]*([0-9]+[.)]|[-*]) /, "", line)
          if (NF) { para = para (started ? " " : "") line; started = 1 }
          else if (started) { close_para(); inn = 0 } }
    END { close_para(); print last }' "$1"
}

# ── the automatic note ───────────────────────────────────────────────────────
# Newest note whose <field> equals <value>, other than <own sid>.
newest_note() {
  jq -r --arg f "$1" --arg v "$2" --arg s "$3" \
    'select(.[$f] == $v and .session_id != $s) | "\(.updated)\t\(.session_id)"' \
    "$ndir"/*.json 2>/dev/null | sort -rn | head -1 | cut -f2
}

section() { awk -v h="## $2" '$0 == h { p = 1; next } /^## / { p = 0 } p && NF' "$1"; }

session_name() {
  jq -r --arg s "$1" 'select(.sessionId == $s) | .name // empty' \
    "$HOME"/.claude/sessions/*.json 2>/dev/null | head -1
}

# ── beads ────────────────────────────────────────────────────────────────────
# In progress, as JSON: the status line's cache when fresh, else the tracker
# itself (the repository's pinned wrapper when it has one), given four seconds.
# Sets beads_state: read | unread | none.
beads_json() {
  local root=$1 key cache out p i=0 bdc=bd
  beads_state=none
  [ -n "$root" ] && [ -d "$root/.beads" ] || return
  beads_state=unread
  key=$(printf '%s' "$root" | shasum | cut -c1-12)
  cache="${TMPDIR:-/tmp}/claude-statusline/beads-$key.json"
  if [ -s "$cache" ] && [ $(( now - $(mtime_of "$cache") )) -lt 600 ]; then
    beads_state=read; cat "$cache"; return
  fi
  [ -x "$root/tools/bd" ] && bdc="$root/tools/bd"
  command -v "$bdc" >/dev/null 2>&1 || return
  out=$(mktemp)
  "$bdc" -C "$root" list --status in_progress --brief --skip-labels --json -q > "$out" 2>/dev/null &
  p=$!
  while kill -0 "$p" 2>/dev/null && [ $i -lt 40 ]; do sleep 0.1; i=$((i + 1)); done
  if kill -0 "$p" 2>/dev/null; then kill "$p" 2>/dev/null
  elif jq -e . "$out" >/dev/null 2>&1; then beads_state=read; cat "$out"
  fi
  rm -f "$out"
}

# ── the entry ────────────────────────────────────────────────────────────────
# Sets $visible (for the person), $context (for Claude), $entry (status line).
# Returns 1 when there is nothing worth saying.
render() {
  local sid=$1 cwd=$2 source=$3
  local top common main_top repo branch conv="" hdir="" hfile="" htime=0
  top=$(gq "$cwd" rev-parse --show-toplevel)
  common=$(gq "$cwd" rev-parse --path-format=absolute --git-common-dir)
  [ -n "$top" ] && IFS=$'\t' read -r conv hdir < <(convention "$top")
  [ -n "$hdir" ] && hfile=$(list_handovers "$hdir" | head -1)
  [ -n "$hfile" ] && htime=$(doc_time "$hfile" "$top")

  # The note of the last session here: this session's own on resume, else the
  # newest of this checkout.
  local npick=""
  [ "$source" = resume ] && [ -s "$ndir/$sid.md" ] && npick=$sid
  [ -z "$npick" ] && npick=$(newest_note checkout "${top:-$cwd}" "$sid")
  [ -z "$top" ] && [ -z "$npick" ] && return 1

  # Where.
  if [ -n "$top" ]; then
    main_top=$(dirname "$common"); repo=$(basename "$main_top")
    [ "$main_top" != "$top" ] && repo="$repo [worktree $(basename "$top")]"
    branch=$(gq "$cwd" branch --show-current)
    [ -z "$branch" ] && branch="detached@$(gq "$cwd" rev-parse --short HEAD)"
    visible="↪ Einstieg · $repo ⎇ $branch"
  else
    visible="↪ Einstieg · ${cwd/#$HOME/~}"
  fi

  # The handover. Its CONTENT flows into Claude's context — in a cloned
  # repository that is an invitation (bead hit): whoever controls the clone
  # controls journal/*.md. Content therefore flows only when the person has
  # allowed the repository (see the trust note in the header). Without a hit:
  # metadata only — the person still sees title and age, Claude reads the file
  # itself when it needs it.
  local trust="${HANDOVER_TRUST:-$HOME/.claude/handover-trust}"
  local vertraut="" origin
  if [ -n "$top" ] && [ -s "$trust" ]; then
    origin=$(gq "$top" remote get-url origin 2>/dev/null)
    [ -n "$origin" ] && printf '%s' "$origin" | grep -qE -f "$trust" 2>/dev/null && vertraut=1
  fi

  local hctx="" rel next title addenda
  if [ -n "$hfile" ]; then
    rel=${hfile#"$top"/}
    title=$(doc_title "$hfile")
    addenda=$(grep -c -i -E '^#+ (addendum|nachtrag)' "$hfile")
    visible="$visible
Übergabe: „$(printf '%s' "$title" | oneline 110)“ · $(ago $(( now - htime )))"
    [ "${addenda:-0}" -gt 0 ] && visible="$visible · mit Nachtrag"
    local older
    older=$(list_handovers "$hdir" | sed -n '2,4p' | while read -r f; do printf -- '- %s – %s\n' "${f#"$top"/}" "$(doc_title "$f")"; done)
    if [ -n "$vertraut" ]; then
      next=$(next_step "$hfile")
      [ -n "$next" ] && visible="$visible
▶ Nächster Schritt: $(printf '%s' "$next" | oneline 170)"
      entry="Übergabe $(ago $(( now - htime ))) · ▶ $(printf '%s' "${next:-$title}" | oneline 130)"
      local body; body=$(cat "$hfile")
      [ ${#body} -gt 6000 ] && body="${body:0:6000}
[… gekürzt – die ganze Datei lesen: $rel]"
      hctx="Jüngste Übergabe im Repository: $rel (geändert $(ago $(( now - htime ))))
$body${older:+

Ältere Übergaben, neueste zuerst:
$older}"
    else
      entry="Übergabe $(ago $(( now - htime ))) · „$title“"
      hctx="Übergabe im Repository: $rel (geändert $(ago $(( now - htime )))). Der Inhalt wird nicht automatisch eingelesen: Das Repository steht nicht in der Vertrauensliste (${trust#"$HOME"/} — eine Regex je Zeile, gegen die origin-URL). Lies die Datei selbst, wenn du sie brauchst.${older:+

Ältere Übergaben, neueste zuerst:
$older}"
    fi
  elif [ -n "$conv" ]; then
    visible="$visible
Noch keine Übergabe in ${hdir#"$top"/}/ – /uebergabe legt die erste an."
    hctx="Übergabe: keine – ${hdir#"$top"/}/ ist leer."
  elif [ -n "$top" ]; then
    visible="$visible
Dieses Repo hat keinen Übergabe-Ordner – /uebergabe fragt, wohin."
    hctx="Übergabe: Das Repository hat keinen Übergabe-Ordner (weder docs/journal/handover/ noch journal/)."
  fi

  # The safety net: did the last session keep working after that handover?
  local nctx="" nmeta nname nupd nturns nnext
  if [ -n "$npick" ]; then
    nmeta="$ndir/$npick.json"
    nname=$(jq -r '.name // empty' "$nmeta"); nupd=$(jq -r '.updated // 0' "$nmeta")
    nturns=$(jq -r '.turns_after_handover // 0' "$nmeta")
    if [ "$nupd" -gt "$htime" ] && [ "$nturns" -gt 0 ]; then
      nnext=$(section "$ndir/$npick.md" "Nächster Schritt")
      if [ -n "$hfile" ]; then
        visible="$visible
⚠ Danach lief ${nname:+Session „$nname“}${nname:-die letzte Session} noch $nturns $(answers "$nturns") weiter, ohne neue Übergabe ($(ago $(( now - nupd ))))"
      else
        visible="$visible
Automatische Notiz der letzten Session${nname:+ „$nname“} ($(ago $(( now - nupd ))))"
      fi
      [ -n "$nnext" ] && visible="$visible
  Notiz sagt als Nächstes: $(printf '%s' "$nnext" | oneline 150)"
      [ -z "$entry" ] && entry="Notiz $(ago $(( now - nupd ))) · ▶ $(printf '%s' "$nnext" | oneline 130)"
      nctx="Automatische Notiz der letzten Session${nname:+ „$nname“} ($(ago $(( now - nupd ))), $nturns $(answers "$nturns") nach der letzten Übergabe). Von Haiku aus den letzten Antworten zusammengefasst – ein Sicherheitsnetz, keine Übergabe und keine Quelle:
$(cat "$ndir/$npick.md")"
    fi
  fi

  # What is true now, measured.
  local facts=() measured="" changes behind ahead bj bl joined
  if [ -n "$top" ]; then
    changes=$(gq "$cwd" status --porcelain | wc -l | tr -d ' ')
    if [ "$changes" -eq 1 ]; then facts+=("1 Datei geändert, nicht committet")
    elif [ "$changes" -gt 1 ]; then facts+=("$changes Dateien geändert, nicht committet")
    else facts+=("nichts Uncommittetes"); fi
    if gq "$cwd" rev-parse --abbrev-ref '@{u}' >/dev/null; then
      read -r behind ahead < <(gq "$cwd" rev-list --left-right --count '@{u}...HEAD')
      [ "${behind:-0}" -gt 0 ] && facts+=("↓$behind hinterher")
      [ "${ahead:-0}" -gt 0 ] && facts+=("↑$ahead nicht gepusht")
      [ "${behind:-0}" -eq 0 ] && [ "${ahead:-0}" -eq 0 ] && facts+=("aktuell mit Remote")
    else
      facts+=("kein Upstream")
    fi
    local broot=$top btmp; [ -d "$top/.beads" ] || broot=$main_top
    # Not $(…): beads_json sets beads_state, and a subshell would lose it.
    btmp=$(mktemp); beads_json "$broot" > "$btmp"; bj=$(cat "$btmp"); rm -f "$btmp"
    case "$beads_state" in
      read)
        bl=$(printf '%s' "$bj" | jq -r '(.issues // . // []) | length as $n
              | if $n == 0 then "keine Beads in Arbeit"
                else "◆ \($n) Bead\(if $n > 1 then "s" else "" end) in Arbeit: "
                     + ([.[:2][] | "„" + (.title | if length > 45 then .[:44] + "…" else . end) + "“"] | join(", "))
                     + (if $n > 2 then " (+\($n - 2))" else "" end) end' 2>/dev/null)
        [ -n "$bl" ] && facts+=("$bl")
        measured="Beads in Arbeit (Titel – ID):
$(printf '%s' "$bj" | jq -r '(.issues // . // [])[] | "- \(.title) (\(.id))"' 2>/dev/null)" ;;
      unread)
        facts+=("Beads nicht gelesen")
        measured="Beads: nicht gelesen (keine Antwort in 4 s) – das heißt nicht „keine in Arbeit“." ;;
    esac
    joined=$(printf '%s · ' "${facts[@]}"); joined=${joined% · }
    visible="$visible
Jetzt: $joined"
    [ -n "$hfile" ] && visible="$visible
Datei: $rel"
    measured="Branch $branch, HEAD $(gq "$cwd" rev-parse --short HEAD)
Gegen Remote (Stand des letzten Fetch): $joined
Geänderte Dateien (git status --short, höchstens 15):
$(gq "$cwd" status --short | head -15)
$measured"
  fi

  context="Einstieg in diese Session (Hook ~/.claude/hooks/handover.sh, Regeln aus coding-harness AGENTS.md „Communication and session continuity“).

${hctx}
${nctx:+
$nctx
}
Gerade gemessen, beim Start:
$measured

So gehst du damit um:
- Die Person hat beim Start eine Kurzfassung gesehen.
- Beginne deine erste Antwort mit einer kurzen Orientierung: **Wo wir stehen** / **Nächster Schritt** / **Was ich von dir brauche** („gerade nichts“, wenn nichts nötig ist). Ist die erste Nachricht eine konkrete Aufgabe, halte die Orientierung bei drei Zeilen und arbeite dann daran.
- Verlange nicht, dass die Person den letzten Chat rekonstruiert oder den ganzen Backlog liest.
- Die Übergabe hat einen Stichtag: prüfe Arbeitsbaum und PR-Stand, bevor du dich auf sie stützt. Aussagen der automatischen Notiz erst recht.
- Endet die Session oder bittet die Person darum: Übergabe mit /uebergabe als Datei im Repository schreiben und in der Schlussnachricht verlinken."
  return 0
}

case "$1" in
  start)
    input=$(cat)
    sid=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
    cwd=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)
    source=$(printf '%s' "$input" | jq -r '.source // "startup"' 2>/dev/null)
    [ -z "$sid" ] || [ -z "$cwd" ] && exit 0
    [ "$source" = compact ] && exit 0      # the compaction summary carries it
    entry=""
    render "$sid" "$cwd" "$source" || exit 0
    [ -n "$entry" ] && printf '%s' "$entry" > "$rdir/$sid.entry"
    # The note this session continues, as the base for its own.
    base=$(newest_note checkout "$(gq "$cwd" rev-parse --show-toplevel || echo "$cwd")" "$sid")
    [ -n "$base" ] && printf '%s' "$base" > "$rdir/$sid.base"
    jq -n --arg v "$visible" --arg c "$context" \
      '{systemMessage: $v, hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $c}}'
    ;;

  show)
    entry=""
    render "preview" "${2:-$PWD}" startup && printf '%s\n' "$visible"
    ;;

  where)
    top=$(gq "${2:-$PWD}" rev-parse --show-toplevel)
    [ -z "$top" ] && { echo "none"; exit 0; }
    IFS=$'\t' read -r conv hdir < <(convention "$top")
    if [ -z "$conv" ]; then echo "none	$top"; exit 0; fi
    printf '%s\t%s\n' "$conv" "$hdir"
    list_handovers "$hdir" | head -3 | while read -r f; do printf '  %s – %s\n' "${f#"$top"/}" "$(doc_title "$f")"; done
    ;;

  note)
    sid=$2; cwd=$3; t0=${4:-0}
    text=$(cat)
    printf '%s\n' "$text" | grep -q '^## Nächster Schritt' || exit 0
    top=$(gq "$cwd" rev-parse --show-toplevel)
    common=$(gq "$cwd" rev-parse --path-format=absolute --git-common-dir)
    # Did this turn write a handover? Then the count starts again from zero.
    htime=0
    if [ -n "$top" ]; then
      IFS=$'\t' read -r conv hdir < <(convention "$top")
      [ -n "$hdir" ] && hf=$(list_handovers "$hdir" | head -1) && [ -n "$hf" ] && htime=$(mtime_of "$hf")
    fi
    prev=$(jq -r '.turns_after_handover // 0' "$ndir/$sid.json" 2>/dev/null); prev=${prev:-0}
    if [ "$t0" -gt 0 ] && [ "$htime" -ge "$t0" ]; then turns=0; else turns=$(( prev + 1 )); fi
    printf '%s\n' "$text" > "$ndir/$sid.md.tmp" && mv "$ndir/$sid.md.tmp" "$ndir/$sid.md"
    jq -n --arg sid "$sid" --arg name "$(session_name "$sid")" --arg cwd "$cwd" \
          --arg checkout "${top:-$cwd}" --arg repo "$common" \
          --arg branch "$(gq "$cwd" branch --show-current)" \
          --argjson t "$now" --argjson turns "$turns" \
       '{session_id: $sid, name: $name, cwd: $cwd, checkout: $checkout, repo: $repo,
         branch: $branch, updated: $t, turns_after_handover: $turns}' \
       > "$ndir/$sid.json.tmp" && mv "$ndir/$sid.json.tmp" "$ndir/$sid.json"
    find "$ndir" -type f -mtime +90 -delete 2>/dev/null
    ;;
esac
exit 0
