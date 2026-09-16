#!/usr/bin/env python3
"""
ci_gates.py — extrahiert die Verifikationsliste aus der CI-Definition.

**Es gibt genau eine Gate-Liste, und sie steht in `.github/workflows/ci.yml`.**
Der lokale Runner haelt keine zweite; er fragt hier nach. Der Grund ist nicht
Bequemlichkeit, sondern eine gemessene Erfahrung: Zwei gepflegte Listen driften,
und die Divergenz faellt erst auf, wenn jemand sich auf die falsche verlassen
hat.

> „Divergenz wird nicht erkannt — sie ist unmoeglich, weil es nichts gibt, wovon
> abzuweichen waere."

Nicht jeder Schritt ist lokal ausfuehrbar: Schritte, die eine Marketplace-Action
benutzen (Markdown-Lint, externer Link-Check), haben kein Kommando. Sie werden
mitgefuehrt und als `local_runnable: false` ausgewiesen — **weggelassen wuerden
sie unsichtbar**, und eine Liste, die verschweigt, was sie nicht abdeckt, liest
sich wie Vollstaendigkeit.

Usage:
    python3 scripts/ci_gates.py --list            # menschenlesbar
    python3 scripts/ci_gates.py --format=json     # maschinenlesbar
    python3 scripts/ci_gates.py --commands        # nur die ausfuehrbaren Kommandos

Exit-Codes: 0 = gelesen, 2 = CI-Definition fehlt oder ist unlesbar.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CI_FILE = REPO_ROOT / ".github" / "workflows" / "ci.yml"
# Zwei Jobs, eine Liste. `verify` haengt am Pull Request, `drift` am Timer —
# der Unterschied ist die Beweglichkeit der Gegenseite (ADR-028 R2), nicht die
# Wichtigkeit. Ein Drift-Schritt, der hier fehlte, waere unsichtbar wie die neun
# Scripts, die bis zum 2026-08-14 gar keinen Aufrufer hatten.
JOBS = ("verify", "drift")

# Scripts ohne Aufrufer — mit dem Grund, warum das richtig ist.
#
# Die Regel dahinter: jedes Script hat einen Aufrufer **oder** einen Grund
# (RB-G3). Ohne diese Liste ist ein absichtlich ungenutztes Werkzeug von einem
# vergessenen nicht zu unterscheiden — und am 2026-08-14 waren neun von
# einundzwanzig ohne Aufrufer, ohne dass irgendwo stand, welche davon Absicht war.
#
# Wer hier einen Eintrag streicht, muss einen Schritt in `ci.yml` anlegen;
# `tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason` haelt
# beide Seiten zusammen.
OHNE_AUFRUFER: dict[str, str] = {
    "_verdict.py": "Bibliothek — das gemeinsame Exit-Vokabular, kein eigenstaendiges Werkzeug",
    "leakcheck.py": (
        "Vorbedingung einer lokalen Sitzung, kein CI-Schritt. Die Denylist liegt "
        "ausserhalb des Repositories — sie benennt, wonach gesucht wird, und das ist "
        "selbst eine Aussage ueber den Kunden. In der CI gibt es sie folglich nicht, "
        "und das Script blockte dort bei jedem Lauf. Ein Gate, das immer rot ist, "
        "wird abgeschaltet und schuetzt danach nichts. Aufrufer ist "
        "`make leakcheck NAME=<change>` vor jeder Sitzung an einem Fremdendpunkt; "
        "geprueft wird es von `tests/test_leakcheck.py` gegen ein gesaetes Geheimnis"
    ),
    "bd_neu.py": (
        "Interaktives Kommando — es legt einen Vorgang an und schreibt damit in die "
        "eingebettete Dolt-Datenbank, die dieses Repo nicht traegt. Ein CI-Schritt "
        "haette nichts anzulegen und wuerde den Tracker in einem Lauf veraendern, den "
        "niemand angefordert hat. Aufrufer ist `make bead`; die Prefix-Ableitung "
        "selbst prueft `tests/test_bd_neu.py` gegen erfundene Bestaende"
    ),
    "gate_record.py": (
        "Bibliothek — der Zustandsautomat des Gate-Records. Er wird von "
        "`tests/test_gate_record.py` und `tests/test_validators.py` gefahren; ein "
        "eigener CI-Schritt haette keinen Gegenstand, solange in diesem Repo keine "
        "echten Records liegen (sie entstehen in der Instanz)"
    ),
    "handover_schema.py": (
        "Bibliothek — die eine Feldliste der Uebergaben. Sie wird von "
        "`tests/test_feedback_channel.py` importiert und von `templates/handover.md` "
        "gezeigt; ein eigener CI-Schritt haette nichts zu pruefen, was der Test nicht "
        "schon prueft"
    ),
    "query_status.py": "interaktive Abfrage fuer Menschen, kein Gate",
    "export_mermaid_assets.py": (
        "braucht `mermaid-cli` (Chromium) und je Lauf eine Eingabedatei mit Zielverzeichnis; "
        "ein `--check` ueber alle Assets existiert nicht. Bis dahin manuell (`wp-p3.7.1`)"
    ),
    "sync_learnings.py": "braucht `--project-path` auf die Projekt-Instanz — die in der CI nicht ausgecheckt ist",
    "sync_skills_registry.py": "dito: liest die Skills der Instanz read-only",
    "sync_contract_models.py": "dito: vergleicht die vendorierten Contract-Modelle mit der Instanz",
    "validate_skill_outputs.py": "dito: prueft die Skill-Outputs im `analysis-output/` der Instanz",
    "render_beads_export.py": (
        "noch kein Gate, mit Absicht. Es rendert `.beads/issues.jsonl` aus dem Dolt-Store und "
        "wird erst scharfgeschaltet, wenn die 33 Vorgaenge, die es heute nur im Git gibt, im "
        "Store stehen — bis dahin blockt es selbst. `tests/test_render_beads_export.py` faehrt "
        "jede Regel gegen ein Fixture"
    ),
    "rebuild_bead_store.py": (
        "einmalige Reparatur, kein Gate. Es fuehrt den reviewten Export auf `master` mit einem "
        "Schnappschuss des lokalen Dolt-Stores zusammen und erzeugt die Eingabe fuer den Neubau "
        "der Vorgangsdatenbank — beide Eingaben entstehen ausserhalb des Repos und altern. "
        "`tests/test_rebuild_bead_store.py` faehrt jede Regel gegen ein Fixture"
    ),
    "osi_beads_koerbe.py": (
        "Belegskript einer datierten Uebergabe. Es braucht drei eingefrorene Exporte "
        "aus dem Tracker der Instanz, die nicht im Repo liegen und dort auch nicht "
        "hingehoeren — ein Tracker-Stand altert, die Uebergabe ist auf ihren Stichtag "
        "datiert. `tests/test_osi_beads_koerbe.py` faehrt jede Regel gegen ein Fixture"
    ),
    "new_change.py": (
        "Einstieg, kein Gate — legt `plans/changes/<name>/` an und ruft "
        "`plans_registry.check()` selbst; `tests/test_workflow_entry.py` faehrt "
        "jede Regel gegen ein Fixture"
    ),
    "cc-claude.sh": (
        "Sitzungsprofil, von einem Menschen gestartet — startet eine eigene "
        "Claude-Code-Sitzung und kann deshalb nicht als CI-Schritt laufen. "
        "Anthropic-Profil fuer Stufe 1 und die Eskalationsroute in Stufe 2. "
        "Aufrufer ist ein Mensch; die Startlogik prueft "
        "`tests/test_model_profiles.py` per Unterprozess"
    ),
    "cc-sonnet.sh": "dito (`cc-claude.sh`): Anthropic-Profil, auf Sonnet gepinnt (Stufe-2-Eskalation)",
    "cc-glm.sh": "dito (`cc-claude.sh`): GLM-5.3-Profil fuer substanzielle Phase-4-Teilschritte (Stufe 2, vorbereitet, nicht aktiv)",
    "cc-glm-flash.sh": "dito (`cc-claude.sh`): GLM-5.3-Flash-Profil fuer Routine-Teilschritte (Stufe 2, vorbereitet, nicht aktiv)",
    "cc-kimi.sh": "dito (`cc-claude.sh`): Kimi-K2.7-Profil fuer Review-Folgerunden (Stufe 2, vorbereitet, nicht aktiv)",
    "cc-kimi-k3.sh": "dito (`cc-claude.sh`): Kimi-K3-Profil fuer die erste Review-Runde (Stufe 2, vorbereitet, nicht aktiv)",
    "_cc-common.sh": (
        "Bibliothek — gemeinsame Basis der `scripts/cc-*.sh`-Profile, per "
        "`source` eingebunden, kein eigenstaendiges Werkzeug; geprueft von "
        "`tests/test_model_profiles.py`"
    ),
    "check_worktree_state.sh": (
        "Vorbedingung vor jeder Agentensitzung in einem Arbeitsbaum und vor "
        "`make change` — kein CI-Schritt, weil die CI keinen Arbeitsbaum im "
        "hiesigen Sinn hat. Aufrufer sind `scripts/new_change.py` und "
        "`scripts/run_change.sh`; geprueft von `tests/test_worktree_state.py`"
    ),
    "run_change.sh": (
        "Orchestriert die Phasen 4-6 einer Aenderung unter Stufe-2-Routing, von "
        "einem Menschen gestartet — kein CI-Schritt, weil Stufe 2 vorbereitet, "
        "aber nicht aktiv ist (`docs/WORKFLOW.md` Abschnitt 4). Geprueft von "
        "`tests/test_orchestrator.py`"
    ),
}

# `sync_learnings.py`, `sync_skills_registry.py`, `sync_contract_models.py` und
# `validate_skill_outputs.py` teilen einen Grund: sie brauchen ein Lesetoken auf
# ein fremdes Repo. Das ist eine Entscheidung ueber Zugriff, keine ueber Technik
# — und sie ist bis heute nicht getroffen. Bis zum 2026-09-08 stand hier, sie
# sei "ein offener Punkt in V-05"; V-05 hat aber einen anderen Gegenstand (den
# `drift`-Job und den Aufrufer-Test, beides gebaut) und nennt kein Lesetoken.
#
# Die vier stehen hier namentlich und nicht als "die letzten vier": als die
# Liste wuchs, meinte diese Formulierung ploetzlich vier andere Eintraege, und
# ein Leser haette `new_change.py` dem falschen Grund zugeordnet.


# Scripts ohne Test — mit dem Grund und dem besitzenden Vorgang.
#
# Die dritte Sperrklinke neben `OHNE_AUFRUFER` (hier) und `OHNE_MUTATIONSTEST`
# (in `tests/test_ci.py`). Sie beantwortet die Frage, die die beiden anderen
# nicht stellen: *laeuft dieses Script in irgendeinem Test?* Ein Werkzeug ohne
# Aufrufer ist sichtbar untaetig; ein Werkzeug ohne Test ist unsichtbar kaputt.
#
# Gemessen am 2026-09-08 waren es sechs. Zwei davon — `query_status.py` und
# `sync_learnings.py` — haben seitdem eigene Testdateien; `build_sales_deck.py`
# wurde geloescht (D1, entschieden 2026-09-08). Die Liste steht damit bei drei
# und darf nur fallen (`test_the_test_exemption_list_only_shrinks`).
#
# Der Maszstab ist Ausfuehrung, nicht Erwaehnung: belegt ist ein Script, wenn
# eine Datei unter `tests/` sein Modul importiert oder `scripts/<name>` als
# Unterprozess startet. Der naive Maszstab ("der Name kommt in einer Testdatei
# vor") lieferte zwei statt sechs, weil zwei der Scripts ausschliesslich in
# *Kommentaren* vorkamen.
OHNE_TEST: dict[str, str] = {
    "export_mermaid_assets.py": (
        "`slugify` und `extract_blocks` waeren testbar, `render_batch` braucht "
        "`mermaid-cli` (Chromium) — hier laeuft weder `node` noch `npx`. "
        "Vorgang `wp-p3.7.1`"
    ),
    "validate_contract.py": (
        "laeuft als Gate (drei Aufrufe) und hat trotzdem keinen Test — F-A-29. "
        "Gehoert Vorgang `wp-p1-verbesserung.10`, hier nur deklariert, nicht behoben"
    ),
    "validate_paradigm_catalog.py": ("dito, ein Aufruf. Gehoert Vorgang `wp-p1-verbesserung.10`"),
}

# Marketplace-Actions, deren Werkzeug es auch lokal gibt.
#
# Warum das hier steht und nicht im Runner: Der Runner haelt keine Kommandos.
# Und warum die Argumente NICHT mitgeschrieben werden: Sie werden aus der
# Action-Konfiguration in `ci.yml` abgeleitet. Schriebe man die Globs hier
# nochmal hin, gaebe es zwei Listen von Globs — genau die Drift, gegen die
# dieses Modul gebaut ist.
#
# Der Anlass: Der Markdown-Lint galt als "nur in der CI", weil er als Action
# eingebunden ist. Sein Werkzeug laeuft aber lokal. Zwei CI-Durchlaeufe sind an
# einem Befund gescheitert, den ein lokaler Lauf in vier Sekunden gezeigt haette.
LOKALE_ENTSPRECHUNG = {
    "DavidAnson/markdownlint-cli2-action": lambda w: [
        "npx",
        "--yes",
        "markdownlint-cli2",
        *[g for g in str(w.get("globs", "")).split("\n") if g.strip()],
    ],
    # lychee bekommt bewusst keine: Es fragt fremde Server. Ein lokaler Lauf
    # sagt etwas ueber die Netzverbindung, nicht ueber diesen Pull Request.
}


def _lokales_kommando(step: dict[str, Any]) -> str | None:
    """Das lokale Aequivalent einer Marketplace-Action, aus ihrer eigenen Konfiguration."""
    uses = str(step.get("uses") or "")
    bauer = LOKALE_ENTSPRECHUNG.get(uses.split("@", 1)[0])
    if bauer is None:
        return None
    teile = bauer(step.get("with") or {})
    return " ".join(f'"{t}"' if " " in t or "*" in t else t for t in teile)


def gates() -> list[dict[str, Any]]:
    """Alle Schritte der CI-Definition, in ihrer Reihenfolge."""
    if not CI_FILE.is_file():
        raise FileNotFoundError(f"CI-Definition fehlt: {CI_FILE}")
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    schritte: list[tuple[str, dict[str, Any]]] = []
    for job in JOBS:
        try:
            for step in doc["jobs"][job]["steps"]:
                schritte.append((job, step))
        except (KeyError, TypeError) as exc:
            raise ValueError(f"Job '{job}' nicht gefunden in {CI_FILE.name}") from exc

    out: list[dict[str, Any]] = []
    for job, step in schritte:
        # Schritte ohne Namen sind Infrastruktur (checkout, setup-python) und
        # kein Gate. Sie tragen bewusst keinen — so muss man sie nicht ausnehmen.
        if "name" not in step:
            continue
        cmd = step.get("run")
        ersatz = None if isinstance(cmd, str) else _lokales_kommando(step)
        out.append(
            {
                "id": step.get("id"),
                "job": job,
                "name": step["name"],
                "command": cmd.strip() if isinstance(cmd, str) else ersatz,
                "action": step.get("uses"),
                "local_runnable": isinstance(cmd, str) or ersatz is not None,
                # Ein Schritt, der lokal nur ueber ein Ersatzwerkzeug laeuft, ist
                # nicht dasselbe wie einer, der es direkt tut. Der Unterschied
                # gehoert ausgewiesen, nicht eingeebnet.
                "via_local_equivalent": ersatz is not None,
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Liest die eine Gate-Liste aus .github/workflows/ci.yml.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--list", action="store_true", help="menschenlesbare Uebersicht")
    ap.add_argument("--commands", action="store_true", help="nur die ausfuehrbaren Kommandos")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--drift", action="store_true", help="auch die zeitgesteuerten Schritte")
    args = ap.parse_args()

    try:
        alle = gates()
    except (FileNotFoundError, ValueError, yaml.YAMLError) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(alle, indent=2, ensure_ascii=False))
        return 0

    if args.commands:
        for g in alle:
            if g["local_runnable"] and (args.drift or g["job"] == "verify"):
                print(g["command"])
        return 0

    lokal = [g for g in alle if g["local_runnable"]]
    print(f"{len(alle)} Gates in {CI_FILE.relative_to(REPO_ROOT)} — {len(lokal)} lokal ausfuehrbar\n")
    for g in alle:
        marke = "~" if g.get("via_local_equivalent") else (" " if g["local_runnable"] else "*")
        # Der Timer-Schritt ist als solcher gekennzeichnet: er laeuft nicht an
        # diesem Pull Request, und wer das nicht sieht, wartet vergeblich auf ihn.
        takt = " ⏱" if g["job"] == "drift" else ""
        print(f"{marke}{takt} [{g['id'] or '—'}] {g['name']}")
        if g["local_runnable"]:
            zusatz = "  (lokales Aequivalent der Action)" if g.get("via_local_equivalent") else ""
            print(f"      {g['command']}{zusatz}")
        else:
            print(f"      (Marketplace-Action: {g['action']}) — laeuft nur in der CI")
    print("\n~ = lokal ueber ein Ersatzwerkzeug · * = gar nicht lokal · ⏱ = laeuft am Timer, nicht am Pull Request.")
    print("`scripts/verify_all.sh` faehrt den Rest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
