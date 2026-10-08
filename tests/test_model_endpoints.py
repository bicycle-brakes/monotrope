"""Jedes genannte Modell loest gegen einen deklarierten Endpunkt auf (RB-A6).

**Die Luecke, die das schliesst.** `docs/WORKFLOW.md` regelt seit jeher, welches
Modell in welcher Phase laeuft. Wo es laeuft und was es sehen darf, stand bis
zum 2026-09-08 nirgends: `rg` ueber `docs/governance/` auf `residen|endpunkt|
datenabfluss` lieferte keinen einzigen normativen Treffer. Ein Agent konnte ein
Modell nennen, und niemand hielt den Namen gegen etwas.

Die Auflage ist nicht theoretisch. Kundencode traegt Struktur und Bezeichner des
Kunden — ein Modell, das ihn sieht, sieht das Datenmodell, auch ohne eine
einzige Zeile Nutzdaten.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ENDPUNKTE = REPO_ROOT / "model-endpoints.yaml"
AGENTEN = REPO_ROOT / ".claude" / "agents"
WORKFLOW = REPO_ROOT / "docs" / "WORKFLOW.md"
PROMPTS = REPO_ROOT / "prompts"

RESIDENZEN = ("anbieter-erklaert", "region-waehlbar", "nicht-erklaert")
ABRECHNUNGEN = ("token", "abonnement")


def _erklaerung() -> dict:
    """Die Erklaerung, defensiv geladen.

    Defensiv, weil `@pytest.mark.parametrize` beim **Sammeln** laeuft: eine
    kaputte oder leere Datei liess pytest bis zum 2026-09-08 mit einem
    `ValueError` beim Ermitteln der Test-ID abbrechen — und dann lief
    `test_the_declaration_is_not_empty`, das genau davor warnen soll, gar nicht
    erst. Ein Sammelfehler ist kein Befund, sondern ein blinder Fleck.
    """
    try:
        geladen = yaml.safe_load(ENDPUNKTE.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        geladen = {}
    if not isinstance(geladen, dict):
        geladen = {}
    # `setdefault` ersetzt ein vorhandenes `None` NICHT: steht in der Datei der
    # nackte Schluessel `endpunkte:` ohne Wert, liefert yaml `{"endpunkte": None}`,
    # und `parametrize(argvalues=None)` stirbt wieder beim Sammeln. Der Schluessel
    # ist da, der Wert fehlt — genau der Fall, den die Erstfassung uebersah.
    geladen["endpunkte"] = geladen.get("endpunkte") or []
    geladen["datenklassen"] = geladen.get("datenklassen") or {}
    if not isinstance(geladen["endpunkte"], list):
        geladen["endpunkte"] = []
    if not isinstance(geladen["datenklassen"], dict):
        geladen["datenklassen"] = {}
    return geladen


def prompt_modelle() -> list[tuple[Path, str]]:
    """Jeder Phasen-Prompt mit dem Modell, das er nennt.

    RB-A6 sagt "jedes Modell, das hier genannt wird". Bis zum 2026-09-08 las der
    Erzwinger nur `.claude/agents/` und die Routing-Tabelle — die sieben Prompts
    nannten sechs Modelle, die niemand gegen die Erklaerung hielt. Und
    `prompts/` reist als `mechanismus` mit: die Luecke waere mitgereist.
    """
    gefunden: list[tuple[Path, str]] = []
    if not PROMPTS.is_dir():
        return gefunden
    for p in sorted(PROMPTS.glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Der Punkt darf NICHT ausgeschlossen werden: "Fable 5.1" und
        # "Haiku 4.5" tragen ihn in der Version. Ein Regex, der ihn verbietet,
        # fand vier der sechs Prompts nicht — und haette gemeldet, alle
        # gefundenen loesten auf.
        #
        # Zweisprachig, seit die Prompts englisch sind (2026-09-10). Der alte
        # Regex kannte nur `**Modell:**`; nach der Uebersetzung haette er nichts
        # mehr gefunden, `parametrize` haette eine leere Liste bekommen — und
        # ein parametrisierter Test ueber einer leeren Liste ist GRUEN. Das Gate
        # waere im selben Commit ausgefallen, ohne dass etwas rot wird. Dagegen
        # steht zusaetzlich `test_prompts_are_found_at_all`.
        m = re.search(r"^\*\*(?:Modell|Model):\*\*\s*([^\n—]+?)\s*(?:—|\.\s*$|$)", text, re.M)
        if not m:
            continue
        wert = m.group(1).strip()
        # Phase 5 ist deterministisch und nennt ausdruecklich "keines" — das ist
        # eine Aussage, kein Modellname.
        if wert.lower().startswith(("keines", "keins", "kein ", "none")):
            continue
        gefunden.append((p, wert))
    return gefunden


def _endpunkt_ids(e: object) -> str:
    """Eine ID auch fuer einen kaputten Eintrag — sonst stirbt das Sammeln."""
    return e.get("name", "(ohne-name)") if isinstance(e, dict) else "(kein-mapping)"


def zugelassene_modelle() -> set[str]:
    return {m for e in _erklaerung()["endpunkte"] if isinstance(e, dict) for m in (e.get("modelle") or [])}


def agent_modelle() -> list[tuple[Path, str]]:
    """Jede Agent-Definition mit dem Modell, das sie pinnt."""
    gefunden: list[tuple[Path, str]] = []
    if not AGENTEN.is_dir():
        return gefunden
    for p in sorted(AGENTEN.glob("*.md")):
        # Auch diese Funktion laeuft zur Importzeit. Eine Datei, die nicht als
        # UTF-8 dekodiert, riss das Sammeln ab — und dann lief
        # `test_agents_are_found_at_all`, die Gegenprobe fuer genau diesen Fall,
        # nicht. Die eine Haelfte war gehaertet, diese nicht.
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        m = re.search(r"^model:\s*(\S+)\s*$", text, re.M)
        if m:
            gefunden.append((p, m.group(1)))
    return gefunden


# ---------------------------------------------------------------------------
# Die Menge ist nicht leer
# ---------------------------------------------------------------------------


def test_the_declaration_is_not_empty() -> None:
    """Eine leere Zulassungsliste laesst alles durch und prueft nichts (RB-G7)."""
    e = _erklaerung()
    assert e["endpunkte"], "kein einziger Endpunkt deklariert"
    assert e["datenklassen"], "keine einzige Datenklasse deklariert"
    assert zugelassene_modelle(), "kein einziges Modell zugelassen"


def test_prompts_are_found_at_all() -> None:
    """Ohne gefundene Prompts prueft der Test unten nichts (RB-G7).

    Die Luecke, die das schliesst: `prompt_modelle()` liest das Modell ueber
    einen Regex. Aendert sich die Schreibweise in den Prompts — bei der
    Uebersetzung ins Englische am 2026-09-10 tat sie das —, liefert die Funktion
    eine leere Liste. `@pytest.mark.parametrize` ueber einer leeren Liste ist
    gruen. Das Gate waere still ausgefallen, und zwar in genau dem Commit, der
    es haette rot machen muessen.

    Fuer die Agent-Definitionen gab es diese Gegenprobe seit jeher; fuer die
    Prompts fehlte sie.
    """
    gefunden = prompt_modelle()
    assert gefunden, (
        "kein einziger Phasen-Prompt nennt ein Modell — liest der Regex in "
        "`prompt_modelle()` noch die Schreibweise, die in prompts/ steht?"
    )
    # Sieben Phasen plus optionale Zwischenschritte; Phase 5 nennt ausdruecklich
    # keines. Die Untergrenze haelt fest, dass es um die Menge geht, nicht um
    # einen einzelnen Treffer.
    assert len(gefunden) >= 5, f"nur {len(gefunden)} Prompt(s) mit Modell gefunden"


def test_agents_are_found_at_all() -> None:
    """Ohne Agent-Definitionen prueft der Test unten nichts (RB-G7)."""
    assert agent_modelle(), "keine Agent-Definition mit `model:` gefunden — liest der Test das richtige Verzeichnis?"


# ---------------------------------------------------------------------------
# Die Erklaerung ist vollstaendig
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("endpunkt", _erklaerung()["endpunkte"], ids=_endpunkt_ids)
def test_every_endpoint_states_operator_residency_and_billing(endpunkt: object) -> None:
    """Ein Endpunkt ohne Betreiber ist ein Name, keine Zusage."""
    assert isinstance(endpunkt, dict), f"Eintrag ist kein Mapping: {endpunkt!r}"
    for feld in ("name", "betreiber", "residenz", "abrechnung", "darf_sehen", "modelle"):
        assert endpunkt.get(feld), f"{endpunkt.get('name')}: Feld '{feld}' fehlt oder ist leer"
    assert endpunkt["residenz"] in RESIDENZEN, (
        f"{endpunkt['name']}: residenz '{endpunkt['residenz']}' liegt ausserhalb von {RESIDENZEN}"
    )
    assert endpunkt["abrechnung"] in ABRECHNUNGEN, (
        f"{endpunkt['name']}: abrechnung '{endpunkt['abrechnung']}' liegt ausserhalb von {ABRECHNUNGEN}"
    )


@pytest.mark.parametrize("endpunkt", _erklaerung()["endpunkte"], ids=_endpunkt_ids)
def test_only_a_declared_data_class_may_be_seen(endpunkt: object) -> None:
    """`darf_sehen` benennt Klassen aus dem Vokabular, keine erfundenen."""
    assert isinstance(endpunkt, dict), f"Eintrag ist kein Mapping: {endpunkt!r}"
    bekannt = set(_erklaerung()["datenklassen"])
    fremd = set(endpunkt["darf_sehen"]) - bekannt
    assert not fremd, f"{endpunkt['name']}: unbekannte Datenklasse(n) {sorted(fremd)}"


def test_customer_code_never_reaches_an_endpoint_without_stated_residency() -> None:
    """Die eigentliche Auflage — und der Grund, warum diese Datei existiert.

    Kundencode traegt Struktur und Bezeichner des Kunden. Ein Endpunkt ohne
    erklaerte Residenz kann die Frage 'wo liegt das' nicht beantworten, und sie
    wird erst gestellt, wenn die Antwort teuer ist.
    """
    verletzer = [
        e.get("name")
        for e in _erklaerung()["endpunkte"]
        if isinstance(e, dict) and "kundencode" in (e.get("darf_sehen") or []) and e.get("residenz") == "nicht-erklaert"
    ]
    assert not verletzer, f"Endpunkt(e) ohne erklaerte Residenz, die Kundencode sehen duerfen: {verletzer}"


def test_no_endpoint_is_cleared_for_customer_rows() -> None:
    """Zeilen verlassen die Umgebung des Kunden nicht — keine Ausnahme, kein Anbieter."""
    verletzer = [
        e.get("name")
        for e in _erklaerung()["endpunkte"]
        if isinstance(e, dict) and "kundendaten" in (e.get("darf_sehen") or [])
    ]
    assert not verletzer, (
        f"Endpunkt(e) fuer Kundendaten freigegeben: {verletzer}. "
        "Die Maschine baut die Pipeline, sie liest die Daten nicht."
    )


# ---------------------------------------------------------------------------
# Jedes genannte Modell loest auf
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("pfad,modell", agent_modelle(), ids=lambda v: getattr(v, "name", str(v)))
def test_every_agent_model_resolves_to_a_declared_endpoint(pfad: Path, modell: str) -> None:
    """Nicht gelistet ist BLOCK — dieselbe Regel wie in den beiden Manifesten."""
    assert modell in zugelassene_modelle(), (
        f"{pfad.name} pinnt '{modell}', das in keinem Endpunkt von model-endpoints.yaml steht.\n"
        "Entweder den Endpunkt eintragen (mit Betreiber, Residenz und Abrechnungsart) "
        "oder das Modell wechseln."
    )


def _kandidaten(anzeige: str) -> set[str]:
    """Anzeigename ("Sonnet 5") auf moegliche IDs ("claude-sonnet-5").

    Two spellings of a version: dots turned into dashes (`claude-sonnet-5-5`,
    the id Anthropic gives) and dots kept (`glm-5.3`, `gpt-6.1-sol`, the ids
    other vendors give).
    """
    kern = anzeige.lower().replace(" ", "-").replace(".", "-")
    with_dots = anzeige.lower().replace(" ", "-")
    return {f"claude-{kern}", kern, with_dots, f"claude-{with_dots}"}


def _loest_auf(anzeige: str, ids: set[str]) -> bool:
    """Gleichheit, nicht Teilzeichenkette.

    `any(kern in i for i in ids)` liess "**Sonnet**" ohne Generation durchgehen,
    weil "sonnet" in "claude-sonnet-5" steckt — die Tabelle haette aufhoeren
    koennen, eine Generation zu nennen, und die Pruefung waere gruen geblieben.
    """
    return bool(_kandidaten(anzeige) & ids)


def routing_models(text: str) -> list[str]:
    """The model names of the routing rows in `text`.

    A routing row starts with a phase number and an optional letter (`2a`,
    `4b`), then a phase name of one or more words, then the model in bold. The
    pattern used to read one digit and one word, and skipped the rows a stage 2
    adds.
    """
    return re.findall(r"^\| \d[a-z]? [A-Za-z][A-Za-z ]*? \| \*\*([^*]+)\*\* \|", text, re.M)


def test_every_model_in_the_routing_table_resolves() -> None:
    """Auch die Doktrin nennt Modelle — und auch die muessen aufloesen.

    Sonst gilt die Regel fuer Agent-Definitionen und nicht fuer die Tabelle, aus
    der ein Mensch sein Modell waehlt.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    tabelle = routing_models(text)
    assert tabelle, "kein Modell im Routing von docs/WORKFLOW.md gefunden (RB-G7)"
    # Die Tabelle nennt Anzeigenamen ("Haiku 4.5"), die Erklaerung IDs.
    ids = zugelassene_modelle()
    for anzeige in tabelle:
        if anzeige == "the ladder":
            continue  # no model id: the ids live in the `opencode-go` entry, checked by its own test
        assert _loest_auf(anzeige, ids), (
            f"docs/WORKFLOW.md routet auf '{anzeige}', das in keinem Endpunkt steht. "
            f"Gesucht: {' oder '.join(sorted(_kandidaten(anzeige)))}"
        )


