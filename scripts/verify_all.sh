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
#
# Temporary areas (bead coding-harness-bxxt.3): every run (cheap phase included) owns a
# process-id-named pytest temporary area under one private per-user parent and
# removes it when the run ends. Export HARNESS_VERIFY_KEEP_TMP=1 to keep a
# FAILED run's area for inspection — the runner prints its absolute path, the
# area then needs manual removal, and no later run sweeps it. A successful run
# removes its area regardless, and every other value of the variable removes
# normally.

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

# ── The runner-owned temporary area (bead coding-harness-bxxt.3) ───────────
#
# Every run allocates a temporary area named after its own process id
# under one private per-user managed parent, exports that area as
# PYTEST_DEBUG_TEMPROOT, and removes it when it ends — after a green or a red
# verdict alike, and on a handled SIGINT, SIGTERM, SIGHUP or SIGQUIT, which
# keep the supervisor's 128-plus-signal status. A run keeps its area for
# inspection only when HARNESS_VERIFY_KEEP_TMP was exactly 1 before the gates
# started; the area is then born under a non-numeric name (`keep-<pid>`) and
# its absolute path is printed, so no sweep can take it and a hard kill cannot
# lose the request. Retained areas need manual removal.
#
# Hard-kill boundary: a SIGKILL runs no trap, so its unretained area waits for
# the NEXT start under the same managed parent — that start removes every
# unretained sibling area whose named process no longer exists. Liveness is a
# process-id check only: no descendant protection, no lease, and a reused
# process id may defer reclamation (its stale area fails allocation loudly
# instead of being shared). Only direct children of the parent whose names are
# all digits are inspected; any other name is skipped, never followed or
# touched. A digit name that is no valid process id (0, a non-ASCII digit, a
# number beyond the platform's range) and an inaccessible or unsafe entry is reported with its path and reason and ends
# the run before any gate — a storage failure never turns verification green.
# The managed parent lives under the caller's original PYTEST_DEBUG_TEMPROOT,
# or the platform temporary parent, and travels to nested runs through
# HARNESS_VERIFY_TMP_PARENT so they find the same siblings; TMPDIR stays
# unchanged.
verify_tmp_parent="${HARNESS_VERIFY_TMP_PARENT:-}"
if [ -z "$verify_tmp_parent" ]; then
    verify_tmp_base="${PYTEST_DEBUG_TEMPROOT:-${TMPDIR:-/tmp}}"
    case "$verify_tmp_base" in
        /*) ;;
        *) verify_tmp_base="$PWD/$verify_tmp_base" ;;
    esac
    verify_tmp_parent="$verify_tmp_base/verify-runs-$(id -u)"
fi
case "$verify_tmp_parent" in
    /*/verify-runs-"$(id -u)") ;;
    *) echo "verify-tmp: refusing $verify_tmp_parent: not an absolute managed parent named verify-runs-$(id -u)" >&2; exit 2 ;;
esac
if ! verify_tmp_error=$(mkdir -p -m 700 -- "$verify_tmp_parent" 2>&1); then
    echo "verify-tmp: cannot create the managed parent $verify_tmp_parent: $verify_tmp_error" >&2
    exit 2
fi
# Validate the parent and reclaim dead siblings; the interpreter below decides
# each entry and performs the removal itself, and never follows a symlink.
if ! verify_tmp_identity=$("$PYTHON" - "$verify_tmp_parent" <<'PYEOF'
import ctypes
import os
import shutil
import stat
import sys

parent = sys.argv[1]


def refuse(path, reason):
    print(f"verify-tmp: refusing {path}: {reason}", file=sys.stderr)
    raise SystemExit(2)


try:
    info = os.lstat(parent)
except OSError as exc:
    refuse(parent, f"cannot inspect the managed parent ({exc})")
if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
    refuse(parent, "not a real directory")
if info.st_uid != os.geteuid():
    refuse(parent, "not owned by this user")
if stat.S_IMODE(info.st_mode) != 0o700:
    try:
        os.chmod(parent, 0o700)
    except OSError as exc:
        refuse(parent, f"cannot make the managed parent private ({exc})")
identity = f"{info.st_dev}:{info.st_ino}"
try:
    with os.scandir(parent) as scan:
        entries = sorted(scan, key=lambda entry: entry.name)
except OSError as exc:
    refuse(parent, f"cannot read the managed parent ({exc})")
for entry in entries:
    name = entry.name
    if not name.isdigit():
        continue
    pid_text = name.lstrip("0")
    max_pid = (1 << (ctypes.sizeof(ctypes.c_int) * 8 - 1)) - 1
    if not name.isascii() or not pid_text or len(pid_text) > len(str(max_pid)):
        refuse(entry.path, "invalid pid: expected ASCII digits naming a positive process id within the platform range")
    pid = int(pid_text)
    if pid > max_pid:
        refuse(entry.path, "invalid pid: outside the platform process-id range")
    try:
        info = entry.stat(follow_symlinks=False)
    except FileNotFoundError:
        continue
    except OSError as exc:
        refuse(entry.path, f"cannot inspect it ({exc})")
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        refuse(entry.path, "not a managed run area (symlink or not a directory)")
    if info.st_uid != os.geteuid():
        refuse(entry.path, "not owned by this user")
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        pass
    except OSError:
        continue
    else:
        continue
    try:
        shutil.rmtree(entry.path)
    except FileNotFoundError:
        pass
    except OSError as exc:
        refuse(entry.path, f"cannot remove it ({exc})")
print(identity)
PYEOF
)
then
    exit 2
