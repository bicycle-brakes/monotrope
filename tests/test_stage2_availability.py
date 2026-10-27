"""Synthetic endpoint failures exercise preparation and the report boundary."""

from __future__ import annotations

import datetime as dt
import fcntl
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
import stage2_availability as availability  # noqa: E402
from test_stage2 import REPO_ROOT, TEST_FREE, TEST_LADDER, VERDICT, World  # noqa: E402
from test_stage2 import world as stage2_world  # noqa: E402

world = stage2_world


def enable(w: World, **changes) -> None:
    path = w.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["availability_preflight"] = {"flash_size": 3, "max_age_seconds": 900, "exclude_until": [], **changes}
    path.write_text(yaml.safe_dump(data))
    w.script(pi=[{"stdout": "OK"}] * 5)


def receipt(w: World) -> dict:
    return json.loads(w.record().with_name("availability.json").read_text())


def test_preparation_filters_failures_and_requires_main_chat_report(world: World, capsys) -> None:
    """Criterion 17: catalog presence alone, fixed Flash ids and silent review starts fail."""
    enable(world)
    world.script(
        pi=[
            {
                "model": model,
                **({"exit": 1, "stderr": "model_coming_soon"} if model == "mimo-v2.6-flash" else {"stdout": "OK"}),
            }
            for model in [*TEST_FREE, *TEST_LADDER]
        ]
    )
    assert world.run("prepare-loop") == 0
    prepared = receipt(world)
    state = prepared["state"]
    assert state["paid"]["flash"] == ["deepseek-v4.1-flash", "mimo-v2.6-pro"]
    assert "model_coming_soon" in state["availability"]["failed"]["mimo-v2.6-flash"]
    assert not world.record().exists(), "a probe was counted as review history"
    output = capsys.readouterr().out
    assert "Report this selection in the main conversation" in output
    calls = len(world.reviews())
    assert world.run("review-loop") == 2
    assert len(world.reviews()) == calls, "review started without report acknowledgment"
    world.script(pi=[{"stdout": "No finding."}] * 2)
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 0
    recorded = stage2.read_state(world.record().read_text(), "")
    assert recorded["availability"] == state["availability"]


@pytest.mark.parametrize("verb", ["prepare-loop", "release-loop", "review-loop"])
def test_each_record_verb_is_refused_by_its_own_lock(world: World, capsys, verb: str) -> None:
    """R-14 (O190-1): each locked call site is driven alone, in a world where the verb gets past its own checks."""
    if verb == "prepare-loop":
        enable(world)
    elif verb == "release-loop":
        world.write_findings(VERDICT)
    else:
        world.script(pi=[{"stdout": "No finding."}] * 2)
    path = stage2.lock_path("demo", world.root)
    path.parent.mkdir(parents=True, exist_ok=True)
    capsys.readouterr()
    with path.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        assert world.run(verb) == 2
    error = capsys.readouterr().err
    assert f"another run holds the loop record `{stage2.record_key('demo', world.root)}`" in error, error
    assert world.reviews() == [], "a refused run still called a reviewer"
    assert world.run(verb) == 0, f"{verb} did not get past its own checks once the lock was free"
    assert "another run holds" not in capsys.readouterr().err


