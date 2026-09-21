"""Das Regelwerk haelt, was es behauptet.

Eine Regelliste ist die Sorte Dokument, die am leisesten verrottet. Sie wird
einmal geschrieben, alle sind einverstanden, und danach wandern die Tests, auf
die sie zeigt: einer wird umbenannt, einer zieht in eine andere Datei, einer
wird geloescht, weil er "nichts mehr faengt". Die Regel bleibt stehen und liest
sich unveraendert streng — nur haelt sie niemand mehr.

Deshalb prueft diese Datei nicht die Regeln (das tun die genannten Erzwinger),
sondern die **Zuordnung**: dass jede Regel auf Stufe 3 oder hoeher einen
Erzwinger nennt, den es gibt, und dass jede darunter ein Ventil mit Datum
traegt. Eine Regel ohne beides ist eine Bitte, die sich als Regel ausgibt.
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
    """Liest die Regeltabellen. Eine Zeile, die nicht passt, wird nicht stumm verworfen."""
    gefunden: list[Regel] = []
    for zeile in quelle.read_text(encoding="utf-8").splitlines():
        m = ZEILE_RE.match(zeile)
        if not m:
            continue
        # Auf unescapten Pipes trennen — RB-H1 nennt `\|\| true` in seinem Text.
        spalten = [s.strip() for s in re.split(r"(?<!\\)\|", m.group(2))]
        # Regel · Stufe · Erzwinger · Gilt in · (leerer Rest hinter dem Schluss-Pipe)
        assert len(spalten) >= 4, f"{m.group(1)}: {len(spalten)} Spalten, erwartet 4"
        text, stufe_roh, erzwinger_roh, gilt_in = spalten[0], spalten[1], spalten[2], spalten[3]
        assert stufe_roh.isdigit(), f"{m.group(1)}: Stufe {stufe_roh!r} ist keine Zahl"
        # Refs sind mit `·` getrennt; `::foo` erbt die Datei der vorigen Referenz.
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
    assert text.startswith("---\n"), "kein Frontmatter"
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
# Die Liste selbst
# ---------------------------------------------------------------------------


def test_the_list_is_not_empty() -> None:
    """Gruen ueber null Regeln waere die Bestaetigung, dass nichts gilt (RB-G7)."""
    assert len(REGELN) >= 30, f"nur {len(REGELN)} Regeln geparst — das Muster passt nicht mehr"


def test_no_two_rules_share_an_id() -> None:
    ids = [r.id for r in REGELN]
    doppelt = sorted({i for i in ids if ids.count(i) > 1})
    assert not doppelt, f"doppelt vergeben: {doppelt}"


def test_every_family_is_numbered_without_a_gap() -> None:
    """Eine Luecke ist entweder eine geloeschte Regel oder ein Tippfehler — beides gehoert benannt."""
    nach_familie: dict[str, list[int]] = {}
    for r in REGELN:
        nach_familie.setdefault(r.id[3], []).append(int(r.id[4:]))
    for familie, nummern in nach_familie.items():
        assert sorted(nummern) == list(range(1, len(nummern) + 1)), f"Familie {familie}: {sorted(nummern)}"


def test_every_rule_id_referenced_anywhere_exists() -> None:
    """Ein Verweis auf eine Regel, die es nicht gibt, ist eine Regel, die niemand liest."""
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
    assert verweise, "Vorbedingung: irgendwo wird ueberhaupt eine Regel zitiert."
    assert not unbekannt, "Verweis auf eine Regel, die das Regelwerk nicht kennt:\n  " + "\n  ".join(unbekannt)


# ---------------------------------------------------------------------------
# Stufe und Erzwinger — der eigentliche Vertrag
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("regel", REGELN, ids=lambda r: r.id)
def test_rules_at_level_three_or_higher_name_an_existing_enforcer(regel: Regel) -> None:
    """Ab Stufe 3 behauptet die Regel, dass eine Maschine sie haelt. Dann muss es die geben."""
    if regel.stufe < 3:
        return
    echte = [e for e in regel.erzwinger if not e.startswith("Ramp:")]
    assert echte, f"{regel.id} steht auf Stufe {regel.stufe} und nennt nur Ventile"
    fehlend = [e for e in echte if not _enforcer_da(e)]
    assert not fehlend, (
        f"{regel.id} nennt einen Erzwinger, den es nicht gibt: {fehlend}\n"
        "Entweder der Test wurde umbenannt — dann hier nachziehen — oder die Regel "
        "steht in Wahrheit auf Stufe 2 und braucht ein Ventil."
    )


@pytest.mark.parametrize("regel", REGELN, ids=lambda r: r.id)
def test_rules_without_an_enforcer_are_at_most_level_two_and_carry_a_dated_ramp(regel: Regel) -> None:
    """Eine Regel, die niemand haelt, sagt das — und sagt, bis wann.

    Ohne Ventil ist "vorlaeufig nur Konvention" der Dauerzustand: niemand merkt,
    dass die Bedingung laengst haelt, weil nichts danach fragt.
    """
    if regel.stufe >= 3:
        return
    ventile = [e.split(":", 1)[1] for e in regel.erzwinger if e.startswith("Ramp:")]
    assert ventile, f"{regel.id} steht auf Stufe {regel.stufe} und nennt kein Ventil"
    for name in ventile:
        assert name in VENTILE, f"{regel.id}: Ventil {name!r} steht nicht in ramp_valves.valves()"
        assert VENTILE[name].deadline is not None, (
            f"{regel.id}: Ventil {name!r} hat keine Frist. Ein Praedikat allein misst den "
            "Bestand, nie die Arbeit daran."
        )


def test_every_named_ramp_exists_and_no_valve_is_orphaned() -> None:
    """Beide Richtungen. Ein Ventil ohne Regel bewacht nichts."""
    genannt = {e.split(":", 1)[1] for r in REGELN for e in r.erzwinger if e.startswith("Ramp:")}
    fehlend = sorted(genannt - set(VENTILE))
    assert not fehlend, f"im Regelwerk genannt, in ramp_valves.py nicht vorhanden: {fehlend}"

    # Lint-Ventile und das Provenienz-Ventil gehoeren keiner Regel — sie sind
    # aelter als diese Seite und stehen ausdruecklich hier als Ausnahme.
    ohne_regel = sorted(
        n for n in VENTILE if n not in genannt and not n.startswith("lint-") and n != "provenance-review"
    )
    assert not ohne_regel, f"Ventil ohne Regel: {ohne_regel}"


def test_no_rule_stands_on_level_one() -> None:
    """Stufe 1 heisst: sie steht geschrieben und sonst nichts. Dann gehoert sie nicht hierher."""
    schwach = [r.id for r in REGELN if r.stufe < 2]
    assert not schwach, f"reine Konvention im Regelwerk: {schwach}"


@pytest.mark.parametrize("regel", REGELN, ids=lambda r: r.id)
def test_every_rule_says_where_it_applies(regel: Regel) -> None:
    assert regel.gilt_in.strip(), f"{regel.id} sagt nicht, wo sie gilt"
    unbekannt = set(regel.gilt_in.split()) - {"P", "L", "I"}
    assert not unbekannt, f"{regel.id}: unbekannter Geltungsbereich {unbekannt}"


# ---------------------------------------------------------------------------
# Kopf, Wortlaut, Verlauf
# ---------------------------------------------------------------------------


def test_the_regelwerk_is_human_decided() -> None:
    """Eine Regelliste ist eine Entscheidung, kein Bericht.

    `review.status` steht auf `pending` und nicht auf `reviewed`: der Roster
    kennt heute einen Handle, und ein Name unter einem Text, den diese Person
    als Autorin geschrieben hat, waere genau die Signatur, gegen die RB-M2
    existiert. Das Ventil `provenance-review` haelt den Zustand sichtbar.
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
    assert verlauf, "kein Aenderungsverlauf"
    assert verlauf[0][0] == version, f"Kopf sagt {version}, oberster Eintrag {verlauf[0][0]}"
    als_tupel = [tuple(int(t) for t in v.split(".")) for v, _ in verlauf]
    assert als_tupel == sorted(als_tupel, reverse=True), f"Verlauf nicht absteigend: {verlauf}"


