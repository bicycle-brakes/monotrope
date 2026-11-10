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
        measured_wire_apis=("openai-completions",),
        address=ADDRESS,
        **({"paid": (), "exclusion": None} | more),
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


@pytest.mark.parametrize("path", ["review", "research"])
def test_paid_admission_reason_wins_over_declaration_exclusion(world, monkeypatch, capsys, path):
    """A simultaneous declaration exclusion must not hide a paid/free collision."""
    if path == "research":
        from test_stage2_research_availability import declare_paid_free

        fixture = Fixture(world, monkeypatch)
        declare_paid_free(fixture)
        fixture.edit_declaration(
            lambda data: data.update(ausgeschlossen=[{"klasse": "public-web", "modelle": ["beam-free"]}])
        )
        assert fixture.prepare() == 0
        assert fixture.receipt()["state"]["free"]["dropped"].get("beam-free") == stage2_free.PAID_REASON
    else:
        enable(world)
        declare_paid(world, "beam-free")
        declaration = world.root / "model-endpoints.yaml"
        data = yaml.safe_load(declaration.read_text())
        data["ausgeschlossen"] = [{"klasse": "framework", "modelle": ["beam-free"]}]
        declaration.write_text(yaml.safe_dump(data))
        world.script(
            pi_catalog="provider model context input output\nopencode-go beam-free 128000 0 0\n"
            "opencode-go acme-v1-free 128000 0 0\n",
            pi=[{"stdout": "OK"}] * 5,
        )
        assert world.run("prepare-loop") == 0
    assert f"beam-free: {stage2_free.PAID_REASON}" in capsys.readouterr().out


def test_research_destination_refusal_keeps_shared_assessment_reason(world, monkeypatch, capsys):
    fixture = Fixture(world, monkeypatch)
    fixture.catalog.pi.append(pi_model("foreign-free", baseUrl="https://evil.example/x"))
    fixture.catalog.tools["foreign-free"] = {"id": "foreign-free", "tool_call": True}
    assessed = []
    real = stage2_go.assess

    def spy(policy, model, definition_):
        verdict = real(policy, model, definition_)
        if model == "foreign-free":
            assessed.append(verdict.problem)
        return verdict

    monkeypatch.setattr(stage2_go, "assess", spy)
    assert fixture.prepare() == 0
    state = fixture.receipt()["state"]
    candidate = next(c for c in state["catalog"]["candidates"] if c["id"] == "foreign-free")
    assert candidate["reason"] == "destination-refused", "destination permission bypassed the shared assessment"
    assert assessed and candidate["detail"] == assessed[0]
    assert state["free"]["dropped"]["foreign-free"] == assessed[0]
    assert f"Dropped (free): foreign-free: {assessed[0]}" in capsys.readouterr().out
    assert "foreign-free" not in fixture.probed()
    assert {"alpha-free", "beta-free"} <= set(state["free"]["selected"])


@pytest.mark.parametrize("selector", ["shared", "research"])
@pytest.mark.parametrize("omitted", ["paid", "exclusion"])
def test_selectors_require_admission_inputs(selector, omitted):
    admission = {"paid": (), "exclusion": None}
    del admission[omitted]
    with pytest.raises(TypeError, match=omitted):
        if selector == "shared":
            stage2_free.select([], stage2_free.Policy(GO), fresh=set(), **admission)
        else:
            swarm.select_research_catalog(
                research_catalog().bridge(),
                {"provider": GO, "suffix": "-free", "include": [], "exclude": []},
                [],
                expected_version=stage2.PI_VERSION,
                address=ADDRESS,
                **admission,
            )


@pytest.mark.parametrize("veto", ["paid", "excluded"])
def test_explicit_research_include_refuses_hard_veto(world, monkeypatch, capsys, veto):
    fixture = Fixture(world, monkeypatch)

    def declare(data):
        data["research_swarm"]["online_free"]["include"] = ["alpha-free"]
        if veto == "paid":
            entry = next(item for item in data["endpunkte"] if item["name"] == GO)
            entry["modelle"].append("alpha-free")
        else:
            data["ausgeschlossen"] = [{"klasse": "public-web", "modelle": ["alpha-free"]}]

    fixture.edit_declaration(declare)
    assert fixture.prepare() == 2, "an explicit hard-vetoed include must refuse the declaration"
    diagnostic = capsys.readouterr().err
    assert "explicit free include is ineligible: alpha-free" in diagnostic
    assert ("paid model" if veto == "paid" else "excluded") in diagnostic
    assert "Go catalog is unmeasured" not in diagnostic
    assert "alpha-free" not in fixture.probed()


