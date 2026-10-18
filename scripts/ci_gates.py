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
import re
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

# The generated workflow's names (bead coding-harness-ei0). The verify gates run
# in the matrix job, one leg per declared interpreter; a summary job named
# SUMMARY_JOB sums the legs up. Its id is the check's context, so it keeps the
# name the ruleset on `main` requires — `verify` — and has no `name:` of its own.
MATRIX_JOB = "gates"
SUMMARY_JOB = "verify"

# The one branch whose pushes start the workflow; every other branch is checked
# through its pull request (bead coding-harness-cac).
MAIN_BRANCH = "main"

# The one line that installs the toolchain in every CI job: the hash-checked
# lock and nothing else. The package versions live in `pyproject.toml` and, with
# their hashes, in `requirements-ci.txt` — never in this file.
INSTALL = "python3 -m pip install --require-hashes -r requirements-ci.txt"

# A declared interpreter is a minor version of Python 3: "3.11", never "3.x".
_INTERPRETER = re.compile(r"3\.(?:0|[1-9][0-9]*)")

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
    "adoption.py": (
        "Library — reads the day a repository adopted a gate for the gates that exempt older changes; "
        "tests/test_adoption.py runs it"
    ),
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
    "leakcheck.py": (
        "Run before every foreign call by scripts/stage2.py and by hand as make leakcheck; it needs "
        "the denylist each machine keeps outside the repository, which no CI step holds"
    ),
    "stage2.py": (
        "Entry point, not a gate — starts the stage-2 reviewers on the maintainer's machine, with a "
        "subscription and a credential no CI step holds; tests/test_stage2.py runs it against stand-ins"
    ),
    "stage2_runs.py": (
        "Entry point, not a gate - a person counts what stage-2 runs left in their change folders and pastes "
        "the output into a research note; it decides nothing; tests/test_stage2_runs.py runs it"
    ),
    "stage2_session.py": (
        "Helper of scripts/stage2.py session, never an entry point of its own — it opens a macOS Terminal "
        "window for an interactive model session; tests/test_stage2_session.py runs it against stand-ins"
    ),
    "stage2_research_refs.py": (
        "Pure frozen-reference library, not a CLI gate; the amended research map/report pipeline consumes it. "
        "Direct structural and claim-cap contracts live in tests/test_stage2_research_refs.py; "
        "legacy dispatcher integration remains pending during the research-swarm implementation."
    ),
    "stage2_research_map.py": (
        "Pure finder-union and neighbour preparation library, not a CLI gate; the amended explore pipeline "
        "consumes it. tests/test_stage2_research_map.py exercises exact union and frozen neighbour boundaries; "
        "actual scheduler integration remains pending."
    ),
    "stage2_research_snapshot.py": (
        "Transient frozen-input library, not a CLI gate; the amended research pipeline will own its "
        "context-managed copies and drift checks. tests/test_stage2_research_snapshot.py exercises "
        "working bytes, untracked inputs, cleanup and exact runner-owned appends. Scheduler integration is pending."
    ),
    "stage2_research_history.py": (
        "Local frozen-HEAD history library, not a CLI gate; stage2_research_snapshot.py shares its "
        "local-only Git boundary. tests/test_stage2_research_history.py exercises history bounds and failures; "
        "the amended topic-6 dispatcher still needs to consume the packet."
    ),
    "stage2_research_report.py": (
        "Pure topic-report and runner-evidence validation library, not a CLI gate; the amended research "
        "dispatcher will consume it. tests/test_stage2_research_report.py exercises raw syntax, local/history/"
        "page evidence, namespaces and topic-specific fields; actual dispatcher integration remains pending."
    ),
    "stage2_research_judge.py": (
        "Pure whole-packet sizing and independent claim-score library, not a CLI gate; the amended "
        "judge pipeline will consume it. tests/test_stage2_research_judge.py exercises exact size limits, "
        "claim coverage and terminal-outcome precedence. Dispatch/reconciliation integration remains pending."
    ),
    "stage2_research_dispatch.py": (
        "Pure cancellable stage-dispatch library, not a CLI gate; the amended swarm runner will consume it. "
        "tests/test_stage2_research_dispatch.py exercises provider queues, ordering, gate serialization, "
        "deadlines and cancel/reap with real child processes; scheduler integration remains pending."
    ),
    "stage2_swarm.py": (
        "Helper of scripts/stage2.py explore, never an entry point of its own — it runs the phase-1 "
        "research swarm only through the runner; tests/test_stage2_swarm.py runs it against stand-ins"
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
    "touch_map.py": (
        "Entry point, not a gate — an agent runs it before a pull request and pastes its output "
        "(prompts/07-commit.md); tests/test_touch_map.py runs it"
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


def _tools_fehler(tools: Any) -> list[str]:
    """The `tools` block: only `python`, a non-empty list of distinct `3.<n>` texts.

    Package versions are not a gate-file fact — `pyproject.toml` and the lock hold
    them — so a key besides `python` is refused, not ignored (bead
    coding-harness-ei0).
    """
    if not isinstance(tools, dict):
        return ["tools: missing or not a mapping — it must hold `python`, a list of interpreter versions"]
    fehler = [
        f"tools.{key}: only `python` belongs here; package versions live in pyproject.toml and requirements-ci.txt"
        for key in tools
        if key != "python"
    ]
    versionen = tools.get("python")
    if not isinstance(versionen, list) or not versionen:
        fehler.append('tools.python: must be a non-empty list of versions, e.g. ["3.11", "3.12"]')
        return fehler
    for v in versionen:
        if not isinstance(v, str) or not _INTERPRETER.fullmatch(v):
            fehler.append(f'tools.python: {v!r} is not a quoted version of the form "3.<n>"')
    texte = [v for v in versionen if isinstance(v, str)]
    if len(set(texte)) != len(texte):
        fehler.append(f"tools.python: a version appears twice in {versionen!r}")
    return fehler


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
    fehler.extend(_tools_fehler(doc.get("tools")))
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


def interpreters() -> list[str]:
    """The declared interpreters, oldest first — `tools.python` of the gate file.

    The generated workflow runs the verify gates once per entry, and the drift job
    once on the last (bead coding-harness-ei0). The schema is checked first, like
    `gates()` does, so a malformed list never reaches the generator.
    """
    fehler = validate_schema()
    if fehler:
        raise ValueError("Gate-Datei verletzt das Schema: " + "; ".join(fehler))
    doc = yaml.safe_load(GATE_FILE.read_text(encoding="utf-8"))
    return list(doc["tools"]["python"])


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


def _toolchain(python_version: str) -> list[str]:
    """The toolchain steps: Python everywhere, pinned Pi where tools/pi exists — in this order.

    `actions/setup-python` first: `python3` after it is the declared interpreter,
    and `INSTALL` then installs the hash-checked lock into exactly that one
    (bead coding-harness-ei0). `actions/setup-node` reads the exact runtime from
    `tools/pi/.node-version`, and `tools/pi/install.sh` installs the locked Pi
    that both jobs' pytest then runs the offline contracts against (ADR 0019).
    Like checkout, none of these steps carries the `if` of a gate: without them
    no gate has a subject.
    """
    steps = [
        "      - name: Set up the declared interpreter",
        "        id: setup-python",
        "        uses: actions/setup-python@v5",
        "        with:",
        f"          python-version: {python_version}",
        "      - name: Install the pinned toolchain",
        "        id: setup-deps",
        f"        run: {INSTALL}",
    ]
    if not (REPO_ROOT / "tools" / "pi").is_dir():
        return steps
    return steps + [
        "      - name: Set up the declared Node runtime",
        "        id: setup-node",
        "        uses: actions/setup-node@v4",
        "        with:",
        "          node-version-file: tools/pi/.node-version",
        "      - name: Install the pinned Pi",
        "        id: setup-pi",
        "        run: bash tools/pi/install.sh",
    ]


def _summary_job() -> list[str]:
    """The check `verify`: red unless every leg of the matrix job passed.

    The ruleset on `main` requires one check, `verify`, and it counts a skipped job
    as passed. So the job needs the matrix job, runs under `always()` (without it a
    failed or skipped `needs` skips this job too, and a skipped job reports
    success), and fails unless the legs' aggregate result is exactly `success` —
    not merely "not failure": `cancelled` and `skipped` are red too (bead
    coding-harness-ei0). The event condition keeps it off the schedule runs, where
    the matrix job is skipped on purpose.
    """
    return [
        f"  {SUMMARY_JOB}:",
        f"    needs: {MATRIX_JOB}",
        "    if: always() && (github.event_name == 'push' || github.event_name == 'pull_request')",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - name: Every leg of the gates passed",
        "        run: |",
        f'          echo "{MATRIX_JOB}: ${{{{ needs.{MATRIX_JOB}.result }}}}"',
        f'          test "${{{{ needs.{MATRIX_JOB}.result }}}}" = success',
    ]


def generate_ci() -> str:
    """Die abgeleitete ci.yml — deterministisch, aus der einen Liste."""
    alle = gates()
    versionen = interpreters()
    # Quoted: an unquoted `3.10` is the number 3.1 to YAML. Built outside the f-string
    # below, which may not reuse its own quotes before Python 3.12.
    matrix = ", ".join(f'"{v}"' for v in versionen)
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
        f"    branches: [{MAIN_BRANCH}]",
        "  pull_request:",
        "  schedule:",
        '    - cron: "23 4 * * *"',
        "  workflow_dispatch:",
        "",
        "concurrency:",
        "  group: verify-${{ github.event_name }}-${{ github.ref }}",
        "  cancel-in-progress: ${{ github.event_name == 'pull_request' }}",
        "",
        "jobs:",
        f"  {MATRIX_JOB}:",
        "    if: github.event_name == 'push' || github.event_name == 'pull_request'",
        # One leg per declared interpreter, and no fail-fast: a red leg must not
        # cancel the other, for the reason bead coding-harness-bl2 gave for steps.
        "    strategy:",
        "      fail-fast: false",
        "      matrix:",
        f"        python: [{matrix}]",
        "    runs-on: ubuntu-latest",
        "    steps:",
        *_checkout(pruefe),
        *_toolchain("${{ matrix.python }}"),
    ]
    # Bead coding-harness-4t8: der Schritt gehoert nur in Jobs, die einen Gate
    # mit needs_tracker haben — dort, wo niemand ihn braucht, waere er Dekoration.
    if any(g["needs_tracker"] for g in pruefe):
        zeilen.extend(_tracker_hydratation())
    for g in aktionen:
        zeilen.extend(_schritt(g))
    for g in kommandos:
        zeilen.extend(_schritt(g))
    zeilen.extend(_summary_job())
    # The drift gates read the outside world, not the interpreter: one run, under
    # the last declared interpreter.
    zeilen.extend(
        [
            "  drift:",
            "    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'",
            "    runs-on: ubuntu-latest",
            "    steps:",
            *_checkout(drift),
            *_toolchain('"' + versionen[-1] + '"'),
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
            if g["placement"] == "writer":
                zusatz += " — laeuft nur lokal (make verify), nicht in der CI"
            print(f"      {g['command']}{zusatz}")
        else:
            print(f"      (Marketplace-Action: {g['action']}) — laeuft nur in der CI")
    print("\n~ = lokal ueber ein Ersatzwerkzeug · * = gar nicht lokal · ⏱ = Drift-Job (Timer).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
