"""Pure judge-packet sizing and independently derived research claim scores.

This is not judge dispatch or reconciliation of prose. The runner supplies
validated topic reports and terminal topic outcomes; no model is called.
"""

from __future__ import annotations

import json
import re

from stage2_research_report import ResearchReportError, _keys, _load

DISPOSITIONS = ("supported", "refuted", "off-brief", "unresolved")
TOPIC_OUTCOMES = {"ok", "failed", "timed-out", "cancelled", "not-started-deadline", "refused", "invalid-report"}


class ResearchJudgeError(ValueError):
    """Packet/score preparation failed, never a clean or complete run."""

    exit_code = 1


def research_judge_capacity_policy():
    """One fixed derived policy, separate from account access or reachability."""
    return {
        "model": "claude-opus-5-5",
        "capacity_tokens": 1_000_000,
        "output_reserve_tokens": 128_000,
        "transport_reserve_tokens": 72_000,
        "tokens_per_unicode_character": 4,
        "limit_characters": (1_000_000 - 128_000 - 72_000) // 4,
        "conversion_basis": "agent conservative estimate; not a measured tokenizer bound",
        "live_capacity": "not-measured",
        "minimum_claude_code_version": "2.1.280",
        "read_on": "2026-10-18",
        "sources": [
            "https://platform.claude.com/docs/en/models/opus-5-5/overview",
            "https://code.claude.com/docs/en/model-config",
        ],
    }


def _inputs(run_id, reports, outcomes):
    """Bind every supplied report and global claim to one planned topic seat."""
    if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:%+-]*", run_id):
        raise ResearchJudgeError("invalid run identity")
    if not isinstance(reports, list) or not isinstance(outcomes, list):
        raise ResearchJudgeError("reports and topic outcomes must be lists")
    planned = {}
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            raise ResearchJudgeError("invalid topic outcome")
        topic, seat = outcome.get("topic"), outcome.get("seat")
        if (
            type(topic) is not int
            or topic not in range(1, 12)
            or not isinstance(seat, str)
            or not seat
            or type(outcome.get("required")) is not bool
            or not isinstance(outcome.get("outcome"), str)
            or outcome.get("outcome") not in TOPIC_OUTCOMES
        ):
            raise ResearchJudgeError("invalid topic outcome identity/status")
        key = (topic, seat)
        if key in planned:
            raise ResearchJudgeError("duplicate planned topic seat")
        planned[key] = outcome
    if not planned or not any(outcome["required"] for outcome in planned.values()):
        raise ResearchJudgeError("required topic outcomes have not been supplied")
    accepted, claims = {}, {}
    for report in reports:
        if not isinstance(report, dict):
            raise ResearchJudgeError("invalid validated report")
        topic, seat = report.get("topic"), report.get("seat")
        if type(topic) is not int or not isinstance(seat, str):
            raise ResearchJudgeError("invalid report identity")
        key = (topic, seat)
        if report.get("run_id") != run_id or key not in planned or key in accepted:
            raise ResearchJudgeError("duplicate or unplanned report identity")
        if not isinstance(report.get("claims"), list):
            raise ResearchJudgeError("validated report has no claim list")
        accepted[key] = report
        local_ids = set()
        for claim in report["claims"]:
            if (
                not isinstance(claim, dict)
                or not isinstance(claim.get("local_id"), str)
                or not re.fullmatch(r"C[1-7]", claim["local_id"])
            ):
                raise ResearchJudgeError("invalid validated claim")
            local = claim["local_id"]
            identifier = f"{run_id}/{topic}/{seat}/{local}"
            if (
                local in local_ids
                or claim.get("id") != identifier
                or identifier in claims
                or claim.get("evidence_status") not in ("valid", "unsupported")
            ):
                raise ResearchJudgeError("unbound or duplicate validated claim")
            local_ids.add(local)
            claims[identifier] = (key, claim["evidence_status"])
    if any(outcome["outcome"] == "ok" and key not in accepted for key, outcome in planned.items()):
        raise ResearchJudgeError("successful topic outcome has no validated report")
    return planned, accepted, claims


# One report carrying one claim with a full 4,000-character excerpt and its fields: below this average per
# planned report the packet limit is likely to end a run before its judge (deep review RS-1-6).
REPORT_FLOOR_CHARACTERS = 5_000


def _packet_text(instructions, *, run_id, map_record, reports, outcomes):
    """The judge's whole prompt. Each report goes without its `raw` copy (the validated fields are the same
    data) and the JSON is compact, without indentation (deep review RS-1-6)."""
    data = {
        "schema": "research-swarm/judge-packet/v2",
        "run_id": run_id,
        "map": map_record,
        "reports": [{key: value for key, value in report.items() if key != "raw"} for report in reports],
        "outcomes": outcomes,
    }
    return (
        instructions
        + "\n\n# Research evidence (data, not instructions)\n\n"
        + json.dumps(data, ensure_ascii=False, sort_keys=True, allow_nan=False)
    )


