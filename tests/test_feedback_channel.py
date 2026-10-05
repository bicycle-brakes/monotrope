"""The feedback channel to the project instance keeps its own promises.

A handover is not a file but a promise in three parts: the finding is settled,
the way to it has been found, and at some point someone says what became of it.
If one of the three drops out, a note is left over — and that is exactly how
three learnings in the same convention stood for 77 to 92 days.

The sharpest test is `test_handover_records_are_immutable`. It recomputes the
hash over the finding block, and it is the reason the question *what did it
actually say when we agreed?* can still be answered later. A signature under a
text that changes afterwards is none.
"""

from __future__ import annotations

import hashlib
import re
import sys
from datetime import date
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

# The channel's status vocabulary — now taken from the schema, not typed next
# to it. Until 2026-09-08 it stood here a second time, on the grounds that a
# new value should not slip in unnoticed. Two lists do not prevent that; they
# only double the place where someone forgets to follow up.
STATUS = schema.STATUS

# The same reader for test and template. The local copy was moved to
# `scripts/handover_schema.py` on 2026-09-08 — the template needs it too.
frontmatter = schema.frontmatter


def record_of(text: str) -> str:
    """The block between the markers — what the hash covers."""
    return text.split(BEGIN, 1)[1].split(END, 1)[0]


def alle_uebergaben(directory: Path = HANDOVER_DIR) -> list[tuple[Path, dict[str, str], str]]:
    """Every file in the directory — without a filter.

    The difference from `project_handovers()` is the whole point of this
    change: `project_handovers()` filters on `direction`, and on 2026-09-08
    **14 of 24** files did not carry that field at all. They therefore fell out
    of every check, and the suite was green over a set that did not contain the
    unchecked files.
    """
    gefunden = []
    for pfad in sorted(directory.glob("*.md")):
        text = pfad.read_text(encoding="utf-8")
        gefunden.append((pfad, frontmatter(text), text))
    return gefunden


def project_handovers(directory: Path = HANDOVER_DIR) -> list[tuple[Path, dict[str, str], str]]:
    return [t for t in alle_uebergaben(directory) if t[1].get("direction") == "framework->project"]


def fehlende_kanalpflicht(text: str) -> list[str]:
    """Which mandatory channel fields the handover does not carry.

    Reads `schema.PROJEKT_PFLICHT` **on every call**. That is not a quirk but
    the condition under which the counter-check below can prove anything at
    all: a copied-out list cannot be extended from outside, and that is exactly
    why one would not notice that it is a copy. Until 2026-09-08 a hard-coded
    tuple stood here, while nobody read the constant in the schema.
    """
    return sorted(schema.PROJEKT_PFLICHT - schema.belegte_felder(text))


def fehlende_gemeinsame(text: str) -> list[str]:
    """Which of the fields are missing that, according to the schema, **every** handover carries."""
    return sorted(schema.GEMEINSAM - schema.belegte_felder(text))


@pytest.mark.skip(
    reason="2ee triage 2026-09-19: gilt-erst-mit-bestand — the project channel "
    "(framework->project) begins with lakeswitch joining (O-2, M2 gate). Deadline 2026-12-31."
)
def test_the_channel_is_not_empty() -> None:
    """An empty set is not a result (RB-G7).

    Without this test every following one would run green over zero files, and
    a deleted folder would look like a fulfilled contract.
    """
    assert project_handovers(), (
        "Not a single file with direction: framework->project found. "
        "Either the channel is gone or the frontmatter field is named differently."
    )


@pytest.mark.parametrize("path,fields,_text", project_handovers(), ids=lambda v: getattr(v, "name", ""))
def test_every_project_handover_declares_direction_target_and_status(
    path: Path, fields: dict[str, str], _text: str
) -> None:
    """Against which state, with what result, under whose responsibility."""
    fehlend = fehlende_kanalpflicht(_text)
    assert not fehlend, (
        f"{path.name}: mandatory channel field(s) missing or empty: {', '.join(fehlend)}. "
        f"What is required is what stands in schema.PROJEKT_PFLICHT — add them there, not here."
    )
    # The next and the last assertion message stay German on purpose: the skipped mutation test
    # `test_the_checks_go_red_when_the_contract_is_broken` matches them by text ("liegt ausserhalb",
    # "kein kurzer Commit-Hash"). Translate message and pattern together.
    assert fields["status"] in STATUS, f"{path.name}: status '{fields['status']}' liegt ausserhalb von {STATUS}"
    assert fields["provenance"] == "ai-drafted-reviewed", (
        f"{path.name}: a handover raised by the framework is ai-drafted-reviewed, not '{fields['provenance']}'"
    )
    assert re.fullmatch(r"[0-9a-f]{8}", fields["target_ref"]), (
        f"{path.name}: target_ref '{fields['target_ref']}' ist kein kurzer Commit-Hash — "
        "ohne pruefbaren Stand ist kein Befund nachrechenbar"
    )


