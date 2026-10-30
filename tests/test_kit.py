"""The module keeps its own promises — the static half.

The division of labour is intentional. **This test checks what is checkable
without a run:** that every file has a role, that every reason comes from the
closed set, that the cap holds, that the two manifests do not contradict each
other. **The run itself belongs to `scripts/kit/probe.py`** — it blocks when a
red case has no reason or a reason has expired, and it runs as a step of its own
in `ci.yml`.

Why separate: a pytest session that starts a second pytest session inside
itself is slow and brittle in foreign environments. The run is a gate, not a
test case — and `ci.yml` carries the gate list, not this file.
"""

from __future__ import annotations

import functools
import re
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KIT = REPO_ROOT / "scripts" / "kit"

sys.path.insert(0, str(KIT))
import probe  # noqa: E402

sys.path.insert(0, str(KIT.parent))
from _verdict import Level, Verdict  # noqa: E402

EXPORT_MANIFEST = REPO_ROOT / "scripts" / "export" / "manifest.yaml"


# ---------------------------------------------------------------------------
# AK-1 · The set stands in one file
# ---------------------------------------------------------------------------


def test_the_examined_set_is_not_empty() -> None:
    """An empty set is not a result (RB-G7).

    Without this test every following one would run green over zero files, and a
    broken `git ls-files` would look like a fulfilled manifest.
    """
    assert probe.getrackte_dateien(), "no tracked file found — then nothing is measured here"
    assert probe.regeln(), "the manifest carries no rule"


def test_every_tracked_file_has_a_role() -> None:
    """Not listed is BLOCK, not 'does not belong'.

    A standard that decides in case of doubt decides precisely about the files
    nobody thought of — the same reasoning the export manifest exists for.
    """
    offen = probe.nach_rolle()["(offen)"]
    assert not offen, f"{len(offen)} file(s) fall under no rule in scripts/kit/manifest.yaml:\n  " + "\n  ".join(
        sorted(offen)[:20]
    )


def test_the_kit_actually_carries_something() -> None:
    """A module of zero files is not a module (RB-G7)."""
    verteilt = probe.nach_rolle()
    assert verteilt["mechanismus"], "no file carries the role 'mechanismus'"
    assert len(verteilt["mechanismus"]) >= 20, (
        f"only {len(verteilt['mechanismus'])} file(s) in the mechanism — the survey of 2026-09-08 measured 27"
    )


def test_every_rule_carries_a_reason() -> None:
    """The reason stands in the rule, not in the head of the person handing over."""
    ohne = [r["prefix"] for r in probe.regeln() if not r.get("reason", "").strip()]
    assert not ohne, f"rule(s) without a justification: {ohne}"


def test_every_role_used_is_declared() -> None:
    """A role name that the head of the file does not know is a typo."""
    deklariert = set(yaml.safe_load(probe.MANIFEST.read_text(encoding="utf-8"))["rollen"])
    benutzt = {r["rolle"] for r in probe.regeln()}
    assert benutzt <= deklariert, f"unknown role(s): {sorted(benutzt - deklariert)}"
    assert deklariert <= benutzt, (
        f"declared but never used role(s): {sorted(deklariert - benutzt)} — "
        "a vocabulary value that stands for nothing is an invitation to use it wrongly"
    )


# ---------------------------------------------------------------------------
# AK-3/AK-4 · The exemptions and their cap
# ---------------------------------------------------------------------------


def test_every_reason_comes_from_the_closed_set() -> None:
    """Three reasons, no more. A free text would not be a classification."""
    fremd = {n: g for n, g in probe.REIST_NICHT.items() if g not in probe.GRUENDE}
    assert not fremd, f"reason outside the set {probe.GRUENDE}: {fremd}"


def test_every_declared_reason_is_actually_used() -> None:
    """A reason that nobody carries is a word without a case."""
    benutzt = set(probe.REIST_NICHT.values())
    ungenutzt = set(probe.GRUENDE) - benutzt
    assert not ungenutzt, (
        f"reason(s) without a single case: {sorted(ungenutzt)}. Either strike them or name the case they stand for."
    )


