"""The state machine of the gate record — and the counter-check to every rule.

Three findings from `docs/governance/fehler-katalog.md` have the same cause: an
acceptance that was kept as a *field*. F-A-58 carries significance **critical
(data)** — three contracts stood at `accepted` against a withdrawn acceptance.

This file checks the four conditions from `quality-gates.md` §6 one by one, and
each in its violated form. A test that knows only the green case does not prove
that the derivation rejects anything at all.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gate_record as g  # noqa: E402

VORLAGE = REPO / "templates" / "gate-record.yaml"


def _gueltiger_record() -> dict:
    """A record that fulfils all four conditions — the basis of every mutation."""
    return {
        "gate": "HG-1",
        "subject": {"kind": "entity-contract", "path": "contracts/x.yaml", "sha256": "abc123"},
        "state": "ACCEPTED",
        "author": "autorin",
        "last_pusher": "autorin",
        "history": [
            {"to": "DRAFT", "at": "2026-01-01T00:00:00Z", "by": "autorin"},
            {"to": "IN_REVIEW", "at": "2026-01-02T00:00:00Z", "by": "autorin"},
        ],
        "signers": [
            {
                "role": "data-architect",
                "handle": "architektin",
                "at": "2026-01-03T00:00:00Z",
                "review_url": "https://example.invalid/pr/1#review-1",
            },
            {
                # HG-1 requires data architect AND business side (`fachseite`).
                # Until 2026-09-08 `data-product-owner` stood here — the role of
                # HG-2 — and nothing noticed, because the set of roles was never
                # checked.
                "role": "fachseite",
                "handle": "eignerin",
                "at": "2026-01-03T12:00:00Z",
                "review_url": "https://example.invalid/pr/1#review-2",
            },
        ],
    }


def test_a_complete_record_is_accepted() -> None:
    """The precondition: the green case is really green.

    Without it any mutation below could be red for any other reason, and the
    tests would claim something they do not measure.
    """
    ok, gruende = g.ist_abgenommen(_gueltiger_record(), "abc123")
    assert ok, f"the complete record is rejected: {gruende}"


# --- Condition 1: roles, handles, review URLs ------------------------------


def test_a_gate_with_a_missing_required_role_is_not_accepted() -> None:
    """Seeded counter-check to the finding of 2026-09-08 — the core of F-A-58.

    The independent review of PR #124 brought an HG-1 record with **one**
    signature to `(True, [])`: `ist_abgenommen()` checks whether existing
    entries are filled in completely, but not whether the set of roles required
    by the gate has been reached. A gate that lets one of two signatures through
    is not a gate.
    """
    r = _gueltiger_record()
    r["signers"] = [r["signers"][0]]  # only the architect, the business side is missing
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "an HG-1 record with only one of two mandatory roles counts as accepted"
    assert any("fachseite" in x for x in gruende), gruende


def test_an_invented_role_does_not_replace_a_required_one() -> None:
    """Two entries are not two roles.

    The second case from the same review: the same number of signatures, but
    under freely invented role strings. If one counts only entries, that is
    indistinguishable from a real acceptance.
    """
    r = _gueltiger_record()
    for s_, rolle in zip(r["signers"], ("irgendwas", "irgendwas-anderes"), strict=True):
        s_["role"] = rolle
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "two invented roles count as the two mandatory roles of HG-1"
    assert any("kennt die Rolle" in x for x in gruende), gruende


def test_one_human_in_two_roles_is_one_signature() -> None:
    """The `und` (and) in quality-gates.md means two humans, not two rows."""
    r = _gueltiger_record()
    r["signers"][1]["handle"] = r["signers"][0]["handle"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "the same person in both mandatory roles counts as two signatures"
    assert any("mehreren Rollen" in x for x in gruende), gruende


def test_an_unknown_gate_has_no_required_set_and_is_refused() -> None:
    """Without a required set every signature is enough — that must be loud (RB-G7)."""
    r = _gueltiger_record()
    r["gate"] = "HG-9"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "an unknown gate can be accepted"
    assert any("PFLICHT_ROLLEN" in x for x in gruende), gruende


def test_the_required_roles_match_the_governance_table() -> None:
    """`PFLICHT_ROLLEN` and quality-gates.md §4 say the same — or it gets noticed.

    The table is normative, the dict is machine-readable. Two versions of the
    same statement drift apart as soon as nobody holds them against each other;
    then the rule stands in one place and the effect in the other.
    """
    tabelle = (REPO / "docs" / "governance" / "quality-gates.md").read_text(encoding="utf-8")
    zeilen = [z for z in tabelle.splitlines() if z.startswith("| **HG-")]
    assert len(zeilen) == len(g.PFLICHT_ROLLEN), (
        f"quality-gates.md names {len(zeilen)} human gates, PFLICHT_ROLLEN knows "
        f"{len(g.PFLICHT_ROLLEN)} — one of the two was not updated"
    )
    for zeile in zeilen:
        spalten = [s.strip() for s in zeile.strip("|").split("|")]
        gate = spalten[0].strip("* ")
        wer = spalten[3]
        assert gate in g.PFLICHT_ROLLEN, f"{gate} stands in the table but not in PFLICHT_ROLLEN"
        namen = [t.strip() for t in wer.split("**und**")]
        assert len(namen) == len(g.PFLICHT_ROLLEN[gate]), (
            f"{gate}: the table names {len(namen)} role(s) ({wer}), PFLICHT_ROLLEN {len(g.PFLICHT_ROLLEN[gate])}"
        )
        for prosa in g.PFLICHT_ROLLEN[gate].values():
            assert prosa in wer, f"{gate}: PFLICHT_ROLLEN names {prosa!r}, the table does not: {wer!r}"


def test_a_record_without_signers_is_not_accepted() -> None:
    r = _gueltiger_record()
    r["signers"] = []
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("kein Unterzeichner" in x for x in gruende)


def test_a_signer_without_a_review_url_is_not_accepted() -> None:
    """A consent without a citation cannot be looked up."""
    r = _gueltiger_record()
    del r["signers"][0]["review_url"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("Review-URL" in x for x in gruende)


def test_a_role_without_a_human_is_not_a_signature() -> None:
    r = _gueltiger_record()
    del r["signers"][1]["handle"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("Handle" in x for x in gruende)


# --- Condition 2: consent after the submission -----------------------------


def test_a_signature_before_the_review_started_is_not_accepted() -> None:
    """A consent from before the submission applies to a different text — F-A-52."""
    r = _gueltiger_record()
    r["signers"][0]["at"] = "2026-01-01T06:00:00Z"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("vor der Vorlage" in x for x in gruende)


def test_the_last_review_transition_counts_not_the_first() -> None:
    """After return and renewed submission an old consent no longer counts."""
    r = _gueltiger_record()
    r["history"] += [
        {"to": "DRAFT", "at": "2026-01-04T00:00:00Z", "by": "autorin"},
        {"to": "IN_REVIEW", "at": "2026-01-05T00:00:00Z", "by": "autorin"},
    ]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "both consents lie before the second submission and must not continue to apply"
    assert any("vor der Vorlage" in x for x in gruende)


def test_a_record_never_submitted_is_not_accepted() -> None:
    r = _gueltiger_record()
    r["history"] = [{"to": "DRAFT", "at": "2026-01-01T00:00:00Z", "by": "autorin"}]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("nie vorgelegt" in x for x in gruende)


# --- Condition 3: not oneself -----------------------------------------------


def test_an_author_cannot_sign_their_own_record() -> None:
    r = _gueltiger_record()
    r["signers"][0]["handle"] = "autorin"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("Schleife" in x for x in gruende)


def test_the_last_pusher_cannot_sign_either() -> None:
    r = _gueltiger_record()
    r["last_pusher"] = "architektin"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("gepusht" in x for x in gruende)


# --- Condition 4: binding to the subject -----------------------------------


def test_a_changed_subject_invalidates_the_signature() -> None:
    """The core of RB-M1: what is changed after the signature is unsigned."""
    ok, gruende = g.ist_abgenommen(_gueltiger_record(), "ein-anderer-hash")
    assert not ok and any("geaendert" in x for x in gruende)


def test_a_missing_subject_hash_is_not_accepted() -> None:
    r = _gueltiger_record()
    del r["subject"]["sha256"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("an nichts gebunden" in x for x in gruende)


def test_an_unchecked_binding_is_named_not_silent() -> None:
    """Without today's hash the fourth condition is NOT checked — and that is
    said. Waving it through silently would be the most dangerous outcome here
    (RB-G7)."""
    ok, gruende = g.ist_abgenommen(_gueltiger_record(), None)
    assert not ok and any("NICHT geprueft" in x for x in gruende)


# --- The state is derived, not set -----------------------------------------


def test_accepted_is_derived_not_set() -> None:
    """`state: ACCEPTED` alone is not enough — F-A-58.

    The record here carries the state and still violates three conditions.
    Exactly that is how three contracts of the instance stood at `accepted`.
    """
    nackt = {"gate": "HG-1", "state": "ACCEPTED", "subject": {}, "history": [], "signers": []}
    ok, gruende = g.ist_abgenommen(nackt, "abc123")
    assert not ok
    assert len(gruende) >= 3, f"only {len(gruende)} reasons — the derivation checks too little: {gruende}"


@pytest.mark.parametrize(
    "von,nach",
    [("DRAFT", "ACCEPTED"), ("ACCEPTED", "ACCEPTED"), ("WITHDRAWN", "ACCEPTED"), ("DRAFT", "WITHDRAWN")],
)
def test_an_unknown_transition_is_refused(von: str, nach: str) -> None:
    with pytest.raises(g.UngueltigerUebergang):
        g.pruefe_uebergang(von, nach)


@pytest.mark.parametrize(
    "von,nach",
    [("DRAFT", "IN_REVIEW"), ("IN_REVIEW", "ACCEPTED"), ("ACCEPTED", "WITHDRAWN"), ("WITHDRAWN", "DRAFT")],
)
def test_the_allowed_transitions_pass(von: str, nach: str) -> None:
    g.pruefe_uebergang(von, nach)


def test_every_state_can_be_left() -> None:
    """A dead end in the automaton would be a state that nobody gets out of."""
    for zustand in g.ZUSTAENDE:
        assert g.UEBERGAENGE.get(zustand), f"{zustand} has no exit"


# --- The template ----------------------------------------------------------


def test_the_template_is_a_draft_not_an_example_of_acceptance() -> None:
    """A template that pretends ACCEPTED teaches the error."""
    record = yaml.safe_load(VORLAGE.read_text(encoding="utf-8"))
    assert record["state"] == "DRAFT"
    ok, _ = g.ist_abgenommen(record, record["subject"]["sha256"])
    assert not ok, "the template counts as accepted — then it is a free pass"


def test_the_template_carries_every_required_field() -> None:
    record = yaml.safe_load(VORLAGE.read_text(encoding="utf-8"))
    fehlend = sorted(g.pflichtfelder() - set(record))
    assert not fehlend, f"the template leaves out mandatory fields: {fehlend}"


def test_a_record_without_a_required_field_is_caught() -> None:
    """Counter-check to the test above."""
    record = yaml.safe_load(VORLAGE.read_text(encoding="utf-8"))
    verstuemmelt = copy.deepcopy(record)
    del verstuemmelt["signers"]
    assert sorted(g.pflichtfelder() - set(verstuemmelt)) == ["signers"]