def test_marking_a_repair_waits_for_no_one_and_loses_no_round(world: World) -> None:
    """R-14 (O190-4): `repair` rewrites the record whole, so it takes the record's lock like the other verbs."""
    world.write_record([("L1-1", "taken — test_a", "no")])
    line = next(row for row in world.record().read_text(encoding="utf-8").splitlines() if row.startswith("| L1-1"))
    cells = stage2.split_row(line)
    taken = [("record", [*cells[:7], " \\| ".join(cells[7:-1]), cells[-1]])]
    fixes = {"L1-1": "fixed — not a test — the doctrine names it"}
    before = world.record().read_text(encoding="utf-8")
    path = stage2.lock_path("demo", world.root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(stage2.CallFailed, match="L1-1"):
            stage2.mark_repaired_record("demo", taken, fixes, world.root)
    assert world.record().read_text(encoding="utf-8") == before, "a held record was rewritten"
    stage2.mark_repaired_record("demo", taken, fixes, world.root)
    assert "fixed — not a test — the doctrine names it" in world.record().read_text(encoding="utf-8")


def test_an_accepted_receipt_is_spent_by_the_round_that_is_written(world: World, monkeypatch) -> None:
    """R-14 (O190-3): a failed first attempt leaves the receipt; a written round 1 spends it."""
    enable(world)
    assert world.run("prepare-loop") == 0
    prepared = receipt(world)
    path = availability.receipt_path(world.root, "demo", stage2)
    real = stage2.require_pi

    def missing() -> None:
        raise stage2.Refused("the pinned Pi is not installed")

    monkeypatch.setattr(stage2, "require_pi", missing)
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 2
    assert not world.record().exists(), "a failed attempt left a round behind"
    assert path.exists(), "a failed attempt spent the receipt"
    monkeypatch.setattr(stage2, "require_pi", real)
    world.script(pi=[{"stdout": "No finding."}] * 2)
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 0
    assert not availability.receipt_path(world.root, "demo", stage2).exists(), "the receipt survived its round"
    rounds = len(world.reviews())
    # A consumed receipt and a clean round: the loop is finished (3), not refused (2).
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == stage2.CLEAN_CODE
    assert len(world.reviews()) == rounds, "a spent receipt started a second round"

    assert world.record().exists()
    assert not path.exists(), "the written round did not spend the receipt"


def test_preparation_calls_only_static_toolless_probes(world: World, monkeypatch) -> None:
    """Criterion 17: any source, tools, bare Pi or unchecked call fails this boundary."""
    enable(world)
    launch = stage2.launch
    limits = []

    def capture(command, *args, **kwargs):
        if "--print" in command:
            limits.append(kwargs.get("timeout"))
        return launch(command, *args, **kwargs)

    monkeypatch.setattr(stage2, "launch", capture)
    assert world.run("prepare-loop") == 0
    calls = world.reviews()
    assert len(calls) == len(TEST_FREE) + len(TEST_LADDER)
    for call in calls:
        assert call["path"] == str(world.bin / "pin-pi")
        assert "--no-tools" in call["argv"] and "--tools" not in call["argv"]
        assert call["cwd"] != str(world.root)
        assert "Availability probe only" in call["prompt_file"]
        # Only the free probe carries the diff; the paid probe stays the small static text.
        if not any(f"{model}" in " ".join(call["argv"]) for model in TEST_FREE):
            assert "VALUE = 2" not in call["prompt_file"]
        assert call["argv"][-1] == "Follow the appended availability instructions."
    assert limits == [availability.FREE_PROBE_SECONDS] * len(TEST_FREE) + [60] * len(TEST_LADDER)
    assert world.text().count("prepare-loop · endpoint") == len(calls)


@pytest.mark.parametrize("fault", ["code", "configuration", "expired", "other-worktree", "corrupt"])
def test_prepared_selection_is_bound_to_inputs_and_freshness(world: World, monkeypatch, fault: str) -> None:
    """Criterion 17: stale, malformed or transplanted preparation launches no review."""
    enable(world)
    assert world.run("prepare-loop") == 0
    prepared = receipt(world)
    if fault == "code":
        (world.root / "scripts" / "helper.py").write_text("VALUE = 3\n")
    elif fault == "configuration":
        enable(world, flash_size=2)
    elif fault == "expired":
        later = availability.now() + dt.timedelta(seconds=901)
        monkeypatch.setattr(availability, "now", lambda: later)
    else:
        path = availability.receipt_path(world.root, "demo", stage2)
        if fault == "corrupt":
            path.write_text("not JSON")
        else:
            prepared["binding"]["root"] = "/another/worktree"
            path.write_text(json.dumps(prepared))
    before = len(world.reviews())
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 2
    assert len(world.reviews()) == before


def test_all_failed_preparation_never_creates_a_clean_round_or_reuses_receipt(world: World) -> None:
    """Criterion 17: all failures must invalidate a previously successful selection."""
    enable(world)
    assert world.run("prepare-loop") == 0
    world.script(pi=[{"exit": 1, "stderr": "unavailable"}] * 5)
    assert world.run("prepare-loop") == 2
    assert not availability.receipt_path(world.root, "demo", stage2).exists()
    assert not world.record().exists()


def test_timed_exclusion_prevents_even_the_probe(world: World, monkeypatch) -> None:
    """Criterion 17: timed exclusions cannot be probed before their deadline."""
    enable(
        world,
        exclude_until=[{"model_prefix": "mimo", "until": "2026-10-21T20:34:00+08:00", "reason": "temporary outage"}],
    )
    monkeypatch.setattr(availability, "now", lambda: dt.datetime(2026, 10, 17, tzinfo=dt.UTC))
    assert world.run("prepare-loop") == 0
    assert all("mimo" not in call["argv"][call["argv"].index("--model") + 1] for call in world.reviews())
    assert set(receipt(world)["state"]["availability"]["skipped"]) == {"mimo-v2.6-flash", "mimo-v2.6-pro"}


@pytest.mark.parametrize("released", [False, True])
def test_preparation_cannot_reset_a_started_or_released_run(world: World, released: bool) -> None:
    """Criterion 17: refreshing availability never resets consumed stages."""
    enable(world)
    world.write_record([("L1-1", "rejected — no evidence", "")])
    if released:
        world.write_findings(VERDICT)
        assert world.run("release-loop") == 0
    assert world.run("prepare-loop") == 2
    assert world.reviews() == []


def test_a_maintainer_restart_lets_a_released_run_be_prepared_again(world: World) -> None:
    """ADR 0021 restart amendment (bead coding-harness-0xjr): the restart is the one way back to preparation."""
    enable(world)
    world.write_record([("L1-1", "rejected — no evidence", "")])
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert world.run("prepare-loop") == 2
    assert world.run("release-loop", "demo", "--restart", "--reason", "maintainer asked") == 0
    world.script(pi=[{"stdout": "OK"}] * (len(TEST_FREE) + len(TEST_LADDER)))
    assert world.run("prepare-loop") == 0
    prepared = receipt(world)
    world.script(pi=[{"stdout": "No finding."}] * 2)
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 0
    assert "## Round 2 — " in world.record().read_text(), "the restarted run did not continue the numbering"


def test_paid_review_can_start_without_a_free_candidate(world: World) -> None:
    """Criterion 17: an empty free selection must not suppress reachable paid coverage."""
    enable(world)
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["free_stage"]["exclude"] = [
        {"id": model, "date": "2026-10-17", "reason": "synthetic exclusion"} for model in TEST_FREE
    ]
    path.write_text(yaml.safe_dump(data))
    assert world.run("prepare-loop") == 0
    prepared = receipt(world)
    assert prepared["state"]["free"]["selected"] == []
    assert prepared["state"]["paid"]["flash"] == list(TEST_LADDER)
    world.script(pi=[{"stdout": "No finding."}] * 3)
    assert world.run("review-loop", "demo", "--availability-reported", prepared["report_id"]) == 0
    assert stage2.read_state(world.record().read_text(), "")["consumed"] == ["flash"]


def test_deadline_expiry_permits_a_new_probe_instead_of_assuming_success(world: World, monkeypatch) -> None:
    """Criterion 17: at the exact cutoff excluded candidates are tested, not automatically trusted."""
    cutoff = "2026-10-21T20:34:00+08:00"
    enable(world, exclude_until=[{"model_prefix": "mimo", "until": cutoff, "reason": "outage"}])
    monkeypatch.setattr(availability, "now", lambda: dt.datetime.fromisoformat(cutoff))
    world.script(
        pi=[
            {"model": model, "stdout": "" if model.startswith("mimo") else "OK"} for model in [*TEST_FREE, *TEST_LADDER]
        ]
    )
    assert world.run("prepare-loop") == 0
    assert len(world.reviews()) == 5
    state = receipt(world)["state"]
    assert set(state["availability"]["failed"]) == {"mimo-v2.6-flash", "mimo-v2.6-pro"}
    assert state["paid"]["flash"] == ["deepseek-v4.1-flash"]


def test_repository_declaration_requires_preflight_and_keeps_go_glm_probed() -> None:
    """Criterion 17: removing production enablement defeats this rule; GLM through Go is not excluded.

    The maintainer narrowed the GLM outage to the Z.ai route on 2026-10-18; this
    OpenCode Go preparation must keep probing GLM models.
    """
    rule = availability.settings(REPO_ROOT, stage2)
    assert rule is not None and rule["flash_size"] == 3 and rule["max_age_seconds"] == 900
    assert not any(str(item["model_prefix"]).startswith("glm") for item in rule["exclude_until"])


def test_catalog_presence_does_not_admit_unread_or_unpriced_paid_models(world: World) -> None:
    """Criterion 17: a live catalog may not expand privacy or cost admission."""
    enable(world)
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["modelle_terms"]["mimo-v2.6-flash"].pop("anfragen_5h")
    entry["modelle_terms"]["mimo-v2.6-pro"]["training"] = "Used"
    path.write_text(yaml.safe_dump(data))
    catalog = "provider model context input output\n" + "\n".join(
        f"opencode-go {model} 128000 0 0" for model in [*TEST_FREE, *TEST_LADDER, "unknown-paid"]
    )
    world.script(pi_catalog=catalog, pi=[{"stdout": "OK"}] * 3)
    assert world.run("prepare-loop") == 0
    assert len(world.reviews()) == 3
    state = receipt(world)["state"]
    assert state["paid"]["flash"] == ["deepseek-v4.1-flash"]
    assert "unknown-paid" in state["availability"]["skipped"]
    assert "mimo-v2.6-flash" in state["availability"]["skipped"]
    assert any("mimo-v2.6-pro" in reason for reason in state["availability"]["terms_skipped"])


def test_preparation_warns_inside_the_window_and_never_probes_an_expired_model(
    world: World, monkeypatch, capsys
) -> None:
    """The terms date seam governs preparation (bead coding-harness-abra): a record inside the
    seven-day window warns with model and date, an expired one is filtered before its probe and
    named with its reason — receipt age and reachability stay independent of that seam."""
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 26))
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["modelle_terms"][TEST_LADDER[0]]["valid_until"] = "2026-10-28"
    entry["modelle_terms"][TEST_LADDER[1]]["valid_until"] = "2026-10-25"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    enable(world)
    world.script(pi=[{"stdout": "OK"}] * 5)
    assert world.run("prepare-loop") == 0
    state = receipt(world)["state"]
    assert state["availability"]["terms_warnings"] == [
        f"the data terms of {TEST_LADDER[0]} expire on 2026-10-28 (2 days left)"
    ]
    assert all(TEST_LADDER[1] not in model for model in state["paid"]["ladder"])
    assert any(
        TEST_LADDER[1] in reason and "expired on 2026-10-25" in reason
        for reason in state["availability"]["terms_skipped"]
    )
    probed = [call["argv"][call["argv"].index("--model") + 1] for call in world.reviews()]
    assert not any(TEST_LADDER[1] in model for model in probed), "an expired model was probed"
    out = capsys.readouterr().out
    assert "Terms warning:" in out and "Paid admission skipped:" in out


