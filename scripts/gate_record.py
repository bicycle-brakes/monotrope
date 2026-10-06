"""The gate record — a state machine from which `accepted` is DERIVED.

`docs/governance/quality-gates.md` §6 says it in one sentence: *a gate record is
a file, not a field.* This file turns that into code.

**Why this matters, in numbers.** The error catalogue holds three findings that
share one cause — an acceptance kept as a *field*:

  F-A-52  A signature was withdrawn because the conclusion changed — the name
          stood against text the person never read.
  F-A-53  `accepted_unsigned` collapses two states; the normal case has no
          name.
  F-A-58  Three contracts stand at `accepted` against a withdrawn acceptance.
          Significance: **critical (data)**.

A field can be set. A derived state cannot — it is true or it is not, and the
reasons fall out of the computation.

**That is why there is no setter for `ACCEPTED` here.** `ist_abgenommen()`
returns a pair of verdict and reasons; whoever takes only the verdict loses
nothing but the explanation.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

# The four states from quality-gates.md §6.
ZUSTAENDE: tuple[str, ...] = ("DRAFT", "IN_REVIEW", "ACCEPTED", "WITHDRAWN")

# Allowed edges. What is missing here is forbidden — not "unusual".
#
# `ACCEPTED -> ACCEPTED` is missing on purpose: a second acceptance of the same
# record is not a confirmation but hides that the subject has changed. Whoever
# wants to accept again goes through WITHDRAWN.
UEBERGAENGE: dict[str, tuple[str, ...]] = {
    "DRAFT": ("IN_REVIEW",),
    "IN_REVIEW": ("DRAFT", "ACCEPTED", "WITHDRAWN"),
    "ACCEPTED": ("WITHDRAWN",),
    "WITHDRAWN": ("DRAFT",),
}


# Which roles a gate REQUIRES. From the table in `quality-gates.md` §4, column
# "Wer unterschreibt" — normative there, machine-readable here. The prose name
# comes along so that `test_the_required_roles_match_the_governance_table` can
# hold both sides against each other: a role that stands in only one of the two
# places is a finding, not a detail.
#
# **Why this set exists at all.** Until 2026-09-08 `ist_abgenommen()` only checked
# that the entries that are *present* are filled in completely — not that the
# required set of roles is reached. An HG-1 record with a single signature got
# through as accepted, and so did two entries under freely invented role
# strings. That is exactly the error F-A-58 ("critical (data)") describes: three
# contracts stood at `accepted` against an acceptance that was none.
PFLICHT_ROLLEN: dict[str, dict[str, str]] = {
    "HG-1": {"data-architect": "Data Architect", "fachseite": "Fachseite"},
    "HG-2": {"data-product-owner": "Data Product Owner (Consumer)", "data-architect": "Data Architect"},
    "HG-3": {"produktverantwortlicher": "Produktverantwortlicher", "data-architect": "Data Architect"},
    "HG-4": {"operations-owner": "Operations Owner"},
}


class UngueltigerUebergang(ValueError):
    """A transition the machine does not know."""


def pruefe_uebergang(von: str, nach: str) -> None:
    """Raises if the edge does not exist. No silent pass-through."""
    if von not in ZUSTAENDE:
        raise UngueltigerUebergang(f"unknown source state: {von!r}")
    if nach not in ZUSTAENDE:
        raise UngueltigerUebergang(f"unknown target state: {nach!r}")
    if nach not in UEBERGAENGE[von]:
        raise UngueltigerUebergang(
            f"{von} -> {nach} is not an allowed transition. Allowed from {von}: {UEBERGAENGE[von]}"
        )


def _zeit(wert: Any) -> dt.datetime | None:
    if isinstance(wert, dt.datetime):
        return wert
    if isinstance(wert, str):
        try:
            return dt.datetime.fromisoformat(wert.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _in_review_seit(record: dict) -> dt.datetime | None:
    """When did the record last go to IN_REVIEW?

    The **last** transition counts, not the first: after a return to DRAFT and a
    renewed submission an old approval must not carry over.
    """
    zeiten = [
        _zeit(e.get("at")) for e in record.get("history", []) if isinstance(e, dict) and e.get("to") == "IN_REVIEW"
    ]
    vorhanden = [z for z in zeiten if z is not None]
    return max(vorhanden) if vorhanden else None


def ist_abgenommen(record: dict, heutiger_hash: str | None = None) -> tuple[bool, list[str]]:
    """Derives whether this record is accepted — with a reason per condition.

    The four conditions are in `quality-gates.md` §6. Each yields its own
    sentence when violated; a list of reasons is usable, a bare `False` is not.

    `heutiger_hash` is the hash of the subject **now**. If it is missing, the
    fourth condition is not checked and that is reported explicitly — silence
    would be the most dangerous answer here (RB-G7).
    """
    gruende: list[str] = []

    if record.get("state") != "ACCEPTED":
        gruende.append(f"state is {record.get('state')!r}, not ACCEPTED")

    # 1 · all required roles are present, each with a review URL
    signers = record.get("signers") or []
    pflicht = [s for s in signers if isinstance(s, dict)]
    if not pflicht:
        gruende.append("kein Unterzeichner eingetragen")

    # The gate's set of roles — not just "somebody signed".
    gate = record.get("gate")
    verlangt = PFLICHT_ROLLEN.get(gate)
    if verlangt is None:
        gruende.append(
            f"gate {gate!r} is unknown to PFLICHT_ROLLEN — without a target set any signature is enough, "
            f"and that is no acceptance. Known: {', '.join(sorted(PFLICHT_ROLLEN))}"
        )
    else:
        unterschrieben = {s.get("role") for s in pflicht if s.get("role")}
        fehlend = sorted(set(verlangt) - unterschrieben)
        if fehlend:
            gruende.append(f"{gate} requires {', '.join(sorted(verlangt))} — missing: {', '.join(fehlend)}")
        fremd = sorted(unterschrieben - set(verlangt))
        if fremd:
            gruende.append(
                f"{gate} kennt die Rolle(n) {', '.join(fremd)} nicht — eine erfundene Rolle ersetzt keine verlangte"
            )
        # Two roles in one hand are one signature, not two.
        handles = [s.get("handle") for s in pflicht if s.get("handle")]
        doppelt = sorted({h for h in handles if handles.count(h) > 1})
        if doppelt:
            gruende.append(
                f"{', '.join(doppelt)} unterschreibt in mehreren Rollen — "
                "das 'und' in quality-gates.md meint zwei Menschen, nicht zwei Zeilen"
            )

    for s in pflicht:
        if not s.get("role"):
            gruende.append(f"signer without a role: {s}")
        if not s.get("handle"):
            gruende.append(f"Rolle {s.get('role')!r} ohne Handle — eine Rolle unterschreibt nicht, ein Mensch tut es")
        if not s.get("review_url"):
            gruende.append(f"{s.get('handle')!r} ohne Review-URL — dann ist die Zustimmung nicht nachlesbar")

    # 2 · the approval is dated AFTER the transition to IN_REVIEW
    seit = _in_review_seit(record)
    if seit is None:
        gruende.append("kein Uebergang nach IN_REVIEW in der history — der Record wurde nie vorgelegt")
    else:
        for s in pflicht:
            wann = _zeit(s.get("at"))
            if wann is None:
                gruende.append(f"{s.get('handle')!r} has no readable timestamp")
            elif wann < seit:
                gruende.append(
                    f"{s.get('handle')!r} hat vor der Vorlage zugestimmt "
                    f"({wann.isoformat()} < {seit.isoformat()}) — das ist eine Zustimmung zu einem anderen Text"
                )

    # 3 · the approver is neither author nor last pusher
    autor = record.get("author")
    pusher = record.get("last_pusher")
    for s in pflicht:
        handle = s.get("handle")
        if handle and handle == autor:
            gruende.append(f"{handle!r} ist Autor und Unterzeichner — das ist keine Abnahme, das ist eine Schleife")
        if handle and handle == pusher:
            gruende.append(f"{handle!r} hat zuletzt gepusht und unterschreibt — dieselbe Schleife")

    # 4 · subject.sha256 equals today's hash
    subject = record.get("subject") or {}
    signiert = subject.get("sha256")
    if not signiert:
        gruende.append("subject.sha256 fehlt — dann ist die Unterschrift an nichts gebunden")
    elif heutiger_hash is None:
        gruende.append("kein heutiger Hash uebergeben — die Bindung an den Gegenstand wurde NICHT geprueft")
    elif signiert != heutiger_hash:
        gruende.append(
            f"der Gegenstand hat sich geaendert: signiert {signiert}, heute {heutiger_hash}. "
            "Was nach der Signatur geaendert wird, ist wieder unsigniert (RB-M1)"
        )

    return (not gruende), gruende


def pflichtfelder() -> frozenset[str]:
    """What a record carries — the list the template is checked against."""
    return frozenset({"gate", "subject", "state", "history", "signers"})