def test_sync_impact_entry_exists_for_the_current_version() -> None:
    """Vier Pflichtzeilen. Eine Aenderung ohne sie erzeugt zwei Fassungen derselben Regel."""
    text = REGELWERK.read_text(encoding="utf-8")
    version = str(_frontmatter()["version"])
    start = text.find(f"### {version} — ")
    assert start != -1, f"kein Eintrag fuer {version}"
    ende = text.find("\n### ", start + 1)
    block = text[start : ende if ende != -1 else len(text)]
    for pflicht in ("**Geändert:**", "**Tests:**", "**Agents/Hooks/Templates:**", "**lakeswitch-ai:**"):
        assert pflicht in block, f"SYNC-IMPACT-Eintrag {version} ohne {pflicht}"


def _klausel_aus_regelwerk() -> str:
    """Der Absatz aus §6, ohne Blockquote-Zeichen und ohne die fette Ueberschrift."""
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
    """Normativer Text wird kopiert, nicht nacherzaehlt — und ein Test rechnet nach."""
    aus_regelwerk = _klausel_aus_regelwerk()
    assert aus_regelwerk, "§6 enthaelt die Klausel nicht in der erwarteten Form"

    agenten = sorted((REPO_ROOT / ".claude" / "agents").glob("*.md"))
    assert agenten, "Vorbedingung: es gibt Agent-Definitionen."
    abweichend = [p.name for p in agenten if _klausel_aus_agent(p) != aus_regelwerk]
    assert not abweichend, (
        "Die Klausel im Regelwerk und in diesen Definitionen ist nicht byte-gleich:\n  "
        + "\n  ".join(abweichend)
        + "\n\nVierzehn leicht verschiedene Fassungen waeren vierzehn Regeln."
    )


