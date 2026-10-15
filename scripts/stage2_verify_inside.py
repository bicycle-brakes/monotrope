#!/usr/bin/env python3
"""stage2_verify_inside.py - the verifier's entry point (ADR 0018, criterion 13).

**What this is.** The one program the verifier container runs: it prepares the
candidate's derived files, runs the format step, `make verify` and the time
check (mode `work`), a draft's post-run checks (mode `draft`), one repair
row's red-first proof (mode `red-first`), or a session candidate's
preparation, format and `make verify` without the automatic verbs' time
check (mode `session`), and prints ONE JSON report line:

    {"problems": [...], "owed": bool, "formatted": [...]}

The host reads that line and nothing else; a report that does not arrive is a
failed verification, never a pass. This program runs only inside the verifier
container - or, in the test transport, on the host in its place - so it never
holds a model credential and never has a network: candidate-controlled code
that executes here can reach nothing (criterion 13).

**What this is not.** It is not a second runner. The checks are the
repository's own runner module: the shim adds the candidate's `scripts/` to
`sys.path` when that candidate carries the runner, so a candidate without it
fails loudly instead of importing a host module by accident. In the test
transport the world's root is the repository, so the same module is the one
the suite imported.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATE_SCRIPTS = Path.cwd() / "scripts"
SHIM_SCRIPTS = Path(__file__).resolve().parent


def _runner_module():
    """Import the runner module the verification runs as.

    Preference goes to the candidate's own `scripts/` when it carries the
    runner: the checks measure the candidate's tree with the semantics it
    ships, inside this container where the code can reach nothing.
    """
    if (CANDIDATE_SCRIPTS / "stage2.py").is_file():
        sys.path.insert(0, str(CANDIDATE_SCRIPTS))
    elif (SHIM_SCRIPTS / "stage2.py").is_file():
        sys.path.insert(0, str(SHIM_SCRIPTS))
    import stage2

    return stage2


def _prepare_wrappers() -> None:
    """A real `.venv/bin` with the interpreter and ruff the checks call by path.

    The image installs the locked toolchain into its system interpreter, while
    the gate list and the format step call `.venv/bin/python3` and
    `.venv/bin/ruff` under the candidate root. Small real wrappers - never
    symlinks, which would refuse the export - bridge the two; they live under
    `.venv/`, which never publishes and never counts as a model change.
    """
    if os.environ.get("STAGE2_RUNTIME_STAND_IN"):
        return
    venv_bin = Path.cwd() / ".venv" / "bin"
    venv_bin.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    ruff = shutil.which("ruff") or "ruff"
    for name, target in (("python3", python), ("python", python), ("ruff", ruff)):
        wrapper = venv_bin / name
        wrapper.write_text(f'#!/bin/sh\nexec {target} "$@"\n', encoding="utf-8")
        wrapper.chmod(0o755)


def _mode_work(stage2) -> dict:
    """The work verbs' checks: preparation, format, `make verify`, the time line."""
    plan = Path(os.environ["VERIFY_PLAN"])
    baseline_time = os.environ.get("VERIFY_BASELINE_TIME", "")
    formatted: list[str] = []
    problems = stage2.verify_attempt(Path.cwd(), plan, baseline_time, None, formatted)
    return {"problems": problems, "owed": False, "formatted": formatted}


def _mode_draft(stage2) -> dict:
    """The draft's checks: the one ADR tolerance, `make verify`, the artefacts, the card."""
    change = os.environ["VERIFY_CHANGE"]
    new_adrs = [name for name in os.environ.get("VERIFY_NEW_ADRS", "").splitlines() if name]
    ctx = stage2.context_for(Path.cwd(), change)
    problems, owed = stage2.verify_draft(Path.cwd(), ctx, None, new_adrs)
    return {"problems": problems, "owed": owed, "formatted": []}


