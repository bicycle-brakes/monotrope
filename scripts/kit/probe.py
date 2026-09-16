#!/usr/bin/env python3
"""Die Leerprobe: faehrt den Ablauf in einem Wegwerf-Repo und misst, was traegt.

**Wozu.** Die Behauptung "dieser Ablauf laesst sich uebergeben" ist wertlos,
solange sie ein Satz in einer Prosadatei ist. Dieses Kommando macht sie zu einem
Lauf: es kopiert in ein leeres Verzeichnis, was `manifest.yaml` als
`mechanismus` fuehrt, legt fuer jede `geruest`-Regel einen leeren Rumpf an,
faehrt `pytest` und vergleicht die roten Faelle gegen `REIST_NICHT`.

**Was es nicht tut.** Es schreibt nicht in den Arbeitsbaum, installiert nichts
und repariert keinen roten Fall. Ein Fall, der hier rot ist, ist meistens
zu Recht rot — eine Sperrklinke, die Scriptnamen DIESES Repos verlangt, muss
anderswo rot sein, sonst waere sie eine Sperrklinke ueber einer leeren Menge.

    python3 scripts/kit/probe.py            # fahren und vergleichen
    python3 scripts/kit/probe.py --list     # nur sagen, was kopiert wuerde
    python3 scripts/kit/probe.py --messen   # die roten Namen ausgeben, zum Nachtragen
"""

from __future__ import annotations

import argparse
import functools
import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = Path(__file__).resolve().parent / "manifest.yaml"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from _verdict import Verdict  # noqa: E402

# ---------------------------------------------------------------------------
# Was nicht mitreist — und warum
# ---------------------------------------------------------------------------
#
# Die Namen sind GEMESSEN (ein Lauf von `--messen`), die Gruende sind GESETZT.
# Ein Name ist eine Messung und gehoert der Maschine; ein Grund ist ein Urteil
# und gehoert einem Menschen.
#
# **Beide Richtungen blocken.** Ein roter Fall ohne Eintrag ist ein
# unerklaerter Fehler in einer Uebergabe. Ein Eintrag fuer einen gruenen Fall
# ist schlimmer: ein abgelaufener Grund liest sich wie eine lebende
# Entscheidung. Diese Sitzung hat genau das fuenfmal gefunden.
GRUENDE = (
    "bestand-dieses-repos",  # prueft eine Inventur, die es dort nicht gibt
    "braucht-die-vollstaendige-suite",  # prueft Dateien, die der Kit nicht traegt
    "braucht-ein-gate-das-hier-lebt",  # verlangt einen Erzwinger ausserhalb des Kits
    "geruest-ist-absichtlich-leer",  # liest eine geruest-Datei, die im Ziel ein leerer Rumpf ist
    "gilt-erst-mit-bestand",  # portabel, aber die geprüfte Menge entsteht erst im Ziel
)

# Der fuenfte Grund kam am 2026-09-08 dazu, aus demselben Anlass wie der vierte:
# das Vokabular hatte fuer eine wirkliche Ursache keinen Begriff. Vier Faelle im
# Uebergabe-Kanal standen auf "bestand-dieses-repos" ("prueft eine Inventur, die
# es dort nicht gibt"). Sie pruefen aber keine Inventur — sie sind vollstaendig
# portabel und brauchen nur, dass es ueberhaupt eine Uebergabe gibt. Ein
# frisches Repo hat keine, und das ist richtig so: die Pruefung SOLL dort nicht
# gruen sein, sie hat nur noch nichts zu pruefen.
#
# Der Unterschied zu "bestand-dieses-repos" ist der Zeitpunkt: dort wird eine
# Zahl dieses Repos behauptet und bleibt dort falsch; hier wird eine Menge
# vorausgesetzt, die im Ziel mit dem ersten eigenen Artefakt entsteht.

