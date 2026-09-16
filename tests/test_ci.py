"""Tests ueber die CI selbst — die Gates, die die Gates bewachen.

Zwei Fehlerformen sollen hier haengenbleiben, beide gemessen:

1. **Ein Gate, dessen Trigger enger ist als sein Input, ist gruen, weil es nie
   lief.** Bis zum 31.08.2026 loesten `.claude/**` und `.github/**` in diesem
   Repo kein einziges Gate aus — ein Pull Request, der nur einen Hook aenderte,
   wurde ungeprueft gemergt.

2. **Eine kopierte Gate-Liste ist die Drift, gegen die sie geschrieben wurde.**
   `verify_all.sh` darf keine eigenen Kommandos halten; es fragt `ci_gates.py`,
   und der liest `ci.yml`.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CI_FILE = REPO_ROOT / ".github" / "workflows" / "ci.yml"
RUNNER = REPO_ROOT / "scripts" / "verify_all.sh"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from ci_gates import gates  # noqa: E402


def _einschraenkungen() -> dict[str, list[str]]:
    """Welche Pfad-Einschraenkungen die Trigger tragen — je Trigger, leer wenn keine.

    Bis zum 2026-09-08 stand hier eine Positivliste (`paths:`), und diese Datei
    pruefte, ob sie alles deckt, was die Gates lesen. Sie tat es nicht: neun
    getrackte Dateien loesten keinen Lauf aus, darunter `model-endpoints.yaml`,
    auf der RB-A6 steht. Die Ableitung konnte das nicht sehen, weil sie
    Verzeichnisse aus Zeichenketten-Literalen der Gate-Scripts zog — eine
    Wurzeldatei kommt darin nicht vor.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    # `on` wird von PyYAML als Boolean True geparst (YAML 1.1) — beide Formen zulassen.
    trigger = doc.get("on") or doc.get(True)
    gefunden: dict[str, list[str]] = {}
    for name in ("push", "pull_request"):
        block = trigger.get(name) or {}
        if not isinstance(block, dict):
            continue
        for schluessel in ("paths", "paths-ignore"):
            werte = block.get(schluessel) or []
            if werte:
                gefunden[f"{name}.{schluessel}"] = list(werte)
    return gefunden


# --------------------------------------------------------------------------
# 1 · Der Trigger deckt ab, was die Gates lesen
# --------------------------------------------------------------------------


def test_ci_exists_and_has_gates() -> None:
    assert CI_FILE.is_file(), "Es gibt keine CI-Definition."
    assert len(gates()) >= 10, "Die Verifikationsliste ist verdaechtig kurz."


def test_the_trigger_does_not_restrict_paths() -> None:
    """Jede Aenderung an einer getrackten Datei faehrt die Gates.

    Eine Positivliste altert mit jeder neuen Datei — `model-endpoints.yaml` kam
    in einem spaeteren PR dazu, und niemand zog den Filter nach. Eine
    Ausnahmeliste waere leer: `scripts/kit/probe.py` klassifiziert JEDE
    getrackte Datei ueber `git ls-files`, und `.gitignore` veraendert sogar,
    welche Dateien es sieht. Es gibt keine Datei, deren Aenderung kein Gate
    beruehren kann.
    """
    gefunden = _einschraenkungen()
    assert not gefunden, (
        "Der CI-Trigger schraenkt Pfade ein: "
        + "; ".join(f"{k} = {v}" for k, v in sorted(gefunden.items()))
        + ". Eine Datei, die keinen Lauf ausloest, ist ungeprueft gemergt — und der "
        "naechste unbeteiligte PR wird dafuer rot."
    )


def _oberste_verzeichnisse() -> set[str]:
    """Die getrackten Verzeichnisse der obersten Ebene.

    Aus `git ls-files`, nicht aus `iterdir()`: ein lokales `.venv/` oder
    `htmlcov/` haette sonst die Alternation veraendert und den Test zwischen
    CI und Entwicklermaschine verschieden gemacht.
    """
    ergebnis = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    return {p.split("/", 1)[0] for p in ergebnis.stdout.splitlines() if "/" in p}


def _verzeichnisse_aus_quelltext(quelltext: str, oberste: set[str]) -> set[str]:
    """Welche Verzeichnisse nennt dieser Quelltext als Pfad?

    Zwei Schreibweisen, und die zweite ist der Grund, warum es diese Funktion
    ueberhaupt gibt:

    1. als Literal mit Schraegstrich — `"docs/journal/"`
    2. **segmentweise** — `REPO_ROOT / ".beads" / "issues.jsonl"`

    Die erste Fassung dieser Pruefung kannte nur (1). Der echte Lesepfad des
    Gates `dangling-beads` steht aber in Form (2), und `.beads` kam nur deshalb
    heraus, weil es zufaellig auch in `SKIP_PREFIXES` steht — der Liste der
    Verzeichnisse, die das Gate ausdruecklich **nicht** liest. Die Pruefung war
    gruen, und sie war gruen am Token mit der gegenteiligen Bedeutung.

    Ueber-Erkennung ist hier ungefaehrlich und Absicht: ein Treffer, der kein
    Pfad ist, macht die Menge groesser und den Test damit strenger. Unter-
    Erkennung ist der Ausfall, gegen den geschrieben wird.
    """
    gefunden: set[str] = set()
    for zitat in re.findall(r"""["']([^"'\n]{1,200})["']""", quelltext):
        kopf = zitat.split("/", 1)[0]
        if kopf in oberste and (kopf == zitat or zitat.startswith(kopf + "/")):
            gefunden.add(kopf)
    return gefunden


def _verzeichnisse_die_die_gates_lesen() -> dict[str, set[str]]:
    """Leitet aus den Gate-Kommandos ab, welche Verzeichnisse gelesen werden.

    Die Parametrisierung oben ist eine Handliste: sie prueft, dass ein bekanntes
    Verzeichnis im Filter steht, aber nicht, dass die Liste vollstaendig ist. Eine
    Handliste kann nur so gut sein wie ihr letzter Pfleger — und `.beads/` fehlte
    ihr, obwohl `check_dangling_bead_ids.py` daraus liest.
    """
    oberste = _oberste_verzeichnisse()
    gelesen: dict[str, set[str]] = {}
    for gate in gates():
        for treffer in re.finditer(r"([A-Za-z0-9_./-]+\.py)\b", gate.get("command") or ""):
            rel = treffer.group(1)
            quelle = REPO_ROOT / rel
            if not quelle.is_file():
                continue
            for verzeichnis in _verzeichnisse_aus_quelltext(quelle.read_text(encoding="utf-8"), oberste):
                gelesen.setdefault(verzeichnis, set()).add(rel)
    return gelesen


def _deckt(muster: list[str], verzeichnis: str) -> bool:
    """Segmentweise, nicht als Zeichenketten-Praefix.

    `scripts/**` deckt nicht `script/`, auch wenn `startswith` das behauptet.
    """
    return any(p == verzeichnis or p.startswith(verzeichnis + "/") for p in muster)


