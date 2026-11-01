#!/usr/bin/env python3
"""The kit probe (Leerprobe): runs the workflow in a throwaway repository and measures what carries.

**What for.** The claim "this workflow can be handed over" is worthless as
long as it is a sentence in a prose file. This command turns it into a run: it
copies into an empty directory what `manifest.yaml` lists as `mechanismus`,
creates an empty body for every `geruest` rule, runs `pytest` and compares the
red cases against `REIST_NICHT`.

**What it does not do.** It writes nothing into the working tree, installs
nothing and repairs no red case. A case that is red here is mostly red for a
good reason: a ratchet that asks for THIS repository's script names must be
red elsewhere, or it would be a ratchet over an empty set.

    python3 scripts/kit/probe.py            # run and compare
    python3 scripts/kit/probe.py --list     # only say what would be copied
    python3 scripts/kit/probe.py --messen   # print the red names, to add them
"""

from __future__ import annotations

import argparse
import functools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = Path(__file__).resolve().parent / "manifest.yaml"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from _verdict import Verdict  # noqa: E402

# ---------------------------------------------------------------------------
# What does not travel, and why
# ---------------------------------------------------------------------------
#
# The names are MEASURED (a run of `--messen`), the reasons are SET.
# A name is a measurement and belongs to the machine; a reason is a judgement
# and belongs to a person.
#
# **Both directions block.** A red case without an entry is an unexplained
# failure in a handover. An entry for a green case is worse: an expired reason
# reads like a living decision. The session that wrote this found exactly
# that five times.
GRUENDE = (
    "bestand-dieses-repos",  # checks an inventory that does not exist there
    "braucht-die-vollstaendige-suite",  # checks files the kit does not carry
    "braucht-ein-gate-das-hier-lebt",  # asks for an enforcer outside the kit
    # "geruest-ist-absichtlich-leer" removed on 2026-09-23 (bead coding-harness-1jg.3,
    # step two): the committed copy went, the kit role of the same name dissolved
    # (AK-6, one member), and the kit no longer carries the body files; the cases
    # now measure "braucht-die-vollstaendige-suite".
    # "gilt-erst-mit-bestand" removed on 2026-09-19 (2ee triage): no case carries
    # it today. It returns when the project channel starts with lakeswitch joining
    # (O-2/M2), then with a case, not without one.
)

# The fifth reason came on 2026-09-08, for the same cause as the fourth: the
# vocabulary had no term for a real cause. Four cases in the handover channel
# stood on "bestand-dieses-repos" ("checks an inventory that does not exist
# there"). They check no inventory, though: they are fully portable and only
# need a handover to exist at all. A fresh repository has none, and rightly so:
# the check SHOULD not be green there, it just has nothing to check yet.
#
# The difference from "bestand-dieses-repos" is the timing: there a number of
# this repository is claimed and stays wrong there; here a set is presupposed
# that appears in the target with its first own artefact.

# The fourth reason came on 2026-09-08, after a cross-reading showed that two
# entries had a factually wrong reason: they stood on
# "braucht-die-vollstaendige-suite" ("checks files the kit does not carry"),
# although the kit does carry `model-endpoints.yaml`, as `geruest`, an empty
# body. They went red because the body is empty, not because the file is
# missing. The closed vocabulary had no term for the actual cause, so a wrong
# one had to be chosen. A vocabulary without the right term forces a false
# statement, and the guard below checks membership only, never correctness.

