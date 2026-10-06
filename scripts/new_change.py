#!/usr/bin/env python3
"""The call that creates a change — AK-1 (acceptance criterion 1) from spec.md.

`docs/WORKFLOW.md` describes seven phases, but until today there was no command
that sets up phase 1: `plans/changes/<name>/` with a valid artefact, linked to
a bead in the tracker. Whoever began a change typed the folder and the
frontmatter by hand — and easily missed a required field that
`plans_registry.py --check` would only have found on the next run.

This script closes the gap without opening a second one:

  - It **imports** `plans_registry` and reads its `REQUIRED`,
    `_bead_statuses`, `_bead_export_path`, `render_index` and `check` at run
    time — never copied at import time, so that a test that redirects
    `reg.REPO`, `reg.PLANS` and `reg.INDEX` with `monkeypatch` redirects this
    script too (the same pattern as the `plans` fixture in
    `tests/test_plans_registry.py`).
  - It **requires** an existing bead instead of creating one: calling `bd`
    would mean writing (AGENTS.md), CI has no `bd` (`requirements-ci.txt` does
    not name it), and an artefact with an invented bead would be blocked at
    once by the `dangling-beads` gate — the script would produce what the next
    gate rejects. Requiring and checking is the only form that does the same
    in every environment.
  - It **leaves nothing standing that the next gate rejects**: once before and
    once after writing, `plans_registry.check()` runs, and only a BLOCK that
    the call **added** makes the script roll back. The baseline is no
    subtlety: without it every foreign BLOCK under `plans/` would trigger the
    rollback and the message would pin it on the freshly created, sound
    artefact — the entry would be unusable as long as anything else blocks
    anywhere.

Usage:
    python3 scripts/new_change.py <name> --bead <id> [--owner <role>] [--dry-run]
Exit codes (via `_verdict.Verdict`): 0 = created (INFO), 2 = BLOCK.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plans_registry as reg  # noqa: E402
from _verdict import Level, Verdict  # noqa: E402

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Shorter tokens report almost every name as "related" to almost every other.
MIN_TOKEN_LEN = 4

# The archive form is `YYYY-MM-DD-<name>` (plans/_README.md). Exact, not as a
# suffix glob `*-<name>`: that hit every archived folder whose basename happens
# to end in `-<name>` — `isolation` collided with
# `2026-09-05-workflow-einstieg-und-isolation`, and the call aborted on a
# collision that did not exist.
ARCHIV_PRAEFIX = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-"

# This heading line marks what is generated as a skeleton, not as the result of
# phase 1 — the outline from `prompts/01-explore.md` is deliberately NOT copied
# here (AK-2 holds for this body too: no second place that describes what
# phase 1 does).
BODY_TEMPLATE = """# {titel} — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
"""


def _frontmatter_template(name: str, bead: str, owner: str, heute: str) -> str:
    """Frontmatter with every field from `plans_registry.REQUIRED` filled in.

    Order and extra fields follow `plans/_README.md` — `supersedes` and
    `superseded_by` are the only two fields that may be `null`.

    `provenance: human-written` and **no** `produced_by` block: this file was
    written by a deterministic call that a human issued. It used to say
    `ai-drafted-reviewed` with
    `produced_by: {kind: llm-session, name: unknown}` — a provenance that
    nobody had at the time of writing, and that the provenance gate cannot
    refute, because `plans/` permits exactly the two classes `human-written`
    and `ai-drafted-reviewed`. Whoever fills the body with a language model
    brings both up to date; the generated text says so.
    """
    return f"""---
title: "Research — {name}"
status: draft
implementation_status: none
date: {heute}
last_reviewed: {heute}
updated: {heute}
supersedes: null
superseded_by: null
bead: {bead}
owner: {owner}
provenance: human-written
tags: [research]
---