def test_no_directory_a_gate_reads_is_excluded() -> None:
    """Kein Gate liest aus einem Verzeichnis, das eine Ausnahme ausschliesst.

    Solange `_einschraenkungen()` leer ist, ist das trivial wahr — der Test
    bleibt trotzdem stehen: er ist die Sperrklinke fuer den Tag, an dem jemand
    eine Ausnahme eintraegt. Die Ableitung unten ist bewusst ueber-erkennend.
    """
    ausnahmen = [p for werte in _einschraenkungen().values() for p in werte]
    if not ausnahmen:
        gelesen = _verzeichnisse_die_die_gates_lesen()
        assert gelesen, "die Ableitung findet kein einziges gelesenes Verzeichnis (RB-G7)"
        return
    getroffen = {
        verzeichnis: sorted(skripte)
        for verzeichnis, skripte in _verzeichnisse_die_die_gates_lesen().items()
        if _deckt(ausnahmen, verzeichnis)
    }
    assert not getroffen, "Ausnahmen schliessen Verzeichnisse aus, die Gates lesen: " + "; ".join(
        f"{d}/ (gelesen von {', '.join(s)})" for d, s in sorted(getroffen.items())
    )


def test_die_ableitung_sieht_die_segmentweise_schreibweise() -> None:
    """Gegenprobe auf der Form, an der die erste Fassung gescheitert ist.

    `REPO_ROOT / ".beads" / "issues.jsonl"` — kein Schraegstrich im Literal.
    Genau so steht der Lesepfad in `check_dangling_bead_ids.py`.
    """
    quelle = 'EXPORT = REPO_ROOT / ".beads" / "issues.jsonl"'
    assert _verzeichnisse_aus_quelltext(quelle, {".beads", "docs"}) == {".beads"}


def test_die_ableitung_sieht_die_literale_schreibweise() -> None:
    """Und die andere Form, damit die Erweiterung nicht die erste verliert."""
    quelle = 'SKIP = ("docs/lessons/_rohbefunde/",)\nP = "scripts/x.py"'
    assert _verzeichnisse_aus_quelltext(quelle, {"docs", "scripts"}) == {"docs", "scripts"}


def test_die_ableitung_erfindet_nichts() -> None:
    """Ein Quelltext ohne Pfade ergibt die leere Menge.

    Ohne diese Probe koennte die Erkennung alles Zitierte melden und der Test
    darueber waere nur noch Rauschen.
    """
    assert _verzeichnisse_aus_quelltext('x = "hallo"\ny = "ein Satz mit Leerzeichen"', {"docs"}) == set()


def test_der_echte_lesepfad_des_bead_gates_wird_erkannt() -> None:
    """Nicht ueber SKIP_PREFIXES, sondern ueber die Zeile, die wirklich liest.

    Der alte Test war gruen, weil `.beads/` zufaellig auch in der Liste der
    ausgenommenen Praefixe steht. Diese Probe nimmt genau die Zeile, die den
    Export oeffnet, und sonst nichts.
    """
    quelle = REPO_ROOT / "scripts" / "check_dangling_bead_ids.py"
    zeilen = [z for z in quelle.read_text(encoding="utf-8").splitlines() if z.startswith("EXPORT")]
    assert zeilen, "Die Zeile, die den Bead-Export oeffnet, heisst nicht mehr EXPORT."
    assert _verzeichnisse_aus_quelltext("\n".join(zeilen), _oberste_verzeichnisse()) == {".beads"}


def test_die_ableitung_findet_ueberhaupt_etwas() -> None:
    """Faende sie nichts, waere der Test oben leer und damit immer gruen."""
    gelesen = _verzeichnisse_die_die_gates_lesen()
    assert len(gelesen) >= 5, f"Nur {len(gelesen)} Verzeichnisse abgeleitet: {sorted(gelesen)}"
    assert ".beads" in gelesen


def test_every_gate_has_a_name_and_an_id() -> None:
    """Der Name ist fuer Menschen, die id ist der Schluessel des lokalen Runners."""
    ohne_id = [g["name"] for g in gates() if not g["id"]]
    assert not ohne_id, f"Gates ohne id: {ohne_id}"


def test_every_step_after_a_failing_gate_still_runs() -> None:
    """Ein Schritt hinter einem Ventil braucht `if:`, sonst faellt er lautlos aus.

    `ramp_valves.py` gibt bewusst `exit 1` zurueck, sobald ein Uebergangs-Ventil
    faellig ist — das ist seine Funktion, kein Fehler. GitHub Actions ueberspringt
    danach jeden folgenden Schritt desselben Jobs, der kein `if:` traegt. Ein
    Zeitgeber-Job, dessen Pruefungen ab einem Datum stumm aussetzen, meldet
    weiter gruen: nicht ueber einem sauberen Baum, sondern ueber einer Menge,
    aus der die Pruefungen verschwunden sind.

    Genau das war W-11: `provenance-history` stand ohne `if:` hinter
    `ramp-valves` und waere ab dem 2026-10-31 nie wieder gelaufen. Der Befund
    war ein Jahr im Voraus sichtbar und trotzdem keinem Test aufgefallen — weil
    es keinen gab, der die Reihenfolge liest.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    verletzt: list[str] = []
    ventile = 0
    for job_name, job in (doc.get("jobs") or {}).items():
        gesehen = False
        for schritt in job.get("steps") or []:
            if gesehen and "if" not in schritt:
                verletzt.append(f"{job_name}.{schritt.get('id') or schritt.get('name')}")
            # `ramp_valves.py` ist der eine Schritt, der planmaessig rot wird.
            # Erkannt am Kommando, nicht an der id: eine id ist umbenannt, bevor
            # jemand diesen Test liest.
            if "ramp_valves.py" in str(schritt.get("run", "")):
                gesehen = True
                ventile += 1
    # Ohne diese Zeile ist der Test still gruen, sobald `ramp_valves.py` in
    # keinem Job mehr vorkommt — umbenannt, verschoben, in ein anderes Script
    # gezogen. Er liefe dann ueber die leere Menge und meldete Bestehen, was
    # genau die Fehlerklasse ist, gegen die er geschrieben ist.
    assert ventile, (
        "Kein Schritt faehrt ramp_valves.py — dieser Test lief ueber die leere "
        "Menge. Entweder wurde das Script umbenannt, dann folgt der Test ihm; "
        "oder das Ventil ist weg, dann gehoert dieser Test geloescht."
    )
    assert not verletzt, (
        f"Schritte hinter dem Ventil ohne `if:` — sie setzen aus, sobald ein Uebergangs-Ventil faellig wird: {verletzt}"
    )


def test_every_step_with_an_id_also_carries_a_name() -> None:
    """W-7: die Namenshaelfte, die `test_every_gate_has_a_name_and_an_id` nicht pruefen kann.

    Jener Test liest `gates()`, und `ci_gates.py:152` verwirft dort jeden Schritt
    ohne `name`, bevor die Liste zurueckkommt — bewusst, denn namenlose Schritte
    sind Infrastruktur. Genau deshalb *kann* er die Haelfte nicht sehen, die er
    im Namen fuehrt: ein Gate-Schritt, den jemand ohne Namen anlegt, verschwindet
    lautlos aus `ci_gates.py --list`, aus dem lokalen Laeufer und aus jeder
    Zaehlung, und kein Test wird rot.

    Dieser Test liest deshalb `ci.yml` direkt. Das Kriterium ist die `id`: sie
    vergibt man, um einen Schritt zu referenzieren — wer das tut, meint ein Gate
    und keine Infrastruktur.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    ohne_name = []
    mit_id = 0
    for job_name, job in (doc.get("jobs") or {}).items():
        for schritt in job.get("steps") or []:
            if not schritt.get("id"):
                continue
            mit_id += 1
            if not schritt.get("name"):
                ohne_name.append(f"{job_name}.{schritt['id']}")
    assert mit_id, "Kein Schritt traegt eine id — dieser Test lief ueber die leere Menge."
    assert not ohne_name, (
        f"Schritte mit id, aber ohne Namen — sie fallen aus ci_gates.py --list und aus dem lokalen Laeufer: {ohne_name}"
    )


