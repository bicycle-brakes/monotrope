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
#   bash scripts/verify_all.sh --job docs    # only the document gates (the draft verb, bead coding-harness-77qj)
#   bash scripts/verify_all.sh --ci          # run the CI's gate set: same placement as the derived workflow, action equivalents reported
#   bash scripts/verify_all.sh --list        # show every gate, runnable or not

set -u

# A relative `$PYTHON` is read where the caller stood and exported absolute:
# gates start children in other directories (the leerprobe gate's foreign
# repository), where a relative path names nothing (bead coding-harness-4x2c).
# A bare name (`python3`) stays a PATH lookup.
case "${PYTHON:-}" in
    "" | /*) ;;
    */*) PYTHON="$PWD/$PYTHON" ;;
esac

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

# The arguments the caller handed us, kept before the parse loop consumes them:
# the admission supervisor below re-runs this script with them unchanged.
ORIGINAL_ARGS=("$@")

JOB="verify"
CI_MODE=0
LIST=0
while [ $# -gt 0 ]; do
    case "$1" in
        --job)
            [ $# -ge 2 ] || { echo "--job needs a value (verify|drift|docs)" >&2; exit 2; }
            JOB="$2"; shift 2 ;;
        --ci) CI_MODE=1; shift ;;
        --list) LIST=1; shift ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

if [ "$LIST" -eq 1 ]; then
    exec "$PYTHON" scripts/ci_gates.py --list
fi

# The local worker default (bead coding-harness-l7sc): the pytest gate's `-n
# auto` would otherwise take every logical core, and a probe under that died in
# memory pressure once. So a run without a caller's own choice sizes the
# workers from the machine: the smaller of half the logical cores (floored, at
# least one) and detected memory in 2-GiB steps (at least one). An exported
# PYTEST_XDIST_AUTO_NUM_WORKERS passes through verbatim — an empty value counts
# as unset — and a failed or malformed reading is ignored, never an error: with
# no usable reading the variable stays unset and xdist's own auto applies.
if [ -n "${PYTEST_XDIST_AUTO_NUM_WORKERS:-}" ]; then
    :
else
    worker_cores=""
    worker_bytes=""
    case "$(uname -s 2>/dev/null)" in
        Darwin)
            worker_cores=$(sysctl -n hw.logicalcpu 2>/dev/null) || worker_cores=""
            worker_bytes=$(sysctl -n hw.memsize 2>/dev/null) || worker_bytes=""
            ;;
        Linux)
            worker_cores=$(nproc 2>/dev/null) || worker_cores=""
            worker_kib=$(awk '/^MemTotal:/ { print $2; exit }' /proc/meminfo 2>/dev/null) || worker_kib=""
            # MemTotal is reported in KiB; the bound below counts bytes.
            case "$worker_kib" in
                "" | *[!0-9]* | 0) worker_bytes="" ;;
                *) worker_bytes=$((10#$worker_kib * 1024)) ;;
            esac
            ;;
    esac
    # Only a positive decimal integer is a reading: empty, non-numeric, zero
    # and negative output are all as good as no reading.
    case "$worker_cores" in
        "" | *[!0-9]*) worker_cores="" ;;
        *[1-9]*) ;;
        *) worker_cores="" ;;
    esac
    case "$worker_bytes" in
        "" | *[!0-9]*) worker_bytes="" ;;
        *[1-9]*) ;;
        *) worker_bytes="" ;;
    esac
    worker_cpu_bound=""
    worker_mem_bound=""
    if [ -n "$worker_cores" ]; then
        worker_cpu_bound=$((10#$worker_cores / 2))
        [ "$worker_cpu_bound" -ge 1 ] || worker_cpu_bound=1
    fi
    if [ -n "$worker_bytes" ]; then
        worker_mem_bound=$((10#$worker_bytes / 2147483648))
        [ "$worker_mem_bound" -ge 1 ] || worker_mem_bound=1
    fi
    # Each usable bound alone decides; with both, the smaller one does.
    if [ -n "$worker_cpu_bound" ]; then
        PYTEST_XDIST_AUTO_NUM_WORKERS=$worker_cpu_bound
        if [ -n "$worker_mem_bound" ] && [ "$worker_mem_bound" -lt "$worker_cpu_bound" ]; then
            PYTEST_XDIST_AUTO_NUM_WORKERS=$worker_mem_bound
        fi
        export PYTEST_XDIST_AUTO_NUM_WORKERS
    elif [ -n "$worker_mem_bound" ]; then
        PYTEST_XDIST_AUTO_NUM_WORKERS=$worker_mem_bound
        export PYTEST_XDIST_AUTO_NUM_WORKERS
    else
        unset PYTEST_XDIST_AUTO_NUM_WORKERS
    fi
fi

# One machine-wide admission for this user (queue, free-memory check) before
# any protected work: concurrent full checks across repositories and worktrees
# exhausted the machine (bead coding-harness-p6mu). A valid inherited marker
# (`HARNESS_VERIFY_LOCK_HELD` with its `HARNESS_VERIFY_LOCK_TOKEN`) means this run is nested in an admission an
# ancestor already holds — re-enter the unchanged gate loop directly; the
# module is invoked as `-m scripts.verify_lock`, and the supervisor below
# execs this script again with the original arguments.
if "$PYTHON" -m scripts.verify_lock --held >/dev/null 2>&1; then
    :
else
    exec "$PYTHON" -m scripts.verify_lock -- bash "$PWD/scripts/verify_all.sh" ${ORIGINAL_ARGS[@]+"${ORIGINAL_ARGS[@]}"}
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
    # Quoted for `sh -c`: an absolute path may hold a space; a quote inside it is escaped.
    python_word="'$(printf %s "$PYTHON" | sed "s/'/'\\\\''/g")'"
    lauf_cmd=${cmd/python3/"$python_word"}
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
