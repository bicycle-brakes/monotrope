#!/usr/bin/env python3
"""Hygiene und Index der `plans/`-Artefakte.

Der Arbeitsablauf in `docs/WORKFLOW.md` uebergibt zwischen den Phasen Dateien,
nicht Chat-Verlaeufe. Damit das traegt, muessen die Dateien auffindbar sein und
sagen, woran man ist. Beides verfaellt leise: ein Artefakt ohne Frontmatter ist
fuer jede Abfrage unsichtbar, und eine Spec, die gebaut ist und weiter als aktiv
gefuehrt wird, ist die Doppel-Wahrheit, gegen die `plans/_README.md` geschrieben
ist.

Zwei Modi, und beide sind fuer sich vollstaendig:

    --check    meldet die Hygiene ueber `_verdict` (INFO/DRIFT/BLOCK)
    --index    erzeugt `plans/INDEX.md` neu

Warum getrennt: ein Werkzeug, das beim Pruefen schreibt, kann nicht sagen, ob
der Baum vorher schon stimmte. `--check` fasst nichts an.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _verdict import Level, Ramp, Verdict  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
PLANS = REPO / "plans"
INDEX = PLANS / "INDEX.md"

# `bead` ist Pflicht, weil der Index eine Bead-Spalte rendert: ohne das Feld
# steht dort eine Luecke, und ein Artefakt ohne Vorgang ist Arbeit, die in
# keiner Abfrage auftaucht — `bd ready` kennt sie nicht.
REQUIRED = ("status", "implementation_status", "date", "last_reviewed", "bead")
STATUS = {"draft", "accepted", "superseded"}
IMPLEMENTATION = {"none", "partial", "done"}
STALE_AFTER_DAYS = 90

# Der Index wird erzeugt; die Kopfzeilen stehen hier, damit ein Handedit auffaellt.
INDEX_HEADER = """<!-- GENERIERT von scripts/plans_registry.py --index — nicht von Hand aendern -->

# plans/INDEX.md

Jedes Artefakt unter `plans/`, mit seinen beiden Statusfeldern. Erzeugt, nie
getippt: eine handgepflegte Liste von Dateien altert genau so schnell, wie
Dateien dazukommen.

| Artefakt | status | implementation_status | zuletzt geprueft | Bead |
|---|---|---|---|---|
"""


def _frontmatter(path: Path) -> dict | None:
    """Der YAML-Block am Dateianfang, oder None wenn keiner da ist."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        loaded = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None
    return loaded if isinstance(loaded, dict) else None


def artefacts() -> list[Path]:
    """Jede Markdown-Datei unter `plans/`, ausser den erzeugten und erklaerenden."""
    if not PLANS.exists():
        return []
    return sorted(
        p for p in PLANS.rglob("*.md") if p.name not in {"_README.md", "INDEX.md"} and not p.name.startswith("_")
    )


def _age_days(value: object) -> int | None:
    if isinstance(value, dt.date):
        return (dt.date.today() - value).days
    if isinstance(value, str):
        try:
            return (dt.date.today() - dt.date.fromisoformat(value)).days
        except ValueError:
            return None
    return None


def _bead_export_path() -> Path:
    """Der Pfad wird aus `REPO` abgeleitet -- niemals als Modulkonstante gecacht,
    damit ein Test, der `reg.REPO` monkeypatcht, auch den Exportpfad umlenkt."""
    return REPO / ".beads" / "issues.jsonl"


def _bead_statuses(export_path: Path) -> dict[str, str] | None:
    """`id -> status` aus `.beads/issues.jsonl`, als Datei gelesen.

    Nie ueber das Kommando `bd`: es schreibt die Datei bei jedem Aufruf zurueck,
    und die CI hat kein `bd` (AGENTS.md, spec.md RB "Kein `bd`-Schreibkommando").
    Das Format ist JSON Lines, eine Zeile ein Vorgang.

    Liefert None, wenn der Export fehlt, nicht lesbar ist oder keine einzige
    brauchbare Zeile enthaelt -- das ist der Fall, in dem die Kopplungspruefung
    unten selbst nichts misst, und wird vom Aufrufer als eigener Befund (BLOCK,
    RB-G7) gemeldet statt als Schweigen.
    """
    if not export_path.exists():
        return None
    statuses: dict[str, str] = {}
    for line in export_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and isinstance(row.get("id"), str) and isinstance(row.get("status"), str):
            statuses[row["id"]] = row["status"]
    return statuses or None