def test_the_makefile_runs_what_the_one_list_runs() -> None:
    """W-6: nichts pinnte das Makefile, obwohl es Gate-Kommandos woertlich verdoppelt.

    `make test` und `make staleness` wiederholen, was in `ci.yml` als Gate steht.
    Aendert der Schritt dort seine Flags, driften die beiden lautlos auseinander —
    und lokal gruen zu sein, waehrend die CI rot ist, ist genau der Zustand, gegen
    den `verify_all.sh` argumentiert, indem es keine eigene Liste haelt.

    Verglichen wird die **ganze Rezeptzeile**, nicht ein Teilstring. Die erste
    Fassung dieses Tests fragte `befehl in makefile` und blieb gruen, als die
    Gegenprobe `--tb=short` anhaengte — ein angehaengtes Flag laesst den
    Teilstring stehen und ist genau die Drift, die hier auffallen soll.
    """
    zeilen = {
        z.strip() for z in (REPO_ROOT / "Makefile").read_text(encoding="utf-8").splitlines() if z.startswith("\t")
    }
    aus_ci = {g["command"] for g in gates() if g.get("command")}
    verdoppelt = {
        "python3 -m pytest tests/ -q": "make test",
        "python3 scripts/plans_registry.py --check": "make staleness",
    }
    fehlt = []
    for befehl, target in verdoppelt.items():
        if befehl not in zeilen:
            fehlt.append(f"{target}: keine Rezeptzeile lautet genau '{befehl}'")
        elif befehl not in aus_ci:
            fehlt.append(f"{target}: '{befehl}' steht nicht mehr in der einen Liste (ci.yml)")
    assert not fehlt, "Makefile und die eine Liste sind auseinandergelaufen:\n  " + "\n  ".join(fehlt)


def test_concurrency_group_carries_the_event() -> None:
    """Sonst toetet ein verspaeteter Lauf den, der die Suite ausfuehrt.

    Was uebrig bleibt, ist ein Lauf, gruen gemeldet, Suite nie gelaufen.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    gruppe = doc["concurrency"]["group"]
    assert "event_name" in gruppe, f"Concurrency-Gruppe ohne Event: {gruppe}"


# --------------------------------------------------------------------------
# 2 · Der lokale Runner haelt keine eigene Liste
# --------------------------------------------------------------------------


def test_runner_holds_no_command_list_of_its_own() -> None:
    """`verify_all.sh` darf die Pruefkommandos nicht selbst kennen.

    Gepinnt wird das negativ: Im Script darf kein Aufruf der geprueften Scripts
    stehen — mit genau einer Ausnahme, dem Aufruf von `ci_gates.py`, ueber den
    es die Liste bezieht.
    """
    text = RUNNER.read_text(encoding="utf-8")
    aufrufe = set(re.findall(r"scripts/([a-z_]+\.py)", text))
    assert aufrufe <= {"ci_gates.py"}, (
        f"verify_all.sh ruft Scripts direkt auf: {sorted(aufrufe - {'ci_gates.py'})}. "
        "Damit haelt es eine zweite Liste — genau die Drift, gegen die es geschrieben ist."
    )


def test_runner_reports_what_it_cannot_run() -> None:
    """Weglassen waere unsichtbar; ausweisen ist der Unterschied.

    Eine Liste, die verschweigt, was sie nicht abdeckt, liest sich wie
    Vollstaendigkeit.
    """
    nicht_lokal = [g for g in gates() if not g["local_runnable"]]
    assert nicht_lokal, "Erwartet: mindestens eine Marketplace-Action in der CI."

    ergebnis = subprocess.run(["bash", str(RUNNER), "--list"], cwd=REPO_ROOT, capture_output=True, text=True)
    assert ergebnis.returncode == 0, ergebnis.stderr
    for g in nicht_lokal:
        assert g["id"] in ergebnis.stdout, f"Der Runner verschweigt das Gate '{g['id']}', das er nicht fahren kann."


def test_no_second_verification_workflow() -> None:
    """Es gibt genau eine Verifikationsliste.

    Ein zweiter Workflow mit Pruefschritten waere eine konkurrierende Liste.
    Ein reiner Deploy-Pfad ist keine — er prueft nichts.
    """
    workflows = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
    mit_pruefschritten = []
    for wf in workflows:
        if wf.name == "ci.yml":
            continue
        doc = yaml.safe_load(wf.read_text(encoding="utf-8")) or {}
        for job in (doc.get("jobs") or {}).values():
            for step in job.get("steps", []):
                cmd = step.get("run", "")
                if "scripts/" in cmd or "pytest" in cmd:
                    mit_pruefschritten.append(f"{wf.name}: {cmd.strip()[:60]}")
    assert not mit_pruefschritten, "Pruefschritte ausserhalb von ci.yml gefunden — zweite Liste:\n  " + "\n  ".join(
        mit_pruefschritten
    )


# --------------------------------------------------------------------------
# 3 · Der Ausschluss der Vendoring-Oberflaeche haelt auch beim direkten Aufruf
# --------------------------------------------------------------------------


def test_formatter_exclusion_survives_an_explicit_path() -> None:
    """`exclude` allein filtert nur die Dateisuche, nicht das Argument.

    Wer `ruff format docs/patterns/contract_models.py` tippt, formatiert die
    vendorierte Datei trotz Ausschluss — so ist sie hier schon einmal
    umformatiert worden. Der Ausschluss war da, er galt nur nicht auf dem Weg,
    den ein Mensch nimmt.

    Geprueft wird deshalb das Verhalten, nicht der Konfigurationsstring: Der
    Formatter bekommt die ausgeschlossene Datei ausdruecklich genannt und darf
    sie trotzdem nicht anfassen.
    """
    ziel = REPO_ROOT / "docs" / "patterns" / "contract_models.py"
    assert ziel.is_file(), "Vorbedingung: die vendorierte Datei existiert."

    ergebnis = subprocess.run(
        ["ruff", "format", "--check", str(ziel)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert ergebnis.returncode == 0 and "Would reformat" not in ergebnis.stdout, (
        "Der Formatter sieht die ausgeschlossene Datei, weil sie ausdruecklich genannt "
        "wurde. In ruff.toml fehlt `force-exclude = true`."
    )


def test_a_local_equivalent_derives_its_arguments_from_the_action() -> None:
    """Das Ersatzkommando darf die Argumente der Action nicht wiederholen.

    Sonst gaebe es zwei Listen von Globs — dieselbe Drift, gegen die dieses
    ganze Modul gebaut ist, nur eine Ebene tiefer. Geprueft wird deshalb, dass
    jeder Glob aus der Action-Konfiguration auch im abgeleiteten Kommando steht:
    Aendert jemand die Globs in `ci.yml`, wandert der lokale Lauf mit.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    schritte = {s.get("id"): s for s in doc["jobs"]["verify"]["steps"] if s.get("id")}
    ersatz = [g for g in gates() if g.get("via_local_equivalent")]
    assert ersatz, "Kein Gate mit lokalem Aequivalent — dann prueft dieser Test nichts."

    for g in ersatz:
        konfig = schritte[g["id"]].get("with") or {}
        globs = [x.strip() for x in str(konfig.get("globs", "")).split("\n") if x.strip()]
        assert globs, f"Gate '{g['id']}' hat kein 'globs' in der Action — die Ableitung liefe ins Leere."
        for glob in globs:
            assert glob in g["command"], (
                f"Glob '{glob}' steht in der Action, aber nicht im lokalen Kommando von '{g['id']}'. "
                "Das Ersatzkommando muss aus der Action abgeleitet sein, nicht daneben gepflegt."
            )