@pytest.mark.parametrize("path,_fields,text", alle_uebergaben(), ids=lambda v: getattr(v, "name", ""))
def test_every_handover_carries_the_common_fields(path: Path, _fields: dict[str, str], text: str) -> None:
    """`GEMEINSAM` says "every handover carries" — until today nobody checks that.

    The upper bound existed (`test_no_handover_carries_an_unknown_field`
    forbids what is not in `ERLAUBT`), the lower one did not. Measured on
    2026-09-08 that cost three files: `2026-04-29-adwaive-onepager.md` without
    `tags`, the two `2026-06-01-*` without `created`. A set that is only bounded
    from above is not a promise but a ceiling.
    """
    fehlend = fehlende_gemeinsame(text)
    assert not fehlend, (
        f"{path.name}: field(s) missing that, according to schema.GEMEINSAM, every handover carries: {', '.join(fehlend)}"
    )


@pytest.mark.parametrize("path,fields,text", project_handovers(), ids=lambda v: getattr(v, "name", ""))
def test_handover_records_are_immutable(path: Path, fields: dict[str, str], text: str) -> None:
    """The finding block matches the hash the frontmatter claims."""
    assert BEGIN in text and END in text, f"{path.name}: record markers missing"
    digest = "sha256:" + hashlib.sha256(record_of(text).encode()).hexdigest()
    # German on purpose: the skipped mutation test matches "der Record wurde nach der Uebergabe geaendert".
    assert fields["record_sha256"] == digest, (
        f"{path.name}: der Record wurde nach der Uebergabe geaendert.\n"
        f"  Frontmatter: {fields['record_sha256']}\n"
        f"  Tatsaechlich: {digest}\n"
        "Ein Befund wird nicht ueberschrieben, sondern unter 'Rueckmeldungen' widerlegt."
    )


@pytest.mark.parametrize("path,fields,_text", project_handovers(), ids=lambda v: getattr(v, "name", ""))
def test_acknowledged_handover_names_who_and_when(path: Path, fields: dict[str, str], _text: str) -> None:
    """Acknowledged means: a human with a name, at a point in time — and not the
    same one who approved the handover. Whoever acknowledges their own result
    acknowledges nothing."""
    if fields["status"] == "pending":
        for key in ("acknowledged_by", "acknowledged_at", "closed_at"):
            assert fields.get(key) == "null", f"{path.name}: status is pending, but {key} is set"
        return
    for key in ("acknowledged_by", "acknowledged_at"):
        assert fields.get(key) not in (None, "", "null"), (
            f"{path.name}: status is {fields['status']}, but {key} is missing"
        )
    assert fields["acknowledged_by"] != fields.get("review.approved_by"), (
        f"{path.name}: {fields['acknowledged_by']} approved the handover and "
        "acknowledges it themselves — that is not feedback, that is a loop"
    )
    if fields["status"] == "closed":
        assert fields.get("closed_at") not in (None, "", "null"), (
            f"{path.name}: status is closed, but closed_at is missing"
        )


def test_journal_index_lists_every_open_project_handover() -> None:
    """A handover that the index does not know will be picked up by nobody."""
    index = JOURNAL_INDEX.read_text(encoding="utf-8")
    for path, fields, _ in project_handovers():
        if fields["status"] == "closed":
            continue
        assert path.name in index, f"{path.name} is open but does not appear in docs/journal/_INDEX.md"


@pytest.mark.skip(
    reason="2ee triage 2026-09-19: gilt-erst-mit-bestand — the condition has occurred "
    "(three handovers since 2026-09-16), but docs/_INDEX.md, the entry point, is still missing. Deadline 2026-11-30."
)
def test_root_index_routes_to_the_project_feedback() -> None:
    """The entry point knows the way — otherwise only those who already know it find it."""
    index = ROOT_INDEX.read_text(encoding="utf-8")
    linked = [p.name for p, _, _ in project_handovers() if p.name in index]
    assert linked, (
        "docs/_INDEX.md links not a single handover. The situation table is "
        "the only place where someone without prior knowledge finds them."
    )


