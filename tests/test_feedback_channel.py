"""Der Rueckkanal zur Projekt-Instanz haelt seine eigenen Zusagen.

Eine Uebergabe ist keine Datei, sondern ein Versprechen mit drei Teilen: der
Befund steht fest, der Weg dorthin ist gefunden, und irgendwann sagt jemand, was
daraus geworden ist. Faellt eines der drei weg, bleibt eine Notiz uebrig — und
genau so haben in derselben Konvention drei Learnings 77 bis 92 Tage gestanden.

Der schaerfste Test ist `test_handover_records_are_immutable`. Er rechnet den
Hash ueber den Befundblock nach, und er ist der Grund, warum die Frage *was stand
da eigentlich, als wir zugestimmt haben?* spaeter noch beantwortbar ist. Eine
Unterschrift unter einem Text, der sich danach aendert, ist keine.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
HANDOVER_DIR = REPO_ROOT / "docs" / "journal" / "handover"
ROOT_INDEX = REPO_ROOT / "docs" / "_INDEX.md"
JOURNAL_INDEX = REPO_ROOT / "docs" / "journal" / "_INDEX.md"
FEEDBACK_LOOP = REPO_ROOT / "docs" / "governance" / "framework-witt-feedback-loop.md"
TEMPLATE = REPO_ROOT / "templates" / "handover.md"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import handover_schema as schema  # noqa: E402

BEGIN = schema.RECORD_BEGIN
END = schema.RECORD_END

# Das Statusvokabular des Kanals — jetzt aus dem Schema, nicht daneben getippt.
# Bis zum 2026-09-08 stand es hier ein zweites Mal, mit der Begruendung, ein
# neuer Wert solle nicht unbemerkt einwandern. Zwei Listen verhindern das aber
# nicht, sie verdoppeln nur die Stelle, an der jemand vergisst nachzuziehen.
STATUS = schema.STATUS

# Derselbe Leser fuer Test und Vorlage. Die lokale Kopie ist am 2026-09-08 nach
# `scripts/handover_schema.py` gezogen — die Vorlage braucht sie auch.
frontmatter = schema.frontmatter


def record_of(text: str) -> str:
    """Der Block zwischen den Markern — das, was der Hash abdeckt."""
    return text.split(BEGIN, 1)[1].split(END, 1)[0]


def alle_uebergaben(directory: Path = HANDOVER_DIR) -> list[tuple[Path, dict[str, str], str]]:
    """Jede Datei im Verzeichnis — ohne Filter.

    Der Unterschied zu `project_handovers()` ist der ganze Punkt dieser
    Aenderung: `project_handovers()` filtert auf `direction`, und am 2026-09-08
    trugen **14 von 24** Dateien dieses Feld gar nicht. Sie fielen damit aus
    jeder Pruefung heraus, und die Suite war gruen ueber einer Menge, die die
    ungeprueften Dateien nicht enthielt.
    """
    gefunden = []
    for pfad in sorted(directory.glob("*.md")):
        text = pfad.read_text(encoding="utf-8")
        gefunden.append((pfad, frontmatter(text), text))
    return gefunden


def project_handovers(directory: Path = HANDOVER_DIR) -> list[tuple[Path, dict[str, str], str]]:
    return [t for t in alle_uebergaben(directory) if t[1].get("direction") == "framework->project"]


def fehlende_kanalpflicht(text: str) -> list[str]:
    """Welche Pflichtfelder des Kanals die Uebergabe nicht traegt.

    Liest `schema.PROJEKT_PFLICHT` **bei jedem Aufruf**. Das ist keine Marotte,
    sondern die Bedingung, unter der die Gegenprobe unten ueberhaupt etwas
    beweisen kann: eine abgeschriebene Liste laesst sich nicht von aussen
    erweitern, und genau daran wuerde man nicht merken, dass sie abgeschrieben
    ist. Bis zum 2026-09-08 stand hier ein hartkodiertes Tupel, waehrend die
    Konstante im Schema von niemandem gelesen wurde.
    """
    return sorted(schema.PROJEKT_PFLICHT - schema.belegte_felder(text))


def fehlende_gemeinsame(text: str) -> list[str]:
    """Welche der Felder fehlen, die laut Schema **jede** Uebergabe traegt."""
    return sorted(schema.GEMEINSAM - schema.belegte_felder(text))


def test_the_channel_is_not_empty() -> None:
    """Eine leere Menge ist kein Ergebnis (RB-G7).

    Ohne diesen Test wuerde jeder folgende gruen ueber null Dateien laufen, und
    ein geloeschter Ordner saehe aus wie ein erfuellter Vertrag.
    """
    assert project_handovers(), (
        "Keine einzige Datei mit direction: framework->project gefunden. "
        "Entweder ist der Kanal weg oder das Frontmatter-Feld heisst anders."
    )


@pytest.mark.parametrize("path,fields,_text", project_handovers(), ids=lambda v: getattr(v, "name", ""))
def test_every_project_handover_declares_direction_target_and_status(
    path: Path, fields: dict[str, str], _text: str
) -> None:
    """Gegen welchen Stand, mit welchem Ergebnis, unter wessen Verantwortung."""
    fehlend = fehlende_kanalpflicht(_text)
    assert not fehlend, (
        f"{path.name}: Pflichtfeld(er) des Kanals fehlen oder sind leer: {', '.join(fehlend)}. "
        f"Verlangt wird, was in schema.PROJEKT_PFLICHT steht — dort nachtragen, nicht hier."
    )
    assert fields["status"] in STATUS, f"{path.name}: status '{fields['status']}' liegt ausserhalb von {STATUS}"
    assert fields["provenance"] == "ai-drafted-reviewed", (
        f"{path.name}: eine vom Framework erhobene Uebergabe ist ai-drafted-reviewed, nicht '{fields['provenance']}'"
    )
    assert re.fullmatch(r"[0-9a-f]{8}", fields["target_ref"]), (
        f"{path.name}: target_ref '{fields['target_ref']}' ist kein kurzer Commit-Hash — "
        "ohne pruefbaren Stand ist kein Befund nachrechenbar"
    )


@pytest.mark.parametrize("path,_fields,text", alle_uebergaben(), ids=lambda v: getattr(v, "name", ""))
def test_every_handover_carries_the_common_fields(path: Path, _fields: dict[str, str], text: str) -> None:
    """`GEMEINSAM` sagt "traegt jede Uebergabe" — bis heute prueft das niemand.

    Die obere Schranke gab es (`test_no_handover_carries_an_unknown_field`
    verbietet, was nicht in `ERLAUBT` steht), die untere nicht. Gemessen am
    2026-09-08 kostete das drei Dateien: `2026-04-29-adwaive-onepager.md` ohne
    `tags`, die beiden `2026-06-01-*` ohne `created`. Eine Menge, die man nur
    nach oben begrenzt, ist keine Zusage, sondern eine Obergrenze.
    """
    fehlend = fehlende_gemeinsame(text)
    assert not fehlend, (
        f"{path.name}: Feld(er) fehlen, die laut schema.GEMEINSAM jede Uebergabe traegt: {', '.join(fehlend)}"
    )


@pytest.mark.parametrize("path,fields,text", project_handovers(), ids=lambda v: getattr(v, "name", ""))
def test_handover_records_are_immutable(path: Path, fields: dict[str, str], text: str) -> None:
    """Der Befundblock deckt sich mit dem Hash, den das Frontmatter behauptet."""
    assert BEGIN in text and END in text, f"{path.name}: Record-Marker fehlen"
    digest = "sha256:" + hashlib.sha256(record_of(text).encode()).hexdigest()
    assert fields["record_sha256"] == digest, (
        f"{path.name}: der Record wurde nach der Uebergabe geaendert.\n"
        f"  Frontmatter: {fields['record_sha256']}\n"
        f"  Tatsaechlich: {digest}\n"
        "Ein Befund wird nicht ueberschrieben, sondern unter 'Rueckmeldungen' widerlegt."
    )


@pytest.mark.parametrize("path,fields,_text", project_handovers(), ids=lambda v: getattr(v, "name", ""))
def test_acknowledged_handover_names_who_and_when(path: Path, fields: dict[str, str], _text: str) -> None:
    """Quittiert heisst: ein Mensch mit Namen, zu einem Zeitpunkt — und nicht derselbe,
    der die Uebergabe abgenommen hat. Wer sein eigenes Ergebnis quittiert, quittiert nichts."""
    if fields["status"] == "pending":
        for key in ("acknowledged_by", "acknowledged_at", "closed_at"):
            assert fields.get(key) == "null", f"{path.name}: status ist pending, aber {key} ist gesetzt"
        return
    for key in ("acknowledged_by", "acknowledged_at"):
        assert fields.get(key) not in (None, "", "null"), (
            f"{path.name}: status ist {fields['status']}, aber {key} fehlt"
        )
    assert fields["acknowledged_by"] != fields.get("review.approved_by"), (
        f"{path.name}: {fields['acknowledged_by']} hat die Uebergabe abgenommen und "
        "quittiert sie selbst — das ist keine Rueckmeldung, das ist eine Schleife"
    )
    if fields["status"] == "closed":
        assert fields.get("closed_at") not in (None, "", "null"), (
            f"{path.name}: status ist closed, aber closed_at fehlt"
        )


def test_journal_index_lists_every_open_project_handover() -> None:
    """Eine Uebergabe, die der Index nicht kennt, wird niemand abholen."""
    index = JOURNAL_INDEX.read_text(encoding="utf-8")
    for path, fields, _ in project_handovers():
        if fields["status"] == "closed":
            continue
        assert path.name in index, f"{path.name} ist offen, steht aber nicht in docs/journal/_INDEX.md"


def test_root_index_routes_to_the_project_feedback() -> None:
    """Der Einstieg kennt den Weg — sonst findet ihn nur, wer ihn schon kennt."""
    index = ROOT_INDEX.read_text(encoding="utf-8")
    linked = [p.name for p, _, _ in project_handovers() if p.name in index]
    assert linked, (
        "docs/_INDEX.md verlinkt keine einzige Uebergabe. Die Situationstabelle ist "
        "der einzige Ort, an dem jemand ohne Vorwissen sie findet."
    )


def test_the_feedback_loop_documents_the_reverse_direction() -> None:
    """Die Konvention steht dort, wo die Gegenrichtung schon steht — nicht daneben."""
    text = FEEDBACK_LOOP.read_text(encoding="utf-8")
    assert "## 7. Gegenrichtung" in text, "framework-witt-feedback-loop.md beschreibt nur den Weg Instanz -> Framework"
    for token in ("direction: framework->project", "record_sha256", "acknowledged"):
        assert token in text, f"§7 nennt '{token}' nicht"


def test_the_framework_does_not_claim_to_write_into_the_instance() -> None:
    """Die Asymmetrie ist der Kern des Kanals und muss ausgesprochen sein."""
    text = FEEDBACK_LOOP.read_text(encoding="utf-8")
    section = text.split("## 7. Gegenrichtung", 1)[1]
    assert "nichts in die Instanz" in section, (
        "§7 sagt nicht, dass das Framework in der Instanz nicht schreibt — "
        "genau das ist die Bedingung, unter der dieser Kanal ueberhaupt existiert"
    )


# --- Mutationen: die Tests oben muessen rot werden, wenn jemand den Vertrag bricht ---


@pytest.mark.parametrize(
    "mutation,expected",
    [
        ("record", "der Record wurde nach der Uebergabe geaendert"),
        ("status", "liegt ausserhalb"),
        ("target_ref", "kein kurzer Commit-Hash"),
    ],
)
def test_the_checks_go_red_when_the_contract_is_broken(tmp_path: Path, mutation: str, expected: str) -> None:
    """Manipuliert eine Kopie und behauptet, dass die Pruefung sie faengt.

    Die Kopie ist der Punkt: ein Test, der den Arbeitsbaum mutiert, ist selbst ein
    Eintrag im Fehler-Katalog (F-A-28).
    """
    source = HANDOVER_DIR / "2026-08-14-osi-plan-register.md"
    text = source.read_text(encoding="utf-8")
    if mutation == "record":
        text = text.replace("48 Plaene", "47 Plaene", 1)
    elif mutation == "status":
        text = text.replace("status: pending", "status: erledigt", 1)
    else:
        text = text.replace("target_ref: d5e52138", "target_ref: HEAD", 1)

    copy = tmp_path / source.name
    copy.write_text(text, encoding="utf-8")
    ((path, fields, mutated),) = project_handovers(tmp_path)

    with pytest.raises(AssertionError, match=expected):
        if mutation == "record":
            test_handover_records_are_immutable(path, fields, mutated)
        else:
            test_every_project_handover_declares_direction_target_and_status(path, fields, mutated)


def test_the_route_check_goes_red_when_the_route_is_removed() -> None:
    """Nimmt die Route aus einer Kopie des Index und erwartet Rot."""
    stripped = "\n".join(
        line for line in ROOT_INDEX.read_text(encoding="utf-8").splitlines() if "2026-08-14-osi-" not in line
    )
    assert not [p.name for p, _, _ in project_handovers() if p.name in stripped], (
        "Der Index ohne die Route verlinkt immer noch eine Uebergabe — dann prueft "
        "test_root_index_routes_to_the_project_feedback nicht, was es zu pruefen vorgibt"
    )


@pytest.mark.parametrize(
    "konstante,leser",
    [("PROJEKT_PFLICHT", fehlende_kanalpflicht), ("GEMEINSAM", fehlende_gemeinsame)],
)
def test_the_field_checks_read_the_schema_instead_of_a_copy(
    monkeypatch: pytest.MonkeyPatch, konstante: str, leser: object
) -> None:
    """Gesaete Gegenprobe gegen die zweite Feldliste — der Befund vom 2026-09-08.

    `PROJEKT_PFLICHT` stand im Schema und wurde von **niemandem** gelesen: die
    Pruefung trug ihr eigenes hartkodiertes Tupel. Beide Listen konnten
    auseinanderlaufen, ohne dass etwas rot wurde — wer die Konstante geaendert
    haette, haette am gepruefte Verhalten nichts geaendert. Das ist genau die
    zweite Liste, die AK-6 verbietet, nur mit vertauschten Rollen: nicht die
    alte war veraltet, die neue war tot.

    Die Probe haengt ein Feld an die Konstante, das keine Uebergabe traegt.
    Bleibt der Leser stumm, liest er die Konstante nicht, sondern eine Kopie.
    """
    erfunden = "erfundenes_pflichtfeld"
    monkeypatch.setattr(schema, konstante, getattr(schema, konstante) | {erfunden})
    _, _, text = alle_uebergaben()[0]
    assert erfunden in leser(text), (
        f"schema.{konstante} um '{erfunden}' erweitert und die Pruefung bleibt stumm — "
        "sie liest eine abgeschriebene Liste, nicht das Schema"
    )


# ---------------------------------------------------------------------------
# Was fuer JEDE Uebergabe gilt
#
# Die sechs Pruefungen oben sehen nur `framework->project`. Am 2026-09-08 waren
# das 7 von 24 Dateien — die anderen 17 pruefte niemand, weil sie das Feld, auf
# das gefiltert wird, gar nicht trugen.
# ---------------------------------------------------------------------------


def test_every_handover_declares_a_direction() -> None:
    """Ohne `direction` faellt eine Uebergabe stillschweigend aus jeder Pruefung.

    Die Mengen-Behauptung steht zuerst und ist kein Beiwerk (RB-G7): zeigte das
    Verzeichnis auf null Dateien, waeren alle folgenden Aussagen gruen und
    trotzdem wertlos. Genau diese Form von Gruen ist der Anlass der Aenderung.
    """
    alle = alle_uebergaben()
    assert len(alle) >= 20, f"nur {len(alle)} Uebergaben gefunden — liest der Test das richtige Verzeichnis?"

    ohne = [p.name for p, f, _ in alle if not f.get("direction")]
    assert not ohne, (
        "Uebergabe ohne `direction`:\n  "
        + "\n  ".join(ohne)
        + "\n\nOhne das Feld filtert `project_handovers()` sie heraus, und keine "
        "Pruefung des Kanals sieht sie je."
    )


def test_direction_comes_from_the_closed_set() -> None:
    """Ein dritter Wert waere eine neue Sorte Dokument — das ist eine Entscheidung."""
    falsch = [
        f"{p.name}: {f['direction']}" for p, f, _ in alle_uebergaben() if f.get("direction") not in schema.RICHTUNGEN
    ]
    assert not falsch, f"Richtung ausserhalb von {schema.RICHTUNGEN}: {falsch}"


def test_no_handover_carries_an_unknown_field() -> None:
    """Ein Feldname, den niemand gegen eine Liste haelt, ist stumm.

    Gemessen am 2026-09-08 standen im Bestand `date:` statt `created:` und
    `beads:` statt `bead:` — je einmal, je unbemerkt. Beide sind absichtlich
    nicht in `ERLAUBT`.
    """
    unbekannt: list[str] = []
    for pfad, _, text in alle_uebergaben():
        for feld in sorted(schema.oberste_felder(text) - schema.ERLAUBT):
            unbekannt.append(f"{pfad.name}: {feld}")
    assert not unbekannt, (
        "Unbekanntes Frontmatter-Feld:\n  "
        + "\n  ".join(unbekannt)
        + "\n\nEntweder ein Tippfehler, oder das Feld gehoert nach "
        "`scripts/handover_schema.py` — beides ist eine Entscheidung."
    )


def test_only_a_project_handover_carries_the_channel_contract() -> None:
    """Der strenge Vertrag gehoert dem Kanal.

    Ein `record_sha256` an einer Sitzungsuebergabe behauptet eine Zusage, auf die
    niemand wartet — und verschleiert, welche Dokumente wirklich im Kanal sind.
    """
    daneben: list[str] = []
    for pfad, felder, text in alle_uebergaben():
        if felder.get("direction") == "framework->project":
            continue
        for feld in sorted(schema.oberste_felder(text) & schema.KANAL_EXKLUSIV):
            daneben.append(f"{pfad.name}: {feld}")
    assert not daneben, f"Kanal-Feld an einer Uebergabe ausserhalb des Kanals: {daneben}"


# ---------------------------------------------------------------------------
# Die Vorlage
# ---------------------------------------------------------------------------


def test_the_template_exists_and_names_both_directions() -> None:
    assert TEMPLATE.is_file(), "templates/handover.md fehlt — der Vertrag ist wieder nur Erinnerung"
    text = TEMPLATE.read_text(encoding="utf-8")
    for richtung in schema.RICHTUNGEN:
        assert richtung in text, f"die Vorlage erklaert `{richtung}` nicht"


def _vorlagen_bloecke() -> list[str]:
    """Die YAML-Bloecke der Vorlage.

    Die Vorlage traegt ihr Schema in Codebloecken und **nicht** als echtes
    Frontmatter — `provenance.yaml:213` setzt fuer `templates/` `frontmatter:
    none`, weil ein Frontmatter in einer Vorlage in jede Instanz mitkopiert
    wuerde. Zum Pruefen wird der Block gelesen, als waere er eines.
    """
    text = TEMPLATE.read_text(encoding="utf-8")
    bloecke = re.findall(r"```yaml\n(.*?)```", text, re.S)
    return ["---\n" + b + "---\n" for b in bloecke]


def test_the_template_satisfies_the_schema_it_documents() -> None:
    """Eine Vorlage, die ihr eigenes Schema verletzt, lehrt den Fehler.

    Der erste Block ist der gemeinsame Kopf: er traegt jedes Pflichtfeld. Kein
    Block darf ein Feld nennen, das `ERLAUBT` nicht kennt.
    """
    bloecke = _vorlagen_bloecke()
    assert bloecke, "die Vorlage enthaelt keinen ```yaml-Block — dann zeigt sie kein Schema"

    felder_gesamt: set[str] = set()
    for block in bloecke:
        felder_gesamt |= schema.oberste_felder(block)

    fehlend = sorted(schema.GEMEINSAM - felder_gesamt)
    assert not fehlend, f"die Vorlage laesst Pflichtfelder aus: {fehlend}"
    unbekannt = sorted(felder_gesamt - schema.ERLAUBT)
    assert not unbekannt, f"die Vorlage nennt Felder, die das Schema nicht kennt: {unbekannt}"


def test_the_template_carries_no_real_frontmatter() -> None:
    """`provenance.yaml` verlangt fuer `templates/` `frontmatter: none`.

    Eine Vorlage mit echtem Frontmatter wird in jeder Instanz mitkopiert und
    traegt dort eine Provenienz-Behauptung, die niemand geprueft hat.
    """
    text = TEMPLATE.read_text(encoding="utf-8")
    assert not text.startswith("---\n"), (
        "die Vorlage beginnt mit echtem Frontmatter — es gehoert in einen ```yaml-Block"
    )


def test_the_template_explains_what_the_hash_covers() -> None:
    """Der einzige Teil, den man falsch machen kann, ohne dass es auffaellt."""
    text = TEMPLATE.read_text(encoding="utf-8")
    assert schema.RECORD_BEGIN.strip() in text and schema.RECORD_END in text, (
        "die Vorlage zeigt die record-Marker nicht"
    )
    assert "record_sha256" in text


def test_the_feedback_loop_points_at_the_schema_instead_of_repeating_it() -> None:
    """Zwei Feldlisten sind eine zu viel — die zweite ist immer die veraltete."""
    text = FEEDBACK_LOOP.read_text(encoding="utf-8")
    assert "scripts/handover_schema.py" in text, (
        "§7 nennt die geltende Feldliste nicht; dann ist die Prosa die Liste, und sie altert"
    )
