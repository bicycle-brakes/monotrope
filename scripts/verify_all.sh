#!/usr/bin/env bash
# verify_all.sh — the local runner of the ONE gate list.
#
# It holds no commands of its own: it asks scripts/ci_gates.py, and that reads
# decisions/gates.yaml. A copied command here would be a second list — the
# exact drift this runner was written against. Marketplace actions without a
# local equivalent are reported, never silently skipped.
#
# Under schema 3 the local run is cheap-first (bead coding-harness-bxxt.1):
# the selected gates are ordered by their declared cost class (seconds before
# minutes), and the first blocking failure stops the run — it names every
# selected gate it did not reach. `--ci` keeps running every selected gate.
#
# Usage:
#   bash scripts/verify_all.sh               # run the verify job's local gates
#   bash scripts/verify_all.sh --job drift   # run the drift job's local gates
#   bash scripts/verify_all.sh --job docs    # only the document gates (the draft verb, bead coding-harness-77qj)
#   bash scripts/verify_all.sh --ci          # run the CI's gate set: same placement as the derived workflow, action equivalents reported
#   bash scripts/verify_all.sh --list        # show every gate, runnable or not
#
# Temporary areas (bead coding-harness-bxxt.3): every admitted run owns a
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
                *)
                    # At most 15 digits keeps even KiB-to-byte multiplication
                    # inside signed 64-bit arithmetic; larger readings are unusable.
                    if [ "${#worker_kib}" -le 15 ]; then
                        worker_bytes=$((10#$worker_kib * 1024))
                    fi
                    ;;
            esac
            ;;
    esac
    # Only a positive decimal integer is a reading: empty, non-numeric, zero
    # and negative output are all as good as no reading. Limit raw CPU/byte
    # readings to 18 digits before arithmetic: every such decimal fits in a
    # signed 64-bit integer, independent of its value or leading zeroes.
    [ "${#worker_cores}" -le 18 ] || worker_cores=""
    [ "${#worker_bytes}" -le 18 ] || worker_bytes=""
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
# Keep this boundary callable so both parent relationships can be checked directly.
duration_admission_context() {
    if [ "$1" != "${HARNESS_VERIFY_LOCK_HELD:-}" ]; then
        unset HARNESS_VERIFY_ADMISSION_ID HARNESS_VERIFY_ADMISSION_WAIT 2>/dev/null || :
    fi
}

if "$PYTHON" -m scripts.verify_lock --held >/dev/null 2>&1; then
    # A valid marker means this run nests in an admission an ancestor holds.
    # One shape is the exception: when our parent IS the supervisor that holds
    # the admission (the pid the holder published), this runner is the very
    # command that admission admitted, and its fresh context — measured id and
    # wait — is ours to record. Every genuinely nested run drops that context
    # here, so its helpers resolve the shared wait from the validated
    # ownership record and mark it reused instead of passing the ancestor's
    # admission off as their own (bead coding-harness-1um6).
    duration_admission_context "$PPID"
else
    exec "$PYTHON" -m scripts.verify_lock -- bash "$PWD/scripts/verify_all.sh" ${ORIGINAL_ARGS[@]+"${ORIGINAL_ARGS[@]}"}
fi

# ── The runner-owned temporary area (bead coding-harness-bxxt.3) ───────────
#
# Every admitted run allocates a temporary area named after its own process id
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
if [ -n "${PYTEST_ADDOPTS:-}" ] && ! "$PYTHON" - <<'PYEOF'
import os
import shlex
import sys

try:
    words = shlex.split(os.environ.get("PYTEST_ADDOPTS", ""))
except ValueError as exc:
    print(f"verify-tmp: PYTEST_ADDOPTS is not valid shell quoting ({exc}); refusing to start gates", file=sys.stderr)
    raise SystemExit(2)
# pytest prepends ini addopts supplied by -o/--override-ini as well.
overrides = []
for index, word in enumerate(words):
    if word in ("-o", "--override-ini") and index + 1 < len(words):
        overrides.append(words[index + 1])
    elif word.startswith("-o") and not word.startswith("--"):
        overrides.append(word[2:])
    elif word.startswith("--override-ini="):
        overrides.append(word.partition("=")[2])
try:
    for override in overrides:
        key, sep, value = override.partition("=")
        if sep and key.strip() == "addopts":
            words.extend(shlex.split(value))
except ValueError as exc:
    print(f"verify-tmp: PYTEST_ADDOPTS addopts is not valid shell quoting ({exc}); refusing to start gates", file=sys.stderr)
    raise SystemExit(2)
for word in words:
    if word.startswith("--"):
        name = word.partition("=")[0]
        if name == "--basetemp" or (len(name) > 2 and "--basetemp".startswith(name)):
            print(
                f"verify-tmp: PYTEST_ADDOPTS selects an explicit basetemp ({word!r}); "
                "this runner owns the temporary root, so it refuses the option instead",
                file=sys.stderr,
            )
            raise SystemExit(2)
PYEOF
then
    exit 2
fi
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
if ! "$PYTHON" - "$verify_tmp_parent" <<'PYEOF'
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
PYEOF
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
verify_tmp_cleanup() {
    verify_tmp_status=$?
    trap - EXIT INT TERM HUP QUIT
    if [ "$verify_tmp_status" -eq 0 ] || [ "$verify_tmp_keep" -ne 1 ]; then
        if ! verify_tmp_error=$(rm -rf -- "$verify_tmp_area" 2>&1); then
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
    if [ "$verify_tmp_keep" -ne 1 ]; then
        if ! verify_tmp_error=$(rm -rf -- "$verify_tmp_area" 2>&1); then
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

# ── Measured durations (bead coding-harness-1um6) ──────────────────────────
#
# One run identity per admitted runner, created here — after admission, before
# the report and gate selection, so execution seconds cover both. The helper
# scripts/verify_duration.py holds no gate command and reads no gate list: it
# takes monotonic readings around the existing gate command, appends one JSON
# line per event to the shared state root and refuses substituted
# destinations. A storage failure warns here and leaves the gates, their
# enforcement and the verdict untouched; the run then records no history and
# cannot supply a persisted baseline. The admission supervisor's re-exec above
# reaches this block once — the nested run inherits its ancestor's admission
# and marks it reused instead of measuring a second wait.
DUR_BROKEN=0
# Runs in the parent shell (a $() subshell could not keep the flag), and
# stores the helper's stdout in the named variable; the helper's own
# diagnostics already went to stderr, visibly.
dur_call() {
    local _target="$1"; shift
    local _out=""
    if [ "$DUR_BROKEN" -eq 1 ]; then
        printf -v "$_target" %s ""
        return 1
    fi
    if ! _out=$("$PYTHON" -m scripts.verify_duration "$@"); then
        echo "verify-duration: measurement storage unusable — this run is not recorded; gates and verdicts continue unchanged" >&2
        DUR_BROKEN=1
        printf -v "$_target" %s ""
        return 1
    fi
    printf -v "$_target" %s "$_out"
}
duration_placement=local
[ "$CI_MODE" -eq 1 ] && duration_placement=ci
dur_call exec_t0 clock
dur_call RUN_ID start --job "$JOB" --placement "$duration_placement"

# The report binds the verdict to a state of the world: which commit ran,
# against which base, with which gate configuration.
"$PYTHON" scripts/ci_gates.py --report --job "$JOB" || exit 2

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
stop_gate=""
verbleibend=""
while IFS="$(printf '\t')" read -r gid enf cmd; do
    [ -z "$cmd" ] && continue
    # Cheap-first stop (bead coding-harness-bxxt.1): after the first blocking
    # failure no further selected gate runs. The remaining ids are collected
    # from the already obtained TSV and named in one summary below the loop;
    # `--ci` never sets stop_gate and keeps running every selected gate.
    if [ "$CI_MODE" -ne 1 ] && [ -n "$stop_gate" ]; then
        verbleibend="${verbleibend}${gid}
"
        continue
    fi
    # Werkzeuge aus dem Pin aufloesen (gates.md G-12): `python3` in der Liste
    # heisst "der gepinnte Interpreter", nicht "was der PATH gerade hergibt".
    # Die CI macht dasselbe ueber setup-python mit derselben Version.
    # Quoted for `sh -c`: an absolute path may hold a space; a quote inside it is escaped.
    python_word="'$(printf %s "$PYTHON" | sed "s/'/'\\\\''/g")'"
    lauf_cmd=${cmd/python3/"$python_word"}
    echo ""
    # Keep machine-local interpreter paths out of logs and repair evidence.
    echo "── [$gid] $ $cmd"
    # Monotonic readings immediately around the unchanged gate command; the
    # raw status is captured before any timing operation, so it is the gate
    # command's own and not a helper's (bead coding-harness-1um6).
    g_secs=""
    dur_call g_t0 clock
    sh -c "$lauf_cmd"
    gate_status=$?
    dur_call g_t1 clock
    if [ -n "$RUN_ID" ] && [ -n "$g_t0" ] && [ -n "$g_t1" ]; then
        dur_call g_secs gate --run "$RUN_ID" --gate "$gid" --start "$g_t0" --end "$g_t1" --status "$gate_status" --enforcement "$enf"
    fi
    if [ "$gate_status" -eq 0 ]; then
        echo "── [$gid] gruen"
    elif [ "$enf" = "block" ]; then
        fehler=1
        # `--ci` stays exhaustive (criterion 7 of bead coding-harness-bxxt.1):
        # it reports the blocking failure but stops nothing, so the not-run
        # summary below stays silent and every later selected gate executes.
        [ "$CI_MODE" -eq 1 ] || stop_gate="$gid"
        echo "── [$gid] RED (block) — der Lauf ist rot."
    else
        echo "── [$gid] rot, aber nur $enf — er meldet, er blockiert nicht."
    fi
    # The measured seconds of this gate, beside its verdict (criterion 1).
    [ -n "$g_secs" ] && echo "── [$gid] ${g_secs}s"
done <<GATES
$gate_tsv
GATES

# The not-run summary (bead coding-harness-bxxt.1): every selected gate the
# run did not execute because of the blocking failure, and only those —
# executed and filtered gates are never named. The lines stay outside the
# gate-frame format the evidence parser reads: summary entries have three
# spaces after `──`, while gate frames require exactly one (`^── \[`). Thus
# no skipped gate becomes a gate section, and skipped gates get no timing events: the
# history describes executed commands only.
if [ -n "$verbleibend" ]; then
    echo ""
    echo "── not run — the run stopped at the blocking failure in [$stop_gate]:"
    printf '%s' "$verbleibend" | while IFS= read -r gid; do
        [ -n "$gid" ] && echo "──   [$gid] not run"
    done
fi

# Execution seconds from the admitted runner's measurement start to its final
# verdict; the admission wait is reported beside it, never inside it.
if [ -n "$RUN_ID" ]; then
    duration_verdict=red
    [ "$fehler" -ne 0 ] || duration_verdict=green
    dur_call exec_t1 clock
    dur_call duration_summary end --run "$RUN_ID" --start "$exec_t0" --end "$exec_t1" --verdict "$duration_verdict"
    [ -n "$duration_summary" ] && echo "$duration_summary"
fi

echo ""
if [ "$fehler" -ne 0 ]; then
    echo "VERIFY RED — at least one gate failed; the report above names it."
    exit 1
fi
echo "VERIFY GREEN — every local gate of the '$JOB' job passed."
exit 0
