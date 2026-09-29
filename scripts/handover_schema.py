"""Das Schema der Uebergaben — die eine Feldliste, aus der Test und Vorlage lesen.

Der Rueckkanal ist der einzige Weg, auf dem Wissen zwischen den Repositorien
fliesst: das Framework darf in eine Projekt-Instanz nicht schreiben
(ADR-011/015), also legt es eine Uebergabe ab und wartet auf die Quittung.

Bis zum 2026-09-08 wurde dieser Vertrag **gelebt, aber nirgends aufgeschrieben**.
Die Folge war messbar: 14 von 24 Uebergaben trugen kein `direction`-Feld, und
`project_handovers()` filtert genau darauf — sie fielen damit aus jeder Pruefung
des Kanals heraus. Die Testsuite war gruen ueber einer Menge, die die
ungeprueften Dateien nicht enthielt.

**Warum das hier steht und nicht im Test.** Weil auch die Vorlage
(`templates/handover.md`) dieselbe Liste braucht. Stuende sie im Test, gaebe es
sie zweimal — und die zweite Liste ist immer die, die veraltet.
"""

from __future__ import annotations

# Wer eine Uebergabe empfaengt. Geschlossen: ein dritter Wert waere eine neue
# Sorte Dokument und braucht eine Entscheidung, keinen stillen Eintrag.
#
#   framework->framework  Sitzungsuebergabe in diesem Repo. Niemand wartet auf
#                         eine Quittung; der leichte Vertrag genuegt.
#   framework->project    Der Kanal. Traegt Ziel, Stand, unveraenderlichen
#                         Befundblock und Quittungsfelder. Nur das Projektteam
#                         setzt `acknowledged` und `closed` — per Pull Request
#                         in dieses Repo.
RICHTUNGEN: tuple[str, ...] = ("framework->framework", "framework->project")

# Felder, die JEDE Uebergabe traegt.
GEMEINSAM: frozenset[str] = frozenset(
    {
        "title",
        "category",
        "created",
        "direction",
        "provenance",
        "produced_by",
        "tags",
    }
)

# Der Kanal-Vertrag. Nur bei `direction: framework->project` zulaessig.
#
# **Gemessen am 2026-09-08, und die erste Fassung dieser Menge war falsch.** Sie
# fuehrte auch `target_repo`, `target_ref`, `status`, `bead`, `review` und
# `disclosure` als kanal-exklusiv — der Test schlug daraufhin an sieben
# Sitzungsuebergaben an, die diese Felder voellig zu Recht tragen: auch eine
# Sitzungsuebergabe beschreibt einen Stand (`target_ref`), haengt an einem
# Vorgang (`bead`) und hat einen Zustand (`status`).
#
# Exklusiv ist nur, was die Zusage traegt: der Hash ueber den unveraenderlichen
# Befundblock und die drei Quittungsfelder. Sie an einer Sitzungsuebergabe zu
# fuehren behauptet ein Versprechen, auf das niemand wartet.
KANAL_EXKLUSIV: frozenset[str] = frozenset(
    {
        "record_sha256",
        # Setzt das Projektteam, nicht das Framework.
        "acknowledged_by",
        "acknowledged_at",
        "closed_at",
    }
)

# Was eine Uebergabe im Kanal zusaetzlich VERLANGT (nicht nur darf).
PROJEKT_PFLICHT: frozenset[str] = frozenset({"target_repo", "target_ref", "status", "bead", "record_sha256"})

# Zulaessig in beiden Richtungen, nirgends verlangt. Alles hier ist im Bestand
# belegt — die Menge ist gemessen, nicht ausgedacht.
OPTIONAL: frozenset[str] = frozenset(
    {
        "last_reviewed",
        # The date of the last change. Optional here because a handover outside a
        # `required` prefix does not need one; under the prefixes that are held,
        # `scripts/check_frontmatter_current.py` requires it (bead coding-harness-qd7).
        "updated",
        "related",
        "source",
        "source_workflow",
        "session",
        "maturity",
        "audience",
        "reading_time_min",
        # Auch eine Sitzungsuebergabe beschreibt einen Stand, haengt an einem
        # Vorgang und hat einen Zustand. Siehe den Kommentar ueber KANAL_EXKLUSIV.
        "target_repo",
        "target_ref",
        "status",
        "bead",
        "review",
        "disclosure",
        # Die Kennzahlen des Ablaufs (2026-09-10). Sie sind optional, weil eine
        # Uebergabe ohne Phasenlauf keine hat — aber wo sie stehen, sind sie die
        # einzige Grundlage, auf der die Doktrin sich korrigieren kann. Ohne sie
        # bleibt jede Aussage ueber Gate-Wirkung eine Erwartung.
        "review_rounds",  # Runden bis sauber
        "fix_regen_rounds",  # davon Befunde mit Origin `fix-r<N>` — die Schleife gegen sich selbst
        "late_findings",  # nach dem Commit gefunden; konstante Klassen aendern Gates, nicht das Bauchgefuehl
        "questions",  # gestellte Menschenfragen, nach Klasse
    }
)

