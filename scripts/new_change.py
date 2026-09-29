#!/usr/bin/env python3
"""Der Aufruf, der eine Aenderung anlegt — AK-1 aus spec.md.

`docs/WORKFLOW.md` beschreibt sieben Phasen, aber bis heute gab es keinen
Befehl, der Phase 1 einrichtet: `plans/changes/<name>/` mit einem gueltigen
Artefakt, verknuepft mit einem Vorgang im Tracker. Wer eine Aenderung begann,
tippte den Ordner und das Frontmatter von Hand — und verpasste dabei leicht
ein Pflichtfeld, das `plans_registry.py --check` erst beim naechsten Lauf
gefunden haette.

Dieses Script schliesst die Luecke, ohne eine zweite zu oeffnen:

  - Es **importiert** `plans_registry` und liest dessen `REQUIRED`,
    `_bead_statuses`, `_bead_export_path`, `render_index` und `check` zur
    Laufzeit — nie beim Import kopiert, damit ein Test, der `reg.REPO`,
    `reg.PLANS` und `reg.INDEX` per `monkeypatch` umlenkt, auch dieses Script
    umlenkt (dasselbe Muster wie die Fixture `plans` in
    `tests/test_plans_registry.py`).
  - Es **verlangt** einen vorhandenen Bead, statt einen anzulegen: `bd` zu
    rufen hiesse schreiben (AGENTS.md), die CI hat kein `bd`
    (`requirements-ci.txt` nennt es nicht), und ein Artefakt mit erfundenem
    Bead wuerde vom Gate `dangling-beads` sofort geblockt — das Script erzeugte,
    was das naechste Gate verwirft. Verlangen und pruefen ist die einzige
    Form, die in jeder Umgebung dasselbe tut.
  - Es **laesst nichts stehen, was das naechste Gate verwirft**: einmal vor
    und einmal nach dem Schreiben laeuft `plans_registry.check()`, und nur ein
    BLOCK, den es **dazugebracht** hat, macht das Script rueckgaengig. Die
    Basislinie ist keine Feinheit: ohne sie loeste jeder fremde BLOCK unter
    `plans/` die Ruecknahme aus und die Meldung schob ihn dem gerade
    erzeugten, einwandfreien Artefakt zu — der Einstieg waere unbenutzbar,
    solange irgendwo sonst etwas blockt.

Usage:
    python3 scripts/new_change.py <name> --bead <id> [--owner <rolle>] [--dry-run]
Exit-Codes (ueber `_verdict.Verdict`): 0 = angelegt (INFO), 2 = BLOCK.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plans_registry as reg  # noqa: E402
from _verdict import Level, Verdict  # noqa: E402

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Kuerzere Tokens melden fast jeden Namen als "verwandt" zu fast jedem anderen.
MIN_TOKEN_LEN = 4

# Die Archivform ist `YYYY-MM-DD-<name>` (plans/_README.md). Exakt, nicht als
# Suffix-Glob `*-<name>`: der traf jeden archivierten Ordner, dessen Basename
# zufaellig auf `-<name>` endet — `isolation` kollidierte mit
# `2026-09-05-workflow-einstieg-und-isolation`, und der Aufruf brach mit einer
# Kollision ab, die es nicht gab.
ARCHIV_PRAEFIX = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-"

# Diese Ueberschriften-Zeile markiert das Erzeugte als Skelett, nicht als
# Ergebnis von Phase 1 — die Gliederung aus `prompts/01-explore.md` wird
# absichtlich NICHT hier abgeschrieben (AK-2 gilt auch fuer diesen Rumpf: kein
# zweiter Ort, der beschreibt, was Phase 1 tut).
BODY_TEMPLATE = """# {titel} — Research

Phase 1 nach [`prompts/01-explore.md`](../../../prompts/01-explore.md); diese
Datei ist leer, bis sie gelaufen ist.

