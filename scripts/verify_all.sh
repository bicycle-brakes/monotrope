#!/usr/bin/env bash
# verify_all.sh — the local runner of the ONE gate list.
#
# It holds no commands of its own: it asks scripts/ci_gates.py, and that reads
# decisions/gates.yaml. A copied command here would be a second list — the
# exact drift this runner was written against. Marketplace actions without a
# local equivalent are reported, never silently skipped.
#
# Since the cheap-before-admission order (bead coding-harness-bxxt.6) this
# script is the interpreter bootstrap and nothing else: after the arguments
# are read it execs the shared two-phase scheduler, scripts/verify_run.py —
# the same scheduler scripts.stage2 calls in-process. The scheduler runs
# every cheap (unprotected) gate before the machine's admission is asked
# for, and takes ONE admission for the protected set; `--ci` keeps running
# every selected gate of both phases.
#
# Usage:
#   bash scripts/verify_all.sh               # run the verify job's local gates
#   bash scripts/verify_all.sh --job drift   # run the drift job's local gates
#   bash scripts/verify_all.sh --job docs    # only the document gates (the draft verb, bead coding-harness-77qj)
#   bash scripts/verify_all.sh --ci          # run the CI's gate set: same placement as the derived workflow, action equivalents skipped
#   bash scripts/verify_all.sh --list        # show every gate, runnable or not (not measured, admission-free)

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

# The two phases live in the shared scheduler (bead coding-harness-bxxt.6):
# cheap gates first without any queue wait, one admission for the protected
# set, the tree comparison around the cheap pass, and the exact gate frames
# the evidence parser reads. The local worker default (bead
# coding-harness-l7sc) moved there too, so shell and scheduled full checks size from one place.
#
# An admission context in the environment belongs to whoever measured it. The
# scheduler takes its own admission in-process, so the only context it may
# record as its own is the one a supervisor handed this very runner (our
# parent is the pid the holder published); every other one is an ancestor's,
# dropped here so the run reads it from the validated ownership record and
# marks it reused (bead coding-harness-1um6).
# Keep this boundary callable so both parent relationships can be checked directly.
duration_admission_context() {
    if [ "$1" != "${HARNESS_VERIFY_LOCK_HELD:-}" ]; then
        unset HARNESS_VERIFY_ADMISSION_ID HARNESS_VERIFY_ADMISSION_WAIT 2>/dev/null || :
    fi
}
duration_admission_context "$PPID"
exec "$PYTHON" scripts/verify_run.py --job "$JOB" $([ "$CI_MODE" -eq 1 ] && echo "--ci")
