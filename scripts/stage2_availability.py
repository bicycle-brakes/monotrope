"""Prepare a reachable review ladder; stage2 owns every foreign-model call.

The separate preparation/consumption steps give the orchestrator a chance to
report the selection in the main conversation before any review is launched.
The receipt is external state, never a reviewer-controlled repository artifact.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

# A probe's first limit, and the one longer retry a timed-out probe gets (R-7 of the review-swarm review).
PROBE_SECONDS = 60
PROBE_RETRY_SECONDS = 180


def now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def settings(root: Path, runner) -> dict | None:
    """An absent rule preserves legacy declarations; a present rule fails closed."""
    entry = runner.endpoint_entry(root)
    if "availability_preflight" not in entry:
        return None
    value = entry["availability_preflight"]
    if (
        not isinstance(value, dict)
        or type(value.get("flash_size")) is not int
        or not 1 <= value["flash_size"] <= 3
        or type(value.get("max_age_seconds")) is not int
        or not 1 <= value["max_age_seconds"] <= 3600
        or not isinstance(value.get("exclude_until", []), list)
    ):
        raise runner.Refused(
            "availability_preflight needs flash_size (1..3), max_age_seconds (1..3600) and dated exclusions."
        )
    for item in value.get("exclude_until", []):
        try:
            until = dt.datetime.fromisoformat(item["until"])
            valid = (
                isinstance(item["model_prefix"], str)
                and bool(item["model_prefix"].strip())
                and isinstance(item["reason"], str)
                and bool(item["reason"].strip())
                and until.tzinfo is not None
            )
        except (KeyError, TypeError, ValueError):
            valid = False
        if not valid:
            raise runner.Refused("availability_preflight has an invalid timed exclusion.")
    return value


def binding(root: Path, runner) -> dict:
    return {
        "root": str(root.resolve()),
        "configuration": digest((root / "model-endpoints.yaml").read_text(encoding="utf-8")),
        "diff": digest(runner.change_diff(root)),
    }


def receipt_path(root: Path, change: str, runner) -> Path:
    return runner.record_dir(change, root) / "availability.json"


def report(state: dict) -> str:
    available = state["availability"]
    lines = [
        f"Availability checked: {available['checked_at']}",
        f"Reachable: {', '.join(available['reachable']) or 'none'}",
        f"Free swarm: {', '.join(state['free']['selected']) or 'none'}",
        f"Flash swarm: {', '.join(state['paid']['flash']) or 'none'}",
        f"Paid ladder: {', '.join(state['paid']['rungs']) or 'none'}",
    ]
    lines.extend(f"Unavailable: {model}: {reason}" for model, reason in available["failed"].items())
    lines.extend(f"Skipped: {model}: {reason}" for model, reason in available["skipped"].items())
    lines.append("Reachability is a point-in-time result, not a billing or review-quality measurement.")
    return "\n".join(lines)


def prepare(root: Path, change: str, runner) -> None:
    """Probe candidates without source input or tools, then publish a report receipt."""
    folder = runner.folder_of(root, change)
    rule = settings(root, runner)
    if rule is None:
        raise runner.Refused("this endpoint declares no availability_preflight rule.")
    path = receipt_path(root, change, runner)
    # A failed refresh/probe attempt must never leave an earlier receipt usable.
    path.unlink(missing_ok=True)
    findings = folder / "findings.md"
    text = findings.read_text(encoding="utf-8") if findings.exists() else ""
    record = runner.read_record(change, root)
    if runner.read_state(record, text) is not None or runner.rounds_run(record, text):
        raise runner.Refused("this review run already has history; preparation cannot reset its snapshot or stops.")
    problem = runner.entry_problem(root, runner.OPENCODE)
    if problem:
        raise runner.Refused(problem)
    runner.require_pi()
    free = runner.discover_free(root, allow_empty=True)
    entry = runner.endpoint_entry(root)
    paid = runner.ladder(root)
    skipped = {model: "not admitted; data terms have not been read" for model in runner.unread_catalog_ids(entry, free)}
    candidates = list(free["selected"])
    if not runner.free_diff(root).strip():
        free["skipped"] = "free stage skipped: no implementation source diff"
        skipped.update({model: free["skipped"] for model in candidates})
        candidates = []
    for model in paid:
        if model not in free["overlay"]:
            skipped[model] = "absent from the fresh provider catalog"
        elif runner.request_value(entry, model) is None:
            skipped[model] = "no admitted cost value"
        else:
            candidates.append(model)
    reachable = []
    failed = {}
    slow: dict[str, int] = {}
    key = runner.reviewer_key()
    prompt = "Availability probe only. Reply with OK. Do not review code or request tools."
    for model in dict.fromkeys(candidates):
        for item in rule.get("exclude_until", []):
            prefix = item["model_prefix"].lower()
            matches = model.lower().startswith(prefix) or model.rsplit("/", 1)[-1].lower().startswith(prefix)
            if matches and now() < dt.datetime.fromisoformat(item["until"]):
                skipped[model] = f"unavailable until {item['until']}: {item['reason']}"
                break
        if model in skipped:
            continue
        # A probe that only ran out of time is tried once more with a longer limit: a slow but
        # reachable model must not disappear from the run silently (R-7 of the review-swarm review).
        for attempt, limit in enumerate((PROBE_SECONDS, PROBE_RETRY_SECONDS), 1):
            # Every foreign call is checked and audited on its own, the second one too: an admission
            # withdrawn between the two probes must stop it, and the leak check runs before each call
            # (the review of PR #196).
            admission = runner._free_admission(model in free["selected"], {"free": free})
            endpoint = (runner.OPENCODE, model, "max")
            ctx = runner.preflight(root, change, endpoint, admission_problem=admission)
            ctx.models_store = free.get("models_store")
            result = runner.checked_prompt(ctx, endpoint, prompt, admission)
            if not findings.exists():
                findings.write_text(runner.findings_header(ctx, runner.producer_for(endpoint)), encoding="utf-8")
            runner.append(findings, runner.call_line("prepare-loop", endpoint, result))
            try:
                # All probes, including paid ones, have no repository input or tools.
                runner.run_reviewer(
                    ctx,
                    model,
                    prompt,
                    key,
                    free=True,
                    timeout_seconds=limit,
                    task="Follow the appended availability instructions.",
                )
            except runner.CallFailed as error:
                failed[model] = runner.scrub(str(error), key)
                # Only a stopped call is worth a longer try; a refused one stays refused.
                if "stopped by" not in str(error):
                    break
            else:
                reachable.append(model)
                failed.pop(model, None)
                if attempt > 1:
                    slow[model] = limit
                break
    state = {"free": free, "paid": {}, "consumed": []}
    state["free"]["selected"] = [model for model in free["selected"] if model in reachable]
    admitted = [model for model in paid if model in reachable]
    flash = admitted[: rule["flash_size"]]
    state["paid"] = {"ladder": admitted, "flash": flash, "rungs": admitted[len(flash) :]}
    state["availability"] = {
        "checked_at": now().isoformat(timespec="seconds"),
        "reachable": reachable,
        "failed": failed,
        "slow": slow,
        "skipped": skipped,
        "terms_skipped": runner.skipped_models(root),
    }
    print(report(state))
    for reason in state["availability"]["terms_skipped"]:
        print(f"Paid admission skipped: {reason}")
    if not runner.stages_of(state):
        raise runner.Refused("no reachable admitted reviewer remains; no review round or clean result was produced.")
    receipt = {"version": 1, "binding": binding(root, runner), "state": state}
    token = digest(json.dumps(receipt, sort_keys=True))
    receipt["report_id"] = token
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(receipt, sort_keys=True), encoding="utf-8")
    temporary.replace(path)
    print(
        f"Report this selection in the main conversation, then run review-loop {change} --availability-reported {token}"
    )


def consume(root: Path, change: str, token: str | None, runner) -> dict:
    """Validate acknowledgment, freshness and input identity before any review call."""
    rule = settings(root, runner)
    path = receipt_path(root, change, runner)
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        state = receipt["state"]
        checked = dt.datetime.fromisoformat(state["availability"]["checked_at"])
        content = {key: value for key, value in receipt.items() if key != "report_id"}
        expected = digest(json.dumps(content, sort_keys=True))
        age = (now() - checked).total_seconds()
        valid = (
            rule is not None
            and receipt["version"] == 1
            and receipt["report_id"] == expected == token
            and receipt["binding"] == binding(root, runner)
            and checked.tzinfo is not None
            and 0 <= age <= rule["max_age_seconds"]
            and state["consumed"] == []
            and bool(runner.stages_of(state))
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        valid = False
    if not valid:
        raise runner.Refused(
            "run prepare-loop and report its fresh selection in the main conversation; pass its --availability-reported id."
        )
    # An accepted receipt is spent here: a second review-loop finds none and is refused instead of
    # paying the same selection twice (R-14 of the review-swarm review).
    path.unlink(missing_ok=True)
    return state