@pytest.mark.parametrize("invalid", [None, True, "900", 0, -1, 3601])
def test_invalid_freshness_rule_never_calls_a_model(world: World, invalid) -> None:
    """Criterion 17: an unusable freshness policy cannot silently enable legacy review."""
    enable(world, max_age_seconds=invalid)
    assert world.run("prepare-loop") == 2
    assert world.run("review-loop") == 2
    assert world.reviews() == []


def test_null_preflight_rule_never_silently_enables_legacy_review(world: World) -> None:
    """Criterion 17: a present but null rule is invalid, rather than an opt-out."""
    enable(world)
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["availability_preflight"] = None
    path.write_text(yaml.safe_dump(data))
    assert world.run("prepare-loop") == 2
    assert world.run("review-loop") == 2
    assert world.reviews() == []


def test_timed_family_exclusion_also_covers_namespaced_catalog_ids(world: World, monkeypatch) -> None:
    """Criterion 17: a provider namespace must not bypass the temporary GLM ban."""
    enable(world, exclude_until=[{"model_prefix": "glm", "until": "2026-10-21T20:34:00+08:00", "reason": "outage"}])
    monkeypatch.setattr(availability, "now", lambda: dt.datetime(2026, 10, 17, tzinfo=dt.UTC))
    catalog = "provider model context input output\n" + "\n".join(
        f"opencode-go {model} 128000 0 0" for model in [*TEST_FREE, *TEST_LADDER, "vendor/glm-free"]
    )
    world.script(pi_catalog=catalog, pi=[{"stdout": "OK"}] * 6)
    assert world.run("prepare-loop") == 0
    assert len(world.reviews()) == 5
    assert "vendor/glm-free" in receipt(world)["state"]["availability"]["skipped"]


