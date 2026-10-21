"""Synthetic endpoint failures exercise preparation and the report boundary."""

from __future__ import annotations

import datetime as dt
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
        assert "VALUE = 2" not in call["prompt_file"]
        assert call["argv"][-1] == "Follow the appended availability instructions."
    assert limits == [60] * len(calls)
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
