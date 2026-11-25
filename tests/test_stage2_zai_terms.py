"""The Z.ai subscription expires: the `valid_until` boundary of the `glm-coding-plan` endpoint (bead coding-harness-dcu3).

Explore and implement run over Z.ai (`GLM_FLASH`), and the draft falls back to
`GLM`. Until this change only `opencode-go` carried a terms expiry, so a Z.ai
call ran on whatever the subscription said, or no longer said. The endpoint
now declares a `modelle_terms` record per model; the runner warns within seven
UTC days of its end and refuses every call after it, through the same choke
point (`stage2.declaration_problem`) every Z.ai route already passes.

The record states a subscription end, not a retention or training reading: the
expiry part of the terms rule binds, the Go-only retention and training fields
do not. Each test controls only the terms UTC-date seam, `stage2.terms_today`.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
from test_stage2 import (  # noqa: E402
    OTHER_RED,
    PLAN_CARD,
    REPO_ROOT,
    LocalCommands,
    World,
    codex_ok,
    draft_world,
    gate_red_then_green,
    git,
    red_verify,
    successful_implementation,
)
from test_stage2 import world as stage2_world  # noqa: E402

world = stage2_world

ZAI = "glm-coding-plan"


def zai_record(**overrides: object) -> dict:
    """A subscription-terms record: dated, sourced, with an end date; no retention or training reading."""
    record = {
        "gelesen": "2026-11-15",
        "valid_until": "2026-12-08",
        "quelle": "maintainer's statement in the conversation, 2026-11-15: 2026-12-08 is the last day",
    }
    record.update(overrides)
    return record


def declaration(root: Path, terms: dict | None) -> Path:
    """A declaration with one Z.ai entry carrying `terms` as its `modelle_terms` (omitted when None)."""
    entry = {
        "name": ZAI,
        "betreiber": "Zhipu AI (Z.ai)",
        "residenz": "anbieter-erklaert",
        "abrechnung": "abonnement",
        "darf_sehen": ["framework"],
        "modelle": ["glm-5.4", "glm-5.3-flash"],
    }
    if terms is not None:
        entry["modelle_terms"] = terms
    root.mkdir(parents=True, exist_ok=True)
    (root / "model-endpoints.yaml").write_text(yaml.safe_dump({"endpunkte": [entry]}), encoding="utf-8")
    return root


def on(monkeypatch: pytest.MonkeyPatch, day: str) -> None:
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date.fromisoformat(day))


def set_zai_terms(w: World, model: str, **changes: object) -> None:
    """Rewrite one Z.ai model's terms record in the world's declaration."""
    path = w.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = next(item for item in data["endpunkte"] if item["name"] == ZAI)
    entry.setdefault("modelle_terms", {}).setdefault(model, zai_record()).update(changes)
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


# ---------------------------------------------------------------------------
# The refusal at the one declaration choke point
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("model", ["glm-5.3-flash", "glm-5.4"])
def test_zai_terms_are_valid_through_their_last_utc_day(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, model: str
) -> None:
    """Explore/implement (Flash) and the draft fallback (glm-5.4) are admitted through 2026-12-08, refused after."""
    root = declaration(tmp_path, {m: zai_record() for m in ("glm-5.4", "glm-5.3-flash")})
    on(monkeypatch, "2026-12-08")
    assert stage2.declaration_problem(root, ZAI, model) is None
    on(monkeypatch, "2026-12-09")
    problem = stage2.declaration_problem(root, ZAI, model)
    assert problem == f"the Z.ai subscription for {model} expired on 2026-12-08; no further call runs on it"


def test_zai_record_needs_no_retention_or_training_reading(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The subscription record binds by its end date; the Go page's retention and training fields are not asked for."""
    root = declaration(tmp_path, {m: zai_record() for m in ("glm-5.4", "glm-5.3-flash")})
    on(monkeypatch, "2026-11-15")
    assert stage2.declaration_problem(root, ZAI, "glm-5.3-flash") is None


@pytest.mark.parametrize(
    ("change", "fragment"),
    [
        ({"valid_until": None}, "valid_until is missing"),
        ({"valid_until": "soon"}, "not a quoted ISO date"),
        ({"gelesen": None}, "no dated reading"),
        ({"quelle": ""}, "gelesen/quelle missing"),
    ],
)
def test_an_unusable_zai_record_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, change: dict, fragment: str
) -> None:
    root = declaration(tmp_path, {"glm-5.4": zai_record(), "glm-5.3-flash": zai_record(**change)})
    on(monkeypatch, "2026-11-15")
    problem = stage2.declaration_problem(root, ZAI, "glm-5.3-flash")
    assert problem is not None and fragment in problem


