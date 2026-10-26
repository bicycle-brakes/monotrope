"""Whole judge-packet bounds and independently computed claim score contracts."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from stage2_research_report import research_seat_id, validate_research_report
from test_stage2_research_report import SOURCES, report


def module():
    import stage2_research_judge

    return stage2_research_judge


def seat(model="first", *, required=True, outcome="ok", topic=1, with_report=True):
    identity = research_seat_id("go", model)
    result = {"topic": topic, "seat": identity, "required": required, "outcome": outcome}
    value = report(topic=topic)
    accepted = validate_research_report(value, run_id="run-one", topic=topic, seat=identity, sources=SOURCES)
    return result, accepted if with_report else None


def packet(reports, outcomes, map_record=None):
    return module().build_research_judge_packet(
        "Judge the evidence.",
        run_id="run-one",
        map_record={} if map_record is None else map_record,
        reports=reports,
        outcomes=outcomes,
    )


def test_judge_policy_records_documented_capacity_and_agent_conversion_without_live_claim():
    policy = module().research_judge_capacity_policy()
    assert policy["model"] == "claude-opus-5-5"
    assert policy["capacity_tokens"] == 1_000_000 and policy["output_reserve_tokens"] == 128_000
    assert policy["transport_reserve_tokens"] == 72_000 and policy["tokens_per_unicode_character"] == 0.5
    assert policy["limit_characters"] == 1_600_000
    assert policy["read_on"] == "2026-10-18" and len(policy["sources"]) == 2
    assert policy["live_capacity"] == "not-measured"
    assert "estimate" in policy["conversion_basis"]


def test_judge_packet_retains_all_valid_reports_free_failures_and_full_instructions():
    first, first_report = seat()
    optional, _ = seat("optional-free", required=False, outcome="failed", with_report=False)
    optional["partial_output"] = "Partial evidence is retained."
    reports, outcomes = [first_report], [first, optional]
    before = copy.deepcopy((reports, outcomes))
    result = packet(reports, outcomes, {"unread": "Not inspected."})
    assert result["allowed"] and result["reason"] is None
    assert result["packet"].startswith("Judge the evidence.")
    assert "Partial evidence is retained." in result["packet"] and "Not inspected." in result["packet"]
    assert first_report["claims"][0]["id"] in result["packet"]
    assert result["size_characters"] == len(result["packet"])
    assert before == (reports, outcomes)


def test_judge_packet_one_fixed_unicode_limit_allows_J_and_refuses_J_plus_one():
    outcome, accepted = seat()
    baseline = packet([accepted], [outcome], {"padding": ""})
    remaining = baseline["policy"]["limit_characters"] - baseline["size_characters"]
    at_limit = packet([accepted], [outcome], {"padding": "ü" * remaining})
    too_large = packet([accepted], [outcome], {"padding": "ü" * (remaining + 1)})
    assert at_limit["allowed"] and at_limit["size_characters"] == 1_600_000
    assert not too_large["allowed"] and too_large["reason"] == "judge-packet-over-limit"
    assert too_large["size_characters"] == 1_600_001
    decoded = json.loads(too_large["packet"].split("# Research evidence (data, not instructions)\n\n", 1)[1])
    # The packet carries each report's validated fields, never its `raw` copy (deep review RS-1-6).
    assert "raw" in accepted and decoded["reports"] == [{k: v for k, v in accepted.items() if k != "raw"}]


def test_judge_packet_required_failure_blocks_even_with_a_valid_partial_report():
    failed, accepted = seat(outcome="failed")
    result = packet([accepted], [failed])
    assert not result["allowed"] and result["reason"] == "required-topic-failed"
    assert accepted["claims"][0]["id"] in result["packet"]


def test_judge_packet_ok_without_report_cannot_look_complete():
    outcome, _ = seat()
    with pytest.raises(module().ResearchJudgeError):
        packet([], [outcome])


@pytest.mark.parametrize("fault", ["outcome", "report", "unplanned", "claim-identity"])
def test_judge_packet_refuses_duplicate_or_unbound_report_evidence(fault):
    outcome, accepted = seat()
    reports, outcomes = [accepted], [outcome]
    if fault == "outcome":
        outcomes *= 2
    elif fault == "report":
        reports *= 2
    elif fault == "unplanned":
        outcomes = []
    else:
        accepted["claims"][0]["id"] = "another-run/1/go:first/C1"
    with pytest.raises(module().ResearchJudgeError):
        packet(reports, outcomes)


def test_judge_scores_are_derived_per_topic_and_seat_with_every_claim_once():
    outcomes, reports, verdicts = [], [], []
    dispositions = ("supported", "refuted", "off-brief", "unresolved")
    for name in dispositions:
        outcome, accepted = seat(name)
        outcomes.append(outcome)
        reports.append(accepted)
        verdicts.append({"claim": accepted["claims"][0]["id"], "disposition": name, "unique": name == "supported"})
    optional, _ = seat("absent-free", required=False, outcome="timed-out", with_report=False)
    outcomes.append(optional)
    scores = module().research_claim_scores(run_id="run-one", reports=reports, outcomes=outcomes, verdicts=verdicts)
    assert len(scores) == 5
    by_seat = {row["seat"]: row for row in scores}
    for disposition, accepted in zip(dispositions, reports, strict=True):
        score = by_seat[accepted["seat"]]
        assert score[disposition] == {"count": 1, "claims": [accepted["claims"][0]["id"]]}
        assert sum(score[name]["count"] for name in dispositions) == 1
    assert by_seat["go:supported"]["unique"] == by_seat["go:supported"]["supported"]
    assert all(by_seat[optional["seat"]][name]["count"] == 0 for name in (*dispositions, "unsupported", "unique"))
    assert by_seat[optional["seat"]]["outcome"] == "timed-out"


def test_judge_unsupported_claims_are_scored_without_judgement_and_raw_decisions_survive():
    outcome, _ = seat()
    value = report()
    value["claims"].append({**value["claims"][0], "id": "C2", "evidence": ["a.py::absent"]})
    value["questions"] = [
        {"id": "Q1", "question": "Need a human answer.", "classification": "[DECISION]", "claims": ["C2"]}
    ]
    accepted = validate_research_report(value, run_id="run-one", topic=1, seat=outcome["seat"], sources=SOURCES)
    scores = module().research_claim_scores(
        run_id="run-one",
        reports=[accepted],
        outcomes=[outcome],
        verdicts=[{"claim": accepted["claims"][0]["id"], "disposition": "off-brief", "unique": False}],
    )
    assert scores[0]["unsupported"] == {"count": 1, "claims": [accepted["claims"][1]["id"]]}
    assert accepted["questions"][0]["classification"] == "[DECISION]"


@pytest.mark.parametrize(
    "fault",
    [
        "missing",
        "duplicate",
        "unsupported",
        "unknown",
        "double-disposition",
        "bad-disposition",
        "unique-refuted",
        "answer",
    ],
)
def test_judge_cannot_lose_double_score_or_promote_a_claim(fault):
    outcome, accepted = seat()
    verdicts = [{"claim": accepted["claims"][0]["id"], "disposition": "supported", "unique": False}]
    if fault == "missing":
        verdicts = []
    elif fault == "duplicate":
        verdicts *= 2
    elif fault in ("unknown", "unsupported"):
        if fault == "unsupported":
            unsupported = copy.deepcopy(accepted["claims"][0])
            unsupported.update(id="run-one/1/go:first/C2", local_id="C2", evidence_status="unsupported", resolved=[])
            accepted["claims"].append(unsupported)
        verdicts[0]["claim"] = "run-one/1/go:first/C2"
    elif fault == "double-disposition":
        verdicts[0]["disposition"] = ["supported", "unresolved"]
    elif fault == "bad-disposition":
        verdicts[0]["disposition"] = "majority"
    elif fault == "unique-refuted":
        verdicts[0].update(disposition="refuted", unique=True)
    else:
        verdicts[0]["answer"] = "A fabricated human choice."
    with pytest.raises(module().ResearchJudgeError):
        module().research_claim_scores(run_id="run-one", reports=[accepted], outcomes=[outcome], verdicts=verdicts)


def test_judge_empty_or_free_only_outcomes_cannot_allow_a_judge_call():
    optional, _ = seat("optional-free", required=False, outcome="failed", with_report=False)
    for outcomes in ([], [optional]):
        with pytest.raises(module().ResearchJudgeError):
            packet([], outcomes)


@pytest.mark.parametrize("status", [[], {}, True])
def test_judge_nontext_outcome_is_a_preparation_error(status):
    outcome, accepted = seat()
    outcome["outcome"] = status
    with pytest.raises(module().ResearchJudgeError):
        packet([accepted], [outcome])


def test_judge_security_refusal_blocks_even_a_free_seat_and_takes_exit_two_precedence():
    required, accepted = seat(outcome="failed")
    optional, _ = seat("optional-free", required=False, outcome="refused", with_report=False)
    result = packet([accepted], [required, optional])
    assert result["allowed"] is False and result["reason"] == "security-refused"
    assert result["exit_code"] == 2