def test_invalid_availability_rule_or_leak_stops_before_model_calls(world: World) -> None:
    """Criterion 17: malformed exclusions and leak BLOCK are never ordinary model failures."""
    enable(world, exclude_until=[{"model_prefix": "x", "until": "tomorrow", "reason": "outage"}])
    assert world.run("prepare-loop") == 2
    assert world.reviews() == []
    enable(world)
    (world.root / "scripts" / "helper.py").write_text("LEAKMARK-123456\n")
    assert world.run("prepare-loop") == 2
    assert world.reviews() == []


def test_review_preparation_uses_the_shared_rule_validation_and_probe(world: World, monkeypatch) -> None:
    """Criterion 50 (phase-6 F-27): a second validation or probe for the review swarm is two implementations."""
    enable(world)
    seen: list[str] = []
    for name in ("rule_problem", "excluded_reason", "probe_go", "seal"):
        original = getattr(availability, name)

        def spy(*args, _name=name, _original=original, **kwargs):
            seen.append(_name)
            return _original(*args, **kwargs)

        monkeypatch.setattr(availability, name, spy)
    assert world.run("prepare-loop") == 0
    assert {"rule_problem", "probe_go", "seal"} <= set(seen)
    assert seen.count("probe_go") == len(TEST_FREE) + len(TEST_LADDER)


