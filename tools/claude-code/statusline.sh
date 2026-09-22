#!/bin/bash
# Claude Code status line.
#
#   line 1: repository [worktree] ⎇ branch [./subdir] │ model │ context used
#   line 2: beads in progress in this repository (only if it has .beads/)
#
# Claude Code passes a JSON object on stdin (workspace.*, model.*,
# context_window.*, …); see https://code.claude.com/docs/en/statusline.
# Each printed line is one row; ANSI colours are allowed.

input=$(cat)
j() { printf '%s' "$input" | jq -r "$1" 2>/dev/null; }

cur=$(j '.workspace.current_dir // .cwd // empty')
proj=$(j '.workspace.project_dir // empty')
[ -z "$cur" ] && cur=$PWD

# One colour per kind of information (256-colour palette, tuned for a dark
# theme), so the eye finds each part without reading the line.
c() { printf '\033[38;5;%sm' "$1"; }
bold=$'\033[1m'; dim=$'\033[2m'; reset=$'\033[0m'
c_repo=$(c 39)        # repository        blue
c_branch=$(c 170)     # branch            magenta
c_wt=$(c 245)         # worktree marker   grey
c_model=$(c 116)      # model             teal
c_ok=$(c 114); c_mid=$(c 220); c_high=$(c 203)   # context: green / yellow / red
c_warn=$(c 220)       # cwd warning       yellow
c_beads=$(c 208)      # beads             orange
c_recap=$(c 147)      # recap label       lavender
c_now=$(c 51)         # "now" label       cyan
c_sess=$(c 180)       # parallel sessions tan
c_clash=$(c 203)      # clash warning     red
c_ahead=$(c 75)       # unpushed commits  light blue
yellow=$c_warn; green=$c_ok; red=$c_high
sep=" ${dim}│${reset} "
now=$(date +%s)
cache_dir="${TMPDIR:-/tmp}/claude-statusline"
mkdir -p "$cache_dir"
# BSD stat (macOS) nimmt -f %m als mtime; GNU stat (Linux, CI) liest dasselbe
# als Dateisystem-Status und druckt einen mehrzeiligen Dump mit Exit 0 — der
# haette hier als Cache-Alter gegolten (bead hit). GNU-Form zuerst, dann BSD.
mtime_of() {
  stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0
}

g() { git --no-optional-locks -C "$cur" "$@" 2>/dev/null; }

# ── repository, worktree, branch, position ───────────────────────────────────
top=$(g rev-parse --show-toplevel)
if [ -n "$top" ]; then
  # In a linked worktree the toplevel is the worktree; name the main repository
  # and mark the worktree, so a subagent's checkout is never mistaken for it.
  common=$(g rev-parse --path-format=absolute --git-common-dir)
  main_top=$(dirname "$common")
  repo=$(basename "$main_top")
  wt=""
  [ "$main_top" != "$top" ] && wt=" ${c_wt}[worktree $(basename "$top")]${reset}"
  branch=$(g branch --show-current)
  sync=""
  if [ -z "$branch" ]; then
    branch="detached@$(g rev-parse --short HEAD)"
  else
    # Behind/ahead of the upstream is only as fresh as the last fetch, so fetch
    # in the background at most every five minutes (remote-tracking refs only;
    # the working tree is never touched), and say how old the knowledge is when
    # fetching has not succeeded for an hour.
    fh="$common/FETCH_HEAD"
    fage=$(( now - $(mtime_of "$fh") ))
    flock="$cache_dir/fetch-$(printf '%s' "$common" | shasum | cut -c1-12).lock"
    [ $(( now - $(mtime_of "$flock") )) -gt 120 ] && rmdir "$flock" 2>/dev/null
    if [ "$fage" -ge 300 ] && mkdir "$flock" 2>/dev/null; then
      nohup bash -c 'GIT_TERMINAL_PROMPT=0 GIT_SSH_COMMAND="ssh -o BatchMode=yes" \
        git -C "$1" fetch --quiet --no-tags 2>/dev/null; rmdir "$2"' \
        _ "$top" "$flock" >/dev/null 2>&1 &
    fi
    if g rev-parse --abbrev-ref '@{u}' >/dev/null; then
      read -r behind ahead < <(g rev-list --left-right --count '@{u}...HEAD')
      if [ "${behind:-0}" -eq 0 ] && [ "${ahead:-0}" -eq 0 ]; then
        sync=" ${c_ok}✓ aktuell${reset}"
      else
        [ "${behind:-0}" -gt 0 ] && sync=" ${bold}${c_warn}↓${behind} hinterher${reset}"
        [ "${ahead:-0}" -gt 0 ] && sync="${sync} ${c_ahead}↑${ahead} nicht gepusht${reset}"
      fi
      [ "$fage" -ge 3600 ] && sync="${sync} ${dim}(Fetch vor $(( fage / 3600 )) h)${reset}"
    else
      sync=" ${dim}kein Upstream${reset}"
    fi
  fi
  rel=""
  [ "$cur" != "$top" ] && rel=" ${dim}./${cur#"$top"/}${reset}"
  where="${bold}${c_repo}${repo}${reset}${wt} ${c_branch}⎇ ${branch}${reset}${sync}${rel}"
