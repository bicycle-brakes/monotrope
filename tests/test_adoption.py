"""The reader of the adoption record (ADR 0014), its place in the kit, and the
record's place in provenance.yaml.

The reader is the one module that reads `decisions/adoption.yaml`; the gates
that exempt the changes begun before them ask it for their day by gate id.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "kit"))
import adoption  # noqa: E402
import probe  # noqa: E402

RECORD = "decisions/adoption.yaml"


def _record(root: Path, text: str) -> None:
    (root / "decisions").mkdir(exist_ok=True)
    (root / RECORD).write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "text",
    [
        None,  # the file does not exist
        "adopted: [",  # not valid YAML
        "- a\n- b\n",  # not a mapping
        "adopted:\n  interview-minimums: 2026-10-08\n",  # no schema_version
        "schema_version: 2\nadopted:\n  interview-minimums: 2026-10-08\n",
        "schema_version: '1'\nadopted:\n  interview-minimums: 2026-10-08\n",
        "schema_version: 1\nadopted:\n  interview-minimums: '2026-10-08'\n",  # a quoted day
        "schema_version: 1\nadopted:\n  other-gate: 2026-10-08\n",  # no day for the gate
        "schema_version: 1\n",  # no adopted mapping
        "schema_version: 1\nadopted:\n  interview-minimums: 2026-10-08\n  interview-minimums: 2026-10-09\n",
    ],
)
def test_the_reader_refuses_a_record_it_cannot_read(tmp_path: Path, text: str | None) -> None:
    if text is not None:
        _record(tmp_path, text)
    with pytest.raises(adoption.NotRecorded) as refused:
        adoption.adopted_on(tmp_path, "interview-minimums")
    assert RECORD in str(refused.value)
    assert "interview-minimums: YYYY-MM-DD" in str(refused.value)


def test_the_reader_returns_each_gates_own_day(tmp_path: Path) -> None:
    _record(
        tmp_path,
        "schema_version: 1\nadopted:\n  interview-minimums: 2026-10-08\n  criterion-ledger: 2026-10-11\n",
    )
    assert adoption.adopted_on(tmp_path, "interview-minimums") == date(2026, 10, 8)
    assert adoption.adopted_on(tmp_path, "criterion-ledger") == date(2026, 10, 11)
    with pytest.raises(adoption.NotRecorded):
        adoption.adopted_on(tmp_path, "a-third-gate")


def test_the_gate_and_its_reader_travel_and_the_record_stays() -> None:
    for path in (
        "scripts/check_interview_minimums.py",
        "scripts/adoption.py",
        "tests/test_check_interview_minimums.py",
        "tests/test_adoption.py",
    ):
        rule = probe.rolle(path)
        assert rule is not None and rule[0] == "mechanismus", path
        assert rule[1] == path, f"{path} is left to the catch-all {rule[1]}"
    rule = probe.rolle(RECORD)
    assert rule is not None and rule[0] == "bestand"
    assert rule[1] == RECORD, f"{RECORD} is left to the rule {rule[1]}"


def test_the_adoption_record_is_human_decided() -> None:
    provenance = yaml.safe_load((REPO_ROOT / "provenance.yaml").read_text(encoding="utf-8"))
    entries = [p for p in provenance["paths"] if p.get("prefix") == RECORD]
    assert len(entries) == 1
    assert entries[0]["allowed"] == ["human-decided"]
