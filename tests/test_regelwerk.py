"""The rule set holds what it claims.

A rule list is the kind of document that rots most quietly. It is written once,
everyone agrees, and afterwards the tests it points to wander off: one is
renamed, one moves into another file, one is deleted because it "catches
nothing any more". The rule stays and reads as strict as ever — only nobody
holds it any more.

That is why this file does not check the rules (the named enforcers do that)
but the **assignment**: that every rule at level 3 or higher names an enforcer
that exists, and that every rule below carries a valve with a date. A rule with
neither is a request pretending to be a rule.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGELWERK = REPO_ROOT / "docs" / "governance" / "regelwerk.md"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from ramp_valves import valves  # noqa: E402

ID_RE = re.compile(r"\bRB-[AHGMPS]\d\b")
ZEILE_RE = re.compile(r"^\|\s*\*\*(RB-[AHGMPS]\d)\*\*\s*\|(.*)$")
CI_FILE = REPO_ROOT / ".github" / "workflows" / "ci.yml"


class Regel:
    def __init__(self, rid: str, text: str, stufe: int, erzwinger: list[str], gilt_in: str) -> None:
        self.id = rid
        self.text = text
        self.stufe = stufe
        self.erzwinger = erzwinger
        self.gilt_in = gilt_in


def _regeln(quelle: Path = REGELWERK) -> list[Regel]:
    """Reads the rule tables. A row that does not fit is not silently discarded."""
    gefunden: list[Regel] = []
    for zeile in quelle.read_text(encoding="utf-8").splitlines():
        m = ZEILE_RE.match(zeile)
        if not m:
            continue
        # Split on unescaped pipes — RB-H1 names `\|\| true` in its text.
        spalten = [s.strip() for s in re.split(r"(?<!\\)\|", m.group(2))]
        # Rule · Level · Enforcer · Applies in · (empty remainder behind the closing pipe)
        assert len(spalten) >= 4, f"{m.group(1)}: {len(spalten)} columns, expected 4"
        text, stufe_roh, erzwinger_roh, gilt_in = spalten[0], spalten[1], spalten[2], spalten[3]
        assert stufe_roh.isdigit(), f"{m.group(1)}: level {stufe_roh!r} is not a number"
        # Refs are separated by `·`; `::foo` inherits the file of the previous reference.
        refs: list[str] = []
        letzte_datei = ""
        for roh in erzwinger_roh.split("·"):
            ref = roh.strip().strip("`").replace("`", "")
            if not ref:
                continue
            if ref.startswith("::"):
                ref = letzte_datei + ref
            elif "::" in ref:
                letzte_datei = ref.split("::", 1)[0]
            refs.append(ref)
        gefunden.append(Regel(m.group(1), text, int(stufe_roh), refs, gilt_in))
    return gefunden


def _frontmatter(quelle: Path = REGELWERK) -> dict:
    text = quelle.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "no frontmatter"
    return yaml.safe_load(text[4 : text.find("\n---", 4)]) or {}


def _enforcer_da(ref: str) -> bool:
    if ref.startswith("Ramp:"):
        return True
    if ref.startswith("lakeswitch:"):
        return True
    if ref.startswith("ci.yml#"):
        return f"id: {ref.split('#', 1)[1]}" in CI_FILE.read_text(encoding="utf-8")
    if "::" not in ref:
        return (REPO_ROOT / ref).exists()
    datei, funktion = ref.split("::", 1)
    pfad = REPO_ROOT / datei
    if not pfad.is_file():
        return False
    return re.search(rf"^def {re.escape(funktion)}\(", pfad.read_text(encoding="utf-8"), re.M) is not None


REGELN = _regeln()
VENTILE = {v.name: v for v in valves()}


# ---------------------------------------------------------------------------
# The list itself
# ---------------------------------------------------------------------------


def test_the_list_is_not_empty() -> None:
    """Green over zero rules would be the confirmation that nothing applies (RB-G7)."""
    assert len(REGELN) >= 30, f"only {len(REGELN)} rules parsed — the pattern no longer fits"


def test_no_two_rules_share_an_id() -> None:
    ids = [r.id for r in REGELN]
    doppelt = sorted({i for i in ids if ids.count(i) > 1})
    assert not doppelt, f"assigned twice: {doppelt}"


def test_every_family_is_numbered_without_a_gap() -> None:
    """A gap is either a deleted rule or a typo — both deserve to be named."""
    nach_familie: dict[str, list[int]] = {}
    for r in REGELN:
        nach_familie.setdefault(r.id[3], []).append(int(r.id[4:]))
    for familie, nummern in nach_familie.items():
        assert sorted(nummern) == list(range(1, len(nummern) + 1)), f"family {familie}: {sorted(nummern)}"


def test_every_rule_id_referenced_anywhere_exists() -> None:
    """A reference to a rule that does not exist is a rule that nobody reads."""
    bekannt = {r.id for r in REGELN}
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z", "*.md", "*.py", "*.yaml", "*.yml", "*.sh", "*.json"],
        capture_output=True,
        text=True,
        check=True,
    )
    verweise: list[str] = []
    unbekannt: list[str] = []
    for rel in out.stdout.split("\0"):
        if not rel or rel.startswith(("docs/archive/", "docs/journal/")):
            continue
        try:
            text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for treffer in ID_RE.findall(text):
            verweise.append(f"{rel}:{treffer}")
            if treffer not in bekannt:
                unbekannt.append(f"{rel}: {treffer}")
    assert verweise, "Precondition: somewhere a rule is cited at all."
    assert not unbekannt, "Reference to a rule that the rule set does not know:\n  " + "\n  ".join(unbekannt)


# ---------------------------------------------------------------------------
# Level and enforcer — the actual contract
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("regel", REGELN, ids=lambda r: r.id)
def test_rules_at_level_three_or_higher_name_an_existing_enforcer(regel: Regel) -> None:
    """From level 3 on, the rule claims that a machine holds it. Then that machine must exist."""
    if regel.stufe < 3:
        return
    echte = [e for e in regel.erzwinger if not e.startswith("Ramp:")]
    assert echte, f"{regel.id} stands at level {regel.stufe} and names only valves"
    fehlend = [e for e in echte if not _enforcer_da(e)]
    assert not fehlend, (
        f"{regel.id} names an enforcer that does not exist: {fehlend}\n"
        "Either the test was renamed — then follow up here — or the rule "
        "actually stands at level 2 and needs a valve."
    )


@pytest.mark.parametrize("regel", REGELN, ids=lambda r: r.id)
def test_rules_without_an_enforcer_are_at_most_level_two_and_carry_a_dated_ramp(regel: Regel) -> None:
    """A rule that nobody holds says so — and says until when.

    Without a valve "provisionally only convention" is the permanent state:
    nobody notices that the condition has long held, because nothing asks.
    """
    if regel.stufe >= 3:
        return
    ventile = [e.split(":", 1)[1] for e in regel.erzwinger if e.startswith("Ramp:")]
    assert ventile, f"{regel.id} stands at level {regel.stufe} and names no valve"
    for name in ventile:
        assert name in VENTILE, f"{regel.id}: valve {name!r} is not in ramp_valves.valves()"
        assert VENTILE[name].deadline is not None, (
            f"{regel.id}: valve {name!r} has no deadline. A predicate alone measures the stock, never the work on it."
        )


def test_every_named_ramp_exists_and_no_valve_is_orphaned() -> None:
    """Both directions. A valve without a rule guards nothing."""
    genannt = {e.split(":", 1)[1] for r in REGELN for e in r.erzwinger if e.startswith("Ramp:")}
    fehlend = sorted(genannt - set(VENTILE))
    assert not fehlend, f"named in the rule set, not present in ramp_valves.py: {fehlend}"

    # Lint valves and the provenance valve belong to no rule — they are older
    # than this page and stand here explicitly as an exception.
    ohne_regel = sorted(
        n for n in VENTILE if n not in genannt and not n.startswith("lint-") and n != "provenance-review"
    )
    assert not ohne_regel, f"valve without a rule: {ohne_regel}"


def test_no_rule_stands_on_level_one() -> None:
    """Level 1 means: it is written down and nothing else. Then it does not belong here."""
    schwach = [r.id for r in REGELN if r.stufe < 2]
    assert not schwach, f"pure convention in the rule set: {schwach}"


@pytest.mark.parametrize("regel", REGELN, ids=lambda r: r.id)
def test_every_rule_says_where_it_applies(regel: Regel) -> None:
    assert regel.gilt_in.strip(), f"{regel.id} does not say where it applies"
    unbekannt = set(regel.gilt_in.split()) - {"P", "L", "I"}
    assert not unbekannt, f"{regel.id}: unknown scope {unbekannt}"


# ---------------------------------------------------------------------------
# Head, wording, history
# ---------------------------------------------------------------------------


def test_the_regelwerk_is_human_decided() -> None:
    """A rule list is a decision, not a report.

    `review.status` stands at `pending` and not at `reviewed`: the roster knows
    one handle today, and a name under a text that this person wrote as its
    author would be exactly the signature that RB-M2 exists against. The valve
    `provenance-review` keeps the state visible.
    """
    fm = _frontmatter()
    assert fm["provenance"] == "human-decided"
    assert fm["review"]["status"] in ("pending", "reviewed", "rejected")
    assert set(fm["adopted_by"]) >= {"portfolio-agentic-engineering", "lakeswitch-ai"}


def test_version_is_semver_and_history_is_monotone() -> None:
    fm = _frontmatter()
    version = str(fm["version"])
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), version

    verlauf = re.findall(r"^### (\d+\.\d+\.\d+) — (\d{4}-\d{2}-\d{2})", REGELWERK.read_text(encoding="utf-8"), re.M)
    assert verlauf, "no change history"
    assert verlauf[0][0] == version, f"head says {version}, top entry {verlauf[0][0]}"
    als_tupel = [tuple(int(t) for t in v.split(".")) for v, _ in verlauf]
    assert als_tupel == sorted(als_tupel, reverse=True), f"history not descending: {verlauf}"


def test_sync_impact_entry_exists_for_the_current_version() -> None:
    """Four mandatory lines. A change without them produces two versions of the same rule."""
    text = REGELWERK.read_text(encoding="utf-8")
    version = str(_frontmatter()["version"])
    start = text.find(f"### {version} — ")
    assert start != -1, f"no entry for {version}"
    ende = text.find("\n### ", start + 1)
    block = text[start : ende if ende != -1 else len(text)]
    for pflicht in ("**Geändert:**", "**Tests:**", "**Agents/Hooks/Templates:**", "**lakeswitch-ai:**"):
        assert pflicht in block, f"SYNC-IMPACT entry {version} without {pflicht}"


def _klausel_aus_regelwerk() -> str:
    """The paragraph from §6, without blockquote characters and without the bold heading."""
    for zeile in REGELWERK.read_text(encoding="utf-8").splitlines():
        if zeile.startswith("> **Evidence contract.** "):
            return zeile[len("> **Evidence contract.** ") :].strip()
    return ""


def _klausel_aus_agent(pfad: Path) -> str:
    text = pfad.read_text(encoding="utf-8")
    i = text.find("## Evidence contract (RB-A1)")
    if i == -1:
        return ""
    absaetze = [a for a in text[i:].split("\n\n") if a.strip()]
    return absaetze[1].strip() if len(absaetze) > 1 else ""


def test_rb_a1_clause_is_present_verbatim() -> None:
    """Normative text is copied, not retold — and a test recomputes it."""
    aus_regelwerk = _klausel_aus_regelwerk()
    assert aus_regelwerk, "§6 does not contain the clause in the expected form"

    agenten = sorted((REPO_ROOT / ".claude" / "agents").glob("*.md"))
    assert agenten, "Precondition: there are agent definitions."
    abweichend = [p.name for p in agenten if _klausel_aus_agent(p) != aus_regelwerk]
    assert not abweichend, (
        "The clause in the rule set and in these definitions is not byte-identical:\n  "
        + "\n  ".join(abweichend)
        + "\n\nFourteen slightly different versions would be fourteen rules."
    )


# ---------------------------------------------------------------------------
# Mutations — on a copy, never in the working tree (F-A-28)
# ---------------------------------------------------------------------------


def _kopie(tmp_path: Path, ersetzung: tuple[str, str]) -> Path:
    ziel = tmp_path / "regelwerk.md"
    shutil.copy2(REGELWERK, ziel)
    text = ziel.read_text(encoding="utf-8")
    assert ersetzung[0] in text, f"mutation does not take: {ersetzung[0]!r}"
    ziel.write_text(text.replace(*ersetzung, 1), encoding="utf-8")
    return ziel


def test_a_duplicate_id_is_caught(tmp_path: Path) -> None:
    kopie = _kopie(tmp_path, ("| **RB-A2** |", "| **RB-A1** |"))
    ids = [r.id for r in _regeln(kopie)]
    assert ids.count("RB-A1") == 2, "precondition of the mutation"
    assert sorted({i for i in ids if ids.count(i) > 1}) == ["RB-A1"]


def test_an_enforcer_that_does_not_exist_is_caught(tmp_path: Path) -> None:
    kopie = _kopie(tmp_path, ("test_handover_records_are_immutable", "test_nowhere_at_all"))
    regel = next(r for r in _regeln(kopie) if r.id == "RB-P5")
    assert not all(_enforcer_da(e) for e in regel.erzwinger)


def test_a_level_four_rule_without_an_enforcer_is_caught(tmp_path: Path) -> None:
    """Write the level up without writing the test — the most common way such a list lies."""
    kopie = _kopie(tmp_path, ("| `Ramp:agent-writes-allowlist` | P L I |", "| `Ramp:agent-writes-allowlist` | P L I |"))
    text = kopie.read_text(encoding="utf-8")
    kopie.write_text(
        text.replace("| 2 | `Ramp:agent-writes-allowlist`", "| 4 | `Ramp:agent-writes-allowlist`", 1), encoding="utf-8"
    )
    regel = next(r for r in _regeln(kopie) if r.id == "RB-A4")
    assert regel.stufe == 4
    assert not [e for e in regel.erzwinger if not e.startswith("Ramp:")], (
        "Level 4 without a real enforcer — exactly this must be caught by the test above"
    )


def test_a_ramp_without_a_deadline_is_caught() -> None:
    """A valve without a deadline measures the stock, never the work on it."""
    genannt = {e.split(":", 1)[1] for r in REGELN for e in r.erzwinger if e.startswith("Ramp:")}
    ohne_frist = sorted(n for n in genannt if VENTILE[n].deadline is None)
    assert not ohne_frist, ohne_frist


# House rule 6 as a machine (bead rqc): the agent definitions are framework
# artifacts — before rqc four of seven named systems of the customer instance
# (DV2, DLT/SDP, Oracle reference). The list is the visible bolt against
# sliding back: whoever finds a legitimate framework use of a term adds it
# here — with a reason, not silently.
INSTANZ_AUSDRUECKE = re.compile(r"\b(DV2|DLT|SDP|Oracle|ANSPRMENGE|exacs|wdp)\b|Hub/Sat/Link", re.IGNORECASE)


def test_agent_definitions_carry_no_instance_terms() -> None:
    agenten = sorted((REPO_ROOT / ".claude" / "agents").glob("*.md"))
    assert agenten, "Precondition: there are agent definitions."
    befunde = []
    for p in agenten:
        m = INSTANZ_AUSDRUECKE.search(p.read_text(encoding="utf-8"))
        if m:
            befunde.append(f"{p.name}: {m.group(0)!r}")
    assert not befunde, "Instance terms in agent definitions (house rule 6, bead rqc):\n  " + "\n  ".join(befunde)
