"""Three levels for drift tools — so that an exit code means the same everywhere.

Without a shared vocabulary "exit 1" means something different in every script,
and the consequence is always the same: either the gate blocks on a day when
nobody did anything wrong — then it gets switched off — or it reports green over
a real deviation, and then it measures nothing.

The three levels distinguish **who caused the finding**:

| Level   | Meaning                                                | Exit | Who blocks        |
|---------|--------------------------------------------------------|:----:|-------------------|
| `INFO`  | Notable, but nobody did anything wrong                 |  0   | nobody, counted   |
| `DRIFT` | The project instance has drifted from the state here   |  1   | only `--strict`   |
| `BLOCK` | Artifacts of **this** repo contradict one another      |  2   | always            |

The most important case is `INFO`. A promotion candidate — the instance has a
pattern the framework does not have yet — is **not an error**. The instance is
where new patterns arise; the framework *may* lag behind. Counting that as drift
would leave the gate permanently red from the day it is wired in, without any
pull request being the cause.

The difference between `DRIFT` and `BLOCK` is the **mobility of the two sides**:
with `BLOCK` both sides move by commit in this repo — a contradiction is
therefore always the fault of the commit that created it, and belongs at the
pull request. With `DRIFT` the other side moves without any commit here; that
belongs in a scheduled run, not at somebody else's pull request.

## The transition valve

A new check that turns half the existing stock red on the day it lands gets
waived — and a waived gate measures nothing. A `Ramp` therefore allows
reporting a finding **for now** one level lower. It carries two things that set
it apart from a silent exception:

- a **condition in words** under which it switches up, and
- a **predicate** that measures whether it is met.

Once the condition is met, `Ramp.due` reports it — and a test fails until the
switch-up has happened. So the switch-up hangs on a check and not on memory.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum


class Level(IntEnum):
    """Exit code and severity in one — `max()` over all findings is the exit code."""

    INFO = 0
    DRIFT = 1
    BLOCK = 2


LEVEL_LABEL = {
    Level.INFO: "INFO ",
    Level.DRIFT: "DRIFT",
    Level.BLOCK: "BLOCK",
}


@dataclass(frozen=True)
class Ramp:
    """A finding is reported lower for now, until a named condition holds.

    `condition` appears in the report and tells the human what is being waited for.
    `predicate` tells the test whether waiting may go on.
    `deadline` is the second, independent due date: a date from which the valve
    switches up even if the condition never occurred.

    Why both: a predicate measures whether the existing stock was cleared. It
    does not measure whether anybody worked on it. A valve whose condition never
    occurs because nobody tackles it stays open forever without a date — and is
    then exactly the exception under a better name that this file is written
    against. The date is not a calendar entry: it turns the test red, and a red
    test is a decision, not a reminder slip.
    """

    name: str
    condition: str
    predicate: Callable[[], bool]
    target: Level = Level.BLOCK
    until_then: Level = Level.INFO
    deadline: date | None = None

    @property
    def due(self) -> bool:
        """Is the condition met or the deadline passed?"""
        if self.deadline is not None and date.today() >= self.deadline:
            return True
        return self.predicate()

    def level(self) -> Level:
        return self.target if self.due else self.until_then


@dataclass
class Finding:
    level: Level
    message: str
    detail: str = ""
    ramp: Ramp | None = None

    def effective_level(self) -> Level:
        """The level at which this finding counts today (valve taken into account)."""
        if self.ramp is None:
            return self.level
        return self.level if self.ramp.due else self.ramp.until_then


@dataclass
class Verdict:
    """Collects findings and computes an exit code from them."""

    findings: list[Finding] = field(default_factory=list)

    def add(
        self,
        level: Level,
        message: str,
        detail: str = "",
        ramp: Ramp | None = None,
    ) -> None:
        self.findings.append(Finding(level, message, detail, ramp))

    def info(self, message: str, detail: str = "") -> None:
        self.add(Level.INFO, message, detail)

    def drift(self, message: str, detail: str = "", ramp: Ramp | None = None) -> None:
        self.add(Level.DRIFT, message, detail, ramp)

    def block(self, message: str, detail: str = "", ramp: Ramp | None = None) -> None:
        self.add(Level.BLOCK, message, detail, ramp)

    def at(self, level: Level) -> list[Finding]:
        return [f for f in self.findings if f.effective_level() == level]

    def exit_code(self, strict: bool = False) -> int:
        """Highest level reached. Without `--strict` DRIFT does not block.

        The reason is stated above: the other side of a DRIFT finding moves
        without a commit in this repo. At somebody else's pull request that would
        be noise; in a scheduled run (`--strict`) it is the signal.
        """
        if not self.findings:
            return 0
        worst = max(f.effective_level() for f in self.findings)
        if worst == Level.DRIFT and not strict:
            return 0
        return int(worst)

    def render(self) -> str:
        """Report in reading order: first what blocks, then what merely stands out."""
        if not self.findings:
            return "OK — no deviation."
        out: list[str] = []
        for level in (Level.BLOCK, Level.DRIFT, Level.INFO):
            group = self.at(level)
            if not group:
                continue
            out.append(f"{LEVEL_LABEL[level]} ({len(group)}):")
            for f in group:
                out.append(f"  - {f.message}")
                if f.detail:
                    out.extend(f"      {line}" for line in f.detail.splitlines())
                if f.ramp is not None and not f.ramp.due:
                    out.append(
                        f"      [valve {f.ramp.name}] reported as "
                        f"{LEVEL_LABEL[f.ramp.until_then].strip()} instead of "
                        f"{LEVEL_LABEL[f.ramp.target].strip()}, until: {f.ramp.condition}"
                    )
            out.append("")
        return "\n".join(out).rstrip()


# ---------------------------------------------------------------------------
# The vocabulary of the writers
# ---------------------------------------------------------------------------


def check_verdict(stale: list[str], missing: list[str], regenerate: str) -> int:
    """Exit code for a `--check` of a writing subcommand.

        0  current
        1  stale — the command to regenerate is in the message
        2  missing or not readable

    Why separate from INFO/DRIFT/BLOCK: without `--strict`, `Verdict.exit_code()`
    returns a zero for DRIFT, because the other side of a DRIFT finding moves
    without a commit in this repo. With a writer that is not so — both sides lie
    here, and a stale schema must be red at the pull request (RB-G2).

    And why 1 and 2 differ: "missing" and "stale" have different causes and
    different repairs. A tool that reports both the same way reported a missing
    input as staleness for weeks in a project instance — and everybody started
    the regeneration run, which could find nothing (F-A-11).
    """
    if missing:
        print(f"MISSING: {', '.join(missing)} — never generated or not readable.", file=sys.stderr)
        return 2
    if stale:
        print(f"STALE: {', '.join(stale)} — regenerate with: {regenerate}", file=sys.stderr)
        return 1
    return 0