def _red_first_problem(stage2, baseline: str, test: str) -> str | None:
    """One named test against the baseline's code; None when it was red.

    The same proof `stage2.red_first` runs on the host, in a worktree of the
    candidate's own Git: the attempt's `tests/` travel along, pytest must
    start, and exit 1 or 2 is the red the row needs. The candidate's Git
    metadata is this attempt's private clone, so no neighbour's ref can move;
    the host proof's ref comparison has nothing to protect here.
    """
    root = Path.cwd()
    file, _, function = test.partition("::")
    limit = stage2.RED_FIRST_MINUTES * 60
    environment = dict(os.environ)
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "commit.gpgsign",
            "GIT_CONFIG_VALUE_0": "false",
        }
    )
    with tempfile.TemporaryDirectory(prefix="stage2-red-") as tmp:
        tree = Path(tmp) / "tree"
        done = subprocess.run(
            ["git", "-C", str(root), "worktree", "add", "--detach", str(tree), baseline],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
            timeout=limit,
        )
        if done.returncode != 0:
            return f"{test}: the red-first checkout failed ({done.stdout[-400:]})"
        outcome = None
        try:
            shutil.rmtree(tree / "tests", ignore_errors=True)
            try:
                shutil.copytree(
                    root / "tests",
                    tree / "tests",
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
                )
            except OSError as error:
                outcome = f"{test}: the red-first checkout could not take the attempt's tests ({error})"
            if outcome is None:
                started = subprocess.run(
                    [stage2.red_first_python(root), "-c", "import pytest"],
                    cwd=tree,
                    env=environment,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    errors="replace",
                    check=False,
                    timeout=limit,
                )
                if started.returncode != 0:
                    outcome = (
                        f"{test}: the red-first interpreter cannot start pytest (exit {started.returncode}); "
                        "the named test did not run"
                    )
            if outcome is None:
                proof = subprocess.run(
                    [
                        stage2.red_first_python(root),
                        "-m",
                        "pytest",
                        "-q",
                        "-p",
                        "no:cacheprovider",
                        f"{file}::{function}",
                    ],
                    cwd=tree,
                    env=environment,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    errors="replace",
                    check=False,
                    timeout=limit,
                )
                if proof.returncode not in (1, 2):
                    outcome = (
                        f"{test}: pytest ended {proof.returncode} on the baseline's code; red first is exit 1 or 2"
                    )
        finally:
            subprocess.run(
                ["git", "-C", str(root), "worktree", "remove", "--force", str(tree)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        shutil.rmtree(tmp, ignore_errors=True)
        subprocess.run(["git", "-C", str(root), "worktree", "prune"], capture_output=True, check=False)
    return outcome


def _mode_red_first(stage2) -> dict:
    baseline = os.environ["VERIFY_BASELINE"]
    test = os.environ["VERIFY_TEST"]
    problem = _red_first_problem(stage2, baseline, test)
    return {"problems": [] if problem is None else [problem], "owed": False, "formatted": []}


def _mode_session(stage2) -> dict:
    """A session candidate's checks: preparation, format, `make verify`.

    Deliberately no time-line check: the interactive verb does not owe the
    automatic verbs' measured phase-4 entry (plan step 6), so demanding one
    would fail every honest session.
    """
    root = Path.cwd()
    formatted: list[str] = []
    env = stage2.foreign_env(
        {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "commit.gpgsign",
            "GIT_CONFIG_VALUE_0": "false",
        }
    )
    preparation = stage2.prepare_derived(root, env)
    if preparation:
        return {"problems": preparation, "owed": False, "formatted": formatted}
    line = stage2.format_step(root, env)
    if line is not None:
        formatted.append(line)
    done = stage2.launch(["make", "verify"], root, env)
    if done.returncode != 0:
        return {
            "problems": [f"`make verify` exited {done.returncode}"],
            "owed": False,
            "formatted": formatted,
        }
    return {"problems": [], "owed": False, "formatted": formatted}


def main() -> int:
    """Run one verification mode and print the one report line."""
    report: dict
    try:
        stage2 = _runner_module()
        _prepare_wrappers()
        mode = os.environ.get("VERIFY_MODE", "work")
        if mode == "work":
            report = _mode_work(stage2)
        elif mode == "draft":
            report = _mode_draft(stage2)
        elif mode == "red-first":
            report = _mode_red_first(stage2)
        elif mode == "session":
            report = _mode_session(stage2)
        else:
            report = {"problems": [f"the verifier was given no known mode: {mode}"], "owed": False, "formatted": []}
    except Exception as error:  # noqa: BLE001 - the report must arrive however the checks end
        report = {"problems": [f"{type(error).__name__}: {error}"], "owed": False, "formatted": []}
    print(
        json.dumps(
            {
                "problems": [str(problem) for problem in report["problems"]],
                "owed": bool(report["owed"]),
                "formatted": [str(line) for line in report["formatted"]],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
