"""Cancellable stage dispatcher with provider-wide queues for the research swarm.

Pure orchestration: no model knowledge, no network and no file writes. The caller
supplies the gate (declaration validation plus exact-prompt leak check, one prompt
per call) and a launcher that starts a child with ``start_new_session=True``. The
dispatcher owns queueing, deadlines, timeout, cancellation and reaping, and returns
immutable results plus audit records; only the caller writes research.
"""

from __future__ import annotations

import contextlib
import os
import signal
import subprocess
import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

PER_PROVIDER_LIMIT = 4
TICK = 0.05

OUTCOMES = ("ok", "failed", "timed-out", "cancelled", "not-started-deadline", "refused")


@dataclass(frozen=True)
class Slot:
    """One planned call. ``identity`` carries run id, input state, role, topic, endpoint, model."""

    slot_id: str
    provider: str
    required: bool
    order: tuple
    role_allowance: float
    identity: dict
    prompt: str
    payload: Any = None


@dataclass(frozen=True)
class GateVerdict:
    blocked: bool
    record: Any = None


@dataclass(frozen=True)
class SlotResult:
    slot_id: str
    identity: dict
    required: bool
    outcome: str
    started: bool
    returncode: int | None
    stdout: str
    stderr: str
    gate_record: Any
    allowance: float | None


@dataclass(frozen=True)
class DispatchResult:
    results: tuple
    audit_records: tuple
    exit_code: int
    stopped: bool = field(default=False)


def _own_group(proc):
    """True only when the child leads its own process group (started with a new session)."""
    try:
        return os.getpgid(proc.pid) == proc.pid and proc.pid != os.getpgrp()
    except (ProcessLookupError, PermissionError):
        return False


def _signal_child(proc, sig, group):
    """Signal the child's group when it has one, otherwise the child process itself."""
    with contextlib.suppress(ProcessLookupError, PermissionError):
        if group:
            os.killpg(proc.pid, sig)
        else:
            proc.send_signal(sig)


def _stop_and_reap(proc, grace):
    """Terminate the child (its whole group when it has one), kill after the grace, reap."""
    group = _own_group(proc)
    _signal_child(proc, signal.SIGTERM, group)
    try:
        proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        _signal_child(proc, signal.SIGKILL, group)
        try:
            proc.wait(timeout=max(grace, 5.0))
        except subprocess.TimeoutExpired:  # pragma: no cover - SIGKILL was sent to a live child
            return "", ""
    try:
        return proc.communicate(timeout=max(grace, 1.0))
    except subprocess.TimeoutExpired:
        return "", ""


def _text(value):
    if value is None:
        return ""
    return value if isinstance(value, str) else value.decode("utf-8", "replace")