def test_the_runner_still_admits_what_it_cannot_do_at_all() -> None:
    """Ein Ersatzwerkzeug ist nicht dasselbe wie der echte Schritt.

    Und ein Schritt, der fremde Server abfragt, hat gar kein lokales Aequivalent:
    Ein Lauf hier sagt etwas ueber die Netzverbindung, nicht ueber den Pull
    Request. Das muss der Runner weiterhin ausweisen — eine Liste, die
    verschweigt, was sie nicht abdeckt, liest sich wie Vollstaendigkeit.
    """
    gar_nicht = [g for g in gates() if not g["local_runnable"]]
    assert gar_nicht, "Erwartet: mindestens ein Schritt ohne lokales Aequivalent."
    ergebnis = subprocess.run(["bash", str(RUNNER), "--list"], cwd=REPO_ROOT, capture_output=True, text=True)
    assert ergebnis.returncode == 0, ergebnis.stderr
    for g in gar_nicht:
        assert g["id"] in ergebnis.stdout, f"Der Runner verschweigt '{g['id']}'."


def test_no_workflow_copies_a_whole_directory_into_a_publish_target() -> None:
    """Ein `cp -r` in ein Publish-Verzeichnis ist eine Veroeffentlichung ohne Auswahl.

    Der geloeschte Pages-Workflow tat genau das: `cp -r docs/presentations` in
    das Verzeichnis, das GitHub Pages ausliefert. Von den drei Decks dort trugen
    zwei den Klarnamen des Kunden. Der Workflow stand auf `workflow_dispatch` —
    also nicht tot, sondern einen Klick entfernt.

    Der Test verbietet nicht das Publizieren. Er verbietet die *Kopie ohne
    Auswahl*: was hinausgeht, wird benannt, nicht eingesammelt.
    """
    workflows = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
    assert workflows, "Vorbedingung: es gibt ueberhaupt Workflows."

    treffer: list[str] = []
    for wf in workflows:
        for nr, zeile in enumerate(wf.read_text(encoding="utf-8").splitlines(), 1):
            entkommentiert = zeile.split("#", 1)[0]
            if re.search(r"\bcp\s+-[a-zA-Z]*r", entkommentiert) and re.search(
                r"_site|public|gh-pages|dist", entkommentiert
            ):
                treffer.append(f"{wf.name}:{nr}  {zeile.strip()}")
    assert not treffer, (
        "Rekursive Kopie in ein Publish-Ziel:\n  "
        + "\n  ".join(treffer)
        + "\n\nStattdessen eine Allowlist benannter Dateien — und ein Gate, das die "
        "Denylist ueber das Publish-Verzeichnis faehrt, bevor etwas hochgeht."
    )


def test_the_archived_landing_page_is_not_wired_to_anything() -> None:
    """Archiviert heisst: kein Workflow, kein aktives Dokument zeigt noch darauf."""
    assert not (REPO_ROOT / ".github" / "workflows" / "publish-html.yml").exists()
    assert (REPO_ROOT / "docs" / "archive" / "pages-landing" / "index.html").is_file(), (
        "Die Landing-Page ist weg statt archiviert — dann fehlt der Beleg, wie sie aussah."
    )
    assert not (REPO_ROOT / "docs" / "index.html").exists()

    aktiv = [REPO_ROOT / "README.md", REPO_ROOT / "AGENTS.md", REPO_ROOT / "CLAUDE.md"]
    for datei in aktiv:
        text = datei.read_text(encoding="utf-8")
        assert "publish-html" not in text, f"{datei.name} nennt den geloeschten Workflow"
        assert "publiziert automatisch" not in text, (
            f"{datei.name} behauptet weiter eine automatische Veroeffentlichung"
        )


# --------------------------------------------------------------------------
# Der Drift-Job: die Gegenseite bewegt sich ohne Commit in diesem Repo
# --------------------------------------------------------------------------


def _scripts() -> list[Path]:
    ordner = REPO_ROOT / "scripts"
    kandidaten = list(ordner.glob("*.py")) + list(ordner.glob("*.sh"))
    return sorted(p for p in kandidaten if not p.name.startswith("test_"))


def _heimatlose_namen(namen: list[str], ci: str, runner: str, ohne_aufrufer: dict[str, str]) -> list[str]:
    """Die reine Entscheidung, getrennt von der Dateisuche — damit eine Gegenprobe

    echte Namen durchschicken kann, statt eine Zeichenkette im Quelltext dieser
    Testdatei zu suchen (Befund 11, Runde 2: der Glob sah acht Shell-Skripte
    nicht, und ein Test, der nur den Quelltext liest, haette das nicht gezeigt).
    """
    return [
        name
        for name in namen
        if f"scripts/{name}" not in ci and f"scripts/{name}" not in runner and name not in ohne_aufrufer
    ]


def test_every_script_has_a_caller_or_a_declared_reason() -> None:
    """Ein Werkzeug ohne Aufrufer ist von einem vergessenen nicht zu unterscheiden.

    Am 2026-08-14 hatten neun von einundzwanzig Scripts keinen — und nirgends
    stand, welche davon Absicht war. Seitdem gilt: jedes Script — `*.py` wie
    `*.sh` — steht entweder in einem `run:`-Schritt (`ci.yml`, beide Jobs) oder
    in `ci_gates.OHNE_AUFRUFER` mit einem Grund (RB-G3).

    `ci_gates.py` selbst ist der Aufrufer des lokalen Runners; es zaehlt als
    verdrahtet, sobald `verify_all.sh` es startet.
    """
    from ci_gates import OHNE_AUFRUFER

    ci = CI_FILE.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")

    heimatlos = _heimatlose_namen([p.name for p in _scripts()], ci, runner, OHNE_AUFRUFER)
    assert not heimatlos, (
        "Ohne Aufrufer und ohne Grund:\n  "
        + "\n  ".join(heimatlos)
        + "\n\nEntweder ein Schritt in ci.yml oder eine Zeile in ci_gates.OHNE_AUFRUFER."
    )