def test_review_preparation_refuses_a_rule_the_shared_validator_rejects(world: World) -> None:
    """Criterion 50 (phase-6 F-27): an unknown rule key is refused by the one validator, with no model call."""
    enable(world)
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    entry["availability_preflight"]["measured_wire_apis"] = ["x"]
    path.write_text(yaml.safe_dump(data))
    assert world.run("prepare-loop") == 2
    assert world.reviews() == []


def test_a_probe_that_only_ran_out_of_time_gets_one_longer_try(world: World, monkeypatch) -> None:
    """R-7 of the review-swarm review: a slow but reachable model must not vanish from the run."""
    from test_stage2 import TEST_FREE

    enable(world)
    slow = TEST_FREE[0]
    limits: list[int] = []

    def fake(_runner, _root, _change, model, _key, _audit, _store, **options):
        if model == slow:
            limits.append(options["timeout_seconds"])
            if len(limits) == 1:
                raise stage2.CallFailed(
                    f"pi was stopped by the availability probe limit of {options['timeout_seconds']} seconds"
                )

    monkeypatch.setattr(availability, "probe_go", fake)
    assert world.run("prepare-loop") == 0
    assert limits == [availability.FREE_PROBE_SECONDS, availability.FREE_PROBE_RETRY_SECONDS], "no longer try was made"
    data = receipt(world)["state"]
    assert slow in data["free"]["selected"], "the slow model was dropped after one timeout"
    assert data["availability"]["slow"] == {slow: availability.FREE_PROBE_RETRY_SECONDS}
    assert slow not in data["availability"]["failed"]


def test_the_second_probe_is_checked_and_audited_on_its_own(world: World, monkeypatch) -> None:
    """The review of PR #196: a withdrawn admission stops the second probe, and it gets its own audit line."""
    from test_stage2 import TEST_FREE

    enable(world)
    slow = TEST_FREE[0]
    admissions: list[str | None] = []
    real_preflight = stage2.preflight
    calls = {"n": 0}

    def preflight(*args, **kwargs):
        problem = kwargs.get("admission_problem")
        admissions.append(problem(args[0], slow) if callable(problem) and args[2][1] == slow else None)
        return real_preflight(*args, **kwargs)

    def fake(_runner, _root, _change, model, _key, audit, _store, **_options):
        if model == slow:
            audit.append(
                f"prepare-loop · endpoint opencode-go · model {model} · "
                "leak check clean over 1 files, 1 commits, 1 rules."
            )
            calls["n"] += 1
            if calls["n"] == 1:
                raise stage2.CallFailed("pi was stopped by the availability probe limit of 60 seconds")

    monkeypatch.setattr(stage2, "preflight", preflight)
    monkeypatch.setattr(availability, "probe_go", fake)
    assert world.run("prepare-loop") == 0
    assert len([item for item in admissions if item is not None]) == 0
    lines = [line for line in world.text().splitlines() if "prepare-loop" in line and slow in line]
    assert len(lines) == 2, f"the second probe carries no audit line of its own: {lines}"