# Der Bestand am Tag, an dem die Gegenrichtung scharf wurde (2026-09-15).
#
# Namentlich, nicht als Zahl: ein Ventil, das "die ersten fuenf" traegt, traegt
# auch den sechsten, der morgen dazukommt. So ist jeder NEUE Vorgang ohne
# Artefakt sofort DRIFT, und nur diese fuenf warten.
BESTAND_OHNE_ARTEFAKT = frozenset(
    {
        "portfolio-agentic-engineering-ke1k",
        "portfolio-agentic-engineering-nu5a",
        "portfolio-agentic-engineering-twgy.7",
        "portfolio-agentic-engineering-utdf",
        "portfolio-agentic-engineering-wp-l2",
    }
)


def _bestand_ramp(offen: set[str]) -> Ramp:
    """Die fuenf Altfaelle zaehlen als INFO, bis sie geraeumt sind — oder die Frist haelt.

    Sofort scharf zu schalten hiesse: `plans-drift` ist ab dem ersten Tag rot,
    und zwar ueber einem Zustand, den dieser Pull Request nicht erzeugt hat. Ein
    Gate, das immer rot ist, wird abgeschaltet und schuetzt danach nichts —
    dieselbe Begruendung wie bei `_praesenz_ramp` in
    `validate_change_artefacts.py`.

    Das Ziel ist DRIFT, nicht INFO: das Ventil schaltet von selbst scharf, sobald
    es faellig ist, ohne dass jemand hier nachziehen muss.
    """

    def bestand_geraeumt() -> bool:
        return not (offen & BESTAND_OHNE_ARTEFAKT)

    return Ramp(
        name="bead-ohne-artefakt-bestand",
        condition=(
            "die fuenf am 2026-09-15 laufenden Vorgaenge ohne Artefakt haben einen "
            "Aenderungsordner oder stehen nicht mehr auf 'in_progress' "
            "(spaetestens 2026-11-30)"
        ),
        predicate=bestand_geraeumt,
        target=Level.DRIFT,
        until_then=Level.INFO,
        deadline=dt.date(2026, 11, 30),
    )


