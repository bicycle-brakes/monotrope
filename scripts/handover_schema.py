"""The schema of the handovers — the one field list that test and template read from.

The feedback channel is the only way knowledge flows between the repositories:
the framework must not write into a project instance (ADR-011/015), so it files
a handover and waits for the acknowledgement.

Until 2026-09-08 this contract was **lived but written down nowhere**. The
consequence was measurable: 14 of 24 handovers carried no `direction` field, and
`project_handovers()` filters on exactly that — so they dropped out of every
check of the channel. The test suite was green over a set that did not contain
the unchecked files.

**Why this lives here and not in the test.** Because the template
(`templates/handover.md`) needs the same list too. Were it in the test, it would
exist twice — and the second list is always the one that goes stale.
"""

from __future__ import annotations

# Who receives a handover. Closed: a third value would be a new kind of
# document and needs a decision, not a silent entry.
#
#   framework->framework  Session handover in this repo. Nobody waits for an
#                         acknowledgement; the light contract suffices.
#   framework->project    The channel. Carries target, state, an immutable
#                         findings block and acknowledgement fields. Only the
#                         project team sets `acknowledged` and `closed` — by
#                         pull request into this repo.
RICHTUNGEN: tuple[str, ...] = ("framework->framework", "framework->project")

# Fields EVERY handover carries.
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

# The channel contract. Allowed only with `direction: framework->project`.
#
# **Measured on 2026-09-08, and the first version of this set was wrong.** It
# also listed `target_repo`, `target_ref`, `status`, `bead`, `review` and
# `disclosure` as channel-exclusive — the test then fired on seven session
# handovers that carry these fields quite rightly: a session handover too
# describes a state (`target_ref`), hangs on a work item (`bead`) and has a
# status (`status`).
#
# Exclusive is only what carries the commitment: the hash over the immutable
# findings block and the three acknowledgement fields. Keeping them on a session
# handover claims a promise nobody is waiting for.
KANAL_EXKLUSIV: frozenset[str] = frozenset(
    {
        "record_sha256",
        # Set by the project team, not by the framework.
        "acknowledged_by",
        "acknowledged_at",
        "closed_at",
    }
)

# What a handover in the channel additionally REQUIRES (not merely may carry).
PROJEKT_PFLICHT: frozenset[str] = frozenset({"target_repo", "target_ref", "status", "bead", "record_sha256"})

# Allowed in both directions, required nowhere. Everything here is attested in
# the existing handovers — the set is measured, not made up.
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
        # A session handover too describes a state, hangs on a work item and has
        # a status. See the comment above KANAL_EXKLUSIV.
        "target_repo",
        "target_ref",
        "status",
        "bead",
        "review",
        "disclosure",
        # The metrics of the process (2026-09-10). They are optional because a
        # handover without a phase run has none — but where they stand, they are
        # the only basis on which the doctrine can correct itself. Without them
        # every statement about a gate's effect remains an expectation.
        "review_rounds",  # rounds until clean
        "fix_regen_rounds",  # of these, findings with origin `fix-r<N>` — the loop against itself
        "late_findings",  # found after the commit; constant classes change gates, not gut feeling
        "questions",  # questions put to humans, by class
    }
)

# Expressly NOT included although found in the existing handovers: `date` (once,
# `created` was meant) and `beads` (once, `bead` was meant). Both were silent
# because nobody held the names against a list — they should stand out.
# Corrected on 2026-09-08 in `2026-04-29-adwaive-onepager.md`.
ERLAUBT: frozenset[str] = GEMEINSAM | KANAL_EXKLUSIV | OPTIONAL

# The status vocabulary of the channel.
STATUS: tuple[str, ...] = ("pending", "acknowledged", "closed")

# The markers `record_sha256` is computed over. The findings block between them
# is immutable (RB-P5); an objection goes below it, never into it.
RECORD_BEGIN = "<!-- record:begin -->\n"
RECORD_END = "<!-- record:end -->"


def frontmatter(text: str) -> dict[str, str]:
    """Reads the flat keys of the frontmatter.

    Nested blocks (`review:`, `produced_by:`) are taken with their prefix —
    `review.status` instead of `status`. Without this separation the review
    status would overwrite the handover status, and both are called `status`.
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
    """Only the top-level keys — the ones `ERLAUBT` checks against.

    A nested key such as `review.status` belongs to its parent field and is
    neither allowed nor forbidden on its own.
    """
    return {k for k in frontmatter(text) if "." not in k}


def belegte_felder(text: str) -> set[str]:
    """Which fields a handover really carries — at the top level.

    A block counts as present as soon as one of its children has a value:
    `produced_by` is a block in **all 24** handovers and never a scalar
    (measured 2026-09-08). A check that looks only at `felder["produced_by"]`
    finds the empty string there and takes the field for missing — it would
    have gone red on every single handover, although none omits it.

    `null` counts as absent. The channel carries `acknowledged_by: null`,
    `acknowledged_at: null` and `closed_at: null` while the acknowledgement is
    outstanding — a placeholder for a commitment is not a commitment.
    """
    belegt: set[str] = set()
    for schluessel, wert in frontmatter(text).items():
        if wert and wert != "null":
            belegt.add(schluessel.split(".", 1)[0])
    return belegt


def record_block(text: str) -> str | None:
    """The block between the markers — what the hash covers."""
    if RECORD_BEGIN not in text or RECORD_END not in text:
        return None
    return text.split(RECORD_BEGIN, 1)[1].split(RECORD_END, 1)[0]