def test_a_probe_that_is_refused_is_not_tried_again(world: World, monkeypatch) -> None:
    """A refusal is final: only a stopped call earns the second, longer probe."""
    from test_stage2 import TEST_FREE

    enable(world)
    refused = TEST_FREE[0]
    calls: list[int] = []

    def fake(_runner, _root, _change, model, _key, _audit, _store, **options):
        if model == refused:
            calls.append(options["timeout_seconds"])
            raise stage2.CallFailed("pi exited 1: model_coming_soon")

    monkeypatch.setattr(availability, "probe_go", fake)
    assert world.run("prepare-loop") == 0
    assert calls == [availability.FREE_PROBE_SECONDS], "a refused probe was repeated"
    assert refused in receipt(world)["state"]["availability"]["failed"]


def test_receipts_of_two_worktrees_do_not_meet(world: World) -> None:
    """R-2 through the call sites: each worktree consumes its own receipt, whatever the other prepared later."""
    other = World(shutil.copytree(world.root, world.root.parent / "repo-b", symlinks=True), world.bin, world.state)
    enable(world)
    enable(other)
    assert world.run("prepare-loop") == 0
    mine = receipt(world)
    world.script(pi=[{"stdout": "OK"}] * 5)
    assert other.run("prepare-loop") == 0
    assert receipt(world) == mine, "preparing in one root overwrote the other root's receipt"
    assert world.record().parent != other.record().parent
    world.script(pi=[{"stdout": "No finding."}] * 2)
    assert world.run("review-loop", "demo", "--availability-reported", mine["report_id"]) == 0
    assert other.record().with_name("availability.json").exists(), "a review in one root consumed the other's receipt"
    assert not other.record().exists()
    world.script(pi=[{"stdout": "No finding."}] * 2)
    assert other.run("review-loop", "demo", "--availability-reported", receipt(other)["report_id"]) == 0


def test_a_free_model_is_probed_with_the_real_size_request_and_a_paid_one_is_not(world: World, monkeypatch) -> None:
    """Bead k9rw: a free model passed the tiny probe and failed every real request; it is probed at real size."""
    enable(world)
    checked: list[str] = []
    real_check = availability.leakcheck.check

    def spy(change, denylist, root, items, *args, **kwargs):
        checked.extend(text for _label, text in items)
        return real_check(change, denylist, root, items, *args, **kwargs)

    monkeypatch.setattr(availability.leakcheck, "check", spy)
    assert world.run("prepare-loop") == 0
    calls = world.reviews()
    free_calls = [c for c in calls if any(model in " ".join(c["argv"]) for model in TEST_FREE)]
    paid_calls = [c for c in calls if c not in free_calls]
    assert len(free_calls) == len(TEST_FREE) and len(paid_calls) == len(TEST_LADDER)
    for call in free_calls:
        prompt = call["prompt_file"]
        assert stage2.FREE_REVIEW_BODY in prompt and stage2.ANSWER_FORMAT in prompt
        assert "VALUE = 2" in prompt, "the bounded free diff is missing"
        assert "Availability probe only" in prompt
        assert prompt in checked, "the leak check did not see the exact prompt that was sent"
    for call in paid_calls:
        assert call["prompt_file"] == availability.PROBE_TEXT
        assert call["prompt_file"] in checked


def test_a_free_model_that_fails_the_real_size_probe_is_not_selected(world: World) -> None:
    """Bead k9rw: 'Endpoint is unavailable' on the real-size request makes the free model unavailable."""
    enable(world)
    world.script(
        pi=[
            {
                "model": model,
                **({"exit": 1, "stderr": "429 Endpoint is unavailable"} if model == TEST_FREE[0] else {"stdout": "OK"}),
            }
            for model in [*TEST_FREE, *TEST_LADDER]
        ]
    )
    assert world.run("prepare-loop") == 0
    state = receipt(world)["state"]
    assert TEST_FREE[0] not in state["free"]["selected"]
    assert TEST_FREE[1] in state["free"]["selected"]
    assert "Endpoint is unavailable" in state["availability"]["failed"][TEST_FREE[0]]
