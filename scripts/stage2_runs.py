#!/usr/bin/env python3
"""stage2_runs.py - count what the stage-2 runs left in their change folders.

Bead coding-harness-kw0 asks for the metrics of the first stage-2 runs to be
generated rather than typed. Every number comes from the files the runner
(`scripts/stage2.py`) writes into a change folder, read with the runner's own
row and line constants, so the count and the writer cannot drift apart:

    python3 scripts/stage2_runs.py stage2-session runner-red-gate touch-map-comments
    python3 scripts/stage2_runs.py touch-map-comments --rev a8bc676

Per change it prints one Markdown table row: loop rows taken / rejected /
undecided, rows whose repair broke a test, phase-6 rounds, phase-2a and
phase-6 rows by severity, loop rows the phase-6 reviewer marked `disagree`,
and the stage-2 calls with how many ran behind a clean leak check. Under the
table it lists the calls by verb and gives D-13's criteria as numbers where
one exists (`docs/WORKFLOW.md` §4).

What it cannot count, it says so:

- a call refused by the leak check writes no line, so refusals are not in the
  call count;
- tokens and cost per vendor are not recorded by the runner;
- a `Phase 6` mark is counted as written; what the reviewer agreed or
  disagreed with is the mark's own business.

`--rev <commit>` reads every file from that commit through git; without it the
working tree is read. Exit: 0 printed, 2 a change not found or a bad argument.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import stage2  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CALL_LINE = re.compile(r"^Stage-2 (call|session), \d{4}-\d{2}-\d{2}: (?P<rest>.*)$")
CLEAN = "leak check clean over"
CALL_PREFIXES = ("Stage-2 call, ", "Stage-2 session, ")
SEVERITY_ORDER = ("BLOCKER", "MAJOR", "MINOR")
FOREIGN_ROUTES = (stage2.CODEX, stage2.GLM, stage2.GLM_FLASH)
SEVERITY = stage2.ROW_COLUMNS.index("Severity")
STATUS = stage2.ROW_COLUMNS.index("Status")
MARK = stage2.RELEASED_COLUMNS.index("Phase 6")
COLUMNS = [
    "Change",
    "Measured at",
    "Loop rows: taken / rejected / undecided",
    "Rows marked Broke a test: yes",
    "Phase-6 rounds",
    "Phase-2a rows",
    "Phase-6 rows",
    "Phase-6 disagree marks",
    "Stage-2 calls: clean / total",
]


class NotFound(Exception):
    pass


@dataclass
class Counts:
    taken: int = 0
    rejected: int = 0
    undecided: int = 0
    broke: int = 0
    rounds: int = 0
    spec_review: Counter = field(default_factory=Counter)
    phase6: Counter = field(default_factory=Counter)
    disagree: int = 0
    calls: list[tuple[str, bool]] = field(default_factory=list)

    @property
    def loop_rows(self) -> int:
        return self.taken + self.rejected + self.undecided


def _section(heading: str) -> str | None:
    if heading.startswith("## Phase 2a"):
        return "2a"
    if heading.startswith(stage2.RELEASE_HEADING):
        return "loop"
    if heading.startswith("## Phase 6"):
        return "6"
    return None


def _verb(rest: str, kind: str) -> str:
    return "session" if kind == "session" else rest.split(" · ", 1)[0].strip()


def measure(findings: str, research: str = "") -> Counts:
    """The counts of one change, from the text of its findings.md and research.md."""
    counts = Counts(rounds=len(stage2.VERDICT_LINE.findall(findings)))
    section = None
    header: list[str] = []
    for line in findings.splitlines():
        if line.startswith("## "):
            section = _section(line)
            continue
        cells = stage2.split_row(line)
        if not cells:
            header = []
            continue
        if cells[0].lower() == "id":
            header = cells
        if stage2._furniture(cells):
            continue
        # Every table that has the column, whatever its section or width (phase 6, F-1).
        if (
            "Broke a test" in header
            and len(cells) == len(header)
            and cells[header.index("Broke a test")].lower() == "yes"
        ):
            counts.broke += 1
        if len(cells) == len(stage2.RELEASED_COLUMNS) and stage2.LOOP_ID.fullmatch(cells[0]):
            status = cells[STATUS].lower()
            if status.startswith("taken"):
                counts.taken += 1
            elif status.startswith("rejected"):
                counts.rejected += 1
            else:
                counts.undecided += 1
            if cells[MARK].lower().startswith("disagree"):
                counts.disagree += 1
        elif len(cells) == len(stage2.ROW_COLUMNS) and section in {"2a", "6"}:
            severity = cells[SEVERITY].upper() if cells[SEVERITY].upper() in stage2.SEVERITIES else "other"
            (counts.spec_review if section == "2a" else counts.phase6)[severity] += 1
    for text in (findings, research):
        for line in text.splitlines():
            if not line.startswith(CALL_PREFIXES):
                continue
            # A line with the prefix stays in the count even when the rest is not the runner's form (phase 6, F-2).
            match = CALL_LINE.match(line)
            verb = _verb(match.group("rest"), match.group(1)) if match else "unparsed"
            counts.calls.append((verb, CLEAN in line))
    return counts


# ---------------------------------------------------------------------------
# Where the files come from: the working tree, or one commit
# ---------------------------------------------------------------------------


class Source:
    def __init__(self, root: Path, rev: str | None) -> None:
        self.root = root
        self.rev = None
        if rev is not None:
            # Resolved once: a moving name such as HEAD must not label one commit and read another (phase 6, F-3).
            done = self._git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
            if done.returncode != 0 or not done.stdout.strip():
                raise NotFound(f"git does not know the revision {rev!r}.")
            self.rev = done.stdout.strip()

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self.root), *args], capture_output=True, text=True, encoding="utf-8", check=False
        )

    def label(self) -> str:
        done = self._git("rev-parse", "--short", self.rev or "HEAD")
        sha = done.stdout.strip() if done.returncode == 0 else None
        if self.rev:
            return f"`{sha or self.rev}`"
        return f"tree at `{sha}`" if sha else "tree"

    def read(self, path: str) -> str | None:
        """The file's text, None when it is not there; a file that is not UTF-8 is refused (loop row L2-2)."""
        try:
            if self.rev is None:
                target = self.root / path
                return target.read_text(encoding="utf-8") if target.is_file() else None
            done = self._git("show", f"{self.rev}:{path}")
        except UnicodeDecodeError as error:
            raise NotFound(f"{path} is not UTF-8 text; nothing is counted.") from error
        return done.stdout if done.returncode == 0 else None

    def children(self, path: str) -> list[str]:
        if self.rev is None:
            target = self.root / path
            return sorted(p.name for p in target.iterdir() if p.is_dir()) if target.is_dir() else []
        done = self._git("ls-tree", "-d", "-z", "--name-only", f"{self.rev}:{path}")
        return sorted(name for name in done.stdout.split("\0") if name) if done.returncode == 0 else []