def test_a_zai_model_without_its_record_refuses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Once the endpoint declares terms, a listed model with no record is not admitted on silence."""
    root = declaration(tmp_path, {"glm-5.4": zai_record()})
    on(monkeypatch, "2026-11-15")
    assert stage2.declaration_problem(root, ZAI, "glm-5.4") is None
    problem = stage2.declaration_problem(root, ZAI, "glm-5.3-flash")
    assert problem is not None and "glm-5.3-flash" in problem


def test_zai_without_a_terms_block_refuses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Deleting the block must not reopen the gap: the Z.ai endpoint requires its terms."""
    root = declaration(tmp_path, None)
    on(monkeypatch, "2026-11-15")
    assert stage2.declaration_problem(root, ZAI, "glm-5.3-flash") is not None


# ---------------------------------------------------------------------------
# The runner's verbs: notice before, refusal after, no call started
# ---------------------------------------------------------------------------


def test_explore_over_zai_warns_within_seven_days(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    set_zai_terms(world, "glm-5.3-flash", valid_until="2026-12-08")
    on(monkeypatch, "2026-12-05")
    world.script(claude=[{"stdout": "Fact from `src/app.py` and its symbol `value`."}])
    assert world.run("explore") == 0
    out = capsys.readouterr().out
    assert "Terms warning: the Z.ai subscription for glm-5.3-flash ends on 2026-12-08 (3 days left)" in out
    assert "data terms" not in out
    assert len(world.calls("claude")) == 1


def test_explore_over_zai_prints_no_warning_outside_the_window(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    set_zai_terms(world, "glm-5.3-flash", valid_until="2026-12-08")
    on(monkeypatch, "2026-11-15")
    world.script(claude=[{"stdout": "Fact from `src/app.py` and its symbol `value`."}])
    assert world.run("explore") == 0
    assert "Terms warning" not in capsys.readouterr().out


@pytest.mark.parametrize("verb", ["explore", "implement"])
def test_expired_zai_terms_refuse_explore_and_implement_before_any_call(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], verb: str
) -> None:
    set_zai_terms(world, "glm-5.3-flash", valid_until="2026-12-08")
    on(monkeypatch, "2026-12-09")
    if verb == "implement":
        successful_implementation(world)
    else:
        world.script(claude=[{"stdout": "Fact from `src/app.py` and its symbol `value`."}])
    assert world.run(verb) != 0
    captured = capsys.readouterr()
    assert "the Z.ai subscription for glm-5.3-flash expired on 2026-12-08" in captured.out + captured.err
    assert world.calls("claude") == [], "a Z.ai call started on expired subscription terms"


def test_implement_over_zai_warns_within_seven_days(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Phase 6, F6-1: the notice reaches the implement route too, and the call still runs."""
    set_zai_terms(world, "glm-5.3-flash", valid_until="2026-12-08")
    git(world.root, "commit", "--quiet", "-am", "the subscription's end")  # implement refuses a dirty tree
    on(monkeypatch, "2026-12-05")
    successful_implementation(world)
    assert world.run("implement") == 0
    assert "Terms warning: the Z.ai subscription for glm-5.3-flash ends on 2026-12-08 (3 days left)" in (
        capsys.readouterr().out
    )
    assert world.calls("claude"), "the implement call did not run inside the warning window"


def test_expired_zai_terms_refuse_the_draft_fallback_before_its_call(
    world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Phase 6, F6-1: `draft` preflights Codex only; the glm-5.4 attempt is refused at its own call check."""
    draft_world(world)
    set_zai_terms(world, "glm-5.4", valid_until="2026-12-08")
    git(world.root, "commit", "--quiet", "-am", "the subscription's end")  # a draft refuses a dirty tree
    on(monkeypatch, "2026-12-09")
    red = red_verify(OTHER_RED)["stdout"]
    world.script(
        codex=[codex_ok("T1", "drafted", plant={"plans/changes/demo/plan.md": PLAN_CARD}), codex_ok("T2", "again")],
        claude=[{"stdout": "must not run"}],
    )
    gate_red_then_green(LocalCommands(monkeypatch), red, reds=2)
    assert world.run("draft") != 0
    assert len(world.calls("codex")) == 2, "the refusal must come at the GLM attempt, after both Codex attempts"
    assert world.calls("claude") == [], "a Z.ai draft call started on an expired subscription"
    captured = capsys.readouterr()
    assert "the Z.ai subscription for glm-5.4 expired on 2026-12-08" in captured.out + captured.err


# ---------------------------------------------------------------------------
# The real declaration
# ---------------------------------------------------------------------------


def test_the_real_zai_entry_declares_its_subscription_end() -> None:
    """Every Z.ai model carries a dated, sourced record with a quoted end date (maintainer, 2026-11-15)."""
    data = yaml.safe_load((REPO_ROOT / "model-endpoints.yaml").read_text(encoding="utf-8"))
    entry = next(item for item in data["endpunkte"] if item["name"] == ZAI)
    terms = entry.get("modelle_terms") or {}
    assert set(entry["modelle"]) <= set(terms), "a Z.ai model has no terms record"
    for model in entry["modelle"]:
        record = terms[model]
        assert isinstance(record.get("gelesen"), str) and dt.date.fromisoformat(record["gelesen"])
        assert isinstance(record.get("valid_until"), str) and dt.date.fromisoformat(record["valid_until"])
        assert record.get("quelle"), f"{model} names no source"