def test_select_free_preserves_declaration_vetoes(world, monkeypatch):
    declare_paid(world, "paid-free")
    path = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text())
    data["ausgeschlossen"] = [{"klasse": "framework", "modelle": ["excluded-free"]}]
    path.write_text(yaml.safe_dump(data))
    monkeypatch.chdir(world.root)
    ids = ["paid-free", "excluded-free", "alpha-free"]
    catalog = [{"provider": GO, "model": ident} for ident in ids]
    assert stage2.select_free(review_rule(), catalog, root=world.root) == ["alpha-free"], (
        "the compatibility wrapper admitted a paid or declaration-excluded id"
    )


def test_recorded_maintainer_adr_answer_is_reflected_in_change_contract():
    """The current contract acknowledges the recorded answer and its maintainer provenance."""
    root = Path(__file__).resolve().parents[1]
    answer_path = root / "decisions/answers/research-free-paid/adr.yaml"
    answer = yaml.safe_load(answer_path.read_text())
    assert answer["answer"] == "no" and answer["answered_at"].isoformat() == "2026-11-06"
    obsolete = {
        "spec.md": "no maintainer answer is claimed or written here",
        "plan.md": "do not write an ADR answer",
        "design.md": "No maintainer ADR answer has been recorded by this draft",
    }
    for name, denial in obsolete.items():
        text = (root / "plans/changes/research-free-paid" / name).read_text()
        assert denial not in text, f"{name} denies the existing maintainer answer"
        assert 'The maintainer answered "no"' in text, f"{name} omits the maintainer's answer"
        assert "2026-11-06" in text and "Q-M2" in text and "0baba58f" in text
        assert "decisions/answers/research-free-paid/adr.yaml" in text


def test_select_free_requires_repository_root_from_another_directory(world, monkeypatch, tmp_path):
    declare_paid(world, "paid-free")
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    declaration = yaml.safe_load((world.root / "model-endpoints.yaml").read_text())
    entry = next(item for item in declaration["endpunkte"] if item["name"] == GO)
    entry["modelle"] = []
    (foreign / "model-endpoints.yaml").write_text(yaml.safe_dump(declaration))
    monkeypatch.chdir(foreign)
    catalog = [{"provider": GO, "model": ident} for ident in ["paid-free", "alpha-free"]]
    assert stage2.select_free(review_rule(), catalog, root=world.root) == ["alpha-free"], (
        "selection must apply the named repository's paid veto from a foreign directory"
    )
    with pytest.raises(TypeError, match="root"):
        stage2.select_free(review_rule(), catalog)


@pytest.mark.parametrize("capability_problem", ["no-tool-support", "capability-unavailable"])
def test_research_reports_destination_and_capability_refusals(world, monkeypatch, capsys, capability_problem):
    fixture = Fixture(world, monkeypatch)
    fixture.catalog.pi.append(pi_model("foreign-free", baseUrl="https://evil.example/x"))
    fixture.catalog.tools["foreign-free"] = {"id": "foreign-free", "tool_call": False}
    fixture.catalog.metadata_ok = capability_problem != "capability-unavailable"
    for item in fixture.catalog.pi:
        if item["id"] == "qwen3.8-flash":
            item["api"] = "openai-completions"
    assessed = []
    real = stage2_go.assess

    def spy(policy, model, definition_):
        verdict = real(policy, model, definition_)
        if model == "foreign-free":
            assessed.append(verdict.problem)
        return verdict

    monkeypatch.setattr(stage2_go, "assess", spy)
    assert fixture.prepare() == 0
    state = fixture.receipt()["state"]
    candidate = next(c for c in state["catalog"]["candidates"] if c["id"] == "foreign-free")
    assert assessed, "a capability refusal must not suppress destination assessment"
    assert candidate["reason"] == "destination-refused"
    assert capability_problem in candidate["detail"] and assessed[0] in candidate["detail"]
    assert state["free"]["dropped"]["foreign-free"] == candidate["detail"]
    assert f"Dropped (free): foreign-free: {candidate['detail']}" in capsys.readouterr().out
    assert "foreign-free" not in fixture.probed()
    if capability_problem == "no-tool-support":
        assert {"alpha-free", "beta-free"} <= set(state["free"]["selected"])