@pytest.mark.skip(
    reason="2ee triage 2026-09-19: bestand-dieses-repos — framework-witt-feedback-loop.md "
    "lives in the origin repository; valve until port or transfer. Deadline 2026-11-30."
)
def test_the_feedback_loop_documents_the_reverse_direction() -> None:
    """The convention stands where the reverse direction already stands — not next to it."""
    text = FEEDBACK_LOOP.read_text(encoding="utf-8")
    assert "## 7. Gegenrichtung" in text, (
        "framework-witt-feedback-loop.md describes only the path instance -> framework"
    )
    for token in ("direction: framework->project", "record_sha256", "acknowledged"):
        assert token in text, f"§7 does not name '{token}'"


@pytest.mark.skip(
    reason="2ee triage 2026-09-19: bestand-dieses-repos — framework-witt-feedback-loop.md "
    "lives in the origin repository; valve until port or transfer. Deadline 2026-11-30."
)
def test_the_framework_does_not_claim_to_write_into_the_instance() -> None:
    """The asymmetry is the core of the channel and must be stated explicitly."""
    text = FEEDBACK_LOOP.read_text(encoding="utf-8")
    section = text.split("## 7. Gegenrichtung", 1)[1]
    assert "nichts in die Instanz" in section, (
        "§7 does not say that the framework does not write into the instance — "
        "that is exactly the condition under which this channel exists at all"
    )


# --- Mutations: the tests above must go red when someone breaks the contract ---