# ---------------------------------------------------------------------------
# Mutationen — auf einer Kopie, nie im Arbeitsbaum (F-A-28)
# ---------------------------------------------------------------------------


def _kopie(tmp_path: Path, ersetzung: tuple[str, str]) -> Path:
    ziel = tmp_path / "regelwerk.md"
    shutil.copy2(REGELWERK, ziel)
    text = ziel.read_text(encoding="utf-8")
    assert ersetzung[0] in text, f"Mutation greift nicht: {ersetzung[0]!r}"
    ziel.write_text(text.replace(*ersetzung, 1), encoding="utf-8")
    return ziel


def test_a_duplicate_id_is_caught(tmp_path: Path) -> None:
    kopie = _kopie(tmp_path, ("| **RB-A2** |", "| **RB-A1** |"))
    ids = [r.id for r in _regeln(kopie)]
    assert ids.count("RB-A1") == 2, "Vorbedingung der Mutation"
    assert sorted({i for i in ids if ids.count(i) > 1}) == ["RB-A1"]


def test_an_enforcer_that_does_not_exist_is_caught(tmp_path: Path) -> None:
    kopie = _kopie(tmp_path, ("test_handover_records_are_immutable", "test_nowhere_at_all"))
    regel = next(r for r in _regeln(kopie) if r.id == "RB-P5")
    assert not all(_enforcer_da(e) for e in regel.erzwinger)


def test_a_level_four_rule_without_an_enforcer_is_caught(tmp_path: Path) -> None:
    """Stufe hochschreiben, ohne den Test zu schreiben — der haeufigste Weg, wie so eine Liste luegt."""
    kopie = _kopie(tmp_path, ("| `Ramp:agent-writes-allowlist` | P L I |", "| `Ramp:agent-writes-allowlist` | P L I |"))
    text = kopie.read_text(encoding="utf-8")
    kopie.write_text(
        text.replace("| 2 | `Ramp:agent-writes-allowlist`", "| 4 | `Ramp:agent-writes-allowlist`", 1), encoding="utf-8"
    )
    regel = next(r for r in _regeln(kopie) if r.id == "RB-A4")
    assert regel.stufe == 4
    assert not [e for e in regel.erzwinger if not e.startswith("Ramp:")], (
        "Stufe 4 ohne echten Erzwinger — genau das muss der Test oben fangen"
    )


def test_a_ramp_without_a_deadline_is_caught() -> None:
    """Ein Ventil ohne Frist misst den Bestand, nie die Arbeit daran."""
    genannt = {e.split(":", 1)[1] for r in REGELN for e in r.erzwinger if e.startswith("Ramp:")}
    ohne_frist = sorted(n for n in genannt if VENTILE[n].deadline is None)
    assert not ohne_frist, ohne_frist