def locate(source: Source, change: str) -> str:
    """The change folder, active or archived, as a path from the repository root."""
    if not NAME.fullmatch(change):
        raise NotFound(f"{change!r} is not a change name (lower case, digits and hyphens).")
    active = f"plans/changes/{change}"
    if source.read(f"{active}/findings.md") is not None:
        return active
    archived = [
        n
        for n in source.children("plans/changes/archive")
        if re.fullmatch(rf"\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(change)}", n)
    ]
    if len(archived) > 1:
        raise NotFound(f"{change}: more than one archived folder matches ({', '.join(archived)}).")
    if archived and source.read(f"plans/changes/archive/{archived[0]}/findings.md") is not None:
        return f"plans/changes/archive/{archived[0]}"
    raise NotFound(
        f"{change}: no findings.md under plans/changes/{change}/ or plans/changes/archive/YYYY-MM-DD-{change}/."
    )


# ---------------------------------------------------------------------------
# What is printed
# ---------------------------------------------------------------------------


def severities(counter: Counter) -> str:
    order = [s for s in SEVERITY_ORDER if counter[s]] + (["other"] if counter["other"] else [])
    return ", ".join(f"{counter[s]} {s}" for s in order) or "none"


def row(change: str, folder: str, measured: str, counts: Counts) -> list[str]:
    clean = sum(1 for _, ok in counts.calls if ok)
    return [
        f"`{change}` (`{folder}`)",
        measured,
        f"{counts.taken} / {counts.rejected} / {counts.undecided}",
        str(counts.broke),
        str(counts.rounds),
        severities(counts.spec_review),
        severities(counts.phase6),
        f"{counts.disagree} of {counts.loop_rows}",
        f"{clean} / {len(counts.calls)}",
    ]


