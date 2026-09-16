#!/usr/bin/env python3
"""
ramp_valves.py — die Liste der bewusst offenen Ventile.

Ein neuer Check, der am Tag seiner Einfuehrung den halben Bestand rot faerbt,
ist keine Pruefung, sondern eine Migration. Er wird gewaivt, und ein gewaivtes
Gate misst nichts. Deshalb duerfen Checks hier vorlaeufig tiefer melden, als sie
sollen — **aber nur mit einer Bedingung, unter der sie hochschalten**.

Genau da liegt die Gefahr. „Vorlaeufig nicht blockend" ist der haltbarste
Zustand der Softwareentwicklung: Niemand merkt, dass die Bedingung laengst
erfuellt ist, weil nichts danach fragt. Ein Ventil ohne Faelligkeits-Pruefung
ist kein Uebergang, sondern eine Ausnahme mit besserem Namen.

Diese Datei ist die Antwort darauf. Jedes Ventil nennt

  * **worauf** gewartet wird — in einem Satz, den ein Mensch versteht,
  * **woran man es misst** — als Praedikat, das ein Test ausfuehrt,
  * **was passiert, wenn es haelt** — der Zielzustand.

`tests/test_ramp_valves.py` faellt um, sobald ein Ventil faellig ist und noch
offen steht. Das Hochschalten haengt damit an einem Test und nicht am
Gedaechtnis.

Warum die Lint-Regeln hier stehen und nicht nur in `ruff.toml`: Die Auswahl dort
sagt, was heute geprueft wird. Sie sagt nicht, was als naechstes drankommt und
woran das haengt. Ohne diese Liste ist eine schmale Auswahl von einer
vergessenen nicht zu unterscheiden.

Usage:
    python3 scripts/ramp_valves.py            # Uebersicht: offen / faellig
    python3 scripts/ramp_valves.py --format=json

Exit-Codes: 0 = kein Ventil faellig, 1 = mindestens eines ist faellig.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _verdict import Level, Ramp  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
RUFF_CONFIG = REPO_ROOT / "ruff.toml"


# ---------------------------------------------------------------------------
# Messung
# ---------------------------------------------------------------------------


def selected_rule_groups() -> set[str]:
    """Die Regelgruppen, die `ruff.toml` heute aktiviert."""
    text = RUFF_CONFIG.read_text(encoding="utf-8")
    treffer = re.search(r"^select\s*=\s*\[(.*?)\]", text, re.MULTILINE | re.DOTALL)
    if not treffer:
        return set()
    return set(re.findall(r'"([^"]+)"', treffer.group(1)))


def findings_in_group(gruppe: str) -> int | None:
    """Wie viele Befunde eine Regelgruppe heute meldet. `None` = nicht messbar."""
    ergebnis = subprocess.run(
        ["ruff", "check", "--select", gruppe, "--statistics", "."],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if ergebnis.returncode not in (0, 1):
        return None
    summe = 0
    for zeile in ergebnis.stdout.splitlines():
        teile = zeile.split(maxsplit=1)
        if teile and teile[0].isdigit():
            summe += int(teile[0])
    return summe


# ---------------------------------------------------------------------------
# Die Ventile
# ---------------------------------------------------------------------------

# Regelgruppen, die noch nicht in `select` stehen, weil sie heute Bestand haben.
# Der Satz dahinter sagt, was die Gruppe ueberhaupt prueft — eine Liste aus
# Kuerzeln ist fuer niemanden lesbar, der ruff nicht auswendig kennt.
WARTENDE_LINT_GRUPPEN: dict[str, str] = {
    "E5": "zu lange Zeilen jenseits dessen, was der Formatter umbricht",
    "PL": "Pylint-Erbe: Verschachtelung, Argumentzahl, Vergleichsformen",
    "RUF": "ruff-eigene Regeln, u.a. zu Unicode-Homoglyphen in Zeichenketten",
}


def _lint_valve(gruppe: str, was: str) -> Ramp:
    def bestand_geraeumt() -> bool:
        anzahl = findings_in_group(gruppe)
        return anzahl == 0

    return Ramp(
        name=f"lint-{gruppe}",
        condition=(f"`ruff check --select {gruppe}` meldet nichts mehr — dann gehoert '{gruppe}' ({was}) in select"),
        predicate=bestand_geraeumt,
        target=Level.BLOCK,
        until_then=Level.INFO,
    )


def _roster_handles() -> set[str]:
    """Die verschiedenen Handles im Roster von provenance.yaml."""
    karte = REPO_ROOT / "provenance.yaml"
    if not karte.exists():
        return set()
    try:
        import yaml

        daten = yaml.safe_load(karte.read_text(encoding="utf-8")) or {}
    except Exception:
        return set()
    return {r["handle"] for r in (daten.get("roles") or {}).values() if r.get("handle")}


def provenance_review_valve() -> Ramp:
    """Eine Abnahme braucht einen Zweiten — solange es keinen gibt, ist sie DRIFT.

    `provenance.yaml` verlangt fuer `human-decided` und `ai-drafted-reviewed`
    eine Abnahme mit Namen und Datum. Dieses Repo hat heute einen einzigen
    Handle im Roster, und keiner der zuletzt gemergten Pull Requests traegt eine
    `reviewDecision` — es gibt also niemanden, dessen Zustimmung man eintragen
    koennte. Einen Namen trotzdem zu setzen, waere genau der Fehler, den das
    Feld verhindern soll (F-A-52: ein Name gegen einen Text, den die Person nie
    gelesen hat). Bis ein zweiter Handle existiert, ist "nie abgenommen"
    deshalb sichtbar und nicht blockend.
    """

    def zweiter_da() -> bool:
        return len(_roster_handles()) >= 2

    return Ramp(
        name="provenance-review",
        condition=(
            "provenance.yaml nennt mindestens zwei verschiedene Handles — dann kann "
            "ein Zweiter abnehmen, und `review.status: pending` ist keine Lage mehr, "
            "sondern ein Versaeumnis"
        ),
        predicate=zweiter_da,
        target=Level.BLOCK,
        until_then=Level.DRIFT,
    )


# ---------------------------------------------------------------------------
# Die Regel-Ventile
# ---------------------------------------------------------------------------
#
# `docs/governance/regelwerk.md` haelt 33 normative Regeln, jede mit einer
# Durchsetzungsstufe. Eine Regel auf Stufe 1 oder 2 ist eine Bitte — sie gilt,
# aber nichts faellt um, wenn jemand sie bricht. Genau dort sitzt die Gefahr,
# gegen die diese Datei geschrieben wurde: "vorlaeufig nur Konvention" ist der
# haltbarste Zustand der Softwareentwicklung.
#
# Deshalb traegt jede solche Regel ein Ventil, und das Ventil misst **nicht**
# den Bestand, sondern die Arbeit daran: sein Praedikat ist "der Erzwinger
# existiert". Schreibt jemand den benannten Test, wird das Ventil faellig, und
# `tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open` verlangt,
# dass die Regel im Regelwerk hochgestuft wird. Das Datum daneben ist die
# zweite Haelfte: eine Regel, an der niemand arbeitet, wird trotzdem faellig.


def _enforcer_exists(ref: str) -> bool:
    """Gibt es die benannte Testfunktion wirklich?

    Absichtlich per Textsuche und nicht per Import: ein Import fuehrt fremden
    Modul-Code aus, und dieses Script laeuft in jedem Lauf mit.
    """
    if "::" not in ref:
        return (REPO_ROOT / ref).exists()
    datei, funktion = ref.split("::", 1)
    pfad = REPO_ROOT / datei
    if not pfad.is_file():
        return False
    return re.search(rf"^def {re.escape(funktion)}\(", pfad.read_text(encoding="utf-8"), re.MULTILINE) is not None


# name -> (was fehlt, welcher Erzwinger es schliessen wuerde, Frist)
REGEL_VENTILE: dict[str, tuple[str, str, str]] = {
    "agent-writes-allowlist": (
        "RB-A4: ein schreibender Agent deklariert, wohin er schreiben darf",
        "tests/test_agents.py::test_agents_declare_writes_allowlist_when_they_can_write",
        "2026-11-30",
    ),
    "merge-freshness": (
        "RB-G7: geprueft wird der Merge-Ref, nicht der Branch-Kopf",
        "tests/test_ci.py::test_the_verification_runs_against_the_merge_ref",
        "2026-10-31",
    ),
    "signature-transcription": (
        "RB-M2: eine Signatur wird aus dem Pull Request transkribiert, nie gesetzt",
        "tests/test_validators.py::test_a_signature_is_transcribed_not_typed",
        "2026-11-30",
    ),
    "adversarial-record": (
        "RB-M3: ein abgenommener Contract setzt eine adversariale Quellverifikation voraus",
        "tests/test_validators.py::test_an_accepted_contract_names_a_verification_record",
        "2026-11-30",
    ),
    "boundary-before-close": (
        "RB-M5: alle Gates einer Liefereinheit schliessen vor der Liefereinheit",
        "tests/test_human_gates.py::test_a_unit_cannot_close_while_a_gate_is_open",
        "2026-11-30",
    ),
    "ruleset-assert": (
        "RB-M6: das Branch-Ruleset wird aus dem Repo heraus behauptet",
        "tests/test_repo_settings.py::test_the_ruleset_assertion_runs_in_ci",
        "2026-10-31",
    ),
    "commit-identity": (
        "RB-P4: echte Identitaet und Trailer auf Commits, die Entscheidungen beruehren",
        "tests/test_repo_settings.py::test_recent_commits_carry_a_real_identity_and_trailers",
        "2026-11-30",
    ),
    "closed-vocabulary": (
        "RB-A5: wo ein Agent entscheidet, steht ein geschlossenes Vokabular, kein Freitext",
        "tests/test_skill_outputs.py::test_no_decision_field_accepts_free_text",
        "2026-12-31",
    ),
    "procedures-in-skills": (
        "RB-S2: Prozeduren leben in Skills, nicht in Instruktionsdateien",
        "tests/test_entry_points.py::test_procedures_live_in_skills",
        "2026-12-31",
    ),
    "doc-type": (
        "RB-S3: eine Seite hat genau einen Diataxis-Typ",
        "tests/test_provenance.py::test_every_docs_page_declares_a_doc_type",
        "2026-12-31",
    ),
    "freshness-per-page": (
        "RB-S4: Frische je Seite, abgekuendigte Seite ist nur ein Zeiger",
        "tests/test_validators.py::test_deprecated_pages_are_pointers_only",
        "2026-12-31",
    ),
}


def _regel_ventil(name: str) -> Ramp:
    was, erzwinger, frist = REGEL_VENTILE[name]
    return Ramp(
        name=name,
        condition=(f"{was} — faellig, sobald `{erzwinger}` existiert (spaetestens {frist})"),
        predicate=lambda ref=erzwinger: _enforcer_exists(ref),
        target=Level.BLOCK,
        until_then=Level.INFO,
        deadline=date.fromisoformat(frist),
    )


def valves() -> list[Ramp]:
    """Alle offenen Ventile. Leer waere ein Befund, kein Erfolg."""
    aktiv = selected_rule_groups()
    lint = [_lint_valve(g, was) for g, was in WARTENDE_LINT_GRUPPEN.items() if g not in aktiv]
    regel = [_regel_ventil(n) for n in REGEL_VENTILE]
    return [*lint, provenance_review_valve(), *regel]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Zeigt die bewusst offenen Ventile und ob eines faellig ist.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    offen = valves()
    faellig = [v for v in offen if v.due]

    if args.format == "json":
        print(
            json.dumps(
                [{"name": v.name, "condition": v.condition, "due": v.due} for v in offen],
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1 if faellig else 0

    print(f"{len(offen)} offene(s) Ventil(e) · aktiv in ruff.toml: {', '.join(sorted(selected_rule_groups()))}\n")
    for v in offen:
        marke = "FAELLIG" if v.due else "offen  "
        print(f"  {marke}  {v.name}")
        print(f"           {v.condition}")
    if faellig:
        print(
            "\nMindestens ein Ventil ist faellig: Die Bedingung haelt, der Check steht "
            "aber noch auf der tieferen Stufe. Eine Regel, die nichts mehr kostet und "
            "trotzdem aus bleibt, ist ein verschenktes Gate."
        )
        return 1
    print("\nKein Ventil faellig — alle warten noch auf ihre Bedingung.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