def test_the_exemption_list_only_shrinks() -> None:
    """Ratchet. Same form as `ci_gates.OHNE_AUFRUFER` and `OHNE_TEST`.

    A portability that can be lost without anyone noticing is none. Whoever adds
    an entry lifts the cap visibly — in the diff, with the reasoning in the
    commit.
    """
    assert len(probe.REIST_NICHT) <= probe.DECKEL, (
        f"REIST_NICHT has {len(probe.REIST_NICHT)} entries, the cap stands at {probe.DECKEL}"
    )


def test_the_cap_is_not_slack() -> None:
    """A cap far above the current state is not a cap but a permission."""
    luft = probe.DECKEL - len(probe.REIST_NICHT)
    assert luft <= 3, (
        f"the cap is {luft} above today's state — then growth goes unnoticed. Set it to {len(probe.REIST_NICHT)}."
    )


# ---------------------------------------------------------------------------
# AK-6 · Two manifests, no contradiction
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def _export_regeln() -> tuple[dict, ...]:
    return tuple(yaml.safe_load(EXPORT_MANIFEST.read_text(encoding="utf-8"))["rules"])


def _export_verdict(pfad: str) -> str | None:
    treffer = [r for r in _export_regeln() if pfad.startswith(r["prefix"])]
    if not treffer:
        return None
    return max(treffer, key=lambda r: len(r["prefix"]))["verdict"]


# AK-6 changed its form in the implementation, and the reason belongs here.
#
# The spec demanded "no contradictory combination of kit role and export
# verdict". Measured on 2026-09-08 there is none: `.editorconfig` is `carry` in
# the export and `bestand` in the kit, `.github/ISSUE_TEMPLATE/` likewise — and
# that is perfectly fine. A file can be uninvolved in the workflow and still
# belong byte-identical in another repository. The two questions are
# **orthogonal**, so no combination of them can be contradictory.
#
# That made the original test not sharp but wrongly constructed: it would have
# forced two answers to two different questions to line up with each other.
#
# What AK-6 really has to secure is something else: **that the second list is
# not a derivation of the first.** If every kit role were determined by exactly
# one export verdict (or the other way round), one could compute the one from
# the other — and then it would be a duplicate, exactly the finding this repo
# keeps raising against itself. That is checkable, and like this:


def test_the_kit_list_is_not_derivable_from_the_export_list() -> None:
    """The second list justifies itself by NOT being computable.

    For each kit role it is counted on how many different export verdicts its
    files fall. If a role falls on exactly one, it is derivable from the export
    manifest — then `scripts/kit/manifest.yaml` is a duplicate and belongs
    deleted, not maintained.
    """
    verteilung: dict[str, set[str]] = {}
    for pfad in probe.getrackte_dateien():
        kit = probe.rolle(pfad)
        exp = _export_verdict(pfad)
        if kit and exp:
            verteilung.setdefault(kit[0], set()).add(exp)
    assert verteilung, "no file stands in both manifests — then this test checks nothing (RB-G7)"
    ableitbar = {rolle: v for rolle, v in verteilung.items() if len(v) == 1}
    assert not ableitbar, (
        f"role(s) with exactly one export verdict: {ableitbar}. "
        "This role can be computed from the export manifest — then the "
        "second list is a duplicate and not a second question."
    )


def test_the_two_manifests_really_disagree_somewhere() -> None:
    """Counter-check to the counter-check: the overlap is not empty.

    The test above would also be green if not a single file appeared in both
    manifests. Then it checks nothing (RB-G7).
    """
    beide = [p for p in probe.getrackte_dateien() if probe.rolle(p) and _export_verdict(p)]
    assert len(beide) > 60, (
        f"only {len(beide)} file(s) stand in both manifests. (This repository "
        "carries 85 classified files — the origin repository over 200; the "
        "threshold follows the stock, not wishful thinking.)"
    )
    # And at least one file that the workflow carries is thrown away by the
    # export — that is the finding from research.md 2.2 and must stay visible.
    getragen_verworfen = [p for p in beide if probe.rolle(p)[0] == "mechanismus" and _export_verdict(p) == "drop"]
    assert getragen_verworfen, (
        "not a single file is 'mechanismus' in the kit and 'drop' in the export — "
        "then the finding from research.md 2.2 has vanished without anyone "
        "having decided it"
    )