else
  where="${cur/#$HOME/~} ${dim}(no git)${reset}"
fi

# The session's directory moved since start: say so loudly. Relative hook paths
# and relative commands break silently in exactly this state.
if [ -n "$proj" ] && [ "$cur" != "$proj" ]; then
  where="${bold}${c_warn}⚠ cwd moved${reset} · ${where}"
fi

# ── model ────────────────────────────────────────────────────────────────────
model=$(j '.model.display_name // .model.id // empty')

# ── context window ───────────────────────────────────────────────────────────
# Used = input side of the last API call (input + cache writes + cache reads),
# the same formula as context_window.used_percentage. Shown against the
# auto-compact window when one is set below the model's maximum, because that
# is where the session actually compacts.
k() { LC_ALL=C awk -v n="$1" 'BEGIN {
  if (n >= 1000000) { s = sprintf("%.1f", n/1000000); sub(/\.0$/, "", s); printf "%sM", s }
  else if (n >= 1000) printf "%.0fk", n/1000; else printf "%d", n }'; }
used=$(j '(.context_window.current_usage // empty
          | (.input_tokens // 0) + (.cache_creation_input_tokens // 0) + (.cache_read_input_tokens // 0))
          // .context_window.total_input_tokens // empty')
size=$(j '.context_window.context_window_size // empty')
ctx=""
if [ -n "$size" ]; then
  limit=$size
  compact=$(jq -r '.autoCompactWindow // empty' "$HOME/.claude/settings.json" 2>/dev/null)
  [ -n "$compact" ] && [ "$compact" -lt "$size" ] 2>/dev/null && limit=$compact
  if [ -n "$used" ] && [ "$used" != "null" ]; then
    pct=$(( used * 100 / limit ))
    colour=$green; [ "$pct" -ge 50 ] && colour=$yellow; [ "$pct" -ge 80 ] && colour=$red
    ctx="${dim}ctx${reset} ${colour}$(k "$used")/$(k "$limit") ${pct}%${reset}"
  else
    ctx="${dim}ctx –/$(k "$limit")${reset}"
  fi
  [ "$limit" != "$size" ] && ctx="${ctx} ${dim}(max $(k "$size"))${reset}"
fi

line1=$where
[ -n "$model" ] && line1="${line1}${sep}${c_model}${model}${reset}"
[ -n "$ctx" ] && line1="${line1}${sep}${ctx}"
printf '%s\n' "$line1"

# ── beads in progress ────────────────────────────────────────────────────────
# `bd` takes 0.5–1.5 s, longer than a status line should block, and Claude Code
# cancels a script that is still running when the next update arrives. So the
# answer comes from a cache refreshed in the background; a stale answer is
# shown as stale (dimmed age) rather than hidden.
beads_root=""
if [ -n "$top" ]; then
  if [ -d "$top/.beads" ]; then beads_root=$top
  elif [ -n "$main_top" ] && [ -d "$main_top/.beads" ]; then beads_root=$main_top
  fi
fi
if [ -n "$beads_root" ] && command -v bd >/dev/null 2>&1; then
  key=$(printf '%s' "$beads_root" | shasum | cut -c1-12)
  cache="$cache_dir/beads-$key.json"
  lock="$cache_dir/beads-$key.lock"
  ttl=30
  mtime=$(mtime_of "$cache")
  age=$(( now - mtime ))
  if [ "$age" -ge "$ttl" ] && mkdir "$lock" 2>/dev/null; then
    # A repository that pins its tracker version ships a wrapper; use it.
    bdc=bd; [ -x "$beads_root/tools/bd" ] && bdc="$beads_root/tools/bd"
    nohup bash -c '
      "$4" -C "$1" list --status in_progress --brief --skip-labels --json -q 2>/dev/null > "$2.tmp" \
        && mv "$2.tmp" "$2"
      rm -f "$2.tmp"; rmdir "$3"
    ' _ "$beads_root" "$cache" "$lock" "$bdc" >/dev/null 2>&1 &
  fi
  # A lock older than two minutes belongs to a refresh that died; release it.
  lmt=$(stat -f %m "$lock" 2>/dev/null || stat -c %Y "$lock" 2>/dev/null || echo "$now")
  [ $(( now - lmt )) -gt 120 ] && rmdir "$lock" 2>/dev/null

  if [ -s "$cache" ]; then
    prefix="$(basename "$beads_root")-"
    summary=$(jq -r --arg p "$prefix" '
      (.issues // . // []) as $all
      | ($all | length) as $n
      | if $n == 0 then "none"
        else ($all | sort_by(.updated_at // "") | reverse) as $s
          # Never a bare id: every bead shown carries its title. The two most
          # recently touched are named; the rest are only counted.
          | [ $s[:2][] | "\($o)\(.id | ltrimstr($p))\($r) „\(.title | if length > 45 then .[:44] + "…" else . end)“" ]
          | join("  ·  ")
            + (if $n > 2 then "  \($d)(+\($n - 2) weitere)\($r)" else "" end)
          | "\($o)\($n) Beads in Arbeit:\($r) " + .
        end' --arg o "$c_beads" --arg d "$dim" --arg r "$reset" "$cache" 2>/dev/null)
    if [ -n "$summary" ]; then
      stale=""
      [ "$age" -ge $(( ttl * 4 )) ] && stale=" ${dim}(Stand vor $(( age / 60 )) min)${reset}"
      if [ "$summary" = "none" ]; then
        printf '%s\n' "${dim}◆ keine Beads in Arbeit${reset}${stale}"
      else
        printf '%s\n' "${c_beads}◆${reset} ${summary}${stale}"
      fi
    fi
  else
    printf '%s\n' "${dim}◆ Beads werden geladen …${reset}"
  fi
fi

sid=$(j '.session_id // empty')
rdir="$HOME/.claude/recaps"

# ── parallel sessions ────────────────────────────────────────────────────────
# ~/.claude/hooks/session-scan.sh reads the session registry; the
# parallel-sessions hook uses the same scan, so the line and Claude agree. A
# second session in the *same checkout* is shown in red: two sessions editing
# one working tree overwrite each other without either noticing. A session in
# another worktree of the same repository is only noted.
scan="$HOME/.claude/hooks/session-scan.sh"
if [ -x "$scan" ]; then
  n=0; entries=(); clash=""; sibling=""
  # Zellen ohne Kollaps trennen (bead hit): `IFS=$'\t' read` schob alles hinter
  # einem leeren Feld (Status "") auf die Nachbarn. Die Parameter-Expansion
  # bricht an jedem Tab, auch hinter einem leeren Feld — und der Scan liefert
  # tabfreie Zellen (Tabs im Namen kommen als \\t an).
  while IFS= read -r zeile; do
    [ -z "$zeile" ] && continue
    rel=${zeile%%$'\t'*}; rest=${zeile#*$'\t'}
    label=${rest%%$'\t'*}; rest=${rest#*$'\t'}
    st=${rest%%$'\t'*}; rest=${rest#*$'\t'}
    osid=${rest%%$'\t'*}; ocwd=${rest#*$'\t'}
    [ -z "$osid" ] && continue
    n=$((n + 1))
    case "$rel" in
      clash)   clash="${clash:+$clash, }$label ($st)" ;;
      sibling) sibling="${sibling:+$sibling, }$label" ;;
    esac
    snippet=""
    if [ -s "$rdir/$osid.txt" ]; then
      snippet=$(cut -c1-60 "$rdir/$osid.txt")
      [ "$(wc -c < "$rdir/$osid.txt")" -gt 60 ] && snippet="${snippet}…"
      snippet=" – ${snippet}"
    fi
    entries+=("${c_sess}${label}${reset} ${dim}(${st})${reset}${snippet}")
  done < <("$scan" "$sid" "$cur")
  if [ -n "$clash" ]; then
    printf '%s\n' "${bold}${c_clash}⚠ Gleicher Checkout wie Session ${clash} – Änderungen können kollidieren${reset}"
  fi
  if [ "$n" -gt 0 ]; then
    word="weitere Session"; [ "$n" -gt 1 ] && word="weitere Sessions"
    shown=$(printf '%s  ·  ' "${entries[@]:0:2}"); shown=${shown%  ·  }
    more=""; [ "$n" -gt 2 ] && more="  ${dim}(+$((n - 2)))${reset}"
    note=""; [ -n "$sibling" ] && note="  ${dim}[gleiches Repo, anderer Worktree: ${sibling}]${reset}"
    printf '%s\n' "${c_sess}⧉ ${n} ${word}:${reset} ${shown}${more}${note}"
  fi
fi

# ── rolling recap ────────────────────────────────────────────────────────────
# Written by ~/.claude/hooks/recap.sh: `.txt` after each answer (Haiku, async),
# `.now` from the moment a prompt is sent until that answer is done.
# Until this session has a recap of its own, show where it came in: the latest
# handover's next step (written by ~/.claude/hooks/handover.sh at start).
if [ -n "$sid" ]; then
  [ ! -s "$rdir/$sid.txt" ] && [ -s "$rdir/$sid.entry" ] \
    && printf '%s\n' "${c_recap}↪ Einstieg:${reset} $(cat "$rdir/$sid.entry")"
  [ -s "$rdir/$sid.txt" ] && printf '%s\n' "${c_recap}↻ Recap:${reset} $(cut -c1-220 "$rdir/$sid.txt")"
  [ -s "$rdir/$sid.now" ] && printf '%s\n' "${bold}${c_now}▶ Jetzt:${reset} $(cut -c1-120 "$rdir/$sid.now")"
fi

# Always succeed: a failed last test (no recap yet) must not hide the line.
exit 0
