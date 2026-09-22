#!/usr/bin/env python3
"""ci_gates.py — die eine Gate-Liste und ihre Ableitungen (D-10/O-4, bead bo0).

**Es gibt genau eine Gate-Liste, und sie steht in `decisions/gates.yaml`.**
Dieses Modul ist ihr einziger Leser und leitet daraus alles ab:

  --list            menschenlesbare Uebersicht (auch nicht-lokale Gates)
  --format=json     maschinenlesbar
  --commands        nur die ausfuehrbaren Kommandos eines Jobs
  --report          Commit-SHAs + Konfigurations-Hash: der Lauf bindet sich
  --check-schema    prueft die Gate-Datei gegen ihr eigenes Schema
  --generate-ci     erzeugt `.github/workflows/ci.yml` aus der Liste
  --check-ci        schlaegt Alarm, wenn die committete ci.yml abweicht

`ci.yml` wird nie von Hand editiert: der Gate `ci-drift` haelt die committete
Datei an die Ableitung. Der Runner (`verify_all.sh`) haelt seinerseits keine
einzigen Kommandos — er fragt hier nach. Zwei gepflegte Listen driften, und
die Divergenz faellt erst auf, wenn jemand sich auf die falsche verlassen hat.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE_FILE = REPO_ROOT / "decisions" / "gates.yaml"
CI_FILE = REPO_ROOT / ".github" / "workflows" / "ci.yml"

# Geschlossenes Vokabular (bead bo0). Was hier fehlt, ist kein viertes Wort,
# sondern ein Schemafehler.
ENFORCEMENT: tuple[str, ...] = ("advisory", "report", "block")
JOBS: tuple[str, ...] = ("verify", "drift")

# Scripts ohne Aufrufer in der erzeugten ci.yml — mit dem Grund, warum das
# richtig ist (RB-G3). Jedes Script unter `scripts/` steht entweder als Gate-
# Schritt in ci.yml, wird vom Runner gefahren, oder steht hier mit Grund.
# Wer hier einen Eintrag streicht, braucht einen Schritt in der Gate-Datei;
# tests/test_ci.py haelt beide Seiten zusammen.
OHNE_AUFRUFER: dict[str, str] = {
    "_verdict.py": ("Bibliothek — das gemeinsame Exit-Vokabular der Scripts, kein eigenstaendiges Werkzeug"),
    "gate_record.py": (
        "Bibliothek — der Zustandsautomat des Gate-Records. Er wird von "
        "tests/test_gate_record.py gefahren; ein eigener CI-Schritt haette "
        "keinen Gegenstand, solange hier keine echten Records liegen"
    ),
    "handover_schema.py": (
        "Bibliothek — die eine Feldliste der Uebergaben. Sie wird von "
        "tests/test_feedback_channel.py importiert; ein eigener CI-Schritt "
        "prueft nichts, was der Test nicht schon prueft"
    ),
    "new_change.py": (
        "Einstieg, kein Gate — legt plans/changes/<name>/ an und wird von "
        "einem Menschen mit einer Vorgangs-ID gerufen; tests/test_workflow_entry.py "
        "faehrt es (Bead cke)"
    ),
    "check_worktree_state.sh": (
        "Vorbedingung — new_change.py ruft es vor dem Schreiben auf; ein "
        "eigenes Gate haette keinen Gegenstand, denn die CI faehrt ohnehin "
        "von einem sauberen Checkout aus"
    ),
    "verify_all.sh": (
        "Der lokale Lauf fuer Menschen — make verify ruft ihn. Die CI faehrt "
        "jedes Gate als eigenen Schritt; der Runner haelt selbst keine "
        "Kommandos, er fragt ci_gates.py"
    ),
}

# Scripts ohne Test — mit dem Grund. Die Sperrklinke darf schrumpfen, nie
# wachsen (tests/test_ci.py::test_the_test_exemption_list_only_shrinks).
# Leer seit cke (2026-09-22): der letzte Grund war der fehlende Waechter
# ("check_worktree_state.sh fehlt in diesem Checkout") — der Waechter reist
# jetzt mit, und tests/test_workflow_entry.py faehrt den Einstieg.
OHNE_TEST: dict[str, str] = {}

# Marketplace-Actions, deren Werkzeug es auch lokal gibt. Die Argumente werden
# NICHT hier gepflegt — sie stammen aus dem `with`-Block der Gate-Datei.
# Schriebe man die Globs hier nochmal hin, gaebe es zwei Listen von Globs.
LOKALE_ENTSPRECHUNG: dict[str, Any] = {
    "DavidAnson/markdownlint-cli2-action": lambda w: [
        "npx",
        "--yes",
        "markdownlint-cli2",
        *[g for g in str(w.get("globs", "")).split("\n") if g.strip()],
    ],
    # lychee bekommt bewusst keine: Es fragt fremde Server. Ein lokaler Lauf
    # sagt etwas ueber die Netzverbindung, nicht ueber diesen Pull Request.
}


def _lokales_kommando(action: str, with_block: dict[str, Any] | None) -> str | None:
    """Das lokale Aequivalent einer Marketplace-Action, aus ihrer eigenen Konfiguration."""
    bauer = LOKALE_ENTSPRECHUNG.get(action.split("@", 1)[0])
    if bauer is None:
        return None
    teile = bauer(with_block or {})
    return " ".join(f'"{t}"' if " " in t or "*" in t else t for t in teile)


def validate_schema(doc: dict[str, Any] | None = None) -> list[str]:
    """Prueft die Gate-Datei gegen ihr Schema. Liefert Fehler, leer = ok."""
    if doc is None:
        if not GATE_FILE.is_file():
            return [f"Gate-Datei fehlt: {GATE_FILE}"]
        doc = yaml.safe_load(GATE_FILE.read_text(encoding="utf-8"))
    fehler: list[str] = []
    if not isinstance(doc, dict):
        return ["die Gate-Datei ist kein Mapping"]
    if doc.get("schema_version") != 1:
        fehler.append(f"schema_version muss 1 sein, ist {doc.get('schema_version')!r}")
    gate_liste = doc.get("gates")
    if not isinstance(gate_liste, list) or not gate_liste:
        fehler.append("'gates' fehlt oder ist leer")
        return fehler
    bekannt: set[str] = set()
    for g in gate_liste:
        gid = g.get("id")
        if not gid:
            fehler.append("ein Gate ohne id")
            continue
        if gid in bekannt:
            fehler.append(f"doppelte id: {gid}")
        bekannt.add(gid)
        if not g.get("title"):
            fehler.append(f"{gid}: ohne title")
        if bool(g.get("command")) == bool(g.get("action")):
            fehler.append(f"{gid}: genau eins von command/action ist noetig")
        if g.get("job") not in JOBS:
            fehler.append(f"{gid}: job muss eins von {JOBS} sein, ist {g.get('job')!r}")
        if g.get("enforcement") not in ENFORCEMENT:
            fehler.append(f"{gid}: enforcement muss eins von {ENFORCEMENT} sein")
        if not isinstance(g.get("floor"), bool):
            fehler.append(f"{gid}: floor fehlt oder ist kein Boolean")
        if not g.get("reason"):
            fehler.append(f"{gid}: ohne reason — ein Gate ohne Warum wird nicht gepflegt")
        if g.get("action") and not isinstance(g.get("with"), dict | None):
            fehler.append(f"{gid}: 'with' muss ein Mapping sein")
    return fehler


def gates() -> list[dict[str, Any]]:
    """Alle Gates der einen Liste, in ihrer Reihenfolge."""
    fehler = validate_schema()
    if fehler:
        raise ValueError("Gate-Datei verletzt das Schema: " + "; ".join(fehler))
    doc = yaml.safe_load(GATE_FILE.read_text(encoding="utf-8"))
    out: list[dict[str, Any]] = []
    for g in doc["gates"]:
        aktion = g.get("action")
        kommando = g.get("command")
        ersatz = _lokales_kommando(aktion, g.get("with")) if aktion else None
        out.append(
            {
                "id": g["id"],
                "name": g["title"],
                "job": g["job"],
                "command": kommando if kommando else ersatz,
                "action": aktion,
                "with": g.get("with") or {},
                "enforcement": g["enforcement"],
                "floor": g["floor"],
                "reason": g.get("reason", ""),
                "local_runnable": kommando is not None or ersatz is not None,
                "via_local_equivalent": ersatz is not None,
            }
        )
    return out


def _git(*args: str) -> str | None:
    try:
        erg = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return erg.stdout.strip() or None


def report(job: str) -> dict[str, Any]:
    """Bindet den Lauf an einen Weltzustand: Commit, Basis, Gate-Konfiguration."""
    konfig = GATE_FILE.read_bytes()
    alle = gates()
    return {
        "job": job,
        "candidate": _git("rev-parse", "HEAD"),
        "base": _git("merge-base", "origin/main", "HEAD"),
        "config_sha256": hashlib.sha256(konfig).hexdigest(),
        "gates_total": len(alle),
        "gates_job": sum(1 for g in alle if g["job"] == job),
    }


def _schritt(g: dict[str, Any]) -> list[str]:
    """Ein YAML-Schritt fuer einen Gate — id, name, run/uses, with, enforcement.

    Jeder Gate-Schritt traegt `if: ${{ !cancelled() }}` (bead
    coding-harness-bl2): wird ein frueherer Gate rot, setzt dieser Schritt
    dadurch nicht stumm aus — die CI uebt jeden spaeteren Gate noch aus und
    faellt am Ende insgesamt. So sagen CI und der lokale Lauf dasselbe.
    checkout und setup-deps tragen das `if` bewusst nicht: ohne sie hat kein
    Gate einen Gegenstand.
    """
    zeilen = [
        f"      - name: {g['name']}",
        f"        id: {g['id']}",
        "        if: ${{ !cancelled() }}",
    ]
    if g["action"]:
        zeilen.append(f"        uses: {g['action']}")
    else:
        zeilen.append(f"        run: {g['command']}")
    with_block = g.get("with") or {}
    if with_block:
        zeilen.append("        with:")
        for schluessel, wert in with_block.items():
            teil_zeilen = str(wert).split("\n")
            if len(teil_zeilen) > 1:
                # Block-Literal: ein Wert wie `**/*.md` waere als YAML-Alias
                # invalid. Das Literal nimmt alles wortwoertlich.
                zeilen.append(f"          {schluessel}: |")
                for extra in teil_zeilen:
                    if extra.strip():
                        zeilen.append(f"            {extra}")
            else:
                zeilen.append(f"          {schluessel}: {teil_zeilen[0]}")
    if g["enforcement"] in ("advisory", "report"):
        zeilen.append("        continue-on-error: true")
    return zeilen


def generate_ci() -> str:
    """Die abgeleitete ci.yml — deterministisch, aus der einen Liste."""
    alle = gates()
    pruefe = [g for g in alle if g["job"] == "verify"]
    drift = [g for g in alle if g["job"] == "drift"]
    aktionen = [g for g in pruefe if g["action"]]
    kommandos = [g for g in pruefe if not g["action"]]
    zeilen: list[str] = [
        "name: verify",
        "",
        "# GENERATED by `python3 scripts/ci_gates.py --generate-ci` from decisions/gates.yaml (D-10).",
        "# Hand-edits fail the ci-drift gate on purpose.",
        "",
        "on:",
        "  push:",
        "  pull_request:",
        "  schedule:",
        '    - cron: "23 4 * * *"',
        "  workflow_dispatch:",
        "",
        "concurrency:",
        "  group: verify-${{ github.event_name }}-${{ github.ref }}",
        "  cancel-in-progress: false",
        "",
        "jobs:",
        "  verify:",
        "    if: github.event_name == 'push' || github.event_name == 'pull_request'",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
        "      - name: Install the pinned toolchain",
        "        id: setup-deps",
        "        run: python3 -m pip install pytest==8.3.4 PyYAML ruff==0.9.10",
    ]
    for g in aktionen:
        zeilen.extend(_schritt(g))
    for g in kommandos:
        zeilen.extend(_schritt(g))
    zeilen.extend(
        [
            "  drift:",
            "    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - name: Install the pinned toolchain",
            "        id: setup-deps",
            "        run: python3 -m pip install pytest==8.3.4 PyYAML ruff==0.9.10",
        ]
    )
    for g in drift:
        zeilen.extend(_schritt(g))
    return "\n".join(zeilen) + "\n"


def check_ci() -> int:
    """0 = die committete ci.yml ist genau die Ableitung; 1 = Handgriff gesehen."""
    if not CI_FILE.is_file():
        print(f"ci.yml fehlt: {CI_FILE}")
        print("neu erzeugen: python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml")
        return 1
    soll = generate_ci()
    ist = CI_FILE.read_text(encoding="utf-8")
    if ist == soll:
        print("ci.yml ist genau die Ableitung der Gate-Datei.")
        return 0
    print("ci.yml weicht von der Ableitung ab — Handgriff gesehen (D-10).")
    print("neu erzeugen: python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Liest die eine Gate-Liste und leitet alles daraus ab.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--list", action="store_true", help="menschenlesbare Uebersicht")
    ap.add_argument("--commands", action="store_true", help="nur die ausfuehrbaren Kommandos")
    ap.add_argument(
        "--tsv",
        action="store_true",
        help="zu --commands: id<TAB>enforcement<TAB>kommando — fuer den Runner",
    )
    ap.add_argument("--job", choices=JOBS, default="verify")
    ap.add_argument(
        "--skip-equivalents",
        action="store_true",
        help="Action-Aequivalente auslassen (die CI faehrt die Actions selbst)",
    )
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--report", action="store_true", help="Commit-SHAs und Konfigurations-Hash")
    ap.add_argument("--check-schema", action="store_true", help="Gate-Datei gegen ihr Schema pruefen")
    ap.add_argument("--generate-ci", action="store_true", help="ci.yml auf stdout erzeugen")
    ap.add_argument("--check-ci", action="store_true", help="committete ci.yml gegen die Ableitung pruefen")
    args = ap.parse_args()

    try:
        alle = gates()
    except (FileNotFoundError, ValueError, yaml.YAMLError) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2

    if args.check_schema:
        fehler = validate_schema()
        if fehler:
            print("Gate-Datei verletzt das Schema:")
            for f in fehler:
                print(f"  - {f}")
            return 1
        print(f"Gate-Datei ok: {len(alle)} Gates, Schema 1.")
        return 0

    if args.check_ci:
        return check_ci()

    if args.generate_ci:
        sys.stdout.write(generate_ci())
        return 0

    if args.report:
        print(json.dumps(report(args.job), indent=2))
        return 0

    if args.format == "json":
        print(json.dumps(alle, indent=2, ensure_ascii=False))
        return 0

    if args.commands:
        for g in alle:
            if g["job"] != args.job or not g["local_runnable"]:
                continue
            if args.skip_equivalents and g["via_local_equivalent"]:
                continue
            if args.tsv:
                print(f"{g['id']}\t{g['enforcement']}\t{g['command']}")
            else:
                print(g["command"])
        return 0

    lokal = [g for g in alle if g["local_runnable"]]
    print(f"{len(alle)} Gates in {GATE_FILE.relative_to(REPO_ROOT)} — {len(lokal)} lokal ausfuehrbar\n")
    for g in alle:
        marke = "~" if g["via_local_equivalent"] else (" " if g["local_runnable"] else "*")
        takt = " ⏱" if g["job"] == "drift" else ""
        print(f"{marke}{takt} [{g['id']}] {g['name']}")
        if g["local_runnable"]:
            zusatz = "  (lokales Aequivalent der Action)" if g["via_local_equivalent"] else ""
            print(f"      {g['command']}{zusatz}")
        else:
            print(f"      (Marketplace-Action: {g['action']}) — laeuft nur in der CI")
    print("\n~ = lokal ueber ein Ersatzwerkzeug · * = gar nicht lokal · ⏱ = Drift-Job (Timer).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