def dispatch(
    slots,
    *,
    gate: Callable[[Slot], GateVerdict],
    launcher: Callable[[Slot, float], Any],
    audit: Callable[[Slot, GateVerdict], None] | None = None,
    stop: threading.Event | None = None,
    deadline: float | None = None,
    reserve: float = 0.0,
    clock: Callable[[], float] = time.monotonic,
    per_provider_limit: int = PER_PROVIDER_LIMIT,
    grace: float = 2.0,
) -> DispatchResult:
    """Run one stage. Each slot ends with exactly one terminal outcome."""
    stop = stop if stop is not None else threading.Event()
    ordered = sorted(slots, key=lambda s: (not s.required, s.order))
    queues: dict[str, deque] = {}
    for slot in ordered:
        queues.setdefault(slot.provider, deque()).append(slot)
    gate_lock = threading.Lock()
    results: dict[str, SlotResult] = {}
    sequence: list[str] = []
    security = threading.Event()

    def finish(slot, outcome, *, started=False, rc=None, out="", err="", record=None, allowance=None):
        results[slot.slot_id] = SlotResult(
            slot.slot_id, dict(slot.identity), slot.required, outcome, started, rc, out, err, record, allowance
        )

    def remaining():
        return None if deadline is None else deadline - reserve - clock()

    def out_of_time():
        left = remaining()
        return left is not None and left <= 0

    def launch_next(queue):
        """Pop, gate, audit and launch under the one lock; return (slot, proc, allowance) or None."""
        with gate_lock:
            if not queue:
                return "done"
            slot = queue.popleft()
            sequence.append(slot.slot_id)
            if stop.is_set():
                finish(slot, "cancelled")
                return None
            if out_of_time():
                finish(slot, "not-started-deadline")
                return None
            try:
                verdict = gate(slot)
            except Exception as exc:  # fail closed: an unreadable gate is a refusal
                verdict = GateVerdict(blocked=True, record={"error": f"{type(exc).__name__}: {exc}"})
            if verdict.blocked:
                security.set()
                stop.set()
                finish(slot, "refused", record=verdict.record)
                return None
            if audit is not None:
                try:
                    audit(slot, verdict)
                except Exception as exc:  # an unauditable call must not start
                    security.set()
                    stop.set()
                    finish(slot, "refused", record={"audit_error": f"{type(exc).__name__}: {exc}"})
                    return None
            if stop.is_set():
                finish(slot, "cancelled", record=verdict.record)
                return None
            if out_of_time():
                finish(slot, "not-started-deadline", record=verdict.record)
                return None
            left = remaining()
            allowance = slot.role_allowance if left is None else min(slot.role_allowance, left)
            try:
                proc = launcher(slot, allowance)
            except Exception as exc:
                finish(slot, "failed", record=verdict.record, err=f"launch failed: {exc}", allowance=allowance)
                return None
            return slot, proc, allowance, verdict.record

    def supervise(slot, proc, allowance, record):
        began = clock()
        while True:
            try:
                out, err = proc.communicate(timeout=TICK)
                rc = proc.returncode
                finish(
                    slot,
                    "ok" if rc == 0 else "failed",
                    started=True,
                    rc=rc,
                    out=_text(out),
                    err=_text(err),
                    record=record,
                    allowance=allowance,
                )
                return
            except subprocess.TimeoutExpired:
                pass
            cancelled = stop.is_set()
            if cancelled or clock() - began >= allowance:
                out, err = _stop_and_reap(proc, grace)
                finish(
                    slot,
                    "cancelled" if cancelled else "timed-out",
                    started=True,
                    rc=proc.returncode,
                    out=_text(out),
                    err=_text(err),
                    record=record,
                    allowance=allowance,
                )
                return

    def worker(queue):
        while True:
            launched = launch_next(queue)
            if launched == "done":
                return
            if launched is not None:
                try:
                    supervise(*launched)
                except Exception as exc:
                    slot, proc, allowance, record = launched
                    out, err = _stop_and_reap(proc, grace)
                    finish(
                        slot,
                        "failed",
                        started=True,
                        rc=proc.returncode,
                        out=_text(out),
                        err=_text(err) + f"\nsupervision failed: {type(exc).__name__}: {exc}",
                        record=record,
                        allowance=allowance,
                    )

    threads = []
    for queue in queues.values():
        for _ in range(max(1, min(per_provider_limit, len(queue)))):
            thread = threading.Thread(target=worker, args=(queue,), daemon=True)
            thread.start()
            threads.append(thread)
    for thread in threads:
        thread.join()

    # Final guard: a worker lost to an unexpected error never leaves a slot without an outcome.
    for slot in ordered:
        if slot.slot_id not in results:
            finish(slot, "failed" if slot.slot_id in sequence else "cancelled", err="worker lost before an outcome")
            if slot.slot_id in sequence:
                security.set()
    for slot in ordered:
        if slot.slot_id not in sequence:
            sequence.append(slot.slot_id)
    ordered_results = tuple(results[sid] for sid in sequence)
    records = tuple(
        {
            "slot_id": r.slot_id,
            **r.identity,
            "required": r.required,
            "leak_check": r.gate_record,
            "outcome": r.outcome,
            "started": r.started,
            "returncode": r.returncode,
        }
        for r in ordered_results
    )
    if security.is_set():
        code = 2
    elif any(r.required and r.outcome != "ok" for r in ordered_results):
        code = 1
    else:
        code = 0
    return DispatchResult(ordered_results, records, code, stop.is_set())