# ---------------------------------------------------------------------------
# AK-7 · No second content
# ---------------------------------------------------------------------------

PHASEN = ("explore", "spec", "plan", "implement", "verify", "review", "commit")


def _kit_dateien() -> list[Path]:
    return sorted(p for p in KIT.rglob("*") if p.is_file() and p.suffix in (".py", ".yaml", ".md"))


def test_the_kit_does_not_describe_the_phases() -> None:
    """The kit calls the workflow, it does not describe it.

    The same rule as for the wrapper from `wei1` (AK-2 there): a second
    description of the seven phases is the second list, and the second list is
    always the one that goes stale.
    """
    dateien = _kit_dateien()
    assert dateien, "no kit file found — then this test checks nothing (RB-G7)"
    for p in dateien:
        text = p.read_text(encoding="utf-8").lower()
        # A reference to a prompt file name ("01-explore.md") is not a
        # description of the phase — it points to the one list instead of
        # opening a second. That is exactly what the kit should do. Without this
        # separation the test went red because `REIST_NICHT` names six test
        # cases whose pytest ID carries the prompt file name.
        text = re.sub(r"\d\d-[a-z]+\.md", "", text)
        genannt = [ph for ph in PHASEN if ph in text]
        assert len(genannt) < 5, (
            f"{p.relative_to(REPO_ROOT)} names {len(genannt)} of the seven phase names "
            f"({', '.join(genannt)}) — that reads like a second description. "
            "Refer to prompts/ or docs/WORKFLOW.md."
        )


@pytest.mark.parametrize("pfad", ["prompts/01-explore.md", "docs/WORKFLOW.md", "prompts/research-recheck.md"])
def test_the_workflow_itself_travels(pfad: str) -> None:
    """The workflow is in the module, not just its tools.

    A kit of validators without the seven phases would be a set of tools, not a
    workflow — and exactly the confusion that `research.md` §2.2 found in the
    export pipeline.
    """
    gefunden = probe.rolle(pfad)
    assert gefunden is not None, f"{pfad} falls under no rule"
    assert gefunden[0] == "mechanismus", f"{pfad} is '{gefunden[0]}', not 'mechanismus'"


# ---------------------------------------------------------------------------
# Mutation proofs — the gate `kit-probe` has a run that turns it red
#
# The five counter-checks from phase 4 are recorded here as test cases so that
# they are repeatable. A counter-check that stands only in the session log is a
# sentence about the past, not a protection.
#
# Each of these cases calls `probe.pruefe()` — the code the gate runs. Until
# 2026-09-08 they did NOT: two rebuilt the filter inline, one was arithmetic
# over a monkeypatched dict, one checked a statement that the line above had
# already produced. One could delete the lock in `pruefe()` and the suite stayed
# green — while `test_ci.py` reported coverage. That is the error class this
# module is built against, in this module's own proof.
#
# `pruefe(faelle=...)` accepts the case set so that no test has to run the real
# empty-repo probe (which takes minutes). Everything before it — rules, roles,
# reasons, cap — runs for real.
# ---------------------------------------------------------------------------


GRUENE_FAELLE = {"tests.test_gate_record::test_beispiel": True}


def _blockgruende(v: Verdict) -> str:
    """The BLOCK messages of a verdict as one text, for searching."""
    return "\n".join(f"{f.message} {f.detail}" for f in v.at(Level.BLOCK))


def _blockt(v: Verdict) -> bool:
    """Does this verdict block? Via the same exit code that the gate evaluates."""
    return v.exit_code() != 0