@pytest.mark.parametrize("pfad,anzeige", prompt_modelle(), ids=lambda v: getattr(v, "name", str(v)))
def test_every_model_in_a_phase_prompt_resolves(pfad: Path, anzeige: str) -> None:
    """Die sieben Prompts nennen Modelle — und `prompts/` reist als Mechanismus mit."""
    ids = zugelassene_modelle()
    assert _loest_auf(anzeige, ids), (
        f"{pfad.name} nennt '{anzeige}', das in keinem Endpunkt von model-endpoints.yaml steht. "
        f"Gesucht: {' oder '.join(sorted(_kandidaten(anzeige)))}"
    )


def test_a_dotted_id_resolves_and_a_prefix_does_not() -> None:
    """A display name with a dot resolves to the id that keeps it; a prefix does not."""
    assert _loest_auf("GLM 5.3", {"glm-5.3"})
    assert _loest_auf("gpt-6.1-sol", {"gpt-6.1-sol"})
    assert _loest_auf("Sonnet 5.5", {"claude-sonnet-5-5"})
    assert not _loest_auf("GLM 5", {"glm-5.3"}), "a prefix must not resolve by substring"


def test_the_routing_check_reads_lettered_and_multi_word_rows() -> None:
    """A row with a lettered phase or a phase name of several words is read."""
    text = "| 2a Spec review | **k3** | x |\n| 4b Review loop | **k3** | x |\n"
    assert routing_models(text) == ["k3", "k3"]
    assert routing_models("| 1 | Explore | x |\n") == []


