"""Paid terms expire: the `valid_until` boundary of paid admission (bead coding-harness-abra).

Every case runs the runner against synthetic `opencode-go` declarations and
controls only the terms UTC-date seam, `stage2.terms_today`; the runner's
accounting clocks stay live, and receipt age stays measured by its own clock
(`stage2_availability.now`). The migration assertions (criteria 6 and 7) read
the repository's real declaration, which the orchestrator edits by hand before
phase 4. No test reaches a real endpoint: reviewer and probe calls run through
the stand-ins the shared `world` fixture plants.

Each behavioral test's fault is the refusal the baseline runner lacks: on the
baseline's `terms_problem` every date-question here admits the model instead.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
import stage2_availability as availability  # noqa: E402
from terms_fixtures import admissible_terms  # noqa: E402
from test_stage2 import (  # noqa: E402
    FIXED,
    MALFORMED_ANSWER,
    REPO_ROOT,
    TEST_FLASH,
    TEST_FREE,
    TEST_LADDER,
    TEST_RUNGS,
    VERDICT,
    World,
    decide_record,
    forget_the_run,
    loop_state,
    rows,
    rung_of,
)
from test_stage2 import world as stage2_world  # noqa: E402
from test_stage2_availability import enable, receipt  # noqa: E402
from test_stage2_swarm import sworld as research_world  # noqa: E402

world = stage2_world
sworld = research_world


def set_terms(w: World, model: str, **changes: object) -> None:
    """Rewrite one declared model's terms record in the world's declaration."""
    path = w.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["modelle_terms"][model].update(changes)
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


RECORDED_BASE = "https://opencode.ai/zen/go/v1"


def go_store(model: str) -> dict:
    """A refreshed store whose one Go row sits on the record's path, ready to assess."""
    return {
        "opencode-go": {
            "models": [{"id": model, "provider": "opencode-go", "api": "openai-completions", "baseUrl": RECORDED_BASE}],
            "lastModified": 0,
        }
    }


def disable_preparation(w: World) -> None:
    """Take the availability rule back out: the record's legacy path again."""
    path = w.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry.pop("availability_preflight", None)
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def a_record(**changes: object) -> dict:
    """One admissible record, dated far ahead, with the given fields replaced."""
    return {"modelle_terms": {"m": admissible_terms(**changes)}}