# Ausdruecklich NICHT aufgenommen, obwohl im Bestand gefunden: `date` (einmal,
# gemeint war `created`) und `beads` (einmal, gemeint war `bead`). Beide waren
# stumm, weil niemand die Namen gegen eine Liste hielt — sie sollen auffallen.
# Am 2026-09-08 in `2026-04-29-adwaive-onepager.md` berichtigt.
ERLAUBT: frozenset[str] = GEMEINSAM | KANAL_EXKLUSIV | OPTIONAL

# Das Statusvokabular des Kanals.
STATUS: tuple[str, ...] = ("pending", "acknowledged", "closed")

# Die Marker, ueber die `record_sha256` rechnet. Der Befundblock dazwischen ist
# unveraenderlich (RB-P5); Widerspruch kommt darunter, nie hinein.
RECORD_BEGIN = "<!-- record:begin -->\n"
RECORD_END = "<!-- record:end -->"


def frontmatter(text: str) -> dict[str, str]:
    """Liest die flachen Schluessel des Frontmatters.

    Verschachtelte Bloecke (`review:`, `produced_by:`) werden mit ihrem Praefix
    aufgenommen — `review.status` statt `status`. Ohne diese Trennung wuerde der
    Review-Status den Uebergabe-Status ueberschreiben, und beide heissen `status`.
    """
    if not text.startswith("---\n"):
        return {}
    block = text.split("---\n", 2)[1]
    felder: dict[str, str] = {}
    eltern = None
    for zeile in block.splitlines():
        if not zeile.strip() or zeile.lstrip().startswith("#"):
            continue
        eingerueckt = zeile.startswith((" ", "\t"))
        schluessel, _, wert = zeile.strip().partition(":")
        wert = wert.strip().strip('"')
        if eingerueckt and eltern:
            felder[f"{eltern}.{schluessel.strip()}"] = wert
        else:
            eltern = schluessel.strip() if not wert else None
            felder[schluessel.strip()] = wert
    return felder


def oberste_felder(text: str) -> set[str]:
    """Nur die Schluessel der obersten Ebene — die, gegen die `ERLAUBT` prueft.

    Ein verschachtelter Schluessel wie `review.status` gehoert seinem Elternfeld
    und wird nicht einzeln zugelassen oder verboten.
    """
    return {k for k in frontmatter(text) if "." not in k}


def belegte_felder(text: str) -> set[str]:
    """Welche Felder eine Uebergabe wirklich traegt — auf oberster Ebene.

    Ein Block zaehlt als belegt, sobald eines seiner Kinder einen Wert hat:
    `produced_by` ist in **allen 24** Uebergaben ein Block und nie ein Skalar
    (gemessen 2026-09-08). Eine Pruefung, die nur `felder["produced_by"]`
    ansieht, findet dort den leeren String und haelt das Feld fuer fehlend —
    sie waere an jeder einzelnen Uebergabe rot geworden, obwohl keine es
    auslaesst.

    `null` gilt als unbelegt. Der Kanal traegt `acknowledged_by: null`,
    `acknowledged_at: null` und `closed_at: null`, solange die Quittung
    aussteht — ein Platzhalter fuer eine Zusage ist keine Zusage.
    """
    belegt: set[str] = set()
    for schluessel, wert in frontmatter(text).items():
        if wert and wert != "null":
            belegt.add(schluessel.split(".", 1)[0])
    return belegt


def record_block(text: str) -> str | None:
    """Der Block zwischen den Markern — das, was der Hash abdeckt."""
    if RECORD_BEGIN not in text or RECORD_END not in text:
        return None
    return text.split(RECORD_BEGIN, 1)[1].split(RECORD_END, 1)[0]