fi
# Exclusive creation: two live runs cannot share an area, and a stale area
# with this process id fails the run loudly instead of being reused.
verify_tmp_keep=0
[ "${HARNESS_VERIFY_KEEP_TMP:-}" = "1" ] && verify_tmp_keep=1
if [ "$verify_tmp_keep" -eq 1 ]; then
    verify_tmp_area="$verify_tmp_parent/keep-$$"
else
    verify_tmp_area="$verify_tmp_parent/$$"
fi
if ! verify_tmp_error=$(mkdir -m 700 -- "$verify_tmp_area" 2>&1); then
    echo "verify-tmp: cannot allocate the run area $verify_tmp_area: $verify_tmp_error" >&2
    exit 2
fi
export PYTEST_DEBUG_TEMPROOT="$verify_tmp_area"
export HARNESS_VERIFY_TMP_PARENT="$verify_tmp_parent"
if [ "$verify_tmp_keep" -eq 1 ]; then
    echo "verify-tmp: will keep this run's area only on failure or interruption (HARNESS_VERIFY_KEEP_TMP=1); success removes it: $verify_tmp_area" >&2
fi
# End-of-run cleanup, idempotent across the signal and EXIT handlers: the
# first handler disarms every trap. A failed removal keeps an existing nonzero
# status; after otherwise successful work it turns the run's status into 2, so
# a storage failure never reads as a green verdict.
verify_tmp_remove() {
    "$PYTHON" - "$verify_tmp_parent" "$verify_tmp_identity" "$verify_tmp_area" <<'PYEOF'
import os
import shutil
import stat
import sys

parent, identity, area = sys.argv[1:]
try:
    info = os.lstat(parent)
    if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
        raise OSError(f"managed parent {parent} changed: symlink or not a directory")
    if f"{info.st_dev}:{info.st_ino}" != identity:
        raise OSError(f"managed parent {parent} changed: device or inode differs")
    shutil.rmtree(area)
except OSError as exc:
    print(exc, file=sys.stderr)
    raise SystemExit(2)
PYEOF
}
verify_tmp_cleanup() {
    verify_tmp_status=$?
    trap - EXIT INT TERM HUP QUIT
    if [ "$verify_tmp_status" -eq 0 ] || [ "$verify_tmp_keep" -ne 1 ]; then
        if ! verify_tmp_error=$(verify_tmp_remove 2>&1); then
            echo "verify-tmp: could not remove the run area $verify_tmp_area: $verify_tmp_error — remove it by hand" >&2
            [ "$verify_tmp_status" -eq 0 ] && verify_tmp_status=2
        fi
    else
        echo "verify-tmp: kept for inspection: $verify_tmp_area" >&2
    fi
    exit "$verify_tmp_status"
}
verify_tmp_signal() {
    trap - EXIT INT TERM HUP QUIT
    if [ -n "${verify_run_pid:-}" ]; then
        kill -s "$1" "$verify_run_pid" 2>/dev/null || :
        wait "$verify_run_pid" 2>/dev/null || :
    fi
    if [ "$verify_tmp_keep" -ne 1 ]; then
        if ! verify_tmp_error=$(verify_tmp_remove 2>&1); then
            echo "verify-tmp: could not remove the run area $verify_tmp_area: $verify_tmp_error — remove it by hand" >&2
        fi
    else
        echo "verify-tmp: kept for inspection: $verify_tmp_area" >&2
    fi
    exit $((128 + $1))
}
trap verify_tmp_cleanup EXIT
trap 'verify_tmp_signal 2' INT
trap 'verify_tmp_signal 15' TERM
trap 'verify_tmp_signal 1' HUP
trap 'verify_tmp_signal 3' QUIT

# Let pytest resolve its own option sources, including ini overrides and @files.
# The module lives in this run's area, so nested runs load their own guard and
# no extra repository module or independent option parser is needed.
# The plugin text is the scheduler's own (scripts/verify_run.py), the one the Stage-2
# full check installs as well — no second copy here.
if ! "$PYTHON" scripts/verify_run.py --write-tmp-guard "$verify_tmp_area"; then
    echo "verify-tmp: cannot write pytest guard in $verify_tmp_area" >&2
    exit 2
fi
export HARNESS_VERIFY_TMP_AREA="$verify_tmp_area"
export PYTHONPATH="$verify_tmp_area${PYTHONPATH:+:$PYTHONPATH}"
export PYTEST_ADDOPTS="${PYTEST_ADDOPTS:-} -p harness_verify_tmp"

# The scheduler runs as a background child, not through exec: the EXIT and
# signal traps above must outlive it to remove the area. A handled signal is
# forwarded to the scheduler, which kills its live gate groups and ends with
# 128 plus the signal; the trap then waits for it before removing the area.
"$PYTHON" scripts/verify_run.py --job "$JOB" $([ "$CI_MODE" -eq 1 ] && echo "--ci") <&0 &
verify_run_pid=$!
wait "$verify_run_pid"
exit $?