def test_an_orphan_shell_script_gets_flagged() -> None:
    """Die Gegenprobe zu Befund 11 (Runde 2).

    Faellt dieser Test, faengt die Sperrklinke ein `.sh`-Script ohne Aufrufer
    nicht ab — genau die Luecke, die den Befund ausgeloest hat. Der Name ist
    erfunden (wie bei `test_a_mere_mention_does_not_count_as_a_test` oben): ein
    echter Scriptname stuende woertlich in `ci.yml` oder `verify_all.sh` und
    wuerde die Probe zu einer, die nichts beweist.

    Absichtlich keine zweite Probe gegen den echten `scripts/`-Bestand daneben:
    `_scripts()` haengt an der Scriptmenge dieses Repos, die der Leerprobe
    (`scripts/kit/probe.py`) nicht mitreist (`manifest.yaml`: nur die explizit
    genannten Scripts sind `mechanismus`, der Rest ist `bestand`) — eine
    Realitaetsprobe haette dort ohne eigenes Verschulden rot geschlagen.
    """
    heimatlos = _heimatlose_namen(
        ["verwaistes_werkzeug.sh"],
        ci="",
        runner="",
        ohne_aufrufer={},
    )
    assert heimatlos == ["verwaistes_werkzeug.sh"], (
        "Ein .sh-Script ohne Aufrufer und ohne Grund muss durch dieselbe Pruefung "
        "fallen wie ein .py-Script — tut es das nicht, ist die Erweiterung auf "
        "*.sh nur behauptet, nicht wirksam."
    )


def test_the_glob_itself_finds_a_real_orphan_shell_script() -> None:
    """Die zweite Haelfte der Gegenprobe: nicht nur die Ableitung, auch der Glob.

    Der vorige Test schickt einen erfundenen Namen direkt durch
    `_heimatlose_namen()` — das beweist, dass die Entscheidung Endungen nicht
    unterscheidet, aber nicht, dass `_scripts()` ein `.sh` ueberhaupt SIEHT.
    Vor Befund 11 (Runde 2) glob'te `_scripts()` nur `*.py`; ein `.sh` waere in
    der Kandidatenliste nie angekommen, egal wie die Entscheidung ausgefallen
    waere.

    Deshalb hier ein echtes, aufruferloses `.sh` unter `scripts/` — angelegt und
    wieder geloescht innerhalb dieses Tests, damit nichts davon committet wird
    und die Leerprobe (`scripts/kit/probe.py`) nie einen Blick darauf bekommt:
    die kopiert nach `git ls-files`, eine ungetrackte Datei existiert fuer sie
    nicht.
    """
    ziel = REPO_ROOT / "scripts" / "verwaistes_werkzeug__test_ci_nie_committen.sh"
    ziel.write_text("#!/bin/sh\necho nie aufgerufen\n", encoding="utf-8")
    try:
        from ci_gates import OHNE_AUFRUFER

        ci = CI_FILE.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        heimatlos = _heimatlose_namen([p.name for p in _scripts()], ci, runner, OHNE_AUFRUFER)
        assert ziel.name in heimatlos, (
            f"{ziel.name} liegt unter scripts/, hat keinen Aufrufer und keinen "
            "deklarierten Grund — trotzdem meldet ihn die Pruefung nicht. Der "
            "Glob in _scripts() sieht keine *.sh-Dateien."
        )
    finally:
        ziel.unlink(missing_ok=True)


def test_no_declared_reason_stands_for_a_script_that_has_a_caller() -> None:
    """Die Gruende altern mit. Ein Grund neben einem verdrahteten Script luegt."""
    from ci_gates import OHNE_AUFRUFER

    ci = CI_FILE.read_text(encoding="utf-8")
    ueberholt = [n for n in OHNE_AUFRUFER if f"scripts/{n}" in ci]
    assert not ueberholt, f"laeuft laengst in der CI, traegt aber einen Grund: {ueberholt}"

    fehlend = [n for n in OHNE_AUFRUFER if not (REPO_ROOT / "scripts" / n).is_file()]
    assert not fehlend, f"Grund fuer ein Script, das es nicht gibt: {fehlend}"

    ohne_text = [n for n, grund in OHNE_AUFRUFER.items() if len(grund.strip()) < 10]
    assert not ohne_text, f"Grund ohne Inhalt: {ohne_text}"


# ---------------------------------------------------------------------------
# Die dritte Sperrklinke: ein Script ohne Test
#
# `OHNE_AUFRUFER` fragt, ob ein Script laeuft. `OHNE_MUTATIONSTEST` fragt, ob
# ein Gate rot werden kann. Keine der beiden fragt, ob ein Script ueberhaupt in
# einem Test vorkommt — und genau das war am 2026-09-08 bei sechs Scripts nicht
# der Fall, darunter zwei laufende Gates.
# ---------------------------------------------------------------------------

# Ein Import des Moduls oder ein Start als Unterprozess. Beides heisst: der Code
# wird ausgefuehrt. Ein Vorkommen des Namens in Prosa heisst das nicht.
#
# Gemessen wird ueber den Syntaxbaum, nicht ueber Textsuche — und der Grund dafuer
# ist eine Gegenprobe, die den ersten Entwurf widerlegt hat: der prueft "der Pfad
# kommt vor UND irgendwo in der Datei steht `subprocess`". Sobald
# `test_a_mere_mention_does_not_count_as_a_test` weiter unten den Pfad als
# Beispieltext saet, galt `build_sales_deck.py` als belegt — von genau dem Test,
# der beweisen sollte, dass Erwaehnung nicht zaehlt.
_IMPORT = "^[ \t]*(?:import {mod}\\b|from {mod} import)"


def _zeichenketten(baum: ast.Module) -> set[str]:
    """Jede Zeichenkette des Syntaxbaums — Kommentare stehen dort nicht drin.

    Genau das ist der Trick: die falschen Belege waren **Kommentare** — am
    2026-09-08 nannten `tests/test_dependencies.py` und `tests/test_human_gates.py`
    je ein Script nur in Prosa, und der naive Maszstab zaehlte das als Beleg.
    Ein Syntaxbaum kennt Kommentare nicht.

    Warum nicht enger, nur Zeichenketten *innerhalb eines Aufrufs*: das war der
    zweite Entwurf, und er verlor `export_schemas.py`. Dessen Test baut den Pfad
    segmentweise — `REPO_ROOT / "scripts" / "export_schemas.py"` —, das ist ein
    `BinOp`, kein `Call`. Dieselbe Schreibweise hat in diesem Repo schon einmal
    eine Pfad-Erkennung unterlaufen (siehe `_verzeichnisse_aus_quelltext`).
    """
    return {
        knoten.value for knoten in ast.walk(baum) if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)
    }