# Der vierte Grund kam am 2026-09-08 dazu, nachdem das Gegenlesen zeigte, dass
# zwei Eintraege sachlich falsch begruendet waren: sie standen auf
# "braucht-die-vollstaendige-suite" ("prueft Dateien, die der Kit nicht
# traegt"), obwohl der Kit `model-endpoints.yaml` sehr wohl traegt — als
# `geruest`, also als leeren Rumpf. Rot wurden sie, weil der Rumpf leer ist,
# nicht weil die Datei fehlt. Das geschlossene Vokabular hatte fuer die
# tatsaechliche Ursache keinen Begriff, also musste ein falscher gewaehlt
# werden. Ein Vokabular ohne den richtigen Begriff erzwingt eine falsche
# Aussage — und der Waechter unten prueft nur Mitgliedschaft, nie Richtigkeit.

# Gemessen am 2026-09-08 mit `--messen`; die Zuordnung folgt der Fehlermeldung
# je Fall: ein benannter Erzwinger, den es hier nicht gibt -> das dritte;
# eine fehlende Datei oder eine unerfuellte Vorbedingung -> das zweite;
# eine Behauptung ueber die Inventur dieses Repos -> das erste.
REIST_NICHT: dict[str, str] = {
    "tests.test_ci::test_der_echte_lesepfad_des_bead_gates_wird_erkannt": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_every_gate_step_has_a_mutation_test": "bestand-dieses-repos",
    "tests.test_ci::test_every_script_has_a_caller_or_a_declared_reason": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_every_script_has_a_test_or_a_declared_reason": "bestand-dieses-repos",
    "tests.test_ci::test_formatter_exclusion_survives_an_explicit_path": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_no_declared_reason_cites_a_closed_or_unknown_bead": "bestand-dieses-repos",
    "tests.test_ci::test_no_declared_reason_stands_for_a_script_that_has_a_caller": "bestand-dieses-repos",
    "tests.test_ci::test_no_declared_reason_stands_for_a_script_that_has_a_test": "bestand-dieses-repos",
    "tests.test_ci::test_runner_holds_no_command_list_of_its_own": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_runner_reports_what_it_cannot_run": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_the_archived_landing_page_is_not_wired_to_anything": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_the_glob_itself_finds_a_real_orphan_shell_script": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_the_makefile_runs_what_the_one_list_runs": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_the_runner_still_admits_what_it_cannot_do_at_all": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_every_handover_declares_a_direction": "gilt-erst-mit-bestand",
    "tests.test_feedback_channel::test_journal_index_lists_every_open_project_handover": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_root_index_routes_to_the_project_feedback": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_the_channel_is_not_empty": "gilt-erst-mit-bestand",
    "tests.test_feedback_channel::test_the_checks_go_red_when_the_contract_is_broken[record-der Record wurde nach der Uebergabe geaendert]": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_the_checks_go_red_when_the_contract_is_broken[status-liegt ausserhalb]": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_the_checks_go_red_when_the_contract_is_broken[target_ref-kein kurzer Commit-Hash]": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_the_feedback_loop_documents_the_reverse_direction": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_the_feedback_loop_points_at_the_schema_instead_of_repeating_it": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[GEMEINSAM-fehlende_gemeinsame]": "gilt-erst-mit-bestand",
    "tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[PROJEKT_PFLICHT-fehlende_kanalpflicht]": "gilt-erst-mit-bestand",
    "tests.test_feedback_channel::test_the_framework_does_not_claim_to_write_into_the_instance": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_the_route_check_goes_red_when_the_route_is_removed": "braucht-die-vollstaendige-suite",
    "tests.test_kit::test_the_kit_list_is_not_derivable_from_the_export_list": "braucht-die-vollstaendige-suite",
    "tests.test_kit::test_the_role_check_goes_red_when_a_rule_is_removed": "braucht-die-vollstaendige-suite",
    "tests.test_kit::test_the_two_manifests_really_disagree_somewhere": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_agents_are_found_at_all": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_model_in_the_routing_table_resolves": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01-explore.md-Haiku 4.5]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01a-interview.md-Fable 5.1]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02-spec.md-Fable 5.1]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02a-spec-review.md-Opus 5]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[03-plan.md-Fable 5.1]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[04-implement.md-Sonnet 5]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[06-review.md-Opus 5]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[07-commit.md-Haiku 4.5]": "geruest-ist-absichtlich-leer",
    "tests.test_model_endpoints::test_the_declaration_is_not_empty": "geruest-ist-absichtlich-leer",
    "tests.test_regelwerk::test_rb_a1_clause_is_present_verbatim": "braucht-die-vollstaendige-suite",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-A1]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-A2]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-A3]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-G2]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-G5]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-G6]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-G7]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-H1]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-H2]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-H3]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-H4]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-M1]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-M4]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-M7]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-M8]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-P1]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-P2]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-P3]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-P5]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-S1]": "braucht-ein-gate-das-hier-lebt",
}