# ---------------------------------------------------------------------------
# The opencode-go entry (stage2-mimo)
# ---------------------------------------------------------------------------


def _endpunkt(name: str) -> dict:
    """The one entry declared under `endpunkte:` with this name, or `{}`.

    Defensive like the declaration itself: a test over a missing entry must
    fail on its own assertion, not die on a `KeyError` the reader cannot place.
    """
    for e in _erklaerung()["endpunkte"]:
        if isinstance(e, dict) and e.get("name") == name:
            return e
    return {}


def test_the_opencode_go_entry_is_declared() -> None:
    """Criterion 1: the entry, its fields and the ladder order - refuted by any other value."""
    entry = _endpunkt("opencode-go")
    assert entry["betreiber"] == "OpenCode (Operator Anomaly Innovations, Inc.)"
    assert entry["residenz"] == "anbieter-erklaert"
    assert entry["abrechnung"] == "abonnement"
    assert entry["darf_sehen"] == ["framework"]
    assert entry["modelle"] == ["deepseek-v4.1-flash", "mimo-v2.6-flash", "mimo-v2.6-pro"]


def opencode_remark_problems(remark: str) -> list[str]:
    """Criterion 2: every point of the remark, each one stated by its source."""
    one = " ".join(remark.split())
    found = []
    for needle in (
        "https://opencode.ai/zen/go/v1/chat/completions",
        "https://opencode.ai/zen/go/v1/messages` is not used",
        "refused on 2026-10-08",
        "Pi at the version the runner pins",
        "lists Pi among its validated clients",
        "`x-opencode-session` header",
        '"automatically or programmatically extracts data or Output"',
        '"while you are not logged into the Services"',
        "effective 2026-08-15",
        "accepted this residual risk on 2026-10-08",
        "USD 10 a month",
        "deepseek-v4.1-flash` USD 0.15",
        "0.30 / 1.20",
        "limit USD 60",
        "mimo-v2.6-flash` 0.14 / 0.28, limit USD 60",
        "mimo-v2.6-pro` 0.435 / 0.87, limit USD 15",
        "0 days",
        '"Not used"',
        "valid through 2026-10-31",
        "states no region",
        '"All our models are hosted in the US and EU."',
        "read 2026-10-07",
        "phase 2a",
        "phase 4b",
        "phase 6",
        "scripts/stage2.py",
    ):
        if needle not in one:
            found.append(needle)
    return found


