"""The shared free selection: one rule for the review loop and the research swarm (bead coding-harness-wb40).

Local stand-ins only: no network, no real Pi, no model call. The review adapter, the research adapter and the
call boundaries are driven together, so a rule that lives in only one of them shows up as a disagreement.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
import stage2_free  # noqa: E402
import stage2_go  # noqa: E402
import stage2_swarm as swarm  # noqa: E402
from test_stage2 import World  # noqa: E402
from test_stage2 import world as stage2_world  # noqa: E402
from test_stage2_availability import enable  # noqa: E402
from test_stage2_research_availability import Catalog, Fixture, pi_model  # noqa: E402

world = stage2_world

GO = "opencode-go"
RECORDED_BASE = "https://opencode.ai/zen/go/v1"
MOVED_BASE = "https://opencode.ai/inference/go/v1"
ADDRESS = stage2_go.AddressPolicy(
    host="opencode.ai",
    apis={
        "openai-completions": stage2_go.BaseRecord(
            api="openai-completions", base=RECORDED_BASE, source="the synthetic record", read="2026-10-31"
        )
    },
)


def review_rule(**more) -> dict:
    return {
        "provider": GO,
        "id_suffix": "-free",
        "include": [],
        "exclude": [],
        "input": "implementation-diff",
        **more,
    }


def declare_paid(w: World, *models: str) -> None:
    path = w.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = next(item for item in data["endpunkte"] if item["name"] == GO)
    entry["modelle"] = [*entry["modelle"], *models]
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def definition(ident: str, base: str = RECORDED_BASE) -> dict:
    return {"id": ident, "provider": GO, "api": "openai-completions", "baseUrl": base}


def research_catalog(*extra: dict) -> Catalog:
    """The synthetic catalog of the research tests plus the given Pi rows, each with tool support."""
    catalog = Catalog()
    for row in extra:
        catalog.pi.append(row)
        catalog.tools[row["id"]] = {"id": row["id"], "tool_call": True}
    return catalog


def research_select(catalog: Catalog, policy: dict | None = None, **more) -> dict:
    return swarm.select_research_catalog(
        catalog.bridge(),
        policy or {"provider": GO, "suffix": "-free", "include": [], "exclude": []},
        [],
        expected_version=stage2.PI_VERSION,
        address=ADDRESS,
        **more,
    )


@pytest.mark.parametrize("path", ["review", "research"])
def test_both_preparations_use_shared_selection(world: World, monkeypatch: pytest.MonkeyPatch, path: str) -> None:
    # Planted fault: a preparation keeps its own copy of the membership rule and never calls the shared one.
    seen: list[stage2_free.Policy] = []
    real = stage2_free.select

    def spy(candidates, policy, **kwargs):
        seen.append(policy)
        return real(candidates, policy, **kwargs)

    monkeypatch.setattr(stage2_free, "select", spy)
    if path == "review":
        enable(world)
        assert world.run("prepare-loop") == 0
        assert {policy.include_adds for policy in seen} == {True}, "review bypassed the shared selection"
    else:
        fixture = Fixture(world, monkeypatch)
        assert fixture.prepare() == 0
        assert {policy.include_adds for policy in seen} == {False}, "research bypassed the shared selection"
    assert {policy.provider for policy in seen} == {GO}


def test_preparations_select_same_members_for_equivalent_inputs(world: World) -> None:
    # Planted fault: an otherwise eligible id is selected by one preparation only, such as a paid `-free` id.
    declare_paid(world, "beam-free")
    ids = ["alpha-free", "beam-free", "beta-free", "gamma-free", "step-free", "zeta-free"]
    excluded = [{"id": "step-free", "date": "2026-11-05", "reason": "the same policy for both"}]
    rows = [{"provider": GO, "model": ident} for ident in ids]
    review = stage2.free_selection(
        world.root,
        review_rule(exclude=excluded),
        rows,
        set(ids),
        {ident: definition(ident) for ident in ids},
        ADDRESS,
    )
    added = ("beam-free", "gamma-free", "step-free", "zeta-free")
    catalog = research_catalog(*(pi_model(ident) for ident in added))
    research = research_select(
        catalog,
        {"provider": GO, "suffix": "-free", "include": [], "exclude": ["step-free"]},
        paid=["beam-free"],
    )
    members = {"alpha-free", "beta-free", "gamma-free", "zeta-free"}
    assert set(review.selected) == set(research["selected"]) == members
    assert "beam-free" in review.dropped and "beam-free" not in research["selected"]
    # Order stays each caller's own: catalog order for review, sorted for research.
    assert research["selected"] == sorted(research["selected"])
    assert review.selected == [ident for ident in ids if ident in review.selected]


def test_policy_adapters_preserve_membership_contracts() -> None:
    # Planted fault: provider, freshness, plain ids, include or exclude meaning, vetoes widen or shrink.
    rule = review_rule(
        include=[{"id": "extra-model", "date": "2026-11-05", "reason": "added"}],
        exclude=[{"id": "old-free", "date": "2026-11-05", "reason": "gone"}],
    )
    policy = stage2.free_policy(rule)
    assert policy == stage2_free.Policy(
        provider=GO, suffix="-free", include=("extra-model",), exclude=("old-free",), include_adds=True
    )

    def candidate(ident: str, provider: str = GO) -> stage2_free.Candidate:
        return stage2_free.Candidate(provider, ident)

    names = [
        "alpha-free",
        "old-free",
        "extra-model",
        "plain-model",
        "stale-free",
        "bad|id-free",
        "paid-free",
        "no-free",
    ]
    candidates = [candidate(ident) for ident in names] + [candidate("zen-free", "opencode")]
    fresh = {*names, "zen-free"} - {"stale-free"}

    def deny(ident: str) -> str | None:
        return "excluded by the declaration" if ident == "no-free" else None

    result = stage2_free.select(candidates, policy, fresh=fresh, paid=["paid-free"], exclusion=deny)
    assert result.selected == ["alpha-free", "extra-model"], "an include adds to the suffix; nothing else joins"
    assert result.dropped == {
        "bad|id-free": "not a plain model id",
        "paid-free": stage2_free.PAID_REASON,
        "no-free": "excluded by the declaration",
    }
    assert result.skipped == {"old-free": "excluded", "stale-free": "not-fresh"}
    assert "zen-free" not in {*result.selected, *result.dropped, *result.skipped}, "another provider was considered"

    # A hard veto beats an include, in review's additive meaning.
    additive = stage2_free.Policy(provider=GO, suffix="-free", include=("paid-free", "no-free"), include_adds=True)
    vetoed = stage2_free.select(candidates, additive, fresh=fresh, paid=["paid-free"], exclusion=deny)
    assert "paid-free" not in vetoed.selected and "no-free" not in vetoed.selected

    # Research's meaning: an include restricts, never adds, and an ineligible explicit include still refuses.
    restrictive = stage2_free.Policy(provider=GO, suffix="-free", include=("alpha-free",), include_adds=False)
    narrowed = stage2_free.select(candidates, restrictive, fresh=fresh, paid=["paid-free"], exclusion=deny)
    assert narrowed.selected == ["alpha-free"] and narrowed.skipped["old-free"] == "not-included"
    catalog = research_catalog(pi_model("paid-free"))
    with pytest.raises(swarm.ResearchCatalogError, match="explicit free include is ineligible: paid-free"):
        research_select(
            catalog, {"provider": GO, "suffix": "-free", "include": ["paid-free"], "exclude": []}, paid=["paid-free"]
        )
    chosen = research_select(
        catalog, {"provider": GO, "suffix": "-free", "include": ["beta-free"], "exclude": []}, paid=["paid-free"]
    )
    assert chosen["selected"] == ["beta-free"], "the research include stopped restricting"


def test_both_preparations_share_destination_assessment(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    # Planted fault: a foreign destination survives, a same-host move runs silent, or a caller keeps its own rule.
    assessed: list[str] = []
    real = stage2_go.assess

    def spy(policy, model, definition_):
        assessed.append(model)
        return real(policy, model, definition_)

    monkeypatch.setattr(stage2_go, "assess", spy)
    ids = ["alpha-free", "foreign-free", "moved-free"]
    bases = {"alpha-free": RECORDED_BASE, "foreign-free": "https://evil.example/zen/go/v1", "moved-free": MOVED_BASE}
    review = stage2.free_selection(
        world.root,
        review_rule(),
        [{"provider": GO, "model": ident} for ident in ids],
        set(ids),
        {ident: definition(ident, bases[ident]) for ident in ids},
        ADDRESS,
    )
    assert review.selected == ["alpha-free", "moved-free"]
    assert "refused" in review.dropped["foreign-free"]
    assert any("/inference/go/v1" in notice and "moved-free" in notice for notice in review.notices)
    assert {"alpha-free", "moved-free"} <= set(assessed), "the review selection assessed no destination itself"
    assessed.clear()
    catalog = research_catalog(
        pi_model("foreign-free", baseUrl=bases["foreign-free"]), pi_model("moved-free", baseUrl=MOVED_BASE)
    )
    research = research_select(catalog)
    assert "foreign-free" not in research["selected"] and "moved-free" in research["selected"]
    assert any("/inference/go/v1" in notice and "moved-free" in notice for notice in research["address_notices"])
    assert "moved-free" in assessed, "the research selection assessed no destination itself"


def test_free_call_boundaries_reject_paid_ids_in_frozen_selection(world: World) -> None:
    # Planted fault: a forged or older selection holding an id now admitted as paid authorizes a free call.
    declare_paid(world, "beam-free")
    problem = stage2.free_admission_problem(world.root, "beam-free", ["beam-free"])
    assert problem and "paid model" in problem, "the review boundary trusted a frozen paid id"
    assert stage2.free_admission_problem(world.root, "acme-v1-free", ["acme-v1-free"]) is None
    data = yaml.safe_load((world.root / "model-endpoints.yaml").read_text(encoding="utf-8"))
    problem = swarm.invocation_problem(data, "online_free", GO, "beam-free", selected_free=["beam-free"])
    assert problem and "paid model" in problem, "the research boundary trusted a frozen paid id"
    assert swarm.invocation_problem(data, "online_free", GO, "alpha-free", selected_free=["alpha-free"]) is None