# Obergrenze. Sie darf nur SINKEN. Wer einen Eintrag hinzufuegt, hebt sie
# sichtbar an — im Diff, mit Begruendung im Commit. Eine Portabilitaet, die man
# verlieren kann, ohne dass es auffaellt, ist keine.
#
# 53 -> 59 am 2026-09-08: RB-A6 prueft jetzt auch die sechs Modell-Nennungen in
# `prompts/`. Die Pruefung selbst reist mit (`prompts/` ist `mechanismus`); rot
# wird sie im Zielrepo nur, weil `model-endpoints.yaml` dort ein leerer Rumpf
# ist. Sechs Faelle mehr in der Liste sind der Preis dafuer, dass sechs bis
# dahin ungeprueft genannte Modelle jetzt gegen die Erklaerung aufloesen.
#
# 59 -> 60 am 2026-09-10: `prompts/01a-interview.md` kam dazu — die Phase, in der
# ein Mensch ausgefragt wird, bevor die Spec geschrieben ist. Ein Prompt mehr ist
# eine Modell-Nennung mehr, und die faellt im Zielrepo aus demselben Grund rot
# wie die sechs davor: `model-endpoints.yaml` ist dort ein leerer Rumpf. Der
# Eintrag traegt denselben Grund und ist kein neuer Ausnahmetyp.
#
# 60 -> 61 am 2026-09-10: `prompts/02a-spec-review.md` kam dazu — der Gegenleser,
# der die Spec liest, bevor gebaut wird. Gleiche Klasse, gleicher Grund.
#
# 61 -> 62 am 2026-09-14: `tests.test_ci::test_the_glob_itself_finds_a_real_orphan_shell_script`
# kam dazu — die Gegenprobe zum erweiterten Aufrufer-Zwang (Befund 11, Runde 2)
# legt ein echtes .sh-Script an und liest dafuer denselben lokalen Runner wie
# die beiden Aufrufer- und Test-Sperrklinken-Tests direkt darueber, den der Kit
# nicht mitreist (kein Eintrag in `manifest.yaml`, faellt unter die
# `scripts/`-Auffangregel `bestand`). Gleiche Klasse, gleicher Grund.
DECKEL = 62


# ---------------------------------------------------------------------------
# Das Manifest lesen
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def _manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def regeln() -> list[dict]:
    return _manifest()["rules"]


def geruest_ordner() -> list[str]:
    """Ordner, die im Zielrepo LEER existieren muessen, damit der Ablauf greift.

    Getrennt von den `geruest`-Regeln, weil eine Praefix-Regel `plans/changes/`
    jede Datei DARUNTER mit erfassen wuerde — und das sind die Artefakte dieses
    Repos, also Bestand. Der Ordner reist, sein Inhalt nicht.
    """
    return _manifest().get("geruest_ordner", [])


def _deckt(praefix: str, pfad: str) -> bool:
    """Segmentweise, nicht als Zeichenketten-Praefix.

    `startswith` haelt `docs/WORKFLOW.md.orig` fuer die Datei `docs/WORKFLOW.md`
    und `model-endpoints.yaml.bak` fuer `model-endpoints.yaml` — die Sicherung,
    die ein Mergetool liegen laesst, erbt damit die Rolle des Originals und
    reist als `mechanismus` mit oder wird als `geruest` angelegt. Dieselbe
    Korrektur steht mit derselben Begruendung in `tests/test_ci.py:_deckt`.

    Ein Ordner-Praefix endet auf "/" und deckt alles darunter; ein Datei-Praefix
    deckt genau sich selbst.
    """
    if praefix.endswith("/"):
        return pfad.startswith(praefix)
    return pfad == praefix