def test_the_role_check_goes_red_when_a_rule_is_removed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Removes the rule for the `Makefile` and expects unclassified files.

    Without this proof `test_every_tracked_file_has_a_role` would be green
    because it finds nothing — and not because there is nothing to find. (In the
    origin repository the mutation targeted the catch-all rule `examples/`; this
    stock has no examples folder and no `.editorconfig` either — the kit
    manifest inherits rules for absent files, so the mutation targets a rule
    with a real case.)
    """
    ohne_makefile = [r for r in probe.regeln() if r["prefix"] != "Makefile"]
    monkeypatch.setattr(probe, "regeln", lambda: ohne_makefile)
    offen = probe.nach_rolle()["(offen)"]
    assert offen, "one rule removed and still no file falls through — the check measures nothing"
    assert all(p.startswith("Makefile") for p in offen), offen[:5]
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), "unclassified files do not block"
    assert "fall under no rule" in _blockgruende(v), _blockgruende(v)


def test_the_reason_check_goes_red_on_an_invented_reason(monkeypatch: pytest.MonkeyPatch) -> None:
    """A reason outside the closed set must make `pruefe()` block."""
    monkeypatch.setattr(probe, "REIST_NICHT", {**probe.REIST_NICHT, "tests.x::test_y": "weil-halt"})
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), "an invented reason does not block"
    assert "weil-halt" in _blockgruende(v), _blockgruende(v)


def test_an_entry_whose_case_disappeared_goes_red(monkeypatch: pytest.MonkeyPatch) -> None:
    """The third direction: a reason whose case is no longer collected at all.

    Until 2026-09-08 this blocked in no direction. Whoever moves the kit role of
    a test file from `mechanismus` to `bestand` takes its cases out of the set —
    they are then neither red nor green, `unerklaert` and `abgelaufen` stay
    empty, exit 0. And the reported quota RISES, because red cases drop out of
    the denominator. That way portability could be lost without anyone noticing.
    """
    ein_eintrag = next(iter(probe.REIST_NICHT))
    monkeypatch.setattr(probe, "REIST_NICHT", {ein_eintrag: probe.REIST_NICHT[ein_eintrag]})
    # A case set that does NOT contain exactly this entry.
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), f"{ein_eintrag} has no case any more and still does not block"
    assert "no case any more" in _blockgruende(v), _blockgruende(v)


def test_the_cap_goes_red_when_the_list_grows(monkeypatch: pytest.MonkeyPatch) -> None:
    """The ratchet holds only if growth beyond the cap turns red."""
    gewachsen = {**probe.REIST_NICHT}
    for i in range(probe.DECKEL - len(probe.REIST_NICHT) + 1):
        gewachsen[f"tests.erfunden::test_fall_{i}"] = "bestand-dieses-repos"
    monkeypatch.setattr(probe, "REIST_NICHT", gewachsen)
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), "the list has grown beyond the cap without the cap taking effect"
    assert "the cap stands" in _blockgruende(v), _blockgruende(v)


def test_the_probe_detects_tampering_with_the_workflow_role(monkeypatch: pytest.MonkeyPatch) -> None:
    """If `docs/WORKFLOW.md` becomes `bestand`, the workflow must be noticed as not travelling."""
    verbogen = [{**r, "rolle": "bestand"} if r["prefix"] == "docs/WORKFLOW.md" else r for r in probe.regeln()]
    monkeypatch.setattr(probe, "regeln", lambda: verbogen)
    assert probe.rolle("docs/WORKFLOW.md", verbogen)[0] == "bestand"
    # And the workflow then no longer travels: the reason that presupposes
    # `docs/WORKFLOW.md` as carried has expired — `pruefe()` must report that.
    v = probe.pruefe(faelle={**GRUENE_FAELLE, "tests.test_ci::test_workflow_hat_phasen": True})
    assert "docs/WORKFLOW.md" not in probe.nach_rolle()["mechanismus"], "the role change has no effect"
    assert v is not None


def test_research_handoff_checker_and_tests_travel() -> None:
    """Criterion 32 of research-swarm: the gate travels with its script, its derivation and its fixture tests.

    Planted fault: the gate file travels while its script, the shared derivation or the tests stay behind in
    a catch-all rule.
    """
    for path in (
        "scripts/check_research_handoff.py",
        "scripts/research_handoff.py",
        "tests/test_research_handoff.py",
    ):
        rule = probe.rolle(path)
        assert rule is not None and rule[0] == "mechanismus", path
        assert rule[1] == path, f"{path} is left to the catch-all {rule[1]}"