def calls_line(change: str, counts: Counts) -> str:
    by_verb = Counter(verb for verb, _ in counts.calls)
    listing = ", ".join(f"{verb} {n}" for verb, n in by_verb.items()) or "none"
    clean = sum(1 for _, ok in counts.calls if ok)
    return f"- `{change}`: {listing} — {clean} of {len(counts.calls)} clean"


def routes_cleared(source: Source) -> list[tuple[tuple[str, str, str | None], str | None]]:
    """Each foreign route and why the declaration at this source does not clear it (None when it does)."""
    text = source.read("model-endpoints.yaml")
    with tempfile.TemporaryDirectory() as tmp:
        if text is not None:
            (Path(tmp) / "model-endpoints.yaml").write_text(text, encoding="utf-8")
        return [(route, _problem(Path(tmp), route)) for route in FOREIGN_ROUTES]


def _problem(root: Path, route: tuple[str, str, str | None]) -> str | None:
    """The runner's declaration check, with a shape it cannot read reported, not raised (phase 6, F-4)."""
    try:
        return stage2.declaration_problem(root, route[0], route[1])
    except (AttributeError, TypeError):
        return "model-endpoints.yaml has a shape the declaration check cannot read"


def criteria_lines(measured: list[Counts], routes: list) -> list[str]:
    calls = [ok for counts in measured for _, ok in counts.calls]
    broke = sum(counts.broke for counts in measured)
    cleared = [route for route, problem in routes if problem is None]
    lines = [
        f"- Criterion 1 (measured stage-2 runs, ADR 0007): {len(measured)} runs measured; "
        f"rows marked Broke a test `yes` (any status): {broke}.",
        "- Criterion 2 (lakeswitch-ai's disclosure decision): not measured here; it governs content "
        "this repository never sends (ADR 0007).",
        f"- Criterion 3 (leak check green in every run): {sum(calls)} of {len(calls)} recorded calls clean; "
        "a call the leak check refuses writes no line, so refusals are not in this count.",
        f"- Criterion 4 (foreign endpoint declared with residency): {len(cleared)} of {len(routes)} foreign "
        f"routes cleared by model-endpoints.yaml ({', '.join(f'{r[0]} {r[1]}' for r in cleared) or 'none'}).",
    ]
    lines += [f"  - not cleared: {route[0]} {route[1]} — {problem}" for route, problem in routes if problem]
    lines.append("- Tokens and cost per vendor: not recorded by the runner.")
    return lines


def report(root: Path, changes: list[str], rev: str | None) -> str:
    source = Source(root, rev)
    measured_at = source.label()
    rows, measured, call_lines = [], [], []
    for change in changes:
        folder = locate(source, change)
        counts = measure(source.read(f"{folder}/findings.md") or "", source.read(f"{folder}/research.md") or "")
        rows.append(row(change, folder, measured_at, counts))
        call_lines.append(calls_line(change, counts))
        measured.append(counts)
    parts = [
        stage2.render_table(COLUMNS, rows),
        "Stage-2 calls by verb:\n\n" + "\n".join(call_lines),
        "D-13's criteria at this cut-off:\n\n" + "\n".join(criteria_lines(measured, routes_cleared(source))),
    ]
    return "\n\n".join(parts) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count what stage-2 runs left in their change folders.")
    parser.add_argument("changes", nargs="+", metavar="change")
    parser.add_argument("--rev", help="read every file from this commit instead of the working tree")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        text = report(args.root, args.changes, args.rev)
    except NotFound as error:
        print(f"stage2_runs: {error}", file=sys.stderr)
        return 2
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