def _belegt(script: Path) -> list[str]:
    """Welche Testdateien fuehren dieses Script aus?

    Der Maszstab ist Ausfuehrung, nicht Erwaehnung. Der naive Maszstab
    (`script.name in text`) lieferte am 2026-09-08 zwei ungetestete Scripts statt
    sechs: `build_sales_deck.py` steht in einem Kommentar in
    `tests/test_dependencies.py`, `export_mermaid_assets.py` in einem in
    `tests/test_human_gates.py`. Kein Lauf beruehrt sie.
    """
    treffer: list[str] = []
    muster = re.compile(_IMPORT.format(mod=re.escape(script.stem)), re.M)
    erwartet = {script.name, f"scripts/{script.name}"}
    for datei in _testdateien():
        text = datei.read_text(encoding="utf-8")
        if muster.search(text):
            treffer.append(datei.name)
            continue
        if erwartet & _zeichenketten(ast.parse(text)):
            treffer.append(datei.name)
    return treffer


def test_every_script_has_a_test_or_a_declared_reason() -> None:
    """Ein Werkzeug ohne Test ist unsichtbar kaputt.

    Ohne Aufrufer faellt ein Script auf: es tut nichts. Ohne Test faellt es
    nicht auf — es tut moeglicherweise das Falsche, und niemand fuehrt es aus,
    um es zu merken. Deshalb dieselbe Regel wie bei den Aufrufern: entweder ein
    Test fuehrt es aus, oder es steht mit Grund in `ci_gates.OHNE_TEST`.
    """
    from ci_gates import OHNE_TEST

    ungehalten = [p.name for p in _scripts() if p.name not in OHNE_TEST and not _belegt(p)]
    assert not ungehalten, (
        "Ohne Test und ohne Grund:\n  "
        + "\n  ".join(ungehalten)
        + "\n\nEntweder eine Testdatei, die das Modul importiert oder es als "
        "Unterprozess startet, oder eine Zeile in ci_gates.OHNE_TEST."
    )


def test_a_mere_mention_does_not_count_as_a_test() -> None:
    """Die Gegenprobe zum Maszstab (AK-2).

    Eine Datei, die den Scriptnamen nur im Kommentar nennt, belegt nichts.
    Faellt dieser Test, ist der Maszstab auf Teilstring-Vorkommen
    zurueckgefallen — und dann meldet die Sperrklinke oben Vollstaendigkeit
    ueber einer Menge, die die ungetesteten Scripts gar nicht enthaelt.

    **Der Name ist erfunden.** Ein echter waere hier falsch: die erwarteten
    Zeichenketten stuenden dann woertlich in dieser Datei, `_belegt` faende sie
    im Syntaxbaum von `test_ci.py` — und das Script gaelte als belegt von dem
    Test, der beweisen soll, dass Erwaehnung nicht zaehlt. Genau so ist es beim
    zweiten Entwurf passiert.
    """
    name = "erfundenes_werkzeug.py"
    nur_erwaehnt = f"# scripts/{name} wird hier nur erwaehnt\nimport subprocess\nX = 1\n"
    ausgefuehrt = f"import subprocess\nsubprocess.run(['python3', 'scripts/{name}'])\n"
    segmentweise = f'from pathlib import Path\nSCRIPT = Path("scripts") / "{name}"\n'

    erwartet = {name, f"scripts/{name}"}
    assert not (erwartet & _zeichenketten(ast.parse(nur_erwaehnt))), (
        "Der Name steht nur im Kommentar, und `subprocess` steht in der Datei — "
        "trotzdem beruehrt nichts das Script. Das darf nicht als Beleg zaehlen."
    )
    assert erwartet & _zeichenketten(ast.parse(ausgefuehrt)), (
        "Ein echter Unterprozess-Aufruf muss als Beleg zaehlen, sonst ist der Maszstab wertlos."
    )
    assert erwartet & _zeichenketten(ast.parse(segmentweise)), (
        "Die segmentweise Schreibweise muss als Beleg zaehlen — an ihr ist der "
        "zweite Entwurf gescheitert (`export_schemas.py`)."
    )


def test_the_test_exemption_list_only_shrinks() -> None:
    """Drei ist der Stand vom 2026-09-08. Die Zahl darf fallen und nie steigen.

    Wer ein Script anlegt, schreibt seinen Test; wer einen der Gruende hier
    aufloest, streicht die Zeile. Ohne Deckel waere die Sperrklinke ein
    Ablagefach: jedes neue ungetestete Script bekaeme einen Eintrag, und alles
    bliebe gruen.
    """
    from ci_gates import OHNE_TEST

    assert len(OHNE_TEST) <= 3, (
        f"Die Ausnahmeliste ist auf {len(OHNE_TEST)} gewachsen. Ein neues Script "
        "braucht einen Test, keinen Eintrag hier."
    )


def test_no_declared_reason_stands_for_a_script_that_has_a_test() -> None:
    """Auch diese Gruende altern. Ein Grund neben einem getesteten Script luegt."""
    from ci_gates import OHNE_TEST

    ueberholt = {n: _belegt(REPO_ROOT / "scripts" / n) for n in OHNE_TEST}
    ueberholt = {n: t for n, t in ueberholt.items() if t}
    assert not ueberholt, f"hat laengst einen Test, traegt aber einen Grund: {ueberholt}"

    fehlend = [n for n in OHNE_TEST if not (REPO_ROOT / "scripts" / n).is_file()]
    assert not fehlend, f"Grund fuer ein Script, das es nicht gibt: {fehlend}"

    ohne_text = [n for n, grund in OHNE_TEST.items() if len(grund.strip()) < 10]
    assert not ohne_text, f"Grund ohne Inhalt: {ohne_text}"


# ---------------------------------------------------------------------------
# Gruende, die einen Vorgang nennen
# ---------------------------------------------------------------------------

BEAD_EXPORT = REPO_ROOT / ".beads" / "issues.jsonl"

# `wp-p3.7.1` oder `portfolio-agentic-engineering-wp-p3.7.1` — beide Formen
# kommen in den Gruenden vor. Die Katalog-Nummer `V-10` ist KEINE Vorgangs-ID;
# sie wird ueber den Titel-Praefix aufgeloest.
_VORGANG = re.compile(r"`(?:portfolio-agentic-engineering-)?([a-z0-9]+[a-z0-9.\-]*)`")
_KATALOG = re.compile(r"\bV-(\d{2})\b")


def _bead_status() -> dict[str, str]:
    """`id -> status` aus dem Export, als Datei gelesen.

    Nie ueber das Kommando `bd`: es schreibt die Datei bei jedem Aufruf zurueck,
    und die CI hat kein `bd` — dieselbe Begruendung wie in `plans_registry.py`.
    """
    zeilen = BEAD_EXPORT.read_text(encoding="utf-8").splitlines()
    status: dict[str, str] = {}
    titel: dict[str, str] = {}
    for zeile in zeilen:
        zeile = zeile.strip()
        if not zeile:
            continue
        try:
            satz = json.loads(zeile)
        except json.JSONDecodeError:
            continue
        if isinstance(satz, dict) and isinstance(satz.get("id"), str):
            status[satz["id"]] = str(satz.get("status", ""))
            if isinstance(satz.get("title"), str):
                titel[satz["id"]] = satz["title"]
    # Die Katalog-Nummern als Zweitschluessel: "V-10: ..." -> derselbe Zustand.
    for bid, t in titel.items():
        m = re.match(r"^V-(\d{2})\b", t)
        if m:
            status[f"V-{m.group(1)}"] = status[bid]
    return status


