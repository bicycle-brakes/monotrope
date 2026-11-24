#!/usr/bin/env python3
"""findings_per_model.py — raised, defects accepted, questions settled and rejected per model.

The morning handover's per-model table (bead coding-harness-qut1): one report
reads every active and archived change's findings.md at ONE identified commit
(the requested revision, HEAD by default), never combining commits, and
prints a plain table on standard output while writing the same counts as JSON
Lines under the state directory. Gaps — rows or inputs that cannot be read —
mark both formats incomplete and exit non-zero; they never pass silently
(decisions Q-6).

    python3 scripts/findings_per_model.py [--rev REV] [--root DIR]

``make findings-per-model`` runs this for HEAD, ``make findings-per-model
REV=<revision>`` for the requested revision. The JSON Lines file is
``<state>/findings-per-model/main.jsonl`` for main, ``branches/<encoded
branch>.jsonl`` for a branch name (each branch name encoded as its UTF-8
bytes in lowercase hexadecimal, so distinct names cannot collide), and
``revisions/<full commit>.jsonl`` for a revision that is not a branch. The
state root is ``$XDG_STATE_HOME`` or ``~/.local/state``. The file path is
printed last; each run overwrites only the one output of its own revision.

The JSON Lines contract (spec, criterion 14): one metadata record first —
``{"type":"metadata","commit":"<full hash>","complete":true}`` — then one
``model`` record per model with ``model``, ``raised``, ``defects_accepted``,
``questions_settled`` and ``rejected`` (``model: null`` is unattributed),
``finding`` records with ``change`` and ``id`` for unattributed findings, and
``gap`` records with ``path``, ``id`` (null when unknown) and ``reason``.
Records are deterministic.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import findings_reader as reader  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = "findings-per-model"


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    """One git invocation in root; bytes come back undecoded, the caller decides."""
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)


def full_commit(root: Path, rev: str) -> str:
    """The revision resolved once to a full commit; a moving name never labels one commit and reads another."""
    done = git(root, "rev-parse", "--verify", f"{rev}^{{commit}}")
    if done.returncode != 0:
        raise SystemExit(f"findings-per-model: git does not know the revision {rev!r}.")
    return done.stdout.decode().strip()


def branch_of(root: Path, rev_arg: str | None, sha: str) -> str | None:
    """The branch name the output file follows; None for a revision that is not a branch tip."""
    if rev_arg is None or rev_arg == "HEAD":
        done = git(root, "symbolic-ref", "--short", "-q", "HEAD")
        if done.returncode == 0:
            return done.stdout.decode().strip()
        main = git(root, "rev-parse", "--verify", "refs/heads/main")
        return "main" if main.returncode == 0 and main.stdout.decode().strip() == sha else None
    if rev_arg == "origin/main":
        tip = git(root, "rev-parse", "--verify", "refs/remotes/origin/main")
        return "main" if tip.returncode == 0 and tip.stdout.decode().strip() == sha else None
    tip = git(root, "rev-parse", "--verify", f"refs/heads/{rev_arg}")
    if tip.returncode == 0 and tip.stdout.decode().strip() == sha:
        return rev_arg
    return None


def output_relative(root: Path, rev_arg: str | None, sha: str) -> str:
    """The JSON Lines file of this run, relative to the state directory (decisions F-19, F-28)."""
    branch = branch_of(root, rev_arg, sha)
    if branch is None:
        return f"revisions/{sha}.jsonl"
    if branch == "main":
        return "main.jsonl"
    return f"branches/{branch.encode('utf-8').hex()}.jsonl"


def state_root() -> Path:
    """``$XDG_STATE_HOME/coding-harness/findings-per-model``, or ``~/.local/state`` without the variable."""
    env = os.environ.get("XDG_STATE_HOME")
    base = Path(env) if env else Path.home() / ".local" / "state"
    return base / "coding-harness" / STATE_DIR


def change_folders(root: Path, sha: str, gaps: list[reader.Gap]) -> list[str]:
    """Every active and archived change folder at the commit, in deterministic order."""
    folders: list[str] = []
    for base in ("plans/changes", "plans/changes/archive"):
        done = git(root, "ls-tree", "-d", "-z", "--name-only", f"{sha}:{base}")
        if done.returncode == 0:
            folders += sorted(f"{base}/{name}" for name in done.stdout.decode().split("\0") if name)
        else:
            gaps.append(reader.Gap(base, None, "cannot list changes at commit"))
    return folders


def read_findings(root: Path, sha: str, folder: str, gaps: list[reader.Gap]) -> str | None:
    """findings.md of one change at the commit; an unreadable input is a gap, never a silence."""
    path = f"{folder}/findings.md"
    listing = git(root, "ls-tree", "-z", "--name-only", sha, "--", path)
    if listing.returncode != 0:
        gaps.append(reader.Gap(path, None, "cannot inspect input at commit"))
        return None
    if not listing.stdout:
        return None
    done = git(root, "show", f"{sha}:{path}")
    if done.returncode != 0:
        gaps.append(reader.Gap(path, None, "cannot read input at commit"))
        return None
    try:
        return done.stdout.decode("utf-8")
    except UnicodeDecodeError:
        path = f"{folder}/findings.md"
        gaps.append(reader.Gap(path, None, "input is not valid UTF-8"))
        return None


def collect(
    root: Path,
    sha: str,
    *,
    source: reader.AttributionSource | None = None,
) -> tuple[list[reader.Finding], list[reader.Gap], list[reader.OutsideTable]]:
    """The findings, gaps and outside tables of every change at one commit.

    ``source`` swaps the legacy attribution source for another one; the reader
    call below stays the same (criterion 6).
    """
    findings: list[reader.Finding] = []
    gaps: list[reader.Gap] = []
    outside: list[reader.OutsideTable] = []
    for folder in change_folders(root, sha, gaps):
        text = read_findings(root, sha, folder, gaps)
        if text is None:
            continue
        result = reader.read_change(folder, f"{folder}/findings.md", text, source=source)
        findings += result.findings
        gaps += result.gaps
        outside += result.outside
    findings.sort(key=lambda finding: (finding.change, finding.id))
    gaps.sort(key=lambda gap: (gap.path, gap.id or "", gap.reason))
    outside.sort(key=lambda table: (table.path, table.line, table.label))
    return findings, gaps, outside


def totals_of(findings: list[reader.Finding]) -> list[dict[str, object]]:
    """One record per model with the four counts, unattributed last, attributed sorted."""
    totals: dict[str | None, dict[str, int]] = {}
    for finding in findings:
        if finding.duplicate:
            continue  # a duplicate earns nothing; the roots keep their own credit (criterion 8)
        row = totals.setdefault(finding.model, dict.fromkeys(reader.OUTCOMES, 0))
        row["raised"] += 1
        if finding.outcome is not None:
            row[finding.outcome] += 1
    ordered = sorted(model for model in totals if model is not None)
    if None in totals:
        ordered.append(None)
    return [{"type": "model", "model": model, **totals[model]} for model in ordered]


def jsonl_records(
    sha: str,
    complete: bool,
    models: list[dict[str, object]],
    findings: list[reader.Finding],
    gaps: list[reader.Gap],
) -> list[dict[str, object]]:
    """The deterministic record sequence of the JSON Lines file (spec, criterion 14)."""
    records: list[dict[str, object]] = [{"type": "metadata", "commit": sha, "complete": complete}]
    records += models
    records += [
        {"type": "finding", "change": finding.change, "id": finding.id}
        for finding in findings
        if finding.model is None and not finding.duplicate
    ]
    records += [{"type": "gap", "path": gap.path, "id": gap.id, "reason": gap.reason} for gap in gaps]
    return records


def table(models: list[dict[str, object]], records: list[dict[str, object]]) -> str:
    """The plain per-model table, the same counts as the JSON Lines (criterion 14)."""
    lines = ["| Model | Raised | Defects accepted | Questions settled | Rejected |", "|---|---:|---:|---:|---:|"]
    for record in models:
        label = "unattributed" if record["model"] is None else str(record["model"])
        lines.append(
            f"| {label} | {record['raised']} | {record['defects_accepted']} | "
            f"{record['questions_settled']} | {record['rejected']} |"
        )
    unattributed = [record for record in records if record["type"] == "finding"]
    if unattributed:
        lines.append("\nUnattributed findings:")
        lines.extend(f"- {record['change']}: {record['id']}" for record in unattributed)
    return "\n".join(lines)


def run(root: Path, rev_arg: str | None, out: Callable[[str], object] | None = None) -> int:
    """One report: table to stdout, JSON Lines to the state file, the path printed last."""
    if out is None:
        out = sys.stdout.write  # looked up at call time, so a redirected stdout is honoured
    sha = full_commit(root, rev_arg or "HEAD")
    findings, gaps, outside = collect(root, sha)
    models = totals_of(findings)
    complete = not gaps
    target = state_root() / output_relative(root, rev_arg, sha)
    records = jsonl_records(sha, complete, models, findings, gaps)
    body = "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    except OSError as exc:
        gaps.append(reader.Gap(str(target), None, f"cannot write report: {exc}"))
        complete = False
        records = jsonl_records(sha, complete, models, findings, gaps)

    out(f"Findings per model — cutoff commit {sha}\n\n")
    out(table(models, records) + "\n")
    if gaps:
        out(f"\nIncomplete — {len(gaps)} gap(s), the counts above are not complete:\n")
        for gap in gaps:
            name = gap.id or "(input)"
            out(f"- {gap.path}: {name}: {gap.reason}\n")
    if outside:
        out("\nOutside the count:\n")
        for entry in outside:
            out(f"- {entry.change}: {entry.path}: {entry.label} (line {entry.line}): {entry.rows} row(s)\n")
    out(f"{target}\n")
    return 0 if complete else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--rev", default=None, help="the revision to read (default: HEAD)")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="the repository to read")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.rev)


if __name__ == "__main__":
    raise SystemExit(main())