"""


def _known_field_values(bead: str, heute: str) -> dict[str, str]:
    """What this script can put in for each required field from `REQUIRED`.

    If `plans_registry.REQUIRED` grows by a field for which there is no value
    here, step 4 blocks — instead of writing an artefact that `--check`
    rejects right afterwards.
    """
    return {
        "status": "draft",
        "implementation_status": "none",
        "date": heute,
        "last_reviewed": heute,
        "bead": bead,
    }


def _related_candidates(name: str, plans_root: Path) -> list[str]:
    """Rough preview of the rule from AGENTS.md: search first, then create.

    No abort — whether it is the same topic is for the human to decide. A
    token under four characters is ignored, otherwise almost every name
    reports "related" to almost every other. The threshold is a constant so
    that text and code do not carry it separately.
    """
    tokens = [t for t in name.split("-") if len(t) >= MIN_TOKEN_LEN]
    if not tokens:
        return []
    muster = [re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE) for t in tokens]
    treffer: set[str] = set()
    for teilbaum in ("specs", "changes"):
        wurzel = plans_root / teilbaum
        if not wurzel.exists():
            continue
        for pfad in sorted(wurzel.rglob("*.md")):
            text = pfad.name.lower() + "\n" + pfad.read_text(encoding="utf-8", errors="ignore")
            if any(m.search(text) for m in muster):
                treffer.add(str(pfad.relative_to(plans_root)))
    return sorted(treffer)


WAECHTER = Path(__file__).resolve().parent / "check_worktree_state.sh"


def _worktree_is_sane() -> str | None:
    """Is the tree that is about to be written to on a branch?

    **Why here.** `make change` writes a folder and renders the index. If that
    happens on a detached HEAD, both hang on a commit that no branch holds — it
    only shows when someone looks for the folder. At times five worktrees of
    this repo's main checkout were in exactly this state.

    Checked with `-`: the branch may be any, but it must be one. A running
    rebase halts it as well. The check is **one** — the shell script is the
    implementation, no second rule set stands here.

    Returns: the error message, or None if the tree is usable.
    """
    if not WAECHTER.is_file():
        return f"{WAECHTER.name} missing — the precondition cannot be checked"
    lauf = subprocess.run(
        ["bash", str(WAECHTER), str(reg.REPO), "-"],
        capture_output=True,
        text=True,
    )
    if lauf.returncode != 0:
        return (lauf.stderr or lauf.stdout).strip() or "Guard reports an unusable worktree"
    return None


def _abort(verdict: Verdict, message: str, detail: str = "") -> int:
    verdict.block(message, detail)
    print(verdict.render())
    return verdict.exit_code()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="folder name under plans/changes/, e.g. my-topic")
    parser.add_argument("--bead", required=True, help="existing bead id from the tracker (tools/bd ready)")
    parser.add_argument("--owner", default="Data Architect", help="role from provenance.yaml (default: Data Architect)")
    parser.add_argument("--dry-run", action="store_true", help="only show, write nothing")
    args = parser.parse_args(argv)

    verdict = Verdict()

    # Step 1 · Name
    if not NAME_PATTERN.match(args.name):
        return _abort(
            verdict,
            f"Name '{args.name}' does not match {NAME_PATTERN.pattern}",
            "Allowed: lowercase letters, digits, hyphen as separator — no leading/trailing hyphen.",
        )

    # Step 2 · Bead
    export_path = reg._bead_export_path()
    bead_statuses = reg._bead_statuses(export_path)
    if bead_statuses is None:
        return _abort(
            verdict,
            f"Bead export {export_path} missing or empty",
            "Without the export it cannot be checked whether the bead exists. Fix: `bd export` or let the export hook run.",
        )
    status = bead_statuses.get(args.bead)
    if status is None:
        return _abort(
            verdict,
            f"Bead '{args.bead}' is not in the export {export_path}",
            "The bead must be created and exported first — this script creates none.",
        )
    if status == "closed":
        return _abort(
            verdict,
            f"Bead '{args.bead}' is 'closed' in the export",
            "A new folder on a closed bead would be DRIFT at once (bead closed, artefact not 'done' and archived).",
        )

    # Step 2a · Worktree
    fehler = _worktree_is_sane()
    if fehler is not None:
        return _abort(
            verdict,
            "Worktree is not in a state in which writing is allowed",
            fehler,
        )

    # Step 3 · Repeated creation
    ziel = reg.PLANS / "changes" / args.name
    if ziel.exists():
        return _abort(verdict, f"{ziel.relative_to(reg.REPO)} exists already")
    archiv = reg.PLANS / "changes" / "archive"
    if archiv.exists() and any(archiv.glob(f"{ARCHIV_PRAEFIX}{args.name}")):
        return _abort(verdict, f"plans/changes/archive/ already holds a folder for '{args.name}'")

    verwandt = _related_candidates(args.name, reg.PLANS)
    for pfad in verwandt:
        verdict.info(
            f"possibly related: plans/{pfad}",
            "Before creating, check whether it is the same topic (AGENTS.md).",
        )

    # Step 4 · REQUIRED complete?
    heute = dt.date.today().isoformat()
    bekannt = _known_field_values(args.bead, heute)
    unbekannt = [f for f in reg.REQUIRED if f not in bekannt]
    if unbekannt:
        return _abort(
            verdict,
            f"Required field(s) {unbekannt} — the script knows no value for them",
            "plans_registry.REQUIRED has grown without this script following.",
        )

    frontmatter = _frontmatter_template(args.name, args.bead, args.owner, heute)
    titel = args.name.replace("-", " ")
    inhalt = frontmatter + BODY_TEMPLATE.format(titel=titel)
    research_path = ziel / "research.md"

    if args.dry_run:
        verdict.info(f"[--dry-run] would create: {research_path.relative_to(reg.REPO)}")
        verdict.info(f"[--dry-run] Bead: {args.bead} (status in the export: {status})")
        verdict.info("[--dry-run] Reference: prompts/01-explore.md")
        print(verdict.render())
        print("\n--- Preview research.md ---\n")
        print(inhalt)
        return verdict.exit_code()

    # Step 5 · Baseline, then write
    #
    # The baseline is the difference between "this call broke something" and
    # "something was already broken here". Without it every foreign BLOCK under
    # plans/ would trigger the rollback, and the message would pin it on the
    # freshly created, sound artefact: the documented entry would be unusable
    # as long as any other artefact blocks — and with an error message that
    # points at the wrong file.
    vorher = {f.message for f in reg.check().at(Level.BLOCK)}

    alter_index = reg.INDEX.read_text(encoding="utf-8") if reg.INDEX.exists() else None
    ziel.mkdir(parents=True)
    research_path.write_text(inhalt, encoding="utf-8")

    # Step 6 · Re-render the index, then check what was *added*.
    reg.INDEX.write_text(reg.render_index(), encoding="utf-8")
    nachher = reg.check().at(Level.BLOCK)
    neue_block_befunde = [f for f in nachher if f.message not in vorher]
    if neue_block_befunde:
        shutil.rmtree(ziel)
        if alter_index is None:
            reg.INDEX.unlink(missing_ok=True)
        else:
            reg.INDEX.write_text(alter_index, encoding="utf-8")
        verdict.block(
            "The generated artefact was rejected by the registry check — nothing stays.",
            "\n".join(f.message for f in neue_block_befunde),
        )
        print(verdict.render())
        return verdict.exit_code()

    # Pre-existing BLOCK findings that **still** stand. They are not this call's
    # fault and do not stop it — but keeping quiet would mean the next
    # `make verify` comes as a surprise. What is reported is the intersection of
    # before and after, not `vorher` alone: the missing index blocks before
    # writing and is fixed afterwards, and "pre-existing BLOCK: plans/INDEX.md
    # missing" would then be a message about a state this call has just
    # removed.
    for message in sorted(vorher & {f.message for f in nachher}):
        verdict.info(
            f"pre-existing BLOCK, not from this call: {message}",
            "It stood in the tree before and blocks `make verify` until someone fixes it.",
        )

    # Step 7 · Output
    verdict.info(f"created: {ziel.relative_to(reg.REPO)}")
    verdict.info(f"Bead: {args.bead} (status in the export: {status})")
    verdict.info("next step: prompts/01-explore.md")
    print(verdict.render())
    return verdict.exit_code()


if __name__ == "__main__":
    sys.exit(main())