def check() -> Verdict:
    verdict = Verdict()
    found = artefacts()
    export_path = _bead_export_path()
    bead_statuses = _bead_statuses(export_path)
    if bead_statuses is None:
        export_rel = export_path.relative_to(REPO)
        verdict.block(
            f"Bead-Export {export_rel} fehlt oder ist leer",
            "Dann ist nicht die Kopplung Artefakt<->Vorgang verletzt, sondern die "
            "Pruefung selbst misst nichts (RB-G7). Beheben: `bd export` bzw. den "
            "Export-Hook laufen lassen.",
        )

    if not found:
        # Kein BLOCK: ein frisch eingerichtetes Repo hat legitim null Artefakte.
        # Aber auch kein Schweigen — eine leere Menge wird benannt, nicht
        # weggelassen, sonst liest sich "gruen" wie "geprueft".
        #
        # Und kein `return`: der Index wird trotzdem geprueft. Ein frueher
        # Ausstieg hier hiesse, dass ein getrackter Index, der ein geloeschtes
        # Artefakt weiter auffuehrt, genau in dem Fall unbemerkt bleibt, in dem
        # er am sichersten falsch ist.
        verdict.info(
            "kein Artefakt unter plans/",
            "Der Ablauf ist eingerichtet und noch nicht gelaufen.",
        )

    by_name = {str(p.relative_to(REPO)): p for p in found}
    # D4 (spec.md/plan.md): einmal je Ordner, nicht je Artefakt darin — drei
    # gleichlautende Zeilen fuer einen Ordner waeren Rauschen.
    ordner_ohne_plan_gemeldet: set[Path] = set()
    # Welche Vorgaenge ueberhaupt ein Artefakt haben. Gebraucht fuer die
    # Gegenrichtung der Kopplung unten -- die Schleife hier laeuft ueber
    # Artefakte und kann einen Vorgang, der nie eines bekam, nicht sehen.
    beads_mit_artefakt: set[str] = set()

    for path in found:
        rel = str(path.relative_to(REPO))
        meta = _frontmatter(path)

        if meta is None:
            verdict.block(f"{rel}: kein lesbares Frontmatter", "Ohne Frontmatter ist es fuer jede Abfrage unsichtbar.")
            continue

        for field in REQUIRED:
            if field not in meta:
                verdict.block(f"{rel}: Feld '{field}' fehlt")
            elif meta.get(field) in (None, ""):
                # "vorhanden" und "gefuellt" sind nicht dasselbe: ein
                # Pflichtfeld, das da ist, aber leer (`last_reviewed:`) oder
                # explizit `null` ist, war bisher fuer jede nachgelagerte
                # Pruefung derselbe blinde Fleck wie ein fehlendes Feld --
                # `last_reviewed: null` schaltete so seine eigene Alters- und
                # Lesbarkeitspruefung still ab (AK-4, spec.md Z3). Die zwei
                # Zeiger, die `null` tragen duerfen, sind `supersedes` und
                # `superseded_by` (plans/_README.md) -- beide stehen nicht in
                # REQUIRED und sind von dieser Schleife nicht betroffen.
                verdict.block(f"{rel}: Feld '{field}' ist leer")

        if meta.get("status") not in STATUS | {None}:
            verdict.block(f"{rel}: status '{meta.get('status')}' ist keiner von {sorted(STATUS)}")
        if meta.get("implementation_status") not in IMPLEMENTATION | {None}:
            verdict.block(
                f"{rel}: implementation_status '{meta.get('implementation_status')}' "
                f"ist keiner von {sorted(IMPLEMENTATION)}"
            )

        # Pfadsegmente relativ zu PLANS, nicht Teilstrings von `rel` (R-3):
        # ein Verzeichnis, das zufaellig "changes" heisst -- etwa
        # `plans/specs/changes/spec.md` -- ist keine Aenderung. `PLANS` muss
        # auch nicht "plans" heissen; die Testfixture biegt das um.
        plans_parts = path.relative_to(PLANS).parts
        in_changes = bool(plans_parts) and plans_parts[0] == "changes"
        archived = in_changes and len(plans_parts) > 1 and plans_parts[1] == "archive"

        if in_changes and not archived and meta.get("implementation_status") == "done":
            verdict.drift(
                f"{rel}: gebaut und nicht archiviert",
                "Nach plans/_README.md gehoert das Delta in die lebende Spec und der Rest ins Archiv.",
            )

        # D4 (spec.md §7, plan.md §4 S4): bewegt sich der Code (implementation_status
        # 'partial' oder 'done'), hat Phase 3 stattgefunden — sonst ist der Plan der
        # Code, und das ist der Fall, gegen den "Der Plan ist der Vertrag"
        # (docs/WORKFLOW.md §2) geschrieben ist. DRIFT statt BLOCK: die Eskalation
        # traegt der `--strict`-Lauf (plans-drift), kein fremder Pull Request soll
        # dafuer rot werden. Ein Ordner, dessen Artefakte alle 'none' tragen, ist
        # nicht betroffen -- dort hat sich kein Code bewegt.
        if (
            in_changes
            and not archived
            and meta.get("implementation_status") in {"partial", "done"}
            and not (path.parent / "plan.md").exists()
            and path.parent not in ordner_ohne_plan_gemeldet
        ):
            ordner_ohne_plan_gemeldet.add(path.parent)
            verdict.drift(
                f"{path.parent.relative_to(REPO)}/: implementation_status ist "
                f"'{meta.get('implementation_status')}', aber es gibt kein plan.md",
                "Phase 3 hat nicht stattgefunden, oder der Plan ist der Code.",
            )

        last_reviewed = meta.get("last_reviewed")
        age = _age_days(last_reviewed)
        if last_reviewed is not None and age is None:
            verdict.drift(
                f"{rel}: last_reviewed '{last_reviewed}' ist kein lesbares Datum",
                "Ein unlesbarer Wert ist ein Befund, kein Grund, die Pruefung zu ueberspringen.",
            )
        elif age is not None and age > STALE_AFTER_DAYS and not archived:
            verdict.drift(f"{rel}: seit {age} Tagen nicht geprueft")

        # `date` wird genauso geparst wie `last_reviewed` — nicht fuer die
        # Altersschwelle, nur damit ein unlesbarer Wert nicht stumm bleibt.
        date_value = meta.get("date")
        if date_value is not None and _age_days(date_value) is None:
            verdict.drift(
                f"{rel}: date '{date_value}' ist kein lesbares Datum",
                "Ein unlesbarer Wert ist ein Befund, kein Grund, die Pruefung zu ueberspringen.",
            )

        target = meta.get("superseded_by")
        if target and target not in by_name:
            verdict.block(f"{rel}: superseded_by zeigt auf '{target}', das es nicht gibt")
        elif target:
            back = (_frontmatter(by_name[target]) or {}).get("supersedes")
            if back != rel:
                verdict.drift(
                    f"{rel} -> {target}: die Ablösung ist nicht gegenseitig",
                    "Wer abloest, wird abgeloest — sonst findet nur eine Richtung den Nachfolger.",
                )

        # `supersedes` ist ein eigener, gepruefter Zeiger — nicht nur der
        # Rueckverweis fuer die Gegenseitigkeitspruefung oben. Aufgeloest wird
        # gegen das Repo-Wurzelverzeichnis, nicht gegen die Artefaktmenge
        # `by_name`: der eine lebende Zeiger im Repo verweist absichtlich nach
        # docs/journal/, ausserhalb von plans/.
        supersedes = meta.get("supersedes")
        if supersedes and not (REPO / supersedes).exists():
            verdict.block(f"{rel}: supersedes zeigt auf '{supersedes}', das es nicht gibt")

        # Zustandskopplung Artefakt <-> Vorgang (AK-5, spec.md D3): beide
        # Richtungen sind DRIFT, nicht BLOCK -- `bd close` laeuft typischerweise
        # NACH dem Merge, also traefe ein BLOCK hier nicht den Commit, der ihn
        # erzeugt hat, sondern den naechsten unbeteiligten Pull Request. Geprueft
        # wird nur, was unter changes/ liegt (aktiv oder archiviert) -- eine
        # lebende Capability-Spec unter specs/ wird nach _README.md nie
        # archiviert und hat kein aequivalentes Ziel fuer "Bead zu".
        if in_changes and meta.get("bead"):
            beads_mit_artefakt.add(str(meta["bead"]))

        if bead_statuses is not None and in_changes:
            bead = meta.get("bead")
            if bead:
                status = bead_statuses.get(bead)
                if status is None:
                    # Der Bead kommt im Export gar nicht vor: kann eine frisch
                    # angelegte Aufgabe sein (Export noch nicht nachgezogen) oder
                    # ein Tippfehler im Frontmatter. Beides ist ungeprueft, und
                    # die bewegliche Seite ist der Tracker-Export -- also DRIFT,
                    # nicht BLOCK, und scharf erst unter --strict wie der Rest
                    # dieser Kopplung.
                    verdict.drift(
                        f"{rel}: Bead '{bead}' kommt im Export {export_path.relative_to(REPO)} nicht vor",
                        "Ungeprueft, ob Artefakt- und Vorgangs-Zustand sich widersprechen.",
                    )
                else:
                    closed = status == "closed"
                    done = meta.get("implementation_status") == "done"
                    if closed and not (done and archived):
                        verdict.drift(
                            f"{rel}: Bead '{bead}' ist im Export geschlossen, "
                            "aber das Artefakt ist nicht 'done' und archiviert",
                            "Der Tracker sagt fertig, das Artefakt widerspricht.",
                        )
                    if done and not closed:
                        verdict.drift(
                            f"{rel}: implementation_status ist 'done', aber Bead "
                            f"'{bead}' ist im Export nicht geschlossen (Status: '{status}')",
                            "Das Artefakt sagt fertig, der Tracker widerspricht.",
                        )

    # Gegenrichtung der Kopplung: Vorgang -> Artefakt.
    #
    # Die Schleife oben laeuft ueber Artefakte und fragt zu jedem seinen Bead.
    # Ein Bead, der nie ein Artefakt bekam, liegt ausserhalb ihres Laufbereichs
    # und kann keinen Befund erzeugen -- die Pruefung ist fuer ihn nicht
    # umgangen, sie ist leer.
    #
    # Die beiden RB-G7-Waechter oben decken das nicht ab, und zwar richtigerweise:
    # sie sichern die zwei Mengen, die diese Funktion *liest* (Export leer,
    # null Artefakte). Die leere Menge einer *Relation* ist aber keine der
    # beiden Eingaben, sondern ihre Differenz. Beide Seiten gegen Leere zu
    # sichern, sichert nicht die Beziehung zwischen ihnen.
    #
    # Nur `in_progress`: ein offener Vorgang hat legitim kein Artefakt -- er
    # wird nicht bearbeitet. Ein geschlossener kann aelter sein als der Ablauf.
    # `in_progress` ist die Behauptung "hieran arbeitet gerade jemand", und der
    # Ablauf sagt, dass Arbeit durch einen Aenderungsordner laeuft
    # (docs/WORKFLOW.md: Einstieg ist `make change NAME=... BEAD=...`).
    #
    # DRIFT wie der Rest dieser Kopplung: `bd update --status in_progress` laeuft
    # ohne Commit in diesem Repo, oft in einer anderen Sitzung. Ein BLOCK traefe
    # den naechsten unbeteiligten Pull Request, nicht den, der den Zustand
    # erzeugt hat.
    if bead_statuses is not None:
        laufend = {bid for bid, st in bead_statuses.items() if st == "in_progress"}
        if not laufend:
            # RB-G7 fuer diese Pruefung selbst: keine laufenden Vorgaenge heisst
            # nicht "geprueft und sauber", sondern "nichts zu pruefen gewesen".
            # Das wird benannt, nicht verschwiegen -- sonst liest sich gruen hier
            # wie ein Ergebnis.
            verdict.info(
                "kein Vorgang steht auf 'in_progress'",
                "Die Gegenrichtung der Kopplung hatte nichts zu messen.",
            )
        else:
            ohne = sorted(laufend - beads_mit_artefakt)
            ramp = _bestand_ramp(set(ohne))
            for bid in ohne:
                verdict.drift(
                    f"Bead '{bid}' ist 'in_progress', hat aber kein Artefakt unter plans/changes/",
                    "Der Tracker sagt, hier werde gearbeitet; der Ablauf hat davon nie erfahren. "
                    "Beheben: `make change NAME=<name> BEAD=" + bid + "` -- oder den Vorgang "
                    "zurueck auf 'open' setzen, wenn niemand daran arbeitet.",
                    ramp=ramp if bid in BESTAND_OHNE_ARTEFAKT else None,
                )
            verdict.info(
                f"{len(laufend)} laufende Vorgaenge geprueft, {len(ohne)} ohne Artefakt",
            )

    # Der Index ist erzeugt und getrackt — also gehoert er in dieselbe Pruefung
    # wie jede andere gerenderte Datei: `X == render(Y)`, sonst altert er wie
    # jede handgepflegte Liste, nur unauffaelliger.
    #
    # BLOCK, nicht DRIFT. Die Stufen unterscheiden nach _verdict.py, wer den
    # Befund verursacht hat: DRIFT ist fuer eine Gegenseite, die sich ohne Commit
    # hier bewegt, BLOCK fuer Artefakte dieses Repos, die einander
    # widersprechen. Index und Eingaben liegen beide hier und wandern beide per
    # Commit — der Widerspruch ist immer die Folge des Commits, der ihn erzeugt,
    # und gehoert an dessen Pull Request. Als DRIFT gemeldet waere er ohne
    # `--strict` Exit 0, und der CI-Schritt ruft ohne `--strict`: das Gate stuende
    # gruen ueber einem alternden Index.
    if INDEX.exists():
        if INDEX.read_text(encoding="utf-8") != render_index():
            verdict.block(
                "plans/INDEX.md weicht von seinen Eingaben ab",
                "Beheben: make index",
            )
    else:
        verdict.block("plans/INDEX.md fehlt", "Beheben: make index")

    if found:
        verdict.info(f"{len(found)} Artefakte geprueft")
    return verdict


def render_index() -> str:
    rows = []
    for path in artefacts():
        meta = _frontmatter(path) or {}
        rel = str(path.relative_to(PLANS))
        rows.append(
            f"| [`{rel}`]({rel}) | {meta.get('status', '—')} | "
            f"{meta.get('implementation_status', '—')} | {meta.get('last_reviewed', '—')} | "
            f"{meta.get('bead', '—')} |"
        )
    if not rows:
        rows.append("| _noch kein Artefakt_ | — | — | — | — |")
    return INDEX_HEADER + "\n".join(rows) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Hygiene melden, nichts schreiben")
    mode.add_argument("--index", action="store_true", help="plans/INDEX.md neu erzeugen")
    parser.add_argument("--strict", action="store_true", help="DRIFT blockt ebenfalls")
    args = parser.parse_args(argv)

    if args.index:
        INDEX.write_text(render_index(), encoding="utf-8")
        print(f"geschrieben: {INDEX.relative_to(REPO)}")
        return 0

    verdict = check()
    print(verdict.render())
    return verdict.exit_code(strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