> **Herkunft nachziehen.** Das Frontmatter sagt `provenance: human-written` —
> das gilt für diesen Rumpf. Wer ihn mit einem Sprachmodell füllt, setzt
> `ai-drafted-reviewed` und ergänzt `produced_by:` und `review:`
> (`provenance.yaml`, Klasse `ai-drafted-reviewed`, `review_required: true`).
"""

# Echte Umlaute in BODY_TEMPLATE, obwohl die Kommentare dieser Datei
# transliteriert sind: die Vorlage ist kein Python-Kommentar, sie **ist** der
# Inhalt einer Markdown-Datei. `AGENTS.md` verlangt dort Diakritika, und ein
# Aufruf, der ASCII-Ersatz erzeugt, saet den Verstoss bei jedem Gebrauch neu.


def _frontmatter_template(name: str, bead: str, owner: str, heute: str) -> str:
    """Frontmatter mit jedem Feld aus `plans_registry.REQUIRED` gefuellt.

    Reihenfolge und Zusatzfelder folgen `plans/_README.md` — `supersedes` und
    `superseded_by` sind die einzigen zwei Felder, die `null` sein duerfen.

    `provenance: human-written` und **kein** `produced_by`-Block: geschrieben
    hat diese Datei ein deterministischer Aufruf, den ein Mensch abgesetzt hat.
    Frueher stand hier `ai-drafted-reviewed` mit
    `produced_by: {kind: llm-session, name: unbekannt}` — eine Herkunft, die
    zum Zeitpunkt des Schreibens niemand hatte, und die das Provenienz-Gate
    nicht widerlegen kann, weil `plans/` genau die zwei Klassen
    `human-written` und `ai-drafted-reviewed` zulaesst. Wer den Rumpf mit
    einem Sprachmodell fuellt, zieht beides nach; der erzeugte Text sagt das.
    """
    return f"""---
title: "Research — {name}"
status: draft
implementation_status: none
date: {heute}
last_reviewed: {heute}
updated: {heute}
supersedes: null
superseded_by: null
bead: {bead}
owner: {owner}
provenance: human-written
tags: [research]
---