def test_the_opencode_go_remark_names_every_source() -> None:
    """Criterion 2: the remark says what OpenCode states, with its source and date."""
    remark = _endpunkt("opencode-go")["bemerkung"]
    assert opencode_remark_problems(remark) == []
    planted = remark.replace('"All our models are hosted in the US and EU."', "a region it does not name")
    assert opencode_remark_problems(planted)
    planted = remark.replace("valid through 2026-10-31", "renewed without end")
    assert opencode_remark_problems(planted)
    planted = remark.replace("refused on 2026-10-08", "accepted")
    assert opencode_remark_problems(planted)
    planted = remark.replace("lists Pi among its validated clients", "lists Claude Code as a validated client")
    assert opencode_remark_problems(planted)
    planted = remark.replace("accepted this residual risk on 2026-10-08", "saw no risk")
    assert opencode_remark_problems(planted)
    assert "Claude Code" not in remark and "native session header" not in remark


def _remark_problems(codex: str, glm: str) -> list[str]:
    """What criterion 3 requires of the two old reviewer remarks, as the problems found."""
    problems = []
    if "Used for the spec review (phase 2a) and the review (phase 6)" not in codex:
        problems.append("codex: the phases still routed to it")
    if "the review loop (phase 4b) moved to `opencode-go`" not in codex:
        problems.append("codex: the loop's move")
    if "No review phase routes to it" not in glm:
        problems.append("glm: no review phase")
    if "the review loop (phase 4b) moved to `opencode-go`" not in glm:
        problems.append("glm: the loop's move")
    if not ("stage2.py explore" in glm and "stage2.py implement" in glm):
        problems.append("glm: the work verbs")
    return problems


def test_no_old_reviewer_remark_claims_a_review_phase() -> None:
    """Criterion 3: each old entry says which phases, if any, still route to it."""
    codex = " ".join(_endpunkt("openai-codex")["bemerkung"].split())
    glm = " ".join(_endpunkt("glm-coding-plan")["bemerkung"].split())
    assert _remark_problems(codex, glm) == []
    planted = codex.replace("the review loop (phase 4b) moved to `opencode-go`", "runs every review as before")
    assert _remark_problems(planted, glm) == ["codex: the loop's move"]
