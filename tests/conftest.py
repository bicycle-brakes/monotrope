"""Session-wide test setup: two runtime guards, installed at conftest import.

The stand-in log check: during the test session a declared stand-in log is
read or appended only through the locked helper (`tests/atomic_test_log.py`);
any raw access raises and fails its test, even when the code under test
swallows the error (`tests/stand_in_log_guard.py`; change
flaky-swarm-leak-test, decisions.md#Q-5).

The runner clock guard (decisions.md, runner-clock Q-2): installed before any
test module imports the runner, so a read the runner makes at import (a
default argument, a module-level value) and every reference it binds at
import reach a wrapper. The autouse fixture below then fails any test during
which runner code read a machine clock outside `clock_now`
(`tests/runner_clock_guard.py`).
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import runner_clock_guard  # noqa: E402
import stand_in_log_guard  # noqa: E402

MARKER = "raw_stand_in_log_access"

runner_clock_guard.install()
stand_in_log_guard.install()


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        f"{MARKER}(reason): the test plants an unlocked access of a declared stand-in log itself; "
        "the runtime check is suspended for it",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    stand_in_log_guard.set_test_id(item.nodeid)
    stand_in_log_guard.take_violations()
    marker = item.get_closest_marker(MARKER)
    if marker is not None and not marker.kwargs.get("reason"):
        raise pytest.UsageError(f"{item.nodeid}: @pytest.mark.{MARKER} needs a reason")
    stand_in_log_guard.suspend(marker is not None)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call():
    outcome = yield
    _fail_on_recorded_access(outcome)


def _fail_on_recorded_access(outcome) -> None:
    recorded = stand_in_log_guard.take_violations()
    if recorded and outcome.excinfo is None:
        outcome.force_exception(
            stand_in_log_guard.RawStandInLogAccess(
                "the test passed although it accessed a declared stand-in log outside the helper:\n"
                + "\n".join(recorded)
            )
        )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown():
    # Wrap every finalizer, retaining the test's marker suspension until they finish.
    outcome = yield
    try:
        _fail_on_recorded_access(outcome)
    finally:
        stand_in_log_guard.suspend(False)


@pytest.fixture(autouse=True)
def runner_clock_reads() -> Iterator[None]:
    """Fail a test during which runner code read a machine clock outside `clock_now`."""
    problems = runner_clock_guard.installation_problems()
    if problems:
        pytest.fail(f"the runner clock guard is not in effect: {problems}")
    bound = runner_clock_guard.unscanned_bound_reference_violations()
    if bound:
        pytest.fail(f"the runner holds clock references bound past the guard: {bound}")
    unreported = runner_clock_guard.unreported_import_time_reads()
    if unreported:
        pytest.fail("runner code read a machine clock outside clock_now at import: " + "; ".join(map(str, unreported)))
    start = len(runner_clock_guard.READS)
    with runner_clock_guard.in_test():
        yield
    new = runner_clock_guard.READS[start:]
    if new:
        pytest.fail("runner code read a machine clock outside clock_now: " + "; ".join(map(str, new)))


@pytest.hookimpl(optionalhook=True)
def pytest_testnodedown(node) -> None:
    """Keep worker audits on the controller even when a worker's tests skipped."""
    recorded = getattr(node, "workeroutput", {}).get("stand_in_log_violations", [])
    collected = getattr(node.config, "_stand_in_log_violations", [])
    node.config._stand_in_log_violations = collected + recorded


def pytest_sessionfinish(session: pytest.Session) -> None:
    """A recorded raw access makes the session fail, whatever its test's outcome."""
    recorded = stand_in_log_guard.session_violations()
    if hasattr(session.config, "workeroutput"):
        session.config.workeroutput["stand_in_log_violations"] = recorded
    recorded += getattr(session.config, "_stand_in_log_violations", [])
    if recorded:
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter is not None:
            reporter.write_sep("=", "stand-in log access violations")
            for violation in recorded:
                reporter.write_line(violation)
