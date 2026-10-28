"""The shared admissible-terms builder: its production contract and its isolation.

`terms_fixtures.admissible_terms` is the one construction site for a synthetic
record the unchanged production admission (`stage2.terms_problem`) admits. The
contract test keeps the helper from falling behind the rule: the day a required
default goes missing, a YAML round trip turns a date native, or the rule stops
refusing a record without its expiry, a case here goes red. No case reaches a
real endpoint, reads the repository's real declaration or calls a model.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402
from terms_fixtures import admissible_terms  # noqa: E402

FROZEN_DAY = dt.date(2026, 10, 27)


def test_default_terms_pass_production_admission(monkeypatch: pytest.MonkeyPatch) -> None:
    """The untouched default record is admitted by the production check, judged against a pinned UTC day.

    Fault: a required default missing from the builder, a YAML-native date
    surviving a declaration round trip, or a rule that no longer refuses a
    record without its expiry turns this red.
    """
    monkeypatch.setattr(stage2, "terms_today", lambda: FROZEN_DAY)
    record = admissible_terms()
    assert "anfragen_5h" not in record, "the default grew cost; cost is a deliberate override"
    assert "uebersprungen" not in record, "the default grew a skip marker; a skip is a deliberate act"
    # The fault, planted: the same record without its expiry is refused, so the
    # admission below is the rule's verdict on this record, not a formality.
    lacking = {name: value for name, value in record.items() if name != "valid_until"}
    refused = stage2.terms_problem({"modelle_terms": {"m": lacking}}, "m")
    assert refused is not None and "valid_until is missing" in refused, refused
    assert stage2.terms_problem({"modelle_terms": {"m": record}}, "m") is None
    # A declaration round trip keeps every date a quoted string: a YAML-native
    # date would refuse, so admission after the trip is the contract's proof.
    reread = yaml.safe_load(yaml.safe_dump({"modelle_terms": {"m": admissible_terms()}}))
    assert isinstance(reread["modelle_terms"]["m"]["gelesen"], str)
    assert isinstance(reread["modelle_terms"]["m"]["valid_until"], str)
    assert stage2.terms_problem(reread, "m") is None


def test_terms_overrides_and_mutations_are_isolated() -> None:
    """Overrides, deletions and planted markers on one result never reach a later call's defaults.

    Fault: the builder sharing one record between calls turns this red on the
    first leaked field.
    """
    customized = admissible_terms(aufbewahrung="30 days")
    customized.pop("quelle")
    skipped = admissible_terms(uebersprungen="2026-10-17", grund="planted for another test")
    later = admissible_terms()
    assert later["aufbewahrung"] == "0 days", "an earlier call's override leaked into the defaults"
    assert later["quelle"], "an earlier call's deletion leaked into the defaults"
    assert "uebersprungen" not in later and "grund" not in later, "an earlier call's skip marker leaked"
    assert later["training"] == "Not used" and later["valid_until"] == "2099-01-01"
    # And the customised results keep their own shape.
    assert customized["aufbewahrung"] == "30 days" and "quelle" not in customized
    assert skipped["uebersprungen"] == "2026-10-17" and skipped["grund"] == "planted for another test"