# ---------------------------------------------------------------------------
# Criterion 1: no usable `valid_until`, no admission
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "valid_until",
    [
        None,  # the field is missing
        "",  # empty
        True,  # not a string
        20261031,  # not a string
        dt.date(2026, 10, 31),  # a YAML-native date, not the quoted string
        dt.datetime(2026, 10, 31, 12, 0, tzinfo=dt.UTC),  # a timestamp
        "2026-10-31T00:00:00",  # a timestamp in string form
        "2026-2-3",  # malformed
        "31.10.2026",  # malformed
        " 2026-10-31",  # padded
        "2026-10-31 ",  # padded
        "2026-13-01",  # impossible calendar date
        "2026-02-30",  # impossible calendar date
        "2027-02-29",  # no leap day
    ],
)
def test_paid_terms_require_a_usable_expiry(valid_until: object, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 1: a missing or unusable date admits no paid model, and none is invented."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 26))
    record = a_record()
    if valid_until is None:
        del record["modelle_terms"]["m"]["valid_until"]  # the field is missing
    else:
        record["modelle_terms"]["m"]["valid_until"] = valid_until
    problem = stage2.terms_problem(record, "m")
    assert problem is not None and "m" in problem, problem
    if valid_until is None:
        assert "missing" in problem, problem
    elif isinstance(valid_until, str):
        assert "not a quoted ISO date" in problem, problem
    # The positive control: the quoted ISO string itself admits.
    assert stage2.terms_problem(a_record(valid_until="2026-11-30"), "m") is None


# ---------------------------------------------------------------------------
# Criterion 2: inclusive on the UTC day, decided in UTC
# ---------------------------------------------------------------------------


def test_expiry_is_inclusive_on_the_utc_day(monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 2: valid through the named UTC day, refused the day after — never by the local date."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 31))
    assert stage2.terms_problem(a_record(valid_until="2026-10-31"), "m") is None, "the expiry day admitted"
    assert stage2.terms_problem(a_record(valid_until="2026-11-01"), "m") is None, "a later day admitted"
    expired = stage2.terms_problem(a_record(valid_until="2026-10-30"), "m")
    assert expired and "expired on 2026-10-30" in expired, expired

    # The judgement reads UTC, not the local calendar: at 23:40 UTC a zone a
    # day ahead (UTC+14) already reads 2026-11-01, and it must not decide.
    class LocalDateAhead(dt.date):
        @classmethod
        def today(cls) -> dt.date:
            return dt.date(2026, 11, 1)

    class FrozenDateTime(dt.datetime):
        @classmethod
        def now(cls, _tz=None) -> dt.datetime:
            return dt.datetime(2026, 10, 31, 23, 40, tzinfo=dt.UTC)

    # Lift the constant seam first, or the fakes below are never read and a
    # local-date implementation would pass (review loop row L1-2).
    monkeypatch.undo()
    monkeypatch.setattr(stage2.dt, "date", LocalDateAhead)
    monkeypatch.setattr(stage2.dt, "datetime", FrozenDateTime)
    assert stage2.terms_today() == dt.date(2026, 10, 31), "the local date decided, not UTC"
    assert stage2.terms_problem(a_record(valid_until="2026-10-31"), "m") is None


# ---------------------------------------------------------------------------
# Criterion 3: exclusions name the model, the kind and the passed date
# ---------------------------------------------------------------------------


def test_expiry_skips_name_model_and_reason(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 3: preparation names every excluded id with missing, invalid or passed and the date."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 11, 1))
    set_terms(world, TEST_LADDER[0], valid_until="2026-10-31")
    set_terms(world, TEST_LADDER[1], valid_until=True)
    set_terms(world, TEST_RUNGS[0], valid_until=None)
    named = stage2.skipped_models(world.root)
    assert any(TEST_LADDER[0] in reason and "expired on 2026-10-31" in reason for reason in named), named
    assert any(TEST_LADDER[1] in reason and "not a quoted ISO date" in reason for reason in named), named
    assert any(TEST_RUNGS[0] in reason and "valid_until is missing" in reason for reason in named), named
    assert stage2.ladder(world.root) == [], "an excluded model stayed eligible"
    # The same reasons reach preparation's report and its receipt.
    enable(world)
    world.script(pi=[{"stdout": "OK"}] * 5)
    assert world.run("prepare-loop") == 0
    out = capsys.readouterr().out
    assert "Paid admission skipped:" in out
    assert "expired on 2026-10-31" in out and TEST_LADDER[0] in out
    terms_skipped = receipt(world)["state"]["availability"]["terms_skipped"]
    for model in TEST_LADDER[:2] + TEST_RUNGS:
        assert any(model in reason for reason in terms_skipped), (model, terms_skipped)


# ---------------------------------------------------------------------------
# Criterion 4: the warning window, on preparation and every round
# ---------------------------------------------------------------------------


def test_expiry_warning_window_on_preparation_and_review(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 4: warning from seven days out through the expiry day, none at eight or after.

    Fresh, legacy and resumed rounds each evaluate the current day; a skipped
    record warns too, for a warning is notice, never admission.
    """
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 26))

    def warned(valid_until: str) -> list[str]:
        record = a_record()["modelle_terms"]["m"]
        record["valid_until"] = valid_until
        return stage2.terms_warnings({"modelle": ["m"], "modelle_terms": {"m": record}})

    assert len(warned("2026-11-02")) == 1, "no warning seven days out"
    assert warned("2026-11-02") == ["the data terms of m expire on 2026-11-02 (7 days left)"]
    assert len(warned("2026-11-03")) == 0, "a warning eight days out"
    assert len(warned("2026-10-27")) == 1, "no warning one day out"
    assert len(warned("2026-10-26")) == 1, "no warning on the expiry day"
    assert len(warned("2026-10-25")) == 0, "an expired date warned instead of skipped"
    # A skipped record warns too, for a warning is notice, never admission.
    skipped = a_record(uebersprungen="2026-10-17", grund="wire API", valid_until="2026-11-02")["modelle_terms"]["m"]
    assert stage2.terms_problem({"modelle_terms": {"m": skipped}}, "m") is not None
    assert stage2.terms_warnings({"modelle": ["m"], "modelle_terms": {"m": skipped}}) == [
        "the data terms of m expire on 2026-11-02 (7 days left)"
    ]
    set_terms(world, TEST_LADDER[0], valid_until="2026-10-28")
    # A fresh run's first round is the free swarm; the warning joins its notes.
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 0
    first = capsys.readouterr().err
    line = f"review-loop: Notice: the data terms of {TEST_LADDER[0]} expire on 2026-10-28 (2 days left)."
    assert line in first, first
    # A legacy run's next round re-evaluates the current day and warns again.
    decide_record(world, status=FIXED)
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 0
    second = capsys.readouterr().err
    assert line in second, second
    text = world.record().read_text(encoding="utf-8")
    note = f"Notice: the data terms of {TEST_LADDER[0]} expire on 2026-10-28 (2 days left)."
    assert text.count(note) == 2, "the resumed round did not renew the warning in the record"


# ---------------------------------------------------------------------------
# Criterion 5: a saved admission cannot authorize an expired call
# ---------------------------------------------------------------------------


def test_saved_admission_cannot_authorize_an_expired_call(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 5: receipt-backed and saved selections recheck the day — an expired member dispatches nothing."""
    clock = {"day": dt.date(2026, 10, 31)}
    monkeypatch.setattr(stage2, "terms_today", lambda: clock["day"])
    start = dt.datetime(2026, 10, 31, 23, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(availability, "now", lambda: start)
    set_terms(world, TEST_LADDER[0], valid_until="2026-10-31")
    # Act 1: preparation on the expiry day admits the member into the receipt's
    # Flash swarm; the free round consumes it, and a day later the saved
    # selection refuses instead of dispatching.
    enable(world)
    assert world.run("prepare-loop") == 0
    prepared = receipt(world)
    assert prepared["state"]["paid"]["flash"][0] == TEST_LADDER[0]
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 0
    decide_record(world, status=FIXED)
    record_after_round = world.record().read_text(encoding="utf-8")
    dispatched = len(world.reviews("pi"))
    clock["day"] = dt.date(2026, 11, 1)
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 2
    assert len(world.reviews("pi")) == dispatched, "an expired member was dispatched on the receipt's selection"
    assert world.record().read_text(encoding="utf-8") == record_after_round, "the refusal reset prior run history"
    assert stage2.rounds_run(world.record().read_text(encoding="utf-8"), "") == 1, "the refusal fabricated a round"
    assert "expired on 2026-10-31" in capsys.readouterr().err
    capsys.readouterr()
    # Act 2: a saved selection whose terms expire after the parent's batch
    # validation refuses immediately before the launch, and history stands.
    clock["day"] = dt.date(2026, 10, 31)
    disable_preparation(world)
    forget_the_run(world)
    world.write_record([("L1-1", FIXED, "no")], state=loop_state(("free",)))
    record_before = world.record().read_text(encoding="utf-8")
    dispatched = len(world.reviews("pi"))
    world.script(pi=[{"stdout": rows(1)}] * 2)

    real = stage2.checked_prompt
    checked_members = []

    def flip_after_batch(ctx, endpoint, prompt, admission_problem=None):
        result = real(ctx, endpoint, prompt, admission_problem)
        checked_members.append(endpoint[1])
        if endpoint[1] == TEST_FLASH[1]:
            clock["day"] = dt.date(2026, 11, 1)
        return result

    monkeypatch.setattr(stage2, "checked_prompt", flip_after_batch)
    assert world.run("review-loop") == 2
    assert world.reviews("pi")[dispatched:] == [], "an expired member reached the model after the batch checks"
    assert world.record().read_text(encoding="utf-8") == record_before, "the refusal reset prior run history"
    assert '"consumed": ["free"]' in record_before, "the seeded snapshot was not what the refusal preserved"
    assert checked_members == list(TEST_FLASH), "the test never completed the parent batch checks"
    assert stage2.rounds_run(world.record().read_text(), "") == 1
    assert not world.findings.exists(), "the pre-launch refusal wrote call audits or a round"
    assert "expired on 2026-10-31" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Criterion 5: retries, replacements and probes recheck the day
# ---------------------------------------------------------------------------


def test_paid_retries_and_replacements_recheck_expiry(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 5: a probe retry, the compatibility probe, a Flash replacement and a
    malformed-answer retry each refuse an expired model instead of dispatching it."""
    clock = {"day": dt.date(2026, 10, 31)}
    monkeypatch.setattr(stage2, "terms_today", lambda: clock["day"])
    start = dt.datetime(2026, 10, 31, 12, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(availability, "now", lambda: start)
    # Act 1: the first availability probe of an expiring model times out, the
    # day passes, and the second probe is refused instead of trusted.
    set_terms(world, TEST_LADDER[0], valid_until="2026-10-31")
    enable(world)
    tries: list[str] = []

    def probe(_runner, _root, _change, model, _key, _audit, _store, **_options):
        if model == TEST_LADDER[0]:
            tries.append(model)
            if len(tries) == 1:
                clock["day"] = dt.date(2026, 11, 1)
                raise stage2.CallFailed(
                    f"pi was stopped by the availability probe limit of {availability.PROBE_SECONDS} seconds"
                )
        return "OK"

    real_probe_go = availability.probe_go
    monkeypatch.setattr(availability, "probe_go", probe)
    assert world.run("prepare-loop") == 2
    assert tries == [TEST_LADDER[0]]
    assert not availability.receipt_path(world.root, "demo", stage2).exists(), "a refused attempt left a receipt"
    capsys.readouterr()
    # Act 2: the compatibility probe names the expired model and calls it never.
    monkeypatch.setattr(availability, "probe_go", real_probe_go)
    world.script(pi=[{"stdout": "OK"}] * 4)
    assert world.run("probe") == 0
    probed = [rung_of(call) for call in world.reviews("pi")]
    assert TEST_LADDER[0] not in probed, "an expired model was probed"
    assert set(probed) == {*TEST_FREE, TEST_LADDER[1], TEST_RUNGS[0]}, probed
    out = capsys.readouterr().out
    assert TEST_LADDER[0] in out and "expired on 2026-10-31" in out
    # Act 3: a Flash replacement of a failed member refuses on its own terms.
    disable_preparation(world)
    forget_the_run(world)
    set_terms(world, TEST_LADDER[0], valid_until="2099-01-01")
    set_terms(world, TEST_RUNGS[0], valid_until="2026-10-31")
    world.write_record([("L1-1", FIXED, "no")], state=loop_state(("free",)))
    record_before = world.record().read_text(encoding="utf-8")
    dispatched = len(world.reviews("pi"))
    world.script(pi=[{"model": TEST_FLASH[0], "exit": 1, "stderr": "down"}, {"stdout": rows(1)}])
    # The expired replacement is skipped as not admitted, never called; the round keeps the
    # surviving member's real rows (review-loop-deep-b criterion 1), so nothing is fabricated.
    assert world.run("review-loop") == 0
    made = [rung_of(call) for call in world.reviews("pi")[dispatched:]]
    assert sorted(made) == sorted(TEST_FLASH), "the expired rung was called"
    assert world.record().read_text(encoding="utf-8") != record_before
    err = capsys.readouterr().err
    assert f"{TEST_RUNGS[0]} not admitted" in err and "expired on 2026-10-31" in err
    # Act 4: a malformed first answer is asked again only while the terms hold.
    # Act 3 kept its round, so the Flash stage is set up again from the same record.
    world.write_record([("L1-1", FIXED, "no")], state=loop_state(("free",)))
    record_before = world.record().read_text(encoding="utf-8")
    set_terms(world, TEST_LADDER[0], valid_until="2026-10-31")
    set_terms(world, TEST_LADDER[1], valid_until="2026-10-31")
    set_terms(world, TEST_RUNGS[0], valid_until="2026-10-31")
    clock["day"] = dt.date(2026, 10, 31)

    def expire(_ctx, members, _prompts, _key, **_options):
        clock["day"] = dt.date(2026, 11, 1)
        return {member: stage2.MalformedAnswer(MALFORMED_ANSWER) for member in members}

    monkeypatch.setattr(stage2, "run_swarm", expire)
    world.script(pi=[{"stdout": MALFORMED_ANSWER}] * 4)
    dispatched = len(world.reviews("pi"))
    assert world.run("review-loop") == 2
    assert len(world.reviews("pi")) == dispatched, "a retry was dispatched after the day turned"
    text = world.text()
    assert "audit calls: 2" in text
    assert "was asked again with the format reminder" not in text
    assert world.record().read_text(encoding="utf-8") == record_before


@pytest.mark.parametrize("path", ["retry", "replacement", "prepare", "prepare-retry", "compatibility"])
def test_paid_calls_recheck_expiry_after_leak_scan(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], path: str
) -> None:
    """UTC midnight inside a clean scan must refuse the next paid dispatch, without a completed round."""
    clock = {"day": dt.date(2026, 10, 31)}
    monkeypatch.setattr(stage2, "terms_today", lambda: clock["day"])
    target = TEST_RUNGS[0] if path == "replacement" else TEST_LADDER[0]
    set_terms(world, target, valid_until="2026-10-31")
    record_before = None
    if path.startswith("prepare"):
        enable(world)
    elif path != "compatibility":
        world.write_record([("L1-1", FIXED, "no")], state=loop_state(("free",)))
        record_before = world.record().read_bytes()

    real_check = stage2.leakcheck.check
    scans = []

    def cross_midnight(*args, **kwargs):
        result = real_check(*args, **kwargs)
        prompt = dict(args[3])["prompt"] if len(args) > 3 else ""
        # Paid review scans identify the member in the prompt; preparation
        # probes use identical text, so identify their current model below.
        if path in ("retry", "replacement"):
            hit = f"you are `{target}`" in prompt and (path == "replacement" or stage2.FORMAT_REMINDER in prompt)
        else:
            hit = active_model[0] == target and (path != "prepare-retry" or probe_attempts[0] == 2)
        if hit:
            scans.append(target)
            clock["day"] = dt.date(2026, 11, 1)
        return result

    active_model = [None]
    probe_attempts = [0]
    if path.startswith("prepare"):
        real_probe = availability.probe_go

        def probe(runner, root, change, model, key, audit, store, **options):
            active_model[0] = model
            if model == target:
                probe_attempts[0] += 1
                if path == "prepare-retry" and probe_attempts[0] == 1:
                    raise stage2.CallFailed("pi was stopped by the probe limit")
            return real_probe(runner, root, change, model, key, audit, store, **options)

        monkeypatch.setattr(availability, "probe_go", probe)
    elif path == "compatibility":
        real_checked = stage2.checked_prompt

        def checked(ctx, endpoint, prompt, admission_problem=None):
            active_model[0] = endpoint[1]
            return real_checked(ctx, endpoint, prompt, admission_problem)

        monkeypatch.setattr(stage2, "checked_prompt", checked)

    monkeypatch.setattr(stage2.leakcheck, "check", cross_midnight)
    if path == "replacement":
        world.script(pi=[{"model": TEST_FLASH[0], "exit": 1, "stderr": "down"}, {"stdout": rows(1)}])
    elif path == "retry":
        world.script(pi=[{"model": TEST_FLASH[0], "stdout": MALFORMED_ANSWER}, {"stdout": rows(1)}])
    else:
        world.script(pi=[{"stdout": "OK"}] * 10)
    verb = "prepare-loop" if path.startswith("prepare") else "probe" if path == "compatibility" else "review-loop"
    assert world.run(verb) == 2
    assert scans == [target], "the test did not cross midnight in the target's scan"
    calls = [rung_of(call) for call in world.reviews("pi")]
    assert calls.count(target) == (1 if path == "retry" else 0), (
        "a paid call dispatched after its scan crossed midnight"
    )
    assert "expired on 2026-10-31" in capsys.readouterr().err
    if record_before is not None:
        assert world.record().read_bytes() == record_before, "the refusal changed prior run history"
    if path.startswith("prepare"):
        assert not availability.receipt_path(world.root, "demo", stage2).exists()


# ---------------------------------------------------------------------------
# Criteria 6 and 7: the migration of the real declaration
# ---------------------------------------------------------------------------


def test_non_deepseek_records_receive_reading_plus_thirty_days() -> None:
    """Criterion 6: every non-DeepSeek record expires `gelesen` plus 30 days, or on the end date its prose states.

    The rule, not a date, is pinned: a documented renewal re-reads a record
    and moves both dates, and must not need a test edit (review loop row L1-3).
    """
    entry = stage2.endpoint_entry(REPO_ROOT)
    terms = entry["modelle_terms"]
    assert set(terms) >= set(entry["modelle"]), "a declared paid model has no terms record at all"
    deepseek = {"deepseek-v4.1-flash", "deepseek-v4-pro"}
    for model, record in terms.items():
        if model in deepseek:
            continue
        assert isinstance(record.get("gelesen"), str) and record["gelesen"], model
        assert isinstance(record.get("valid_until"), str), f"{model}: the expiry is not the quoted string"
        expected = (dt.date.fromisoformat(record["gelesen"]) + dt.timedelta(days=30)).isoformat()
        stated = f"valid through {record['valid_until']}" in str(record.get("aufbewahrung", ""))
        assert record["valid_until"] == expected or stated, (
            f"{model}: {record['valid_until']} is neither the reading plus 30 days nor an end date the record states"
        )


def test_both_deepseek_records_use_the_documented_expiry() -> None:
    """Criterion 7: both DeepSeek records carry the source's own end date, after the reading, and the prose.

    The 2026-10-25 re-read set 2026-10-31; a monthly renewal moves both
    dates, so the test pins the rule rather than those dates (review loop row L1-3).
    """
    terms = stage2.endpoint_entry(REPO_ROOT)["modelle_terms"]
    for model in ("deepseek-v4.1-flash", "deepseek-v4-pro"):
        record = terms[model]
        assert isinstance(record.get("valid_until"), str), f"{model}: the expiry is not the quoted string"
        read = dt.date.fromisoformat(record["gelesen"])
        until = dt.date.fromisoformat(record["valid_until"])
        assert read <= until, f"{model}: expires before it was read"
        assert "renewed monthly" in record["aufbewahrung"], model
        assert f"valid through {record['valid_until']}" in record["aufbewahrung"], (
            f"{model}: valid_until is not the end date the source states"
        )
        # The generic 30-day rule did not swallow them.
        assert until != read + dt.timedelta(days=30), f"{model}: the generic rule replaced the source's date"


# ---------------------------------------------------------------------------
# Criterion 8: the runner renews nothing
# ---------------------------------------------------------------------------


def test_terms_evaluation_never_renews_the_declaration(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 8: preparation and a review round read the declared dates and rewrite no byte."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 30))
    set_terms(world, TEST_LADDER[0], valid_until="2026-10-31")
    declaration = world.root / "model-endpoints.yaml"
    enable(world)
    before = declaration.read_bytes()
    world.script(pi=[{"stdout": "OK"}] * 5)
    assert world.run("prepare-loop") == 0
    prepared = receipt(world)
    world.script(pi=[{"stdout": rows(1)}] * 3)
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 0
    assert declaration.read_bytes() == before, "terms evaluation rewrote the declaration"
    assert f"the data terms of {TEST_LADDER[0]} expire on 2026-10-31 (1 day left)" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Criterion 9: expiry preserves every prior admission guard
# ---------------------------------------------------------------------------


def test_expiry_preserves_prior_admission_guards(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 9: a future expiry admits no skipped, unread or training-enabled record, and an
    all-expired ladder reports a refusal, never a clean round."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 26))

    def entry_with(model: str, **changes: object) -> dict:
        return {"modelle_terms": {model: admissible_terms(**changes)}}

    problem = stage2.terms_problem(entry_with("m", uebersprungen="2026-10-17", grund="wire API"), "m")
    assert problem and "was skipped on 2026-10-17" in problem and "valid_until" not in problem, problem
    problem = stage2.terms_problem(entry_with("m", training="Yes"), "m")
    assert problem and "training" in problem and "valid_until" not in problem, problem
    problem = stage2.terms_problem(entry_with("m", aufbewahrung="  "), "m")
    assert problem and "retention" in problem and "valid_until" not in problem, problem
    problem = stage2.terms_problem({"modelle_terms": {}}, "m")
    assert problem and "no dated reading" in problem, "an unread record became admissible by expiry alone"
    # The world act: every paid reading expired, the free round still runs and
    # the next paid stage refuses on expiry — never a clean round.
    for model in TEST_LADDER:
        set_terms(world, model, valid_until="2026-10-25")
    assert stage2.ladder(world.root) == []
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 0
    assert sorted(rung_of(call) for call in world.reviews("pi")) == sorted(TEST_FREE)
    decide_record(world, status=FIXED)
    assert world.run("review-loop") == 2, "an empty eligible selection was reported as a clean round"
    assert stage2.CLEAN_CODE != 2 and "expired on 2026-10-25" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Criterion 10: the warning survives receipt, round and release
# ---------------------------------------------------------------------------


def _check_dispatch_time_warning_evidence(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    preparation: str,
    expiry: str,
) -> None:
    """Warnings first emitted at dispatch survive each caller, including midnight and changed day counts."""
    world = request.getfixturevalue("sworld" if preparation == "research-run" else "world")
    if preparation == "research-run":
        world.complete()
        prepare = world.run
        model = "mimo-v2.6-pro"
    elif preparation == "review":
        world.write_record([("L1-1", FIXED, "no")], state=loop_state(("free",)))
        world.script(pi=[{"stdout": rows(1)}] * 3)

        def prepare():
            return world.run("review-loop")

        model = TEST_LADDER[0]
    elif preparation == "research":
        from test_stage2_research_availability import Fixture

        fx = Fixture(world, monkeypatch)
        prepare, read_receipt = fx.prepare, fx.receipt
        model = "deepseek-v4.1-flash"
    else:
        enable(world)

        def prepare():
            return world.run("prepare-loop")

        def read_receipt():
            return receipt(world)

        model = TEST_LADDER[0]
    set_terms(world, model, valid_until=expiry)
    day = dt.date(2026, 10, 27)
    monkeypatch.setattr(stage2, "terms_today", lambda: day)
    dispatch = stage2.dispatch_go

    def cross_midnight(root, ident, send, *args, **kwargs):
        nonlocal day
        if ident == model:
            day = dt.date(2026, 10, 28)
        result = dispatch(root, ident, send, *args, **kwargs)
        # By evidence creation even this dispatch's warning is out of date:
        # recomputing only at the end cannot recover what was printed.
        day = dt.date(2026, 10, 29) if ident == model else day
        return result

    monkeypatch.setattr(stage2, "dispatch_go", cross_midnight)
    assert prepare() == 0
    output = capsys.readouterr().out
    emitted = list(
        dict.fromkeys(
            line.removeprefix("Terms warning: ") for line in output.splitlines() if line.startswith("Terms warning: ")
        )
    )
    days = (dt.date.fromisoformat(expiry) - dt.date(2026, 10, 28)).days
    warning = f"the data terms of {model} expire on {expiry} ({days} days left)"
    assert warning in emitted, "the synthetic probe did not print the midnight warning"
    if preparation == "research-run":
        evidence = world.research.read_text(encoding="utf-8")
        assert emitted and all(item in evidence for item in emitted), "research publication lost dispatch warnings"
    elif preparation == "review":
        evidence = world.record().read_text(encoding="utf-8")
        assert emitted and all(item in evidence for item in emitted), "round lost dispatch warnings"
        decide_record(world, status=FIXED)
        world.write_findings(VERDICT)
        assert world.run("release-loop") == 0
        assert all(item in world.text() for item in emitted), "release lost dispatch warnings"
    else:
        saved = read_receipt()
        assert availability.verify(saved, saved["report_id"]), "warning evidence must be sealed"
        assert saved["state"]["availability"]["terms_warnings"] == emitted
    assert stage2.retain_terms_warnings([]) == [], "caller leaked warning evidence into later operations"


@pytest.mark.parametrize("preparation", ["loop", "research", "review", "research-run"])
@pytest.mark.parametrize("expiry", ["2026-11-04", "2026-10-31"])
def test_dispatch_time_warnings_reach_every_callers_evidence(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    preparation: str,
    expiry: str,
) -> None:
    """Dispatch warnings survive receipts, review rounds and release, and research publication."""
    _check_dispatch_time_warning_evidence(request, monkeypatch, capsys, preparation, expiry)


@pytest.mark.parametrize("preparation", ["loop", "research"])
@pytest.mark.parametrize("expiry", ["2026-11-04", "2026-10-31"])
def test_preparation_receipt_keeps_warnings_emitted_during_probes(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    preparation: str,
    expiry: str,
) -> None:
    """Keep the regression named by the prior preparation repair evidence."""
    _check_dispatch_time_warning_evidence(request, monkeypatch, capsys, preparation, expiry)


def test_expiry_warnings_survive_receipt_round_and_release(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 10: one day out, the warning stands in the receipt, the round record and the released findings."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 30))
    set_terms(world, TEST_LADDER[0], valid_until="2026-10-31")
    warning = f"the data terms of {TEST_LADDER[0]} expire on 2026-10-31 (1 day left)"
    enable(world)
    world.script(pi=[{"stdout": "OK"}] * 5)
    assert world.run("prepare-loop") == 0
    assert receipt(world)["state"]["availability"]["terms_warnings"] == [warning]
    assert "Terms warning:" in capsys.readouterr().out
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop", "demo", "--availability-reported", receipt(world)["report_id"]) == 0
    assert warning in world.record().read_text(encoding="utf-8")
    decide_record(world, status=FIXED)
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert warning in world.text(), "releasing the round lost the warning"


@pytest.mark.parametrize("case", ["prepare-leak", "prepare-probe", "prepare-expiry", "review-expired", "review-leak"])
def test_expiry_warnings_print_before_a_refused_call(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], case: str
) -> None:
    """A refusal in admission, leak checking or a probe cannot hide another model's warning."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 26))
    set_terms(world, TEST_LADDER[1], valid_until="2026-10-28")
    warning = f"the data terms of {TEST_LADDER[1]} expire on 2026-10-28 (2 days left)"
    seen = []

    def refuse(*_args, **_kwargs):
        output = capsys.readouterr()
        seen.append(output.out + output.err)
        raise stage2.Refused("synthetic call refusal")

    if case.startswith("prepare"):
        enable(world)
        if case == "prepare-probe":
            monkeypatch.setattr(availability, "probe_go", refuse)
        elif case == "prepare-expiry":
            # Skip the free probes so the first scan belongs to the expiring
            # paid model. A warning must precede its post-scan refusal too.
            monkeypatch.setattr(stage2, "free_diff", lambda _root: ("", None))
            set_terms(world, TEST_LADDER[0], valid_until="2026-10-26")
            real_check = availability.leakcheck.check

            def expire_during_scan(*args, **kwargs):
                output = capsys.readouterr()
                seen.append(output.out + output.err)
                result = real_check(*args, **kwargs)
                monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 27))
                return result

            monkeypatch.setattr(availability.leakcheck, "check", expire_during_scan)
        else:
            monkeypatch.setattr(availability.leakcheck, "check", refuse)
        verb = "prepare-loop"
    else:
        world.write_record([("L1-1", FIXED, "no")], state=loop_state(("free",)))
        if case == "review-expired":
            set_terms(world, TEST_LADDER[0], valid_until="2026-10-25")
        else:
            monkeypatch.setattr(stage2, "checked_prompt", refuse)
        verb = "review-loop"
    assert world.run(verb) == 2
    output = capsys.readouterr()
    assert warning in "".join(seen) + output.out + output.err
    if case != "review-expired":
        assert seen, "the active call path never reached the refusal callback"
    if seen:
        assert warning in seen[0], "warning was emitted only after the refused call"
    assert world.reviews() == []
    if verb == "prepare-loop":
        assert not availability.receipt_path(world.root, "demo", stage2).exists()
    else:
        assert stage2.rounds_run(world.record().read_text(), world.text() if world.findings.exists() else "") == 1


def test_spent_refusal_says_no_model_is_substituted(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An expiry-enriched spent-run refusal retains the no-substitution guarantee."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 11, 1))
    for model in TEST_LADDER:
        set_terms(world, model, valid_until="2026-10-31")
    state = loop_state(("free",))
    state["paid"] = {"ladder": [], "flash": [], "rungs": []}
    world.write_record([("L1-1", FIXED, "no")], state=state)
    before = world.record().read_bytes()
    assert world.run("review-loop") == 2
    error = capsys.readouterr().err
    assert "expired on 2026-10-31" in error
    assert "No model is substituted." in error
    assert world.reviews() == []
    assert world.record().read_bytes() == before


@pytest.mark.parametrize("boundary", ["probe", "selected-probe", "dispatch"])
@pytest.mark.parametrize("cross_during_scan", [False, True])
def test_research_probes_and_dispatch_recheck_expiry(
    world: World, monkeypatch: pytest.MonkeyPatch, boundary: str, cross_during_scan: bool
) -> None:
    """Criterion 5: saved research admission cannot outlive paid terms, even across a leak scan."""
    from types import SimpleNamespace

    import stage2_research_run as research
    from stage2_research_dispatch import Slot

    model = TEST_LADDER[0]
    set_terms(world, model, valid_until="2026-10-31")
    day = dt.date(2026, 10, 31)
    monkeypatch.setattr(stage2, "terms_today", lambda: day)
    launches = []

    def launch(*args, **_kwargs):
        launches.append(args)
        return SimpleNamespace(returncode=0, stdout="OK", stderr="")

    def scan(*_args, **_kwargs):
        nonlocal day
        if cross_during_scan and expire:
            day = dt.date(2026, 11, 1)
        return SimpleNamespace(
            verdict=SimpleNamespace(render=lambda: "clean", exit_code=lambda: 0),
            files=1,
            commits=0,
            rules=1,
        )

    monkeypatch.setattr(stage2, "launch", launch)
    monkeypatch.setattr(stage2.leakcheck, "check", scan)
    entry = {"role": "repository", "endpoint": availability.GO, "model": model}
    run = SimpleNamespace(root=world.root, runner=stage2, change="demo", free=[], entries={"saved": entry})
    slot = Slot("saved", availability.GO, True, (0,), 60, {}, "research prompt")
    audit = []
    expire = False

    def probe():
        if boundary == "selected-probe":
            selection = SimpleNamespace(
                runner=stage2,
                root=world.root,
                change="demo",
                key="test-key",
                audit=audit,
                models_store=go_store(model),
                probed={},
                models={f"{availability.GO}/{model}": {"state": "not-probed", "admitted": True}},
            )
            return availability._Selection.reachable(selection, availability.GO, model, "framework")
        return availability.probe_go(stage2, world.root, "demo", model, "test-key", audit, go_store(model))

    if boundary != "dispatch":
        probe()
        assert len(launches) == 1
    else:
        assert not research.Run.gate(run, slot).blocked

    # The selection and its admission were made on the inclusive expiry day.
    # Either resume tomorrow or cross midnight inside the per-call leak scan.
    expire = True
    if not cross_during_scan:
        day = dt.date(2026, 11, 1)
    before = (list(launches), list(audit), dict(run.entries))
    if boundary != "dispatch":
        refusal = None
        try:
            probe()
        except stage2.Refused as error:
            refusal = str(error)
        assert refusal is not None, "expired research terms still authorized a probe"
        assert model in refusal
        assert "expired on 2026-10-31" in refusal
    else:
        verdict = research.Run.gate(run, slot)
        assert verdict.blocked, verdict
        assert model in verdict.record["refused"]
        assert "expired on 2026-10-31" in verdict.record["refused"]
    assert (launches, audit, run.entries) == before


def _check_paid_dispatch(world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Direct sends cannot rely on caller admission, even tool-free probes and research launches."""
    from types import SimpleNamespace

    import stage2_research_run as research
    from stage2_research_dispatch import Slot

    model = TEST_LADDER[0]
    set_terms(world, model, valid_until="2026-10-31")
    day = dt.date(2026, 10, 27)
    monkeypatch.setattr(stage2, "terms_today", lambda: day)
    sent = []

    def send(*args, **kwargs):
        sent.append((args, kwargs))
        return SimpleNamespace(returncode=0, stdout="OK", stderr="")

    monkeypatch.setattr(stage2, "launch", send)
    monkeypatch.setattr(research.subprocess, "Popen", send)
    monkeypatch.setattr(availability, "_checked_probe", lambda *_args: None)
    ctx = stage2.Context(world.root, "demo", world.research.parent, "test-bead")
    ctx.models_store = go_store(model)
    entry = {"program": "pi", "model": model, "endpoint": availability.GO, "role": "repository"}
    run = SimpleNamespace(
        runner=stage2,
        root=world.root,
        entries={"saved": entry},
        scratch={},
        line=lambda _text: None,
        pi_command=lambda *_args: (["synthetic-pi"], world.root, {}),
        selection={"catalog": {"models_store": go_store(model)}},
    )
    slot = Slot("saved", availability.GO, True, (0,), 60, {}, "prompt")
    calls = [
        lambda: stage2.run_reviewer(ctx, model, "prompt", "key"),
        lambda: stage2.run_reviewer(ctx, model, "prompt", "key", free=True),
        lambda: availability.probe_go(stage2, world.root, "demo", model, "key", [], go_store(model)),
        lambda: research.Run.launch(run, slot, 60),
        lambda: stage2.run_swarm(ctx, [model], {model: "prompt"}, "key", free=False),
    ]
    for call in calls:
        capsys.readouterr()
        call()
        output = capsys.readouterr()
        assert model in output.out and "2026-10-31" in output.out, "dispatch omitted the advance warning"
        for scratch in run.scratch.values():
            scratch.cleanup()
        run.scratch.clear()
    assert len(sent) == len(calls)
    day = dt.date(2026, 11, 1)
    for call in calls:
        with pytest.raises(stage2.Refused, match="expired on 2026-10-31"):
            call()
    assert len(sent) == len(calls), "an expired call reached the transport"


def _check_research_preparation_warnings(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Research preparation prints current warnings before probing and seals them in its receipt."""
    from test_stage2_research_availability import Fixture

    fx = Fixture(world, monkeypatch)
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 27))
    model = "deepseek-v4.1-flash"
    set_terms(world, model, valid_until="2026-10-31")
    warning = f"the data terms of {model} expire on 2026-10-31 (4 days left)"
    real_probe = availability.probe_go
    seen = []

    def probe(*args, **kwargs):
        seen.append(capsys.readouterr().out)
        return real_probe(*args, **kwargs)

    monkeypatch.setattr(availability, "probe_go", probe)
    assert fx.prepare() == 0
    assert seen and warning in seen[0], "preparation did not warn before its first probe"
    state = fx.receipt()["state"]
    assert warning in state["availability"]["terms_warnings"]
    assert warning in availability.research_report(state)
    del state["availability"]
    assert availability.research_report(state), "legacy receipts without warnings must remain readable"


@pytest.mark.parametrize("boundary", ["dispatch", "preparation"])
def test_every_paid_dispatch_rechecks_terms_at_one_point(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], boundary: str
) -> None:
    """The shared send guard and shared preparation evidence protect every paid route."""
    if boundary == "preparation":
        _check_research_preparation_warnings(world, monkeypatch, capsys)
    else:
        _check_paid_dispatch(world, monkeypatch, capsys)