def rolle(pfad: str, regelmenge: list[dict] | None = None) -> tuple[str, str] | None:
    """Rolle und Regel-Praefix fuer einen Pfad — laengster passender Praefix gewinnt.

    Gibt `None` zurueck, wenn keine Regel passt. Das ist BLOCK, nicht
    "gehoert nicht dazu": ein Standard, der im Zweifel entscheidet, entscheidet
    genau ueber die Dateien, an die niemand gedacht hat.
    """
    treffer = [r for r in (regelmenge or regeln()) if _deckt(r["prefix"], pfad)]
    if not treffer:
        return None
    beste = max(treffer, key=lambda r: len(r["prefix"]))
    return beste["rolle"], beste["prefix"]


@functools.lru_cache(maxsize=1)
def _ls_files() -> tuple[tuple[str, ...], tuple[str, ...]]:
    # `-z` ist kein Detail: ohne ihn quotet git jeden Namen mit Sonderzeichen
    # ("docs/archive/… \342\200\224 …"), und der gequotete Name faellt unter
    # keine Praefix-Regel. Eine Datei waere unklassifiziert geblieben, weil ihr
    # Name ein Gedankenstrich enthaelt.
    # `--others --exclude-standard` ist kein Detail: ohne sie sieht die Probe
    # eine neu angelegte, noch nicht vorgemerkte Datei NICHT. Am 2026-09-08 lief
    # das Gate lokal gruen ueber einen Stand, den es nach dem Commit nicht mehr
    # gab — die CI war rot, und zwar zu Recht. Eine Pruefung, die den
    # Arbeitsbaum anders sieht als den Commit, prueft den falschen Baum. Das ist
    # dieselbe Fehlerklasse, gegen die dieses Modul gebaut ist: gruen, weil das
    # Kaputte nicht in der geprueften Menge liegt.
    # ABER: `--others` sieht auch, was der Commit gerade NICHT enthalten wird —
    # eine Notizdatei, ein Scratch-Skript. Die als BLOCK zu werten, macht das
    # Gate an einem Tag rot, an dem niemand etwas falsch gemacht hat, und
    # `scripts/_verdict.py` sagt, was mit solchen Gates passiert: sie werden
    # abgeschaltet. Deshalb zwei Mengen statt einer.
    def _lauf(*args: str) -> tuple[str, ...]:
        aus = subprocess.run(
            ["git", "ls-files", "-z", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return tuple(sorted({z for z in aus.stdout.split("\0") if z}))

    im_commit = _lauf("--cached")
    daneben = tuple(x for x in _lauf("--others", "--exclude-standard") if x not in set(im_commit))
    return im_commit, daneben


def getrackte_dateien() -> list[str]:
    """Was der Commit enthalten wird: der Index. Unklassifiziert = BLOCK."""
    return list(_ls_files()[0])


def unversionierte_dateien() -> list[str]:
    """Was daneben liegt. Unklassifiziert = DRIFT, benannt, aber nicht blockend."""
    return list(_ls_files()[1])


def nach_rolle() -> dict[str, list[str]]:
    """Jede getrackte Datei ihrer Rolle zugeordnet; `None` sammelt die Unklassifizierten."""
    rm = regeln()
    aus: dict[str, list[str]] = {"mechanismus": [], "bestand": [], "geruest": [], "(offen)": []}
    for pfad in getrackte_dateien():
        gefunden = rolle(pfad, rm)
        aus[gefunden[0] if gefunden else "(offen)"].append(pfad)
    return aus


# ---------------------------------------------------------------------------
# Die Probe
# ---------------------------------------------------------------------------


def _baue(ziel: Path) -> None:
    """Kopiert den Mechanismus und legt fuer jede geruest-Regel einen Rumpf an."""
    verteilt = nach_rolle()
    for pfad in verteilt["mechanismus"]:
        quelle = REPO_ROOT / pfad
        if not quelle.is_file():
            continue
        (ziel / pfad).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(quelle, ziel / pfad)
    # Geruest: existieren muss es, der Inhalt gehoert dem Zielrepo. Eine Kopie
    # von hier waere die Inventur dieses Repos unter fremdem Namen.
    for r in regeln():
        if r["rolle"] != "geruest":
            continue
        p = ziel / r["prefix"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("", encoding="utf-8")
    for ordner in geruest_ordner():
        (ziel / ordner).mkdir(parents=True, exist_ok=True)
        (ziel / ordner / ".gitkeep").write_text("", encoding="utf-8")
    subprocess.run(["git", "init", "--quiet"], cwd=ziel, check=True)
    subprocess.run(["git", "add", "-A"], cwd=ziel, check=True, capture_output=True)
    subprocess.run(
        ["git", "-c", "user.email=probe@invalid", "-c", "user.name=probe", "commit", "--quiet", "-m", "Leerprobe"],
        cwd=ziel,
        check=False,
        capture_output=True,
    )


def _faelle(ziel: Path) -> dict[str, bool]:
    """Jeder gesammelte Testfall auf gruen/rot. Sammelfehler zaehlen als rot."""
    bericht = ziel / "junit.xml"
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no", "-p", "no:cacheprovider", f"--junit-xml={bericht}"],
        cwd=ziel,
        capture_output=True,
        text=True,
    )
    if not bericht.is_file():
        return {}
    aus: dict[str, bool] = {}
    for fall in ET.parse(bericht).getroot().iter("testcase"):
        name = f"{fall.get('classname', '')}::{fall.get('name', '')}"
        gescheitert = any(k.tag in ("failure", "error") for k in fall)
        uebersprungen = any(k.tag == "skipped" for k in fall)
        if uebersprungen:
            continue
        aus[name] = not gescheitert
    return aus


def fahre() -> dict[str, bool]:
    ziel = Path(tempfile.mkdtemp(prefix="kit-probe-"))
    try:
        _baue(ziel)
        return _faelle(ziel)
    finally:
        shutil.rmtree(ziel, ignore_errors=True)


# ---------------------------------------------------------------------------
# Das Urteil
# ---------------------------------------------------------------------------


def pruefe(faelle: dict[str, bool] | None = None) -> Verdict:
    v = Verdict()
    verteilt = nach_rolle()

    if verteilt["(offen)"]:
        v.block(
            f"{len(verteilt['(offen)'])} getrackte Datei(en) fallen unter keine Regel",
            "\n".join(sorted(verteilt["(offen)"])[:20]),
        )

    offen_daneben = [p for p in unversionierte_dateien() if rolle(p) is None]
    if offen_daneben:
        v.drift(
            f"{len(offen_daneben)} unversionierte Datei(en) fallen unter keine Regel",
            "Sie gehen nicht in den Commit, also blockt das hier nicht. Wer eine davon "
            "vormerkt, sieht sie beim naechsten Lauf als BLOCK:\n" + "\n".join(sorted(offen_daneben)[:20]),
        )

    if not verteilt["mechanismus"]:
        v.block("keine einzige Datei traegt die Rolle 'mechanismus' — die Probe misst nichts (RB-G7)")
        return v

    for name, grund in sorted(REIST_NICHT.items()):
        if grund not in GRUENDE:
            v.block(
                f"{name}: Grund {grund!r} liegt ausserhalb der geschlossenen Menge", "erlaubt: " + " · ".join(GRUENDE)
            )

    if len(REIST_NICHT) > DECKEL:
        v.block(
            f"REIST_NICHT hat {len(REIST_NICHT)} Eintraege, der Deckel steht auf {DECKEL}",
            "Die Liste darf nur schrumpfen. Wer sie waechst, hebt den Deckel sichtbar an.",
        )

    faelle = fahre() if faelle is None else faelle
    if not faelle:
        v.block("die Probe hat keinen einzigen Testfall gesammelt — dann misst sie nichts (RB-G7)")
        return v

    rot = sorted(n for n, ok in faelle.items() if not ok)
    gruen = sorted(n for n, ok in faelle.items() if ok)

    unerklaert = [n for n in rot if n not in REIST_NICHT]
    if unerklaert:
        v.block(
            f"{len(unerklaert)} rote(r) Fall/Faelle ohne deklarierten Grund",
            "\n".join(unerklaert[:25])
            + ("\n  …" if len(unerklaert) > 25 else "")
            + "\n\nNachtragen mit: python3 scripts/kit/probe.py --messen",
        )

    # Die dritte Richtung, gefunden beim Gegenlesen am 2026-09-08: ein Eintrag,
    # dessen Fall gar nicht mehr GESAMMELT wird. Er ist weder rot noch gruen,
    # faellt also durch beide Pruefungen oben. So verliert man Portabilitaet,
    # ohne dass es auffaellt: wer die Kit-Rolle einer Testdatei von
    # `mechanismus` auf `bestand` zieht, nimmt ihre Faelle aus der Menge — die
    # Quote STEIGT dabei sogar, weil rote Faelle aus dem Nenner fallen.
    #
    # Ein umbenannter oder geloeschter Test loest das ebenfalls aus. Das ist
    # Absicht und kein Fehlalarm: ein Grund, dessen Fall es nicht mehr gibt,
    # ist genau so tot wie einer, dessen Fall gruen wurde.
    verwaist = [n for n in REIST_NICHT if n not in faelle]
    if verwaist:
        v.block(
            f"{len(verwaist)} Eintrag/Eintraege in REIST_NICHT haben keinen Fall mehr",
            "\n".join(sorted(verwaist)[:25])
            + ("\n  …" if len(verwaist) > 25 else "")
            + "\n\nEntweder wurde der Test umbenannt — dann den Eintrag nachziehen — oder "
            "seine Datei reist nicht mehr mit. Der zweite Fall ist der gefaehrliche: "
            "die Portabilitaet sinkt, und die gemeldete Quote steigt.",
        )

    abgelaufen = [n for n in gruen if n in REIST_NICHT]
    if abgelaufen:
        v.block(
            f"{len(abgelaufen)} Eintrag/Eintraege in REIST_NICHT sind gruen geworden",
            "\n".join(abgelaufen[:25])
            + "\n\nEin abgelaufener Grund liest sich wie eine lebende Entscheidung. Streichen.",
        )

    v.info(
        f"{len(gruen)} von {len(faelle)} Faellen tragen in ein fremdes Repo ({100 * len(gruen) // len(faelle)} %)",
        f"mechanismus {len(verteilt['mechanismus'])} · geruest {len(verteilt['geruest'])} "
        f"· bestand {len(verteilt['bestand'])} Datei(en)",
    )
    return v


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="nur ausgeben, was kopiert wuerde")
    p.add_argument("--messen", action="store_true", help="die roten Namen als Python-Dict ausgeben")
    p.add_argument("--strict", action="store_true", help="DRIFT blockt ebenfalls")
    args = p.parse_args()

    if args.list:
        verteilt = nach_rolle()
        for r in ("mechanismus", "geruest", "bestand", "(offen)"):
            print(f"{r:<14} {len(verteilt[r]):>4}")
            if r in ("mechanismus", "geruest", "(offen)"):
                for pfad in sorted(verteilt[r]):
                    print(f"    {pfad}")
        return 0

    if args.messen:
        faelle = fahre()
        rot = sorted(n for n, ok in faelle.items() if not ok)
        print(f"# {len(rot)} rot von {len(faelle)} — Gruende von Hand setzen")
        print("REIST_NICHT: dict[str, str] = {")
        for n in rot:
            print(f'    {json.dumps(n)}: "bestand-dieses-repos",')
        print("}")
        return 0

    v = pruefe()
    print(v.render())
    return v.exit_code(strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
