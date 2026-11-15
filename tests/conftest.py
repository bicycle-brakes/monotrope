"""Session-wide test configuration: the runtime check on declared stand-in logs.

During the test session a declared stand-in log is read or appended only
through the locked helper (`tests/atomic_test_log.py`); any raw access raises
and fails its test, even when the code under test swallows the error
(`tests/stand_in_log_guard.py`; change flaky-swarm-leak-test, decisions.md#Q-5).
The wrappers are installed when this file is imported, before any test module.
"""

from __future__ import annotations

import pytest
import stand_in_log_guard

MARKER = "raw_stand_in_log_access"

stand_in_log_guard.install()


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        f"{MARKER}(reason): the test plants an unlocked access of a declared stand-in log itself; "
        "the runtime check is suspended for it",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
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