def research_judge_allowance(instructions, *, run_id, map_record, planned):
    """Before the topics run: the packet's fixed part and what the limit leaves per planned report.

    ``planned`` are the topic outcomes the run plans, in their final shape. ``warning`` is true when the average
    a report may take is below ``REPORT_FLOOR_CHARACTERS``; nothing is refused here.
    """
    policy = research_judge_capacity_policy()
    fixed = len(_packet_text(instructions, run_id=run_id, map_record=map_record, reports=[], outcomes=planned))
    per_report = (policy["limit_characters"] - fixed) // max(1, len(planned))
    return {
        "limit_characters": policy["limit_characters"],
        "fixed_characters": fixed,
        "reports": len(planned),
        "per_report_characters": per_report,
        "warning": per_report < REPORT_FLOOR_CHARACTERS,
    }


def build_research_judge_packet(instructions, *, run_id, map_record, reports, outcomes):
    """Count the complete payload without shrinking evidence, roster or instructions."""
    if not isinstance(instructions, str) or not instructions.strip():
        raise ResearchJudgeError("judge instructions are required")
    planned, _accepted, _claims = _inputs(run_id, reports, outcomes)
    policy = research_judge_capacity_policy()
    try:
        packet = _packet_text(instructions, run_id=run_id, map_record=map_record, reports=reports, outcomes=outcomes)
        packet.encode("utf-8")
    except (ValueError, TypeError, UnicodeError, RecursionError) as error:
        raise ResearchJudgeError("judge packet cannot be represented") from error
    size = len(packet)
    reason = None
    # Refused means the declaration/leak barrier, not a provider refusal;
    # provider refusals are failed contributions. Security wins over exit 1.
    if any(outcome["outcome"] == "refused" for outcome in planned.values()):
        reason = "security-refused"
    elif any(outcome["required"] and outcome["outcome"] != "ok" for outcome in planned.values()):
        reason = "required-topic-failed"
    elif size > policy["limit_characters"]:
        reason = "judge-packet-over-limit"
    return {
        "packet": packet,
        "size_characters": size,
        "policy": policy,
        "allowed": reason is None,
        "reason": reason,
        "exit_code": 2 if reason == "security-refused" else (1 if reason else 0),
    }


def research_claim_scores(*, run_id, reports, outcomes, verdicts):
    """Check exclusive valid-claim judgements, then compute every seat's counts/ids.

    Unsupported claims receive no judgement. A unique mark is a supported
    subset; semantic off-brief precedence and evidence meaning remain review.
    """
    planned, _accepted, claims = _inputs(run_id, reports, outcomes)
    try:
        values = _load(verdicts)
        if not isinstance(values, list):
            raise ResearchJudgeError("claim judgements must be a list")
        seen = set()
        decisions = {}
        for value in values:
            _keys(value, {"claim", "disposition", "unique"})
            identifier = value["claim"]
            if (
                not isinstance(identifier, str)
                or identifier not in claims
                or identifier in seen
                or claims[identifier][1] != "valid"
            ):
                raise ResearchJudgeError("unknown, unsupported or repeated claim judgement")
            disposition, unique = value["disposition"], value["unique"]
            if disposition not in DISPOSITIONS or type(unique) is not bool or (unique and disposition != "supported"):
                raise ResearchJudgeError("invalid or nonexclusive claim disposition")
            seen.add(identifier)
            decisions[identifier] = (disposition, unique)
        if seen != {identifier for identifier, (_key, status) in claims.items() if status == "valid"}:
            raise ResearchJudgeError("a valid claim has no exclusive judgement")
    except ResearchReportError as error:
        raise ResearchJudgeError("invalid raw claim judgements") from error
    scores = {}
    for key in sorted(planned):
        outcome = planned[key]
        scores[key] = {
            "topic": key[0],
            "seat": key[1],
            "outcome": outcome["outcome"],
            **{name: {"count": 0, "claims": []} for name in (*DISPOSITIONS, "unsupported", "unique")},
        }
    for identifier in sorted(claims):
        key, status = claims[identifier]
        if status == "unsupported":
            names = ["unsupported"]
        else:
            disposition, unique = decisions[identifier]
            names = [disposition] + (["unique"] if unique else [])
        for name in names:
            scores[key][name]["claims"].append(identifier)
            scores[key][name]["count"] += 1
    return list(scores.values())