# Measured on 2026-09-08 with `--messen`; the mapping follows each case's
# failure message: a named enforcer that does not exist here -> the third;
# a missing file or an unmet precondition -> the second;
# a claim about this repository's inventory -> the first.
REIST_NICHT: dict[str, str] = {
    "tests.test_ci::test_every_gate_step_has_a_mutation_test": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_every_script_has_a_test_or_a_declared_reason": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_no_declared_reason_cites_a_closed_or_unknown_bead": "bestand-dieses-repos",
    "tests.test_ci::test_no_declared_reason_stands_for_a_script_that_has_a_caller": "bestand-dieses-repos",
    "tests.test_ci::test_der_echte_lesepfad_des_bead_gates_wird_erkannt": "bestand-dieses-repos",
    "tests.test_ci::test_the_makefile_runs_what_the_one_list_runs": "bestand-dieses-repos",
    "tests.test_ci::test_one_version_is_the_interpreter_floor": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_the_cloud_environment_builds_the_venv_with_the_floor": "braucht-die-vollstaendige-suite",
    "tests.test_ci::test_real_pi_is_provisioned_before_contracts": "braucht-die-vollstaendige-suite",
    "tests.test_feedback_channel::test_journal_index_lists_every_open_project_handover": "bestand-dieses-repos",
    "tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[GEMEINSAM-fehlende_gemeinsame]": "bestand-dieses-repos",
    "tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[PROJEKT_PFLICHT-fehlende_kanalpflicht]": "bestand-dieses-repos",
    "tests.test_kit::test_the_kit_list_is_not_derivable_from_the_export_list": "bestand-dieses-repos",
    "tests.test_kit::test_the_role_check_goes_red_when_a_rule_is_removed": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[consistency-auditor.md-claude-sonnet-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[code-generation-orchestrator.md-claude-sonnet-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[entity-builder.md-claude-sonnet-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[entity-deployer.md-claude-sonnet-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[explorer.md-claude-haiku-5-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[migration-supervisor.md-claude-sonnet-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[preconditions-gate-runner.md-claude-sonnet-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[reconciliation-orchestrator.md-claude-sonnet-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[reviewer.md-claude-opus-5-5]": "braucht-die-vollstaendige-suite",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01-explore.md-GLM 5.3 Flash]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01a-interview.md-Opus 5.5]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02-spec.md-gpt-6.1-sol]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02a-spec-review.md-Opus 5.5]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02b-design.md-gpt-6.1-sol]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[03-plan.md-gpt-6.1-sol]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[04-implement.md-GLM 5.3 Flash]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[06-review.md-Opus 5.5]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[07-commit.md-Haiku 5.5]": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_model_in_the_routing_table_resolves": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_no_old_reviewer_remark_claims_a_review_phase": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_no_remark_routes_the_spec_review_to_codex": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_the_declaration_is_not_empty": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_the_opencode_go_entry_is_declared": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_the_opencode_go_remark_names_every_source": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_free_selection_exceptions_require_dates_and_reasons": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_every_new_paid_model_carries_its_terms_reading": "bestand-dieses-repos",
    "tests.test_model_endpoints::test_unread_terms_reach_the_free_stage_alone": "bestand-dieses-repos",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-G7]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-P5]": "braucht-ein-gate-das-hier-lebt",
    "tests.test_regelwerk::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-S1]": "braucht-ein-gate-das-hier-lebt",
}

# The cap. It may only FALL. Whoever adds an entry raises it visibly, in the
# diff, with a reason in the commit. A portability that can be lost without
# anyone noticing is none.
#
# 53 -> 59 on 2026-09-08: RB-A6 now also checks the six model names in
# `prompts/`. The check itself travels (`prompts/` is `mechanismus`); it goes
# red in the target only because `model-endpoints.yaml` is an empty body there.
# Six more cases in the list are the price for six models, named unchecked
# until then, now resolving against the declaration.
#
# 59 -> 60 on 2026-09-10: `prompts/01a-interview.md` came along, the phase in
# which a person is interviewed before the spec is written. One more prompt is
# one more model name, red in the target for the same reason as the six before
# it: `model-endpoints.yaml` is an empty body there. The entry carries the same
# reason and is no new kind of exception.
#
# 60 -> 61 on 2026-09-10: `prompts/02a-spec-review.md` came along, the
# cross-reader who reads the spec before building. Same class, same reason.
#
# 61 -> 62 on 2026-09-14: `tests.test_ci::test_the_glob_itself_finds_a_real_orphan_shell_script`
# came along. The counter-check for the widened caller rule (finding 11, round
# 2) creates a real .sh script and reads the same local runner as the two
# caller and test ratchet tests just above it, which the kit does not carry (no
# entry in `manifest.yaml`; it falls under the `scripts/` catch-all `bestand`).
# Same class, same reason.
# 31 -> 32 on 2026-09-29: `tests.test_ci::test_no_declared_reason_stands_for_a_script_that_has_a_caller`
# came along. `ci_gates.OHNE_AUFRUFER` now names `omnigent_policy.py`, a script with no CI caller
# by nature (the installer runs on the maintainer's machine). The script is `bestand` (the
# `scripts/` catch-all), the list travels with `ci_gates.py`, so in the throwaway repo the entry
# points at a file that is not there. Same class, same reason as the other `bestand-dieses-repos`
# cases: the claim is about this repository's script inventory.
# 32 -> 31 on 2026-09-30: `tests.test_kit::test_the_two_manifests_really_disagree_somewhere`
# carries now. It asks for more than 60 files in both manifests, and the throwaway repo reached
# that when the ADR gate, its command and their two tests joined the mechanism
# (plans/changes/harness-decide-adr). A lowered cap needs no reason; this one says why the entry went.
# 31 -> 32 on 2026-09-30: the loop prompt `prompts/04b-review-loop.md` came along
# (plans/changes/archive/2026-09-30-stage-2-codex-glm). A prompt with a model line is one case more, red in the
# throwaway repo for the reason the other prompt cases are: `model-endpoints.yaml` stays home.
# 32 -> 33 on 2026-10-07: `prompts/02b-design.md` came along (plans/changes/archive/2026-09-30-template-bundle),
# one more prompt with a model line, red in the throwaway repo for the same reason.
# 33 -> 36 on 2026-10-08 (plans/changes/archive/2026-10-07-stage2-mimo): one entry was renamed, not
# added — the loop prompt's model line names the ladder's first rung
# `deepseek-v4.1-flash` where it used to name `GLM 5.3`. Three cases are new:
# `test_the_opencode_go_entry_is_declared`, `test_the_opencode_go_remark_names_every_source`
# and `test_no_old_reviewer_remark_claims_a_review_phase`. All three read
# `model-endpoints.yaml`, which stays home like it did for every prompt case
# above — the same reason, `bestand-dieses-repos`, and no new kind of exception.
# 35 -> 36 on 2026-10-13 (plans/changes/codex-drafts): three prompt cases were renamed, not added —
# the drafting prompts' model lines now lead with the id `gpt-6.1-sol` where they named
# `Opus 5.5`. One case is new: `test_no_remark_routes_the_spec_review_to_codex` reads
# `model-endpoints.yaml`, which stays home — the same reason, `bestand-dieses-repos`.
# The count stays at the cap; no raise.
# 36 -> 37 on 2026-10-13 (plans/changes/ci-minutes): `tests.test_ci::test_one_version_is_the_interpreter_floor`
# came along. It reads `pyproject.toml`, a file the kit does not carry: the missing file maps to
# `braucht-die-vollstaendige-suite`. 37 -> 38 on 2026-10-13: `tests.test_ci::test_the_cloud_environment_builds_the_venv_with_the_floor`
# reads `tools/cloud-env/setup.sh`, also not carried — the same reason.
# 38 -> 39 on 2026-10-15 (plans/changes/pi-pin): `tests.test_ci::test_real_pi_is_provisioned_before_contracts`
# reads `tools/pi/.node-version`, a file the kit does not carry: the missing file maps to
# `braucht-die-vollstaendige-suite`.
# 39 -> 42 on 2026-10-16 (plans/changes/loop-until-clean): the free-stage rule, the paid terms
# records and the class acceptance each got a test, and all three read
# `model-endpoints.yaml` (and `tests.test_model_endpoints::test_free_selection_exceptions_require_dates_and_reasons`
# also `scripts/stage2.py`), which the kit leaves home — `bestand-dieses-repos`, the same reason
# as the entry's older cases.
# 42 -> 44 on 2026-11-01 (bead coding-harness-9ll): the two read-only
# helpers `.claude/agents/explorer.md` (Haiku 5.5) and `.claude/agents/reviewer.md`
# (Opus 5.5, high effort) join the agent definitions, which travel as `mechanismus`,
# while `model-endpoints.yaml` stays home. Their two endpoint cases go red in the
# throwaway repo for the reason the seven before them carry: the kit carries the
# definitions but no endpoint declaration of its own.
DECKEL = 44  # raised on 2026-11-01 (42 -> 44); earlier: raised on 2026-10-16 (39 -> 42); raised on 2026-10-15 (38 -> 39); raised on 2026-10-13 (36 -> 38); raised 2026-10-08 (33 -> 36), raised 2026-10-07 (32 -> 33), raised 2026-10-05 (31 -> 32), 2026-09-30 (31 -> 32), lowered 2026-09-30 (32 -> 31), raised 2026-09-29 (31 -> 32)


# ---------------------------------------------------------------------------
# Reading the manifest
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def _manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def regeln() -> list[dict]:
    return _manifest()["rules"]


def geruest_ordner() -> list[str]:
    """Directories that must exist EMPTY in the target for the workflow to take hold.

    Kept apart from the `geruest` rules, because a prefix rule `plans/changes/`
    would also cover every file BELOW it, and those are this repository's
    artefacts, so inventory (`bestand`). The directory travels, its content does not.
    """
    return _manifest().get("geruest_ordner", [])


def _deckt(praefix: str, pfad: str) -> bool:
    """By path segment, not as a string prefix.

    `startswith` takes `docs/WORKFLOW.md.orig` for the file `docs/WORKFLOW.md`
    and `model-endpoints.yaml.bak` for `model-endpoints.yaml`: the backup a merge
    tool leaves behind would inherit the original's role and travel as
    `mechanismus` or be created as `geruest`. The same correction, for the same
    reason, is in `tests/test_ci.py:_deckt`.

    A directory prefix ends in "/" and covers everything below it; a file prefix
    covers exactly itself.
    """
    if praefix.endswith("/"):
        return pfad.startswith(praefix)
    return pfad == praefix


def rolle(pfad: str, regelmenge: list[dict] | None = None) -> tuple[str, str] | None:
    """Role and rule prefix for a path; the longest matching prefix wins.

    Returns `None` when no rule matches. That is BLOCK, not "does not belong":
    a default that decides when in doubt decides exactly about the files nobody
    thought of.
    """
    treffer = [r for r in (regelmenge or regeln()) if _deckt(r["prefix"], pfad)]
    if not treffer:
        return None
    beste = max(treffer, key=lambda r: len(r["prefix"]))
    return beste["rolle"], beste["prefix"]


@functools.lru_cache(maxsize=1)
def _ls_files() -> tuple[tuple[str, ...], tuple[str, ...]]:
    # `-z` is no detail: without it git quotes every name with special characters
    # ("docs/archive/… \342\200\224 …"), and the quoted name falls under no
    # prefix rule. A file would have stayed unclassified because its name holds
    # a dash.
    # `--others --exclude-standard` is no detail: without them the probe does
    # NOT see a newly created, not yet staged file. On 2026-09-08 the gate ran
    # green locally over a state that no longer existed after the commit; CI
    # was red, and rightly so. A check that sees the working tree differently
    # from the commit checks the wrong tree. That is the very class of fault
    # this module is built against: green because the broken part is not in
    # the checked set.
    # BUT: `--others` also sees what the commit will NOT contain, a note file or
    # a scratch script. Counting those as BLOCK turns the gate red on a day
    # nobody did anything wrong, and `scripts/_verdict.py` says what happens to
    # such gates: they get switched off. Hence two sets instead of one.
    def _lauf(*args: str) -> tuple[str, ...]:
        aus = subprocess.run(
            ["git", "ls-files", "-z", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return tuple(sorted({z for z in aus.stdout.split("\0") if z}))

    im_commit = _lauf("--cached")
    daneben = tuple(x for x in _lauf("--others", "--exclude-standard") if x not in set(im_commit))
    return im_commit, daneben


def getrackte_dateien() -> list[str]:
    """What the commit will contain: the index. Unclassified = BLOCK."""
    return list(_ls_files()[0])


def unversionierte_dateien() -> list[str]:
    """What lies beside it. Unclassified = DRIFT, named but not blocking."""
    return list(_ls_files()[1])


def nach_rolle() -> dict[str, list[str]]:
    """Every tracked file mapped to its role; `(offen)` collects the unclassified ones."""
    rm = regeln()
    aus: dict[str, list[str]] = {"mechanismus": [], "bestand": [], "(offen)": []}
    for pfad in getrackte_dateien():
        gefunden = rolle(pfad, rm)
        aus[gefunden[0] if gefunden else "(offen)"].append(pfad)
    return aus


# ---------------------------------------------------------------------------
# The probe
# ---------------------------------------------------------------------------


def _baue(ziel: Path) -> None:
    """Copies the mechanism and creates the scaffold (`geruest`) directories."""
    verteilt = nach_rolle()
    for pfad in verteilt["mechanismus"]:
        quelle = REPO_ROOT / pfad
        if not quelle.is_file():
            continue
        (ziel / pfad).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(quelle, ziel / pfad)
    for ordner in geruest_ordner():
        (ziel / ordner).mkdir(parents=True, exist_ok=True)
        (ziel / ordner / ".gitkeep").write_text("", encoding="utf-8")
    subprocess.run(["git", "init", "--quiet"], cwd=ziel, check=True)
    subprocess.run(["git", "add", "-A"], cwd=ziel, check=True, capture_output=True)
    subprocess.run(
        ["git", "-c", "user.email=probe@invalid", "-c", "user.name=probe", "commit", "--quiet", "-m", "Leerprobe"],
        cwd=ziel,
        check=False,
        capture_output=True,
    )


def _faelle(ziel: Path) -> dict[str, bool]:
    """Every collected test case as green or red. Collection errors count as red."""
    bericht = ziel / "junit.xml"
    # The foreign repository must not see THIS repository's tracker: CI sets
    # BEAD_RENDER for its own gates, and inherited it would let a test in the
    # throwaway repository go green against our state; the share would rise
    # without anything travelling (bead 1jg.3).
    umgebung = {k: v for k, v in os.environ.items() if k != "BEAD_RENDER"}
    # Only the isolated probe may skip repository commands that do not travel.
    umgebung["HARNESS_KIT_PROBE"] = "1"
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no", "-p", "no:cacheprovider", f"--junit-xml={bericht}"],
        cwd=ziel,
        capture_output=True,
        text=True,
        env=umgebung,
    )
    if not bericht.is_file():
        return {}
    aus: dict[str, bool] = {}
    for fall in ET.parse(bericht).getroot().iter("testcase"):
        name = f"{fall.get('classname', '')}::{fall.get('name', '')}"
        gescheitert = any(k.tag in ("failure", "error") for k in fall)
        uebersprungen = any(k.tag == "skipped" for k in fall)
        if uebersprungen:
            continue
        aus[name] = not gescheitert
    return aus


def fahre() -> dict[str, bool]:
    ziel = Path(tempfile.mkdtemp(prefix="kit-probe-"))
    try:
        _baue(ziel)
        return _faelle(ziel)
    finally:
        shutil.rmtree(ziel, ignore_errors=True)


# ---------------------------------------------------------------------------
# The verdict
# ---------------------------------------------------------------------------


def pruefe(faelle: dict[str, bool] | None = None) -> Verdict:
    v = Verdict()
    verteilt = nach_rolle()

    if verteilt["(offen)"]:
        v.block(
            f"{len(verteilt['(offen)'])} tracked file(s) fall under no rule",
            "\n".join(sorted(verteilt["(offen)"])[:20]),
        )

    offen_daneben = [p for p in unversionierte_dateien() if rolle(p) is None]
    if offen_daneben:
        v.drift(
            f"{len(offen_daneben)} untracked file(s) fall under no rule",
            "They do not go into the commit, so this does not block. Whoever stages one "
            "sees it as BLOCK on the next run:\n" + "\n".join(sorted(offen_daneben)[:20]),
        )

    if not verteilt["mechanismus"]:
        v.block("not a single file carries the role 'mechanismus'; the probe measures nothing (RB-G7)")
        return v

    for name, grund in sorted(REIST_NICHT.items()):
        if grund not in GRUENDE:
            v.block(f"{name}: reason {grund!r} lies outside the closed set", "allowed: " + " · ".join(GRUENDE))

    if len(REIST_NICHT) > DECKEL:
        v.block(
            f"REIST_NICHT has {len(REIST_NICHT)} entries, the cap stands at {DECKEL}",
            "The list may only shrink. Whoever grows it raises the cap visibly.",
        )

    faelle = fahre() if faelle is None else faelle
    if not faelle:
        v.block("the probe collected not a single test case; then it measures nothing (RB-G7)")
        return v

    rot = sorted(n for n, ok in faelle.items() if not ok)
    gruen = sorted(n for n, ok in faelle.items() if ok)

    unerklaert = [n for n in rot if n not in REIST_NICHT]
    if unerklaert:
        v.block(
            f"{len(unerklaert)} red case(s) without a declared reason",
            "\n".join(unerklaert[:25])
            + ("\n  …" if len(unerklaert) > 25 else "")
            + "\n\nAdd them with: python3 scripts/kit/probe.py --messen",
        )

    # The third direction, found in a cross-reading on 2026-09-08: an entry whose
    # case is no longer COLLECTED at all. It is neither red nor green, so it
    # slips through both checks above. That is how portability is lost without
    # anyone noticing: whoever moves a test file's kit role from `mechanismus`
    # to `bestand` takes its cases out of the set, and the share even RISES,
    # because red cases drop out of the denominator.
    #
    # A renamed or deleted test triggers it too. That is intended, not a false
    # alarm: a reason whose case no longer exists is as dead as one whose case
    # went green.
    verwaist = [n for n in REIST_NICHT if n not in faelle]
    if verwaist:
        v.block(
            f"{len(verwaist)} entry/entries in REIST_NICHT have no case any more",
            "\n".join(sorted(verwaist)[:25])
            + ("\n  …" if len(verwaist) > 25 else "")
            + "\n\nEither the test was renamed (then follow with the entry) or "
            "its file no longer travels. The second is the dangerous one: "
            "portability falls while the reported share rises.",
        )

    abgelaufen = [n for n in gruen if n in REIST_NICHT]
    if abgelaufen:
        v.block(
            f"{len(abgelaufen)} entry/entries in REIST_NICHT went green",
            "\n".join(abgelaufen[:25]) + "\n\nAn expired reason reads like a living decision. Remove it.",
        )

    v.info(
        f"{len(gruen)} of {len(faelle)} cases carry into a foreign repository ({100 * len(gruen) // len(faelle)} %)",
        f"mechanismus {len(verteilt['mechanismus'])} · bestand {len(verteilt['bestand'])} file(s)",
    )
    return v


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="only print what would be copied")
    p.add_argument("--messen", action="store_true", help="print the red names as a Python dict (measure)")
    p.add_argument("--strict", action="store_true", help="DRIFT blocks too")
    args = p.parse_args()

    if args.list:
        verteilt = nach_rolle()
        for r in ("mechanismus", "bestand", "(offen)"):
            print(f"{r:<14} {len(verteilt[r]):>4}")
            if r in ("mechanismus", "(offen)"):
                for pfad in sorted(verteilt[r]):
                    print(f"    {pfad}")
        return 0

    if args.messen:
        faelle = fahre()
        rot = sorted(n for n, ok in faelle.items() if not ok)
        print(f"# {len(rot)} red of {len(faelle)}; set the reasons by hand")
        print("REIST_NICHT: dict[str, str] = {")
        for n in rot:
            print(f'    {json.dumps(n)}: "bestand-dieses-repos",')
        print("}")
        return 0

    v = pruefe()
    print(v.render())
    return v.exit_code(strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
