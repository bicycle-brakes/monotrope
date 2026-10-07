#!/usr/bin/env bash
# verify_all.sh — the local runner of the ONE gate list.
#
# It holds no commands of its own: it asks scripts/ci_gates.py, and that reads
# decisions/gates.yaml. A copied command here would be a second list — the
# exact drift this runner was written against. Marketplace actions without a
# local equivalent are reported, never silently skipped.
#
# Usage:
#   bash scripts/verify_all.sh               # run the verify job's local gates
#   bash scripts/verify_all.sh --job drift   # run the drift job's local gates
#   bash scripts/verify_all.sh --ci          # run the CI's gate set: same placement as the derived workflow, action equivalents reported
#   bash scripts/verify_all.sh --list        # show every gate, runnable or not

set -u

# Back to the repository root before anything is chosen, wherever the caller
# stood: `.venv/bin/python3` below is this checkout's own (bead
# coding-harness-ei0).
cd "$(dirname "$0")/.." || exit 2

# The interpreter needs PyYAML (the gate file is YAML). `$PYTHON` if it is set;
# otherwise the first of the checkout's own `.venv/bin/python3` (built by
# `make venv` from the lock) and the `python3` on PATH that imports PyYAML — and
# nowhere else: another repository's environment decides the result by accident,
# and the suite then measures packages the lock does not name. Whoever needs
# another place sets $PYTHON.
PYTHON="${PYTHON:-}"
if [ -z "$PYTHON" ]; then
    for candidate in "$PWD/.venv/bin/python3" "$(command -v python3 || true)"; do
        if [ -n "$candidate" ] && [ -x "$candidate" ] && "$candidate" -c "import yaml" >/dev/null 2>&1; then
            PYTHON="$candidate"
            break
        fi
    done
fi
if [ -z "$PYTHON" ]; then
    echo "no python3 with PyYAML — build the locked environment with make venv, or set \$PYTHON" >&2
    exit 2
fi
# Every gate runs under the interpreter chosen here; the gates' own children
# (a test that starts a script) find it in the environment.
export PYTHON

# A tool a gate calls by its bare name (`ruff`, in the ramp-valve gate) must
# be the locked environment's own — as it is after `source .venv/bin/activate`.
# So the directory of a chosen interpreter that is not on PATH yet goes first.
case "$PYTHON" in
    */*)
        interpreter_dir="${PYTHON%/*}"
        case ":$PATH:" in
            *":$interpreter_dir:"*) ;;
            *) PATH="$interpreter_dir:$PATH"; export PATH ;;
        esac ;;
esac

JOB="verify"
CI_MODE=0
LIST=0
while [ $# -gt 0 ]; do
    case "$1" in
        --job)
            [ $# -ge 2 ] || { echo "--job needs a value (verify|drift)" >&2; exit 2; }
            JOB="$2"; shift 2 ;;
        --ci) CI_MODE=1; shift ;;
        --list) LIST=1; shift ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

if [ "$LIST" -eq 1 ]; then
    exec "$PYTHON" scripts/ci_gates.py --list
fi

# The report binds the verdict to a state of the world: which commit ran,
# against which base, with which gate configuration.
"$PYTHON" scripts/ci_gates.py --report || exit 2

# Die Gate-Liste wird ZUERST geholt und ihr Fehlschlag ist fatal: ein Lauf
# ueber null gemessene Gates darf nicht in einem gruenen Urteil enden
# (Runner-Review 2026-09-21, PR #11). --placement lokal: hosted-only Gates
# misst nur die CI — der lokale Lauf laesst sie deklariert aus (bead 1jg.2),
# die Gate-Datei nennt das placement, nicht der Zufall. --ci misst dagegen
# denselben Satz wie die abgeleitete Workflow (--placement ci): wer den
# Runner in der gehosteten CI aufruft, darf dort nicht ploetzlich ohne die
# hosted-Gates dastehen (Befund 2 an bead coding-harness-1jg.3, Review von
# PR #32). Die Action-Entsprechungen sind dabei REPORT, niemals stilles
# Auslassen.
platzierung=lokal
[ "$CI_MODE" -eq 1 ] && platzierung=ci
gate_tsv=$("$PYTHON" scripts/ci_gates.py --commands --job "$JOB" --placement "$platzierung" --tsv $([ "$CI_MODE" -eq 1 ] && echo "--skip-equivalents")) \
    || { echo "die Gate-Liste liess sich nicht erzeugen — kein VERIFY ohne gemessene Gates" >&2; exit 2; }
[ -n "$gate_tsv" ] || { echo "die Gate-Liste ist leer — ein Job ohne messbare Gates ist ein Konfigurationsfehler" >&2; exit 2; }

echo ""
echo "── gates: job=$JOB ──────────────────────────────────────────────"

# The commands come out of the one list — id, enforcement, command, per tab.
# The runner respects the vocabulary: only `block` turns the run red,
# `report`/`advisory` speak up without blocking.
fehler=0
while IFS="$(printf '\t')" read -r gid enf cmd; do
    [ -z "$cmd" ] && continue
    # Werkzeuge aus dem Pin aufloesen (gates.md G-12): `python3` in der Liste
    # heisst "der gepinnte Interpreter", nicht "was der PATH gerade hergibt".
    # Die CI macht dasselbe ueber setup-python mit derselben Version.
    lauf_cmd=${cmd/python3/"$PYTHON"}
    echo ""
    echo "── [$gid] $ lauf_cmd"
    if sh -c "$lauf_cmd"; then
        echo "── [$gid] gruen"
    elif [ "$enf" = "block" ]; then
        fehler=1
        echo "── [$gid] RED (block) — der Lauf ist rot."
    else
        echo "── [$gid] rot, aber nur $enf — er meldet, er blockiert nicht."
    fi
done <<GATES
$gate_tsv
GATES

echo ""
if [ "$fehler" -ne 0 ]; then
    echo "VERIFY RED — at least one gate failed; the report above names it."
    exit 1
fi
echo "VERIFY GREEN — every local gate of the '$JOB' job passed."
exit 0