def test_no_declared_reason_cites_a_closed_or_unknown_bead() -> None:
    """Ein Grund, der auf einen geschlossenen Vorgang zeigt, haelt eine Ausnahme
    fuer jemanden offen, der nicht mehr da ist.

    Gemessen am 2026-09-08: `build_sales_deck.py` trug *„V-31 loescht ihn mit dem
    Deck-Pfad"*. V-31 war seit dem 2026-08-14 geschlossen — und hatte nie diesen
    Gegenstand, sondern `publish-html.yml` und die Landing-Seite. Die Ausnahme
    stand also auf einer Zusage, die niemand gegeben hatte.
    """
    from ci_gates import OHNE_AUFRUFER, OHNE_TEST

    assert BEAD_EXPORT.is_file(), (
        f"Bead-Export {BEAD_EXPORT.relative_to(REPO_ROOT)} fehlt — dann ist nicht ein "
        "Grund veraltet, sondern diese Pruefung misst nichts (RB-G7)."
    )
    status = _bead_status()
    assert status, "Bead-Export ist leer — die Pruefung misst nichts (RB-G7)."

    schlecht: list[str] = []
    for quelle, dct in (("OHNE_AUFRUFER", OHNE_AUFRUFER), ("OHNE_TEST", OHNE_TEST)):
        for name, grund in dct.items():
            zitiert = set(_VORGANG.findall(grund)) | {f"V-{n}" for n in _KATALOG.findall(grund)}
            for vid in zitiert:
                if vid not in status:
                    continue  # kein Vorgang, sondern ein Dateiname o.ae. — nicht hier pruefen
                if status[vid] == "closed":
                    schlecht.append(f"{quelle}[{name}] nennt {vid}, geschlossen")
    assert not schlecht, (
        "Grund zeigt auf einen geschlossenen Vorgang:\n  "
        + "\n  ".join(schlecht)
        + "\n\nEntweder den Grund berichtigen oder den Vorgang wieder oeffnen."
    )


