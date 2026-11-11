"""The cheap-first local verification — schema 3, early stop, honest history (bead coding-harness-bxxt.1).

The one gate list (decisions/gates.yaml) classifies every gate by declared
cost — `seconds` or `minutes`. The reader (scripts/ci_gates.py) validates that
classification under schema 3 and derives a stable cheap-first order for the
local run only; the runner (scripts/verify_all.sh) stops at the first local
blocking failure, names every selected gate it did not reach, and still ends
with timing and a red verdict. Hosted CI and `--ci` stay exhaustive.

These tests exercise the real reader and runner on synthetic version-3 gate
lists in copied trees — marker commands instead of pytest, no network — and
the transferred kit in a recipient tree built strictly from the manifest's
mechanism files, running without importing a single source-tree module.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import ci_gates  # noqa: E402
import verify_duration  # noqa: E402
import verify_lock  # noqa: E402
from stage2 import red_sections  # noqa: E402

# The runner mechanism the kit transfers (scripts/kit/manifest.yaml classifies
# all four as `mechanismus`); the transfer proof copies exactly these and runs
# them in a recipient tree of their own.
MECHANISM_FILES = (
    "scripts/ci_gates.py",
    "scripts/verify_all.sh",
    "scripts/verify_lock.py",
    "scripts/verify_duration.py",
)


def _tree_files(tree: Path) -> Path:
    """The copied runner, its gate reader, its admission module and its duration helper — no gates yet."""
    (tree / "scripts").mkdir(parents=True)
    (tree / "decisions").mkdir()
    for name in ("verify_all.sh", "ci_gates.py", "verify_lock.py", "verify_duration.py"):
        shutil.copy(REPO_ROOT / "scripts" / name, tree / "scripts" / name)
    return tree


def _write_gate_file(tree: Path, gate_list: list[dict], *, schema_version: int = 3) -> None:
    """A synthetic gate list with explicit schema version and explicit costs."""
    gate_file = {
        "schema_version": schema_version,
        "tools": {"python": ["3.12"]},
        "gates": gate_list,
    }
    (tree / "decisions" / "gates.yaml").write_text(yaml.safe_dump(gate_file, sort_keys=False), encoding="utf-8")


def _gate(
    base: Path,
    gid: str,
    cost: str,
    enforcement: str = "block",
    *,
    ending: str = "true",
    job: str = "verify",
    placement: str = "both",
    subsets: list[str] | None = None,
    action: str | None = None,
    command: str | None = None,
) -> dict:
    """One declared schema-3 gate whose command touches its marker and appends to the run order."""
    gate: dict = {
        "id": gid,
        "title": f"The {gid} gate",
        "job": job,
        "enforcement": enforcement,
        "floor": True,
        "placement": placement,
        "cost": cost,
        "reason": "a seed for the cheap-first proofs",
    }
    if action is not None:
        gate["action"] = action
    else:
        gate["command"] = command or f"touch {base / f'{gid}.ran'}; echo {gid} >> {base / 'order.txt'}; {ending}"
    if subsets:
        gate["subsets"] = subsets
    return gate


def _run_runner(tree: Path, *args: str) -> subprocess.CompletedProcess:
    """The copied runner in its own tree: own state root, floor zero, the pinned interpreter."""
    env = {
        "HOME": str(tree.parent / "home"),
        "PATH": "/usr/bin:/bin:/sbin:/usr/sbin",
        "XDG_STATE_HOME": str(tree.parent / "state"),
        verify_lock.FLOOR_ENV: "0",
        "PYTHON": sys.executable,
    }
    bash = shutil.which("bash") or "/bin/bash"
    return subprocess.run(
        [bash, str(tree / "scripts" / "verify_all.sh"), *args],
        cwd=tree,
        env=env,
        capture_output=True,
        text=True,
    )


def _tree_history(tree: Path) -> list[dict]:
    """The duration history of one runner tree, as its run recorded it."""
    path = tree.parent / "state" / "coding-harness" / verify_duration.HISTORY_NAME
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _not_run_gates(stdout: str) -> list[str]:
    """The gate ids the runner named as not run, in summary order."""
    return re.findall(r"^──   \[([^\]]+)\] not run$", stdout, re.MULTILINE)


# --------------------------------------------------------------------------
# 1 · The reader: cost schema and the local cost order
# --------------------------------------------------------------------------


def test_cost_schema_rejects_missing_and_invalid_costs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """Criterion 1: schema 3 requires a declared `cost` of exactly seconds or minutes — on every gate kind.

    A missing, null, non-string or unknown cost on a plain command gate, an
    advisory gate, a hosted-only action and a drift gate each passes no
    validation, and the CLI refuses the run. (A version-2 list being accepted
    is refuted by the final activation test,
    tests/test_ci.py::test_repository_gate_schema_is_v3.)
    """
    basis = {
        "schema_version": 3,
        "tools": {"python": ["3.12"]},
        "gates": [
            {
                "id": "plain",
                "title": "A plain command gate",
                "command": "true",
                "job": "verify",
                "enforcement": "block",
                "floor": True,
                "placement": "both",
                "cost": "seconds",
                "reason": "a seed for the cost-schema proof",
            },
            {
                "id": "advisory",
                "title": "An advisory gate",
                "command": "true",
                "job": "verify",
                "enforcement": "advisory",
                "floor": False,
                "placement": "both",
                "cost": "minutes",
                "reason": "a seed for the cost-schema proof",
            },
            {
                "id": "hosted",
                "title": "A hosted action gate",
                "action": "example/hosted-only@v1",
                "job": "verify",
                "enforcement": "report",
                "floor": False,
                "placement": "hosted",
                "cost": "minutes",
                "reason": "a seed for the cost-schema proof",
            },
            {
                "id": "drift",
                "title": "A drift gate",
                "command": "true",
                "job": "drift",
                "enforcement": "block",
                "floor": True,
                "placement": "both",
                "cost": "seconds",
                "reason": "a seed for the cost-schema proof",
            },
        ],
    }
    assert ci_gates.validate_schema(basis) == [], "the control: a fully costed schema-3 list passes"

    def mangled(wert: object) -> dict:
        d = copy.deepcopy(basis)
        for g in d["gates"]:
            if wert == "MISSING":
                del g["cost"]
            else:
                g["cost"] = wert
        return d

    for wert, beschreibung in (
        ("MISSING", "a cost deleted from every gate kind"),
        (None, "a null cost"),
        (7, "a numeric cost"),
        (["seconds"], "a list where a class belongs"),
        (True, "a boolean cost"),
        ("hours", "an unknown class"),
        ("", "an empty class"),
    ):
        fehler = ci_gates.validate_schema(mangled(wert))
        assert fehler, (beschreibung, "validation passed although no gate declared a cost")
        for g in basis["gates"]:
            assert any(g["id"] in f and "cost" in f for f in fehler), (beschreibung, g["id"], fehler)

    # The command line refuses it too, not only the function.
    bad_file = tmp_path / "gates.yaml"
    bad_file.write_text(yaml.safe_dump(mangled("hours"), sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(ci_gates, "GATE_FILE", bad_file)
    monkeypatch.setattr(sys, "argv", ["ci_gates.py", "--check-schema"])
    assert ci_gates.main() != 0
    seen = capsys.readouterr()
    assert "cost" in seen.err + seen.out


def test_local_cost_order_preserves_selection_and_ties(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """Criterion 2: the local selection is cheap-first — seconds before minutes, declaration order inside each class.

    The list is deliberately anti-alphabetical and puts a minutes gate first.
    Membership never moves: job, subset, placement and equivalents filter as
    before; `gates()`, the CI placement and a still-readable version-2 list
    keep declaration order.
    """
    base = tmp_path / "order"
    base.mkdir()
    gate_file = {
        "schema_version": 3,
        "tools": {"python": ["3.12"]},
        "gates": [
            _gate(base, "zz-minutes-first", "minutes"),
            _gate(base, "aa-seconds-a", "seconds", subsets=["docs"]),
            _gate(base, "bb-seconds-b", "seconds", subsets=["docs"]),
            _gate(
                base,
                "hosted-expensive",
                "minutes",
                enforcement="report",
                placement="hosted",
                action="example/hosted-only@v1",
            ),
            _gate(base, "cc-drift-minutes", "minutes", job="drift"),
            _gate(base, "dd-drift-seconds", "seconds", job="drift"),
            _gate(base, "writer-seconds", "seconds", placement="writer"),
        ],
    }
    list_file = tmp_path / "gates.yaml"
    list_file.write_text(yaml.safe_dump(gate_file, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(ci_gates, "GATE_FILE", list_file)

    def ids(argv: list[str]) -> list[str]:
        monkeypatch.setattr(sys, "argv", ["ci_gates.py", *argv])
        assert ci_gates.main() == 0
        return [line.split("\t")[0] for line in capsys.readouterr().out.splitlines() if line]

    # The local selection: the cheap class first, ties in declaration order —
    # the expensive gate's first position did not survive, the hosted-only
    # gate stayed filtered out, the writer gate stayed selected.
    assert ids(["--commands", "--placement", "lokal", "--tsv"]) == [
        "aa-seconds-a",
        "bb-seconds-b",
        "writer-seconds",
        "zz-minutes-first",
    ]
    # A subset keeps its own membership and its declaration order.
    assert ids(["--commands", "--job", "docs", "--tsv"]) == ["aa-seconds-a", "bb-seconds-b"]
    # The drift job sorts by cost within its own selection.
    assert ids(["--commands", "--job", "drift", "--placement", "lokal", "--tsv"]) == [
        "dd-drift-seconds",
        "cc-drift-minutes",
    ]
    # The CI placement stays in declaration order — scheduling is local-only.
    assert ids(["--commands", "--placement", "ci", "--tsv"]) == [
        "zz-minutes-first",
        "aa-seconds-a",
        "bb-seconds-b",
    ]
    # `gates()` stays the declaration-order inventory, and every record
    # carries its declared cost (the JSON view rides on these records).
    assert [g["id"] for g in ci_gates.gates()] == [g["id"] for g in gate_file["gates"]]
    assert {g["id"]: g["cost"] for g in ci_gates.gates()} == {g["id"]: g["cost"] for g in gate_file["gates"]}

    # A still-readable version-2 list keeps declaration order: no sorting
    # without a declared schema. (The default job is verify, so the drift
    # gates stay out of this selection.)
    alt = copy.deepcopy(gate_file)
    alt["schema_version"] = 2
    for g in alt["gates"]:
        g.pop("cost", None)
    list_file.write_text(yaml.safe_dump(alt, sort_keys=False), encoding="utf-8")
    assert ids(["--commands", "--placement", "lokal", "--tsv"]) == [
        "zz-minutes-first",
        "aa-seconds-a",
        "bb-seconds-b",
        "writer-seconds",
    ]


def test_catalog_exposes_declared_costs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """Criterion 10: the generated catalogue carries each gate's declared cost in its own column.

    The schema-3 table gains the cost column between enforcement and floor;
    cost-less records keep the committed bootstrap rendering. (The real
    list's classification is checked by
    tests/test_ci.py::test_repository_gate_schema_is_v3.)
    """
    suite = {
        "id": "suite",
        "name": "The suite gate",
        "job": "verify",
        "command": "python3 -m pytest tests/ -q",
        "action": None,
        "with": {},
        "enforcement": "block",
        "floor": True,
        "placement": "both",
        "cost": "minutes",
        "needs_tracker": False,
        "needs_history": False,
        "subsets": [],
        "reason": "the minutes class of the duration baseline",
        "local_runnable": True,
        "via_local_equivalent": False,
    }
    lint = {
        **suite,
        "id": "lint",
        "name": "The lint gate",
        "command": "ruff check .",
        "cost": "seconds",
        "reason": "seconds",
    }
    records = [suite, lint]

    zeilen = [z for z in ci_gates.catalog_rows(records).splitlines() if z.strip()]
    assert zeilen[0] == "| id | title | command / action | job | enforcement | cost | floor | placement | reason |"
    assert zeilen[1] == "|---|---|---|---|---|---|---|---|---|"
    costen = {parts[0].strip(): parts[5].strip() for parts in (z.split("|")[1:-1] for z in zeilen[2:])}
    assert costen == {"suite": "minutes", "lint": "seconds"}, costen

    # An explicit schema argument decides, whatever the records carry.
    assert "cost" not in ci_gates.catalog_rows(records, schema=2)
    assert "| cost |" in ci_gates.catalog_rows([dict(suite)], schema=3)

    # Cost-less records — the bootstrap's fixtures and the still-readable
    # version-2 list — keep the committed eight-column table.
    naked = [{k: v for k, v in suite.items() if k != "cost"}]
    alt = ci_gates.catalog_rows(naked)
    assert alt.splitlines()[0] == "| id | title | command / action | job | enforcement | floor | placement | reason |"
    assert alt.splitlines()[1] == "|---|---|---|---|---|---|---|---|"

    # And the CLI renders the declared list with its costs.
    list_file = tmp_path / "gates.yaml"
    list_file.write_text(
        yaml.safe_dump(
            {
                "schema_version": 3,
                "tools": {"python": ["3.12"]},
                "gates": [
                    {
                        "id": "suite",
                        "title": "The suite gate",
                        "command": "true",
                        "job": "verify",
                        "enforcement": "block",
                        "floor": True,
                        "placement": "both",
                        "cost": "minutes",
                        "reason": "the minutes class of the duration baseline",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(ci_gates, "GATE_FILE", list_file)
    monkeypatch.setattr(sys, "argv", ["ci_gates.py", "--catalog"])
    assert ci_gates.main() == 0
    out = capsys.readouterr().out
    assert "| cost |" in out and "| suite |" in out, out
    assert re.search(r"^\| suite \|[^\n]*\| minutes \|", out, re.MULTILINE), out


# --------------------------------------------------------------------------
# 2 · The runner: the local early stop
# --------------------------------------------------------------------------


def test_local_blocking_failure_stops_before_pytest(tmp_path: Path) -> None:
    """Criterion 3: a blocking seconds failure stops the local run before any minutes gate.

    The list puts the minutes gate first; the cost order moves the failing
    seconds gate ahead of it, its failure stops the run red, and the minutes
    markers are never created.
    """
    base = tmp_path / "stop"
    gates = [
        _gate(base, "suite-minutes", "minutes"),
        _gate(base, "quick-red", "seconds", ending="echo 'a cheap diagnostic'; exit 1"),
        _gate(base, "after-minutes", "minutes"),
    ]
    tree = _tree_files(base / "tree")
    _write_gate_file(tree, gates)
    done = _run_runner(tree)
    assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    assert "VERIFY RED" in done.stdout, done.stdout
    assert "── [quick-red] RED (block)" in done.stdout, done.stdout
    assert (base / "quick-red.ran").exists()
    assert not (base / "suite-minutes.ran").exists(), "the expensive gate ran although a cheap gate had already failed"
    assert not (base / "after-minutes.ran").exists(), "a gate after the blocking failure executed"
    # The cheap gate ran first: declaration order would have started the minutes gate.
    assert (base / "order.txt").read_text(encoding="utf-8") == "quick-red\n", done.stdout


def test_skip_summary_names_only_unexecuted_selected_gates(tmp_path: Path) -> None:
    """Criterion 4: the stop names exactly the selected gates it did not reach — no more, no fewer.

    An executed gate is not labelled skipped, a hosted-only gate filtered out
    of the selection is not named either, and a skipped gate never shows the
    green frame of an executed one.
    """
    base = tmp_path / "skip"
    gates = [
        _gate(base, "first-seconds", "seconds"),
        _gate(base, "red-seconds", "seconds", ending="exit 1"),
        _gate(base, "never-minutes", "minutes"),
        _gate(base, "after-minutes", "minutes"),
        _gate(
            base,
            "hosted-never",
            "minutes",
            enforcement="report",
            placement="hosted",
            action="example/hosted-only@v1",
        ),
    ]
    tree = _tree_files(base / "tree")
    _write_gate_file(tree, gates)
    done = _run_runner(tree)
    assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    out = done.stdout
    assert "the run stopped at the blocking failure in [red-seconds]" in out, out
    assert _not_run_gates(out) == ["never-minutes", "after-minutes"], out
    assert not (base / "never-minutes.ran").exists() and not (base / "after-minutes.ran").exists()
    # An executed gate is never labelled skipped by the failure, and no
    # skipped gate shows the green frame of an executed one.
    assert "── [first-seconds] gruen" in out, out
    assert "──   [first-seconds] not run" not in out
    assert "── [never-minutes] gruen" not in out and "── [after-minutes] gruen" not in out
    assert "hosted-never" not in out, "a gate filtered out of the selection got named as skipped"


def test_green_run_executes_every_selected_gate_once(tmp_path: Path) -> None:
    """Criterion 5: a green run executes every selected gate exactly once — minutes gates included."""
    base = tmp_path / "green"
    gates = [
        _gate(base, "slow-suite", "minutes"),
        _gate(base, "fast-lint", "seconds"),
        _gate(base, "fast-type", "seconds"),
        _gate(base, "slow-probe", "minutes"),
    ]
    tree = _tree_files(base / "tree")
    _write_gate_file(tree, gates)
    done = _run_runner(tree)
    assert done.returncode == 0, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    assert "VERIFY GREEN" in done.stdout, done.stdout
    assert "not run" not in done.stdout, done.stdout
    order = (base / "order.txt").read_text(encoding="utf-8")
    assert order == "fast-lint\nfast-type\nslow-suite\nslow-probe\n", order
    for gid in ("slow-suite", "fast-lint", "fast-type", "slow-probe"):
        assert (base / f"{gid}.ran").exists(), gid
        assert f"── [{gid}] gruen" in done.stdout, done.stdout
        assert re.search(rf"── \[{gid}\] [0-9]+\.[0-9]+s", done.stdout), done.stdout
    events = _tree_history(tree)
    executed = [e["gate"] for e in events if e["event"] == "gate"]
    assert executed == ["fast-lint", "fast-type", "slow-suite", "slow-probe"], events
    assert [e for e in events if e["event"] == "run_end"][0]["verdict"] == "green"


def test_unusable_gate_selection_never_reports_green(tmp_path: Path) -> None:
    """Criterion 5: a failed or empty gate-list generation never ends in a green verdict.

    A malformed list stops the run before any gate; a list whose verify job
    has no locally executable gate is a configuration error, not a pass.
    """
    # (a) The list cannot be generated: a schema-3 gate without a declared cost.
    basis = tmp_path / "broken"
    tree = _tree_files(basis / "tree")
    _write_gate_file(tree, [_gate(basis, "only", "seconds")])
    doc = yaml.safe_load((tree / "decisions" / "gates.yaml").read_text(encoding="utf-8"))
    del doc["gates"][0]["cost"]
    (tree / "decisions" / "gates.yaml").write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    done = _run_runner(tree)
    assert done.returncode == 2, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    assert "VERIFY GREEN" not in done.stdout, done.stdout
    assert "cost" in done.stderr, done.stderr

    # (b) The selection is empty: the only verify gate measures hosted-only.
    leer = tmp_path / "empty"
    tree = _tree_files(leer / "tree")
    _write_gate_file(
        tree,
        [
            _gate(
                leer,
                "hosted-only",
                "minutes",
                enforcement="report",
                placement="hosted",
                action="example/hosted-only@v1",
            )
        ],
    )
    done = _run_runner(tree)
    assert done.returncode == 2, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    assert "VERIFY GREEN" not in done.stdout, done.stdout
    assert "die Gate-Liste ist leer" in done.stderr, done.stderr


@pytest.mark.parametrize("level", ["advisory", "report"])
def test_nonblocking_failures_continue_without_red_verdict(tmp_path: Path, level: str) -> None:
    """Criterion 6: a report or advisory failure stays visible, runs on, and does not turn the verdict red.

    The failing gate is cheap and sorted first — and still nothing after it is
    stopped, nothing shows as not run, and the run exits green when all
    blocking gates passed.
    """
    base = tmp_path / f"nonblocking-{level}"
    gates = [
        _gate(base, f"loud-{level}", "seconds", enforcement=level, ending="exit 1"),
        _gate(base, "behind-minutes", "minutes"),
    ]
    tree = _tree_files(base / "tree")
    _write_gate_file(tree, gates)
    done = _run_runner(tree)
    assert done.returncode == 0, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    assert "VERIFY GREEN" in done.stdout, done.stdout
    assert f"── [loud-{level}] rot, aber nur {level}" in done.stdout, done.stdout
    assert (base / f"loud-{level}.ran").exists()
    assert (base / "behind-minutes.ran").exists(), f"{level}: the failure stopped the run"
    assert (base / "order.txt").read_text(encoding="utf-8") == f"loud-{level}\nbehind-minutes\n"
    assert "not run" not in done.stdout, done.stdout
    events = _tree_history(tree)
    gate_rows = {e["gate"]: e for e in events if e["event"] == "gate"}
    assert set(gate_rows) == {f"loud-{level}", "behind-minutes"}, gate_rows
    assert gate_rows[f"loud-{level}"]["exit"] == 1 and gate_rows[f"loud-{level}"]["enforcement"] == level
    assert [e for e in events if e["event"] == "run_end"][0]["verdict"] == "green"


def test_ci_mode_continues_after_blocking_failure(tmp_path: Path) -> None:
    """Criterion 7: `--ci` stays exhaustive — a blocking failure suppresses no later selected gate.

    The same planted failure that stops a local run red lets the minutes gate
    behind it execute in CI mode, without a not-run summary and with the red
    verdict.
    """
    base = tmp_path / "ci-mode"
    gates = [
        _gate(base, "red-seconds", "seconds", ending="exit 1"),
        _gate(base, "behind-minutes", "minutes"),
    ]
    tree = _tree_files(base / "tree")
    _write_gate_file(tree, gates)
    done = _run_runner(tree, "--ci")
    assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    assert "VERIFY RED" in done.stdout, done.stdout
    assert "── [red-seconds] RED (block)" in done.stdout, done.stdout
    assert (base / "behind-minutes.ran").exists(), "--ci lost a later selected gate after a blocking failure"
    assert (base / "order.txt").read_text(encoding="utf-8") == "red-seconds\nbehind-minutes\n"
    assert "not run" not in done.stdout, done.stdout
    events = _tree_history(tree)
    gate_rows = {e["gate"]: e for e in events if e["event"] == "gate"}
    assert set(gate_rows) == {"red-seconds", "behind-minutes"}, gate_rows
    assert gate_rows["behind-minutes"]["exit"] == 0
    assert [e for e in events if e["event"] == "run_end"][0]["verdict"] == "red"


# --------------------------------------------------------------------------
# 3 · Honest diagnostics and history after the stop
# --------------------------------------------------------------------------


def test_early_stop_preserves_repair_diagnostics(tmp_path: Path) -> None:
    """Criterion 8: the existing repair parser reads the early-stopped run as it read a full one.

    The failed gate's start frame, command, diagnostic and RED line survive
    `red_sections`; the not-run summary produces no gate section of its own
    and names no executed gate.
    """
    base = tmp_path / "diagnostics"
    gates = [
        _gate(base, "suite-minutes", "minutes"),
        _gate(
            base,
            "quick-red",
            "seconds",
            command=(
                f"touch {base / 'quick-red.ran'}; echo quick-red >> {base / 'order.txt'}; "
                "echo 'E   cheap-diagnostic-line'; exit 1"
            ),
        ),
        _gate(base, "after-minutes", "minutes"),
    ]
    tree = _tree_files(base / "tree")
    _write_gate_file(tree, gates)
    done = _run_runner(tree)
    assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    red = red_sections(done.stdout)
    assert red is not None, done.stdout
    assert "── [quick-red] $ touch" in red, red
    assert "E   cheap-diagnostic-line" in red, red
    assert "── [quick-red] RED (block)" in red, red
    # The skip summary is parsed as no gate's section: no minutes gate shows
    # up in the repair evidence, and no "not run" line either.
    assert "suite-minutes" not in red, red
    assert "after-minutes" not in red, red
    assert "not run" not in red, red


def test_early_stop_history_records_only_executed_gates(tmp_path: Path) -> None:
    """Criterion 9: the history of an early-stopped run measures only executed gates and ends red.

    The skipped minutes gates produce no duration events, the one executed
    seconds gate does, and the run-end record exists with the red verdict —
    the stop is never mistaken for a finished green run.
    """
    base = tmp_path / "history"
    gates = [
        _gate(base, "suite-minutes", "minutes"),
        _gate(base, "quick-red", "seconds", ending="exit 1"),
        _gate(base, "after-minutes", "minutes"),
    ]
    tree = _tree_files(base / "tree")
    _write_gate_file(tree, gates)
    done = _run_runner(tree)
    assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    events = _tree_history(tree)
    starts = [e for e in events if e["event"] == "run_start"]
    assert len(starts) == 1 and starts[0]["job"] == "verify" and starts[0]["placement"] == "local"
    run_id = starts[0]["run_id"]
    gate_rows = [e for e in events if e["event"] == "gate"]
    assert [e["gate"] for e in gate_rows] == ["quick-red"], "the history fabricated an event for a skipped gate"
    assert all(row["run_id"] == run_id for row in gate_rows)
    assert gate_rows[0]["exit"] == 1 and isinstance(gate_rows[0]["seconds"], int | float)
    ends = [e for e in events if e["event"] == "run_end"]
    assert len(ends) == 1 and ends[0]["run_id"] == run_id and ends[0]["verdict"] == "red"


# --------------------------------------------------------------------------
# 4 · The kit transfer
# --------------------------------------------------------------------------


def test_transferred_kit_stops_before_expensive_gate(tmp_path: Path) -> None:
    """Criterion 11: the kit's recipient derives the same cheap-first stop from its own list.

    The recipient gets exactly the manifest's mechanism files and a synthetic
    version-3 list with renamed, anti-alphabetical gate ids — the run imports
    nothing from this repository's tree, so no missing dependency and no gate
    identifier of this repository can hide behind the test's imports.
    """
    manifest = yaml.safe_load((REPO_ROOT / "scripts" / "kit" / "manifest.yaml").read_text(encoding="utf-8"))
    reisend = {regel["prefix"] for regel in manifest["rules"] if regel["rolle"] == "mechanismus"}
    for pfad in MECHANISM_FILES:
        assert pfad in reisend, f"{pfad} is not classified as mechanismus — the transferred kit would miss it"

    empfaenger = tmp_path / "recipient"
    (empfaenger / "scripts").mkdir(parents=True)
    (empfaenger / "decisions").mkdir()
    for pfad in MECHANISM_FILES:
        shutil.copy(REPO_ROOT / pfad, empfaenger / pfad)

    def eigener(gid: str, cost: str, ending: str) -> dict:
        return {
            "id": gid,
            "title": f"The recipient's {gid}",
            "command": f"touch {empfaenger / f'{gid}.ran'}; echo {gid} >> {empfaenger / 'order.txt'}; {ending}",
            "job": "verify",
            "enforcement": "block",
            "floor": True,
            "placement": "both",
            "cost": cost,
            "reason": "a seed for the transferred-kit proof",
        }

    (empfaenger / "decisions" / "gates.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 3,
                "tools": {"python": ["3.12"]},
                "gates": [
                    eigener("zz-suite", "minutes", "true"),
                    eigener("aa-red", "seconds", "exit 1"),
                    eigener("mm-after", "minutes", "true"),
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    env = {
        "HOME": str(tmp_path / "home"),
        "PATH": "/usr/bin:/bin:/sbin:/usr/sbin",
        "XDG_STATE_HOME": str(tmp_path / "state"),
        verify_lock.FLOOR_ENV: "0",
        "PYTHON": sys.executable,
    }
    bash = shutil.which("bash") or "/bin/bash"
    done = subprocess.run(
        [bash, str(empfaenger / "scripts" / "verify_all.sh")],
        cwd=empfaenger,
        env=env,
        capture_output=True,
        text=True,
    )
    assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
    assert "VERIFY RED" in done.stdout, done.stdout
    assert (empfaenger / "aa-red.ran").exists()
    assert not (empfaenger / "zz-suite.ran").exists(), "the adopter executed a minutes gate after a cheap failure"
    assert not (empfaenger / "mm-after.ran").exists()
    assert (empfaenger / "order.txt").read_text(encoding="utf-8") == "aa-red\n"
    assert _not_run_gates(done.stdout) == ["zz-suite", "mm-after"], done.stdout
