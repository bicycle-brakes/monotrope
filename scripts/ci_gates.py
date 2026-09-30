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

# Wo ein Gate misst — geschlossen seit bead 1jg.2. both = lokaler Laeufer und
# gehostete CI; writer = nur an einer Schreibmaschine (die abgeleitete ci.yml
# haelt ihn deklariert raus); hosted = nur in der gehosteten CI (der lokale
# Laeufer laesst ihn deklariert aus). Eine deklarierte Auslassung ist eine
# Aussage, kein Schweigen. SCHEMA_VERSION gehoert zur Gate-Datei: ein
# Schemawechsel ist sichtbar, kein stiller.
PLACEMENT: tuple[str, ...] = ("hosted", "writer", "both")
SCHEMA_VERSION = 2

# Scripts ohne Aufrufer in der erzeugten ci.yml — mit dem Grund, warum das
# richtig ist (RB-G3). Jedes Script unter `scripts/` steht entweder als Gate-
# Schritt in ci.yml, wird vom Runner gefahren, oder steht hier mit Grund.
# Wer hier einen Eintrag streicht, braucht einen Schritt in der Gate-Datei;
# tests/test_ci.py haelt beide Seiten zusammen.
OHNE_AUFRUFER: dict[str, str] = {
    "_verdict.py": ("Bibliothek — das gemeinsame Exit-Vokabular der Scripts, kein eigenstaendiges Werkzeug"),
    "bead_render.py": (
        "Bibliothek — der EINE Zugriffspunkt des Tracker-Stands (bead 1jg.3); "
        "die Leser importieren ihn, ein eigener CI-Schritt haette keinen Gegenstand"
    ),
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
    "harness.py": (
        "Entry point, not a gate — a person, or an agent on the maintainer's word, records an ADR "
        "answer with it; tests/test_harness_decide_adr.py runs it"
    ),
    "merge_guard.py": (
        "Library — the one list of ask rules that stop an agent before it merges; "
        "tests/test_merge_guard.py compares .claude/settings.json against it, which "
        "is all a CI step could do"
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
    "omnigent_policy.py": (
        "Library and maintainer tool - the one list of denied Omnigent tools and everything rendered "
        "from it. tests/test_omnigent_deny_layers.py runs it (the render, the merge, and under "
        "Omnigent's own Python the offline policy tests); tools/omnigent/install.sh calls it on the "
        "maintainer's machine, which no CI step can do"
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
    if doc.get("schema_version") != SCHEMA_VERSION:
        fehler.append(f"schema_version muss {SCHEMA_VERSION} sein, ist {doc.get('schema_version')!r}")
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
        if g.get("placement") not in PLACEMENT:
            fehler.append(f"{gid}: placement muss eins von {PLACEMENT} sein, ist {g.get('placement')!r} (bead 1jg.2)")
        elif (
            g.get("action")
            and _lokales_kommando(g["action"], g.get("with") if isinstance(g.get("with"), dict) else None) is None
            and g.get("placement") != "hosted"
        ):
            # Eine Action ohne lokale Entsprechung misst nur in der gehosteten
            # CI. Stuende sie auf both, liesse der lokale Laeufer sie trotzdem
            # aus — still, ueber local_runnable statt ueber die Deklaration.
            fehler.append(f"{gid}: Action ohne lokale Entsprechung misst nur gehostet — placement muss hosted sein")
        if "needs_tracker" in g and not isinstance(g.get("needs_tracker"), bool):
            fehler.append(f"{gid}: needs_tracker muss ein Boolean sein")
        if "needs_history" in g and not isinstance(g.get("needs_history"), bool):
            fehler.append(f"{gid}: needs_history muss ein Boolean sein")
        if g.get("needs_tracker") and bool(g.get("action")):
            # Seit bead 1jg.3 liest auch der drift-Job den Tracker (plans-registry-strict):
            # ohne committete Kopie braucht jeder Job mit einem Tracker-Leser die Hydratation.
            fehler.append(f"{gid}: needs_tracker gilt nur fuer Kommando-Gates (bead 4t8)")
        if not g.get("reason"):
            fehler.append(f"{gid}: ohne reason — ein Gate ohne Warum wird nicht gepflegt")
        if g.get("action") and not isinstance(g.get("with"), dict | None):
            fehler.append(f"{gid}: 'with' muss ein Mapping sein")
    return fehler


def misst_in(gate: dict[str, Any], umfeld: str) -> bool:
    """Ob ein Gate in diesem Umfeld misst (bead 1jg.2) — die eine Stelle der Regel.

    lokal: alles ausser hosted-only. ci: alles ausser writer-only.
    """
    if umfeld == "lokal":
        return gate["placement"] != "hosted"
    if umfeld == "ci":
        return gate["placement"] != "writer"
    raise ValueError(f"unbekanntes Umfeld {umfeld!r}")


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
                "placement": g["placement"],
                "needs_tracker": bool(g.get("needs_tracker")),
                "needs_history": bool(g.get("needs_history")),
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


def _tracker_hydratation() -> list[str]:
    """Der Schritt, der den Tracker-Stand in der CI messbar macht (4t8, 1jg.3).

    Installiert den gepinnten bd checksummverifiziert, holt den Tracker-Stand
    ueber refs/dolt/data — und rendert EINMAL, bevor der erste Gate laeuft.
    `BEAD_RENDER` zeigt auf genau dieses Render: alle Leser des Laufs nehmen
    denselben Stand statt je einer eigenen Messung (D-52, Bedingung 2). Der
    Schritt ist eine Vorbedingung und traegt deshalb wie checkout und
    setup-deps kein `if` (siehe _schritt). `bd bootstrap` klont via git+https
    in einem eigenen Verzeichnis: der Credential-Header von actions/checkout
    gilt nur lokal im Checkout, darum hebt der Schritt ihn nach --global.
    Beim Bootstrap beruehrt bd ausserdem .beads/.gitignore und
    .beads/config.yaml im Checkout — genau dafuer ist dieser Schritt die
    Stelle, an der das passieren darf.
    """
    return [
        "      - name: Hydrate the tracker (pinned bd, checksum-verified)",
        "        id: setup-tracker",
        "        run: |",
        "          bash tools/beads/install.sh",
        "          git fetch origin refs/dolt/data:refs/dolt/data",
        '          header="$(git config --local http.https://github.com/.extraheader || true)"',
        '          if [ -n "$header" ]; then',
        '            git config --global http.https://github.com/.extraheader "$header"',
        # Lokal UND global gesetzt schickt git den Header doppelt ("Duplicate
        # header: Authorization"), und bd bootstrap fiel still auf die
        # committete Kopie zurueck — bis bead 1jg.3 las die CI den Tracker nie
        # aus refs/dolt/data. Der lokale Eintrag geht, der globale bleibt.
        "            git config --local --unset-all http.https://github.com/.extraheader",
        "          fi",
        "          bash tools/bd bootstrap --yes",
        "          mkdir -p .beads",
        "          python3 scripts/render_beads_export.py",
        '          echo "BEAD_RENDER=$PWD/.beads/issues.jsonl" >> "$GITHUB_ENV"',
    ]


def _checkout(job_gates: list[dict[str, Any]]) -> list[str]:
    """Der Checkout eines Jobs — mit voller Historie nur, wenn ein Gate sie braucht.

    Der gehostete Checkout holt einen Commit. Ein Gate, das den letzten
    Aenderungstag einer Datei fragt (`frontmatter-current`), bekaeme fuer jede
    Datei den ausgecheckten Commit zurueck. Es deklariert deshalb `needs_history`,
    und der Job dieses Gates holt alles; kein anderer Job (bead coding-harness-qd7).
    """
    if any(g["needs_history"] for g in job_gates):
        return ["      - uses: actions/checkout@v4", "        with:", "          fetch-depth: 0"]
    return ["      - uses: actions/checkout@v4"]


def generate_ci() -> str:
    """Die abgeleitete ci.yml — deterministisch, aus der einen Liste."""
    alle = gates()
    # Bead 1jg.2: writer-only Gates misst nur die Schreibmaschine — die
    # abgeleitete ci.yml haelt sie deklariert raus, statt sie dort unmoeglich
    # laufen zu lassen. Ein writer-only Gate mit needs_tracker stoesst folglich
    # auch keine Hydratation an.
    pruefe = [g for g in alle if g["job"] == "verify" and misst_in(g, "ci")]
    drift = [g for g in alle if g["job"] == "drift" and misst_in(g, "ci")]
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
        *_checkout(pruefe),
        "      - name: Install the pinned toolchain",
        "        id: setup-deps",
        "        run: python3 -m pip install pytest==8.3.4 PyYAML ruff==0.9.10",
    ]
    # Bead coding-harness-4t8: der Schritt gehoert nur in Jobs, die einen Gate
    # mit needs_tracker haben — dort, wo niemand ihn braucht, waere er Dekoration.
    if any(g["needs_tracker"] for g in pruefe):
        zeilen.extend(_tracker_hydratation())
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
            *_checkout(drift),
            "      - name: Install the pinned toolchain",
            "        id: setup-deps",
            "        run: python3 -m pip install pytest==8.3.4 PyYAML ruff==0.9.10",
        ]
    )
    if any(g["needs_tracker"] for g in drift):
        zeilen.extend(_tracker_hydratation())
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
    ap.add_argument(
        "--placement",
        choices=("lokal", "ci"),
        default=None,
        help="nur Gates, die in diesem Umfeld messen (bead 1jg.2): lokal "
        "schliesst hosted-only aus, ci schliesst writer-only aus",
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
        print(f"Gate-Datei ok: {len(alle)} Gates, Schema {SCHEMA_VERSION}.")
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
            if args.placement and not misst_in(g, args.placement):
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
