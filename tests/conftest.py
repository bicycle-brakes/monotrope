"""Session-wide test setup: the runtime clock guard of the runner (decisions.md, runner-clock Q-2).

The guard is installed here, at conftest import and before any test module
imports the runner, so a read the runner makes at import (a default argument,
a module-level value) and every reference it binds at import reach a wrapper.
The autouse fixture below then fails any test during which runner code read a
machine clock outside `clock_now` (`tests/runner_clock_guard.py`).
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import runner_clock_guard  # noqa: E402

runner_clock_guard.install()


@pytest.fixture(autouse=True)
def runner_clock_reads() -> Iterator[None]:
    """Fail a test during which runner code read a machine clock outside `clock_now`."""
    problems = runner_clock_guard.installation_problems()
    if problems:
        pytest.fail(f"the runner clock guard is not in effect: {problems}")
    bound = runner_clock_guard.unscanned_bound_reference_violations()
    if bound:
        pytest.fail(f"the runner holds clock references bound past the guard: {bound}")
    start = len(runner_clock_guard.READS)
    with runner_clock_guard.in_test():
        yield
    new = runner_clock_guard.READS[start:]
    if new:
        pytest.fail("runner code read a machine clock outside clock_now: " + "; ".join(map(str, new)))