@pytest.mark.parametrize(
    "mutation,expected",
    [
        ("record", "der Record wurde nach der Uebergabe geaendert"),
        ("status", "liegt ausserhalb"),
        ("target_ref", "kein kurzer Commit-Hash"),
    ],
)
@pytest.mark.skip(
    reason="2ee triage 2026-09-19: bestand-dieses-repos — the fixtures are "
    "portfolio handovers (2026-08-14-osi-plan-register); valve until own "
    "fixtures or kit transfer. Deadline 2026-11-30."
)
def test_the_checks_go_red_when_the_contract_is_broken(tmp_path: Path, mutation: str, expected: str) -> None:
    """Tampers with a copy and asserts that the check catches it.

    The copy is the point: a test that mutates the working tree is itself an
    entry in the error catalogue (F-A-28).
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


@pytest.mark.skip(
    reason="2ee triage 2026-09-19: bestand-dieses-repos — framework-witt-feedback-loop.md "
    "lives in the origin repository; valve until port or transfer. Deadline 2026-11-30."
)
def test_the_route_check_goes_red_when_the_route_is_removed() -> None:
    """Removes the route from a copy of the index and expects red."""
    stripped = "\n".join(
        line for line in ROOT_INDEX.read_text(encoding="utf-8").splitlines() if "2026-08-14-osi-" not in line
    )
    assert not [p.name for p, _, _ in project_handovers() if p.name in stripped], (
        "The index without the route still links a handover — then "
        "test_root_index_routes_to_the_project_feedback does not check what it claims to check"
    )


@pytest.mark.parametrize(
    "konstante,leser",
    [("PROJEKT_PFLICHT", fehlende_kanalpflicht), ("GEMEINSAM", fehlende_gemeinsame)],
)
def test_the_field_checks_read_the_schema_instead_of_a_copy(
    monkeypatch: pytest.MonkeyPatch, konstante: str, leser: object
) -> None:
    """Seeded counter-check against the second field list — the finding of 2026-09-08.

    `PROJEKT_PFLICHT` stood in the schema and was read by **nobody**: the check
    carried its own hard-coded tuple. Both lists could drift apart without
    anything turning red — whoever had changed the constant would have changed
    nothing about the checked behaviour. That is exactly the second list that
    AK-6 forbids, only with the roles swapped: it was not the old one that was
    stale, the new one was dead.

    The probe appends a field to the constant that no handover carries. If the
    reader stays silent, it does not read the constant but a copy.
    """
    erfunden = "erfundenes_pflichtfeld"
    monkeypatch.setattr(schema, konstante, getattr(schema, konstante) | {erfunden})
    _, _, text = alle_uebergaben()[0]
    assert erfunden in leser(text), (
        f"schema.{konstante} extended by '{erfunden}' and the check stays silent — "
        "it reads a copied-out list, not the schema"
    )


# ---------------------------------------------------------------------------
# What holds for EVERY handover
#
# The six checks above see only `framework->project`. On 2026-09-08 that was 7
# of 24 files — nobody checked the other 17, because they did not carry the
# field that is filtered on at all.
# ---------------------------------------------------------------------------


@pytest.mark.skip(
    reason="2ee triage 2026-09-19: bestand-dieses-repos — the ≥20 claim measures the "
    "stock of the origin repository. The 2ee-Abschluss valve occurred on 2026-09-20; "
    "the corpus here (three handovers) does not yet carry the quantity claim. "
    "Deadline 2026-12-31 — the corpus is what counts, not the calendar."
)
def test_every_handover_declares_a_direction() -> None:
    """Without `direction` a handover silently drops out of every check.

    The quantity claim comes first and is not an extra (RB-G7): if the directory
    pointed to zero files, all following statements would be green and
    worthless anyway. Exactly this form of green is the reason for the change.
    """
    alle = alle_uebergaben()
    assert len(alle) >= 20, f"only {len(alle)} handovers found — does the test read the right directory?"

    ohne = [p.name for p, f, _ in alle if not f.get("direction")]
    assert not ohne, (
        "Handover without `direction`:\n  "
        + "\n  ".join(ohne)
        + "\n\nWithout the field `project_handovers()` filters it out, and no "
        "check of the channel ever sees it."
    )


def test_direction_comes_from_the_closed_set() -> None:
    """A third value would be a new kind of document — that is a decision."""
    falsch = [
        f"{p.name}: {f['direction']}" for p, f, _ in alle_uebergaben() if f.get("direction") not in schema.RICHTUNGEN
    ]
    assert not falsch, f"direction outside of {schema.RICHTUNGEN}: {falsch}"


def test_no_handover_carries_an_unknown_field() -> None:
    """A field name that nobody holds against a list is silent.

    Measured on 2026-09-08 the stock contained `date:` instead of `created:`
    and `beads:` instead of `bead:` — once each, each unnoticed. Both are
    deliberately not in `ERLAUBT`.
    """
    unbekannt: list[str] = []
    for pfad, _, text in alle_uebergaben():
        for feld in sorted(schema.oberste_felder(text) - schema.ERLAUBT):
            unbekannt.append(f"{pfad.name}: {feld}")
    assert not unbekannt, (
        "Unknown frontmatter field:\n  " + "\n  ".join(unbekannt) + "\n\nEither a typo, or the field belongs in "
        "`scripts/handover_schema.py` — both are a decision."
    )


def test_only_a_project_handover_carries_the_channel_contract() -> None:
    """The strict contract belongs to the channel.

    A `record_sha256` on a session handover claims a promise that nobody is
    waiting for — and obscures which documents are really in the channel.
    """
    daneben: list[str] = []
    for pfad, felder, text in alle_uebergaben():
        if felder.get("direction") == "framework->project":
            continue
        for feld in sorted(schema.oberste_felder(text) & schema.KANAL_EXKLUSIV):
            daneben.append(f"{pfad.name}: {feld}")
    assert not daneben, f"channel field on a handover outside the channel: {daneben}"


# ---------------------------------------------------------------------------
# The template
# ---------------------------------------------------------------------------


def test_the_template_exists_and_names_both_directions() -> None:
    assert TEMPLATE.is_file(), "templates/handover.md is missing — the contract is only memory again"
    text = TEMPLATE.read_text(encoding="utf-8")
    for richtung in schema.RICHTUNGEN:
        assert richtung in text, f"the template does not explain `{richtung}`"


def _vorlagen_bloecke() -> list[str]:
    """The YAML blocks of the template.

    The template carries its schema in code blocks and **not** as real
    frontmatter — `provenance.yaml:213` sets `frontmatter: none` for
    `templates/`, because a frontmatter in a template would be copied into every
    instance. For checking, each block is read as if it were one.
    """
    text = TEMPLATE.read_text(encoding="utf-8")
    bloecke = re.findall(r"```yaml\n(.*?)```", text, re.S)
    return ["---\n" + b + "---\n" for b in bloecke]


def test_the_template_satisfies_the_schema_it_documents() -> None:
    """A template that violates its own schema teaches the error.

    The first block is the common head: it carries every mandatory field. No
    block may name a field that `ERLAUBT` does not know.
    """
    bloecke = _vorlagen_bloecke()
    assert bloecke, "the template contains no ```yaml block — then it shows no schema"

    felder_gesamt: set[str] = set()
    for block in bloecke:
        felder_gesamt |= schema.oberste_felder(block)

    fehlend = sorted(schema.GEMEINSAM - felder_gesamt)
    assert not fehlend, f"the template leaves out mandatory fields: {fehlend}"
    unbekannt = sorted(felder_gesamt - schema.ERLAUBT)
    assert not unbekannt, f"the template names fields that the schema does not know: {unbekannt}"


def test_the_template_carries_no_real_frontmatter() -> None:
    """`provenance.yaml` requires `frontmatter: none` for `templates/`.

    A template with real frontmatter is copied into every instance and carries
    a provenance claim there that nobody has checked.
    """
    text = TEMPLATE.read_text(encoding="utf-8")
    assert not text.startswith("---\n"), "the template starts with real frontmatter — it belongs in a ```yaml block"


def test_the_template_explains_what_the_hash_covers() -> None:
    """The only part that can be done wrong without anyone noticing."""
    text = TEMPLATE.read_text(encoding="utf-8")
    assert schema.RECORD_BEGIN.strip() in text and schema.RECORD_END in text, (
        "the template does not show the record markers"
    )
    assert "record_sha256" in text


@pytest.mark.skip(
    reason="2ee triage 2026-09-19: bestand-dieses-repos — framework-witt-feedback-loop.md "
    "lives in the origin repository; valve until port or transfer. Deadline 2026-11-30."
)
def test_the_feedback_loop_points_at_the_schema_instead_of_repeating_it() -> None:
    """Two field lists are one too many — the second is always the stale one."""
    text = FEEDBACK_LOOP.read_text(encoding="utf-8")
    assert "scripts/handover_schema.py" in text, (
        "§7 does not name the valid field list; then the prose is the list, and it ages"
    )


# ---------------------------------------------------------------------------
# Decay (review #13, 2026-09-21): a skip without a deadline is an exception
# without decay. Every marker above carries a deadline — the sentinel recomputes
# that it is there, readable in the reason, and not yet exceeded.
# ---------------------------------------------------------------------------

_SKIP_FRISTEN: dict[str, str] = {
    "test_the_channel_is_not_empty": "2026-12-31",
    "test_root_index_routes_to_the_project_feedback": "2026-11-30",
    "test_the_feedback_loop_documents_the_reverse_direction": "2026-11-30",
    "test_the_framework_does_not_claim_to_write_into_the_instance": "2026-11-30",
    "test_the_checks_go_red_when_the_contract_is_broken": "2026-11-30",
    "test_the_route_check_goes_red_when_the_route_is_removed": "2026-11-30",
    "test_every_handover_declares_a_direction": "2026-12-31",
    "test_the_feedback_loop_points_at_the_schema_instead_of_repeating_it": "2026-11-30",
}


def test_every_skip_here_carries_a_future_expiry_date() -> None:
    """An expired reason reads like a living decision (RB-P5)."""
    quelle = Path(__file__).read_text(encoding="utf-8")
    bloecke = {
        name: block
        for block, name in re.findall(r"@pytest\.mark\.skip\(\s*reason=(.*?)\)\s*\ndef (\w+)", quelle, re.DOTALL)
    }
    assert set(bloecke) == set(_SKIP_FRISTEN), (
        "Skip markers and deadline list differ — marker without entry: "
        f"{sorted(set(bloecke) - set(_SKIP_FRISTEN))}; entry without marker: "
        f"{sorted(set(_SKIP_FRISTEN) - set(bloecke))}"
    )
    ohne_datum = {name for name, block in bloecke.items() if _SKIP_FRISTEN[name] not in block}
    assert not ohne_datum, (
        f"The deadline of {sorted(ohne_datum)} stands only in the list, not in the reason — "
        "whoever reads the skip must see the date."
    )
    abgelaufen = {name: frist for name, frist in _SKIP_FRISTEN.items() if date.fromisoformat(frist) <= date.today()}
    assert not abgelaufen, (
        "These skips are past their deadline — resolve them (let the test run) "
        f"or move the deadline in a reviewed change: {abgelaufen}"
    )