def test_drift_job_runs_on_schedule_and_dispatch_only() -> None:
    """Der Timer ist die Erzwingung.

    Ein DRIFT-Check ohne `schedule:` ist ein Bericht: die Gegenseite bewegt sich
    ohne Commit in diesem Repo, also kann kein Pull Request ihn ausloesen
    (ADR-028 R2, RB-G3). Und umgekehrt darf der Job nicht an jedem PR haengen —
    er liest eine Aussenwelt, die der PR nicht veraendert hat.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    trigger = doc.get("on") or doc.get(True)
    assert "schedule" in trigger, "kein Timer — der Drift-Job kann nie laufen"
    assert trigger["schedule"], "leerer schedule-Block"
    assert "workflow_dispatch" in trigger, "kein Handstart fuer den Drift-Job"

    drift = doc["jobs"]["drift"]
    bedingung = drift["if"]
    assert "schedule" in bedingung and "workflow_dispatch" in bedingung, bedingung
    assert "push" not in bedingung and "pull_request" not in bedingung, (
        "Der Drift-Job haengt am Pull Request — dann bezahlt jeder PR fuer eine "
        "Messung ueber eine Aussenwelt, die er nicht veraendert hat."
    )

    verify = doc["jobs"]["verify"]
    assert "push" in verify["if"] and "pull_request" in verify["if"], (
        "Der Verifikations-Job muesste sonst auch am Timer laufen und waere dort ohne Aussage."
    )


def test_the_drift_job_runs_the_plans_registry_strictly() -> None:
    """Die zwei Lebenszyklus-Regeln haben ihren Zeitgeber.

    `plans_registry.py` meldet „gebaut und nicht archiviert" und eine
    einseitige Abloesung als DRIFT. Ohne einen Aufruf mit `--strict` bleibt
    das nach ADR-028 R2 ein Bericht statt eines Gates — dieser Test pinnt,
    dass genau dieser Aufruf im `drift`-Job steht.
    """
    treffer = [g for g in gates() if g["job"] == "drift" and "plans_registry.py" in (g["command"] or "")]
    assert treffer, "kein Schritt im drift-Job ruft plans_registry.py auf"
    assert any("--strict" in g["command"] for g in treffer), (
        "plans_registry.py laeuft im drift-Job, aber ohne --strict — dann bleiben "
        "die zwei Lebenszyklus-Regeln weiter unerreichbar fuer einen Exit ungleich 0."
    )


def test_the_drift_job_holds_only_steps_that_can_run() -> None:
    """Ein Schritt, der ohne Instanz-Checkout scheitert, macht den Job chronisch rot.

    Ein Job, der jeden Morgen rot ist, wird nicht gelesen — das ist derselbe
    Ausfall wie gar kein Job, nur mit Rauschen. Deshalb haelt `drift` heute nur,
    was hier laeuft; alles andere traegt einen Grund in `OHNE_AUFRUFER`.
    """
    drift_gates = [g for g in gates() if g["job"] == "drift" and not g["id"].startswith("drift-setup")]
    assert drift_gates, "der Drift-Job hat keinen einzigen Pruefschritt"
    for g in drift_gates:
        assert "oracle-source-inventory" not in g["command"], (
            f"{g['id']} braucht die Projekt-Instanz, die hier nicht ausgecheckt ist"
        )
        assert "--project-path" not in g["command"], f"{g['id']} braucht einen Instanz-Pfad"


# --------------------------------------------------------------------------
# Mutationsdeckung (RB-G4)
# --------------------------------------------------------------------------

# Ein Test, der nur assertiert, dass es heute gruen ist, prueft die Welt und
# nicht das Gate. Erst der Mutationstest sagt etwas ueber das Gate: **wird es
# rot, wenn man das kaputtmacht, wovor es schuetzen soll?**
#
# Diese Namensformen zaehlen als Mutationsnachweis. Die Liste ist absichtlich an
# Namen gebunden und nicht an Kommentare: ein Name wird beim Umbenennen
# mitgezogen, ein Kommentar nicht.
MUTATIONS_NAMEN = re.compile(
    r"^def (test_\w*(?:goes_red|red_on|detects_tampering|refuses|is_caught|catches|"
    r"not_a_write|is_an_error|is_exit_2|never_writes|is_not_a_pass|notices)\w*)\(",
    re.M,
)

# Gates ohne Mutationsnachweis — mit dem Grund und der Absicht.
#
# Diese Liste ist eine **Sperrklinke**: sie darf schrumpfen, nie wachsen. Wer
# ein Gate hinzufuegt, schreibt seinen Mutationstest; wer einen der Gruende hier
# aufloest, streicht die Zeile. Das Ventil `gate-mutation-coverage` traegt die
# Frist (RB-G4).
OHNE_MUTATIONSTEST: dict[str, str] = {
    "contract-template": "validate_contract.py hat ueberhaupt keine Tests (F-A-29, V-10)",
    "contract-examples": "dito — dieselbe Luecke, drei Aufrufe",
    "contract-mock": "dito — derselbe Pruefling, dritter Aufruf",
    "paradigm-catalog": "validate_paradigm_catalog.py hat keine Tests (F-A-29, V-10)",
    "catalog-test": "ist selbst ein Test — sein Mutationsgegenstueck waere ein Test ueber einen Test",
    "composer-test": "ist selbst ein Test; die Mutation liegt in tests/test_codegen_shared.py",
    "blueprint-roundtrip": "ist selbst ein Test; der Roundtrip ist seine eigene Mutation",
    "ruff-format": "fremdes Werkzeug mit eigener Testsuite; wir mutieren nicht dessen Formatierer",
    "ruff-check": "dito — die Auswahl der Regelgruppen haelt stattdessen ramp_valves.py",
    "pytest": "faehrt die Mutationstests selbst; ein Mutant dafuer waere zirkulaer",
    "markdownlint": "fremdes Werkzeug ueber eine Marketplace-Action; wir mutieren nicht dessen Regelwerk",
    "lychee": "dito, und advisory",
}


def test_the_mutation_exemption_list_only_shrinks() -> None:
    """W-8: die Sperrklinke, die der Kommentar verspricht und kein Test hielt.

    `OHNE_MUTATIONSTEST` fuehrt Gates, fuer die es kein Mutationsgegenstueck gibt.
    Der zugehoerige Test behauptet drei Dinge — keine Ausnahme fuer ein
    verschwundenes Gate, keine fuer ein bereits abgedecktes, keine Dublette —
    aber **nicht, dass die Liste nicht wachsen darf**. Wer ein neues Gate ohne
    Gegenprobe anlegt, traegt es ein, und alles bleibt gruen.

    Zwoelf ist der Stand vom 2026-09-07. Die Zahl darf fallen und nie steigen.
    """
    assert len(OHNE_MUTATIONSTEST) <= 12, (
        f"Die Ausnahmeliste ist auf {len(OHNE_MUTATIONSTEST)} gewachsen. Ein neues Gate "
        "braucht eine gesaete Gegenprobe, keinen Eintrag hier."
    )


def _testdateien() -> list[Path]:
    return sorted((REPO_ROOT / "tests").glob("test_*.py"))


def _pruefling(gate: dict) -> str:
    """Woran haengt dieses Gate — das Script, das es faehrt."""
    befehl = gate.get("command") or ""
    # Der Unterordner muss mit: bis zum 2026-09-08 endete das Muster vor dem
    # zweiten `/`, und ein Script unter `scripts/kit/` war fuer die Sperrklinke
    # unsichtbar — sie meldete "kein Script erkennbar" und verlangte eine
    # Ausnahme fuer ein Gate, das seinen Mutationsnachweis laengst hatte.
    m = re.search(r"(?:scripts|docs/patterns)/(?:[A-Za-z_]+/)*([A-Za-z_]+\.py)", befehl)
    if m:
        return m.group(1)
    # Ein Gate kann auch eine Testdatei selbst fahren — `ruleset-drift` prueft
    # eine Aussage ueber die Repo-Konfiguration, fuer die es kein Script gibt
    # und geben soll: ein Werkzeug, das Rulesets aendern kann, waere ein
    # groesseres Risiko als der Befund, den es findet. Seine Mutationsnachweise
    # liegen dann in genau dieser Datei, und dort sucht die Sperrklinke sie auch.
    m = re.search(r"(tests/[A-Za-z_]+\.py)", befehl)
    return m.group(1) if m else ""


def test_every_gate_step_has_a_mutation_test() -> None:
    """Jedes Gate hat einen Lauf, der es rot macht — oder einen Grund in der Sperrklinke.

    Gemessen am 2026-08-14: neun von einundzwanzig Schritten hatten keinen. Vier
    davon, weil ihr Werkzeug ueberhaupt keine Tests hatte.
    """
    quellen = {p: p.read_text(encoding="utf-8") for p in _testdateien()}

    ohne: list[str] = []
    for g in gates():
        gid = g["id"]
        if gid.endswith("setup-deps"):
            continue
        ziel = _pruefling(g)
        if not ziel:
            if gid not in OHNE_MUTATIONSTEST:
                ohne.append(f"{gid} (kein Script erkennbar)")
            continue
        if ziel.startswith("tests/"):
            # Faehrt das Gate eine Testdatei, liegen ihre Nachweise IN dieser
            # Datei. Die Suche unten wuerde stattdessen jede Datei akzeptieren,
            # die den Pfad nur ERWAEHNT — am 2026-09-08 machte das
            # `test_workflow_entry.py` zum Beleg fuer `ruleset-drift`, weil es
            # den Namen in einer Liste fuehrt und irgendeinen eigenen
            # Mutationsnachweis hat. Eine Deckung, die von einer Nennung
            # ausgeht, deckt nichts.
            datei = REPO_ROOT / ziel
            belegt = datei.is_file() and bool(MUTATIONS_NAMEN.search(datei.read_text(encoding="utf-8")))
        else:
            belegt = any(MUTATIONS_NAMEN.search(text) for p, text in quellen.items() if ziel in text)
        if not belegt and gid not in OHNE_MUTATIONSTEST:
            ohne.append(f"{gid} → {ziel}")

    assert not ohne, (
        "Gate ohne Mutationsnachweis und ohne Eintrag in der Sperrklinke:\n  "
        + "\n  ".join(ohne)
        + "\n\nEntweder einen `*_goes_red_when_*`-Test schreiben oder den Grund "
        "in OHNE_MUTATIONSTEST eintragen — beides ist eine Entscheidung, Schweigen nicht."
    )


def test_the_mutation_ratchet_only_turns_one_way() -> None:
    """Ein Eintrag in der Sperrklinke, dessen Gate laengst gedeckt ist, luegt.

    Und ein Eintrag fuer ein Gate, das es nicht mehr gibt, haelt eine Ausnahme
    fuer etwas offen, das niemand mehr faehrt.
    """
    quellen = {p: p.read_text(encoding="utf-8") for p in _testdateien()}
    bekannt = {g["id"]: g for g in gates()}

    verwaist = sorted(set(OHNE_MUTATIONSTEST) - set(bekannt))
    assert not verwaist, f"Ausnahme fuer ein Gate, das es nicht gibt: {verwaist}"

    ueberholt = []
    for gid in OHNE_MUTATIONSTEST:
        ziel = _pruefling(bekannt[gid])
        if ziel and any(MUTATIONS_NAMEN.search(t) for p, t in quellen.items() if ziel in t):
            ueberholt.append(gid)
    assert not ueberholt, f"laengst gedeckt, steht aber noch in der Sperrklinke: {ueberholt}"

    ohne_grund = [g for g, grund in OHNE_MUTATIONSTEST.items() if len(grund.strip()) < 10]
    assert not ohne_grund, f"Ausnahme ohne Grund: {ohne_grund}"