"""


def _known_field_values(bead: str, heute: str) -> dict[str, str]:
    """Was dieses Script fuer jedes Pflichtfeld aus `REQUIRED` einsetzen kann.

    Waechst `plans_registry.REQUIRED` um ein Feld, fuer das es hier keinen
    Wert gibt, blockt Schritt 4 — statt ein Artefakt zu schreiben, das
    `--check` gleich darauf verwirft.
    """
    return {
        "status": "draft",
        "implementation_status": "none",
        "date": heute,
        "last_reviewed": heute,
        "bead": bead,
    }


def _related_candidates(name: str, plans_root: Path) -> list[str]:
    """Grobe Vorschau der Regel aus AGENTS.md: erst suchen, dann anlegen.

    Kein Abbruch — ob es dasselbe Thema ist, entscheidet der Mensch. Ein
    Token unter vier Zeichen wird ignoriert, sonst meldet fast jeder Name
    "verwandt" zu fast jedem anderen. Die Schwelle steht als Konstante, damit
    Text und Code sie nicht getrennt tragen.
    """
    tokens = [t for t in name.split("-") if len(t) >= MIN_TOKEN_LEN]
    if not tokens:
        return []
    muster = [re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE) for t in tokens]
    treffer: set[str] = set()
    for teilbaum in ("specs", "changes"):
        wurzel = plans_root / teilbaum
        if not wurzel.exists():
            continue
        for pfad in sorted(wurzel.rglob("*.md")):
            text = pfad.name.lower() + "\n" + pfad.read_text(encoding="utf-8", errors="ignore")
            if any(m.search(text) for m in muster):
                treffer.add(str(pfad.relative_to(plans_root)))
    return sorted(treffer)


WAECHTER = Path(__file__).resolve().parent / "check_worktree_state.sh"


def _worktree_is_sane() -> str | None:
    """Steht der Baum, in dem gleich geschrieben wird, auf einem Zweig?

    **Warum hier.** `make change` schreibt einen Ordner und rendert den Index.
    Geschieht das an einem losgeloesten HEAD, haengt beides an einem Commit, den
    kein Zweig haelt — sichtbar wird das erst, wenn jemand den Ordner sucht. Am
    Hauptcheckout dieses Repos hingen zeitweise fuenf Arbeitsbaeume in genau
    diesem Zustand.

    Geprueft wird mit `-`: der Zweig darf jeder sein, aber es muss einer sein.
    Ein laufender Rebase haelt ebenfalls an. Die Pruefung ist **eine** — das
    Shell-Script ist die Implementierung, hier steht kein zweites Regelwerk.

    Rueckgabe: die Fehlermeldung, oder None wenn der Baum benutzbar ist.
    """
    if not WAECHTER.is_file():
        return f"{WAECHTER.name} fehlt — die Vorbedingung ist nicht pruefbar"
    lauf = subprocess.run(
        ["bash", str(WAECHTER), str(reg.REPO), "-"],
        capture_output=True,
        text=True,
    )
    if lauf.returncode != 0:
        return (lauf.stderr or lauf.stdout).strip() or "Waechter meldet einen unbenutzbaren Arbeitsbaum"
    return None


def _abort(verdict: Verdict, message: str, detail: str = "") -> int:
    verdict.block(message, detail)
    print(verdict.render())
    return verdict.exit_code()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="Ordnername unter plans/changes/, z.B. mein-thema")
    parser.add_argument("--bead", required=True, help="vorhandene Vorgangs-ID aus dem Tracker (tools/bd ready)")
    parser.add_argument("--owner", default="Data Architect", help="Rolle aus provenance.yaml (Default: Data Architect)")
    parser.add_argument("--dry-run", action="store_true", help="nur anzeigen, nichts schreiben")
    args = parser.parse_args(argv)

    verdict = Verdict()

    # Schritt 1 · Name
    if not NAME_PATTERN.match(args.name):
        return _abort(
            verdict,
            f"Name '{args.name}' passt nicht auf {NAME_PATTERN.pattern}",
            "Erlaubt: Kleinbuchstaben, Ziffern, Bindestrich als Trenner — kein fuehrender/abschliessender Bindestrich.",
        )

    # Schritt 2 · Bead
    export_path = reg._bead_export_path()
    bead_statuses = reg._bead_statuses(export_path)
    if bead_statuses is None:
        return _abort(
            verdict,
            f"Bead-Export {export_path} fehlt oder ist leer",
            "Ohne Export ist nicht pruefbar, ob der Vorgang existiert. Beheben: `bd export` bzw. den Export-Hook laufen lassen.",
        )
    status = bead_statuses.get(args.bead)
    if status is None:
        return _abort(
            verdict,
            f"Bead '{args.bead}' steht nicht im Export {export_path}",
            "Der Vorgang muss zuerst angelegt und exportiert werden — dieses Script legt keinen an.",
        )
    if status == "closed":
        return _abort(
            verdict,
            f"Bead '{args.bead}' ist im Export 'closed'",
            "Ein neuer Ordner an einem geschlossenen Vorgang waere sofort DRIFT "
            "(Bead geschlossen, Artefakt nicht 'done' und archiviert).",
        )

    # Schritt 2a · Arbeitsbaum
    fehler = _worktree_is_sane()
    if fehler is not None:
        return _abort(
            verdict,
            "Arbeitsbaum ist nicht in einem Zustand, in dem geschrieben wird",
            fehler,
        )

    # Schritt 3 · Mehrfacherzeugung
    ziel = reg.PLANS / "changes" / args.name
    if ziel.exists():
        return _abort(verdict, f"{ziel.relative_to(reg.REPO)} existiert schon")
    archiv = reg.PLANS / "changes" / "archive"
    if archiv.exists() and any(archiv.glob(f"{ARCHIV_PRAEFIX}{args.name}")):
        return _abort(verdict, f"plans/changes/archive/ traegt schon einen Ordner fuer '{args.name}'")

    verwandt = _related_candidates(args.name, reg.PLANS)
    for pfad in verwandt:
        verdict.info(
            f"moeglicherweise verwandt: plans/{pfad}",
            "Vor dem Anlegen erst pruefen, ob es dasselbe Thema ist (AGENTS.md).",
        )

    # Schritt 4 · REQUIRED vollstaendig?
    heute = dt.date.today().isoformat()
    bekannt = _known_field_values(args.bead, heute)
    unbekannt = [f for f in reg.REQUIRED if f not in bekannt]
    if unbekannt:
        return _abort(
            verdict,
            f"Pflichtfeld(er) {unbekannt} — das Script kennt keinen Wert dafuer",
            "plans_registry.REQUIRED ist gewachsen, ohne dass dieses Script mitgezogen wurde.",
        )

    frontmatter = _frontmatter_template(args.name, args.bead, args.owner, heute)
    titel = args.name.replace("-", " ")
    inhalt = frontmatter + BODY_TEMPLATE.format(titel=titel)
    research_path = ziel / "research.md"

    if args.dry_run:
        verdict.info(f"[--dry-run] wuerde anlegen: {research_path.relative_to(reg.REPO)}")
        verdict.info(f"[--dry-run] Bead: {args.bead} (Status im Export: {status})")
        verdict.info("[--dry-run] Verweis: prompts/01-explore.md")
        print(verdict.render())
        print("\n--- Vorschau research.md ---\n")
        print(inhalt)
        return verdict.exit_code()

    # Schritt 5 · Basislinie, dann schreiben
    #
    # Die Basislinie ist der Unterschied zwischen "dieser Aufruf hat etwas
    # kaputtgemacht" und "hier war schon etwas kaputt". Ohne sie loeste jeder
    # fremde BLOCK unter plans/ die Ruecknahme aus, und die Meldung schob ihn
    # dem gerade erzeugten, einwandfreien Artefakt zu: der dokumentierte
    # Einstieg waere unbenutzbar, solange irgendein anderes Artefakt blockt —
    # und zwar mit einer Fehlermeldung, die auf die falsche Datei zeigt.
    vorher = {f.message for f in reg.check().at(Level.BLOCK)}

    alter_index = reg.INDEX.read_text(encoding="utf-8") if reg.INDEX.exists() else None
    ziel.mkdir(parents=True)
    research_path.write_text(inhalt, encoding="utf-8")

    # Schritt 6 · Index neu rendern, dann pruefen, was *dazugekommen* ist.
    reg.INDEX.write_text(reg.render_index(), encoding="utf-8")
    nachher = reg.check().at(Level.BLOCK)
    neue_block_befunde = [f for f in nachher if f.message not in vorher]
    if neue_block_befunde:
        shutil.rmtree(ziel)
        if alter_index is None:
            reg.INDEX.unlink(missing_ok=True)
        else:
            reg.INDEX.write_text(alter_index, encoding="utf-8")
        verdict.block(
            "Das erzeugte Artefakt wurde vom Registry-Check verworfen — nichts bleibt stehen.",
            "\n".join(f.message for f in neue_block_befunde),
        )
        print(verdict.render())
        return verdict.exit_code()

    # Vorbestehende BLOCK-Befunde, die **immer noch** stehen. Sie sind nicht die
    # Schuld dieses Aufrufs und halten ihn nicht auf — verschweigen wuerde aber
    # heissen, dass der naechste `make verify` ueberrascht. Gemeldet wird der
    # Schnitt aus vorher und nachher, nicht `vorher` allein: der fehlende Index
    # blockt vor dem Schreiben und ist danach behoben, und "vorbestehender
    # BLOCK: plans/INDEX.md fehlt" waere dann eine Meldung ueber einen Zustand,
    # den dieser Aufruf gerade beseitigt hat.
    for message in sorted(vorher & {f.message for f in nachher}):
        verdict.info(
            f"vorbestehender BLOCK, nicht von diesem Aufruf: {message}",
            "Er stand schon vorher im Baum und blockt `make verify`, bis ihn jemand behebt.",
        )

    # Schritt 7 · Ausgabe
    verdict.info(f"angelegt: {ziel.relative_to(reg.REPO)}")
    verdict.info(f"Bead: {args.bead} (Status im Export: {status})")
    verdict.info("naechster Schritt: prompts/01-explore.md")
    print(verdict.render())
    return verdict.exit_code()


if __name__ == "__main__":
    sys.exit(main())
