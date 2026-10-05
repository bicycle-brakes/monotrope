#!/bin/sh
# recheck-agent - the agent step of the weekly research re-check: one Hermes one-shot run as the
# service user _chhermes. Installed root-owned (README, "Install") as
#   /usr/local/libexec/coding-harness/recheck-agent
# and started by scripts/research_recheck.py as
#   sudo -n -u _chhermes /usr/local/libexec/coding-harness/recheck-agent <run dir>
# Standard output is Hermes's event stream (one JSON object per line); the exit code is Hermes's
# (0 completed, 1 failed, 130 interrupted) or 142 when the alarm below ends it.
#
# The service user may not change this file. The orchestrator may not signal a process of that
# user, so the wall-time cap lives here: Hermes runs under an alarm of its own.
set -eu

HERMES_BIN=/opt/hermes/venv/bin/hermes
SERVICE_HOME=/Users/_chhermes
RUNS_ROOT=/Users/Shared/coding-harness-hermes/runs
CAP_SECONDS=2700    # 45 minutes; the orchestrator ends the process group after 50
MAX_TURNS=60

[ "$#" -eq 1 ] || { echo "usage: recheck-agent <run dir>" >&2; exit 2; }
case "$1" in
    *..*) echo "recheck-agent: refusing a run directory with '..' in it" >&2; exit 2 ;;
    "$RUNS_ROOT"/?*) ;;
    *) echo "recheck-agent: refusing a run directory outside $RUNS_ROOT" >&2; exit 2 ;;
esac
run_dir=$1
[ -f "$run_dir/in/query.md" ] || { echo "recheck-agent: no $run_dir/in/query.md" >&2; exit 2; }
[ -d "$run_dir/work" ] || { echo "recheck-agent: no $run_dir/work" >&2; exit 2; }
[ -x "$HERMES_BIN" ] || { echo "recheck-agent: no $HERMES_BIN" >&2; exit 2; }

umask 002    # a note the agent writes stays readable by the maintainer, who is in the group _chhermes
cd "$run_dir/work"
exec env -i \
    HOME="$SERVICE_HOME" \
    HERMES_HOME="$SERVICE_HOME/.hermes" \
    HERMES_WRITE_SAFE_ROOT="$run_dir/work" \
    PATH="/usr/bin:/bin" \
    perl -e 'alarm shift; exec @ARGV' "$CAP_SECONDS" \
    "$HERMES_BIN" chat --oneshot --query-file "$run_dir/in/query.md" \
    --toolsets web,file --ignore-rules --format stream-json \
    --max-turns "$MAX_TURNS" --source tool
