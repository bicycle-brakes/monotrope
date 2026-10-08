#!/usr/bin/env python3
"""
ramp_valves.py — the list of deliberately open valves.

A new check that turns half the existing stock red on the day it lands is not a
check but a migration. It gets waived, and a waived gate measures nothing. So
checks may report lower than they should for now — **but only with a condition
under which they switch up**.

That is where the danger lies. "Not blocking for now" is the most durable state
in software development: nobody notices that the condition has long been met,
because nothing asks. A valve without a due check is not a transition but an
exception under a better name.

This file is the answer. Every valve names

  * **what** is being waited for — in one sentence a person understands,
  * **how it is measured** — as a predicate a test runs,
  * **what happens once it holds** — the target state.

`tests/test_ramp_valves.py` fails as soon as a valve is due and still open. So
the switch-up hangs on a test, not on memory.

Why the lint rules are listed here and not only in `ruff.toml`: the selection
there says what is checked today. It does not say what comes next or what that
depends on. Without this list a narrow selection cannot be told from a
forgotten one.

Usage:
    python3 scripts/ramp_valves.py            # overview: open / due
    python3 scripts/ramp_valves.py --format=json

Exit codes: 0 = no valve due, 1 = at least one is due.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _verdict import Level, Ramp  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
RUFF_CONFIG = REPO_ROOT / "ruff.toml"


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------


def selected_rule_groups() -> set[str]:
    """The rule groups `ruff.toml` activates today."""
    text = RUFF_CONFIG.read_text(encoding="utf-8")
    treffer = re.search(r"^select\s*=\s*\[(.*?)\]", text, re.MULTILINE | re.DOTALL)
    if not treffer:
        return set()
    return set(re.findall(r'"([^"]+)"', treffer.group(1)))


def findings_in_group(gruppe: str) -> int | None:
    """How many findings a rule group reports today. `None` = not measurable."""
    ergebnis = subprocess.run(
        ["ruff", "check", "--select", gruppe, "--statistics", "."],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if ergebnis.returncode not in (0, 1):
        return None
    summe = 0
    for zeile in ergebnis.stdout.splitlines():
        teile = zeile.split(maxsplit=1)
        if teile and teile[0].isdigit():
            summe += int(teile[0])
    return summe


# ---------------------------------------------------------------------------
# The valves
# ---------------------------------------------------------------------------

# Rule groups not yet in `select` because they have findings today. The phrase
# after each says what the group checks at all — a list of abbreviations is
# unreadable for anyone who does not know ruff by heart.
WARTENDE_LINT_GRUPPEN: dict[str, str] = {
    "E5": "overlong lines beyond what the formatter wraps",
    "PL": "Pylint heritage: nesting, argument count, comparison forms",
    "RUF": "ruff's own rules, among others on Unicode homoglyphs in strings",
}


def _lint_valve(gruppe: str, was: str) -> Ramp:
    def bestand_geraeumt() -> bool:
        anzahl = findings_in_group(gruppe)
        return anzahl == 0

    return Ramp(
        name=f"lint-{gruppe}",
        condition=(
            f"`ruff check --select {gruppe}` reports nothing any more — then '{gruppe}' ({was}) belongs in select"
        ),
        predicate=bestand_geraeumt,
        target=Level.BLOCK,
        until_then=Level.INFO,
    )


def _roster_handles() -> set[str]:
    """The distinct handles in the roster of provenance.yaml."""
    karte = REPO_ROOT / "provenance.yaml"
    if not karte.exists():
        return set()
    try:
        import yaml

        daten = yaml.safe_load(karte.read_text(encoding="utf-8")) or {}
    except Exception:
        return set()
    return {r["handle"] for r in (daten.get("roles") or {}).values() if r.get("handle")}


def provenance_review_valve() -> Ramp:
    """A sign-off needs a second person — while there is none, it is DRIFT.

    `provenance.yaml` demands a sign-off with name and date for `human-decided`
    and `ai-drafted-reviewed`. Today this repo has a single handle in the roster,
    and none of the most recently merged pull requests carries a `reviewDecision`
    — so there is nobody whose approval could be entered. Setting a name anyway
    would be exactly the error the field exists to prevent (F-A-52: a name
    against a text the person never read). Until a second handle exists, "never
    signed off" is therefore visible and non-blocking.
    """

    def zweiter_da() -> bool:
        return len(_roster_handles()) >= 2

    return Ramp(
        name="provenance-review",
        condition=(
            "provenance.yaml names at least two distinct handles — then a second "
            "person can sign off, and `review.status: pending` is no longer a "
            "situation but an omission"
        ),
        predicate=zweiter_da,
        target=Level.BLOCK,
        until_then=Level.DRIFT,
    )


# ---------------------------------------------------------------------------
# The rule valves
# ---------------------------------------------------------------------------
#
# `docs/governance/regelwerk.md` holds 33 normative rules, each with an
# enforcement level. A rule at level 1 or 2 is a request — it applies, but
# nothing fails when someone breaks it. That is where the danger sits that this
# file was written against: "convention only for now" is the most durable state
# in software development.
#
# So every such rule carries a valve, and the valve measures **not** the
# existing stock but the work on it: its predicate is "the enforcer exists".
# Once someone writes the named test, the valve becomes due, and
# `tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open` demands that
# the rule be raised in the rule set. The date beside it is the second half: a
# rule nobody works on becomes due anyway.


def _enforcer_exists(ref: str) -> bool:
    """Does the named test function really exist?

    By text search on purpose and not by import: an import runs foreign module
    code, and this script runs in every run.
    """
    if "::" not in ref:
        return (REPO_ROOT / ref).exists()
    datei, funktion = ref.split("::", 1)
    pfad = REPO_ROOT / datei
    if not pfad.is_file():
        return False
    return re.search(rf"^def {re.escape(funktion)}\(", pfad.read_text(encoding="utf-8"), re.MULTILINE) is not None


# name -> (what is missing, which enforcer would close it, deadline)
REGEL_VENTILE: dict[str, tuple[str, str, str]] = {
    "agent-writes-allowlist": (
        "RB-A4: a writing agent declares where it may write",
        "tests/test_agents.py::test_agents_declare_writes_allowlist_when_they_can_write",
        "2026-11-30",
    ),
    # "merge-freshness" (RB-G7) closed on 2026-10-08: tests/test_ci.py asserts the
    # merge ref, the gate `ruleset` the up-to-date requirement; rule set 5.0.0.
    "signature-transcription": (
        "RB-M2: a signature is transcribed from the pull request, never set",
        "tests/test_validators.py::test_a_signature_is_transcribed_not_typed",
        "2026-11-30",
    ),
    "adversarial-record": (
        "RB-M3: an accepted contract presupposes an adversarial source verification",
        "tests/test_validators.py::test_an_accepted_contract_names_a_verification_record",
        "2026-11-30",
    ),
    "boundary-before-close": (
        "RB-M5: all gates of a delivery unit close before the delivery unit",
        "tests/test_human_gates.py::test_a_unit_cannot_close_while_a_gate_is_open",
        "2026-11-30",
    ),
    # "ruleset-assert" (RB-M6) closed on 2026-10-05: the gate `ruleset` asserts the
    # branch ruleset (tests/test_repo_settings.py); rule set 4.0.0 records it.
    "commit-identity": (
        "RB-P4: real identity and trailers on commits that touch decisions",
        "tests/test_repo_settings.py::test_recent_commits_carry_a_real_identity_and_trailers",
        "2026-11-30",
    ),
    "closed-vocabulary": (
        "RB-A5: where an agent decides, a closed vocabulary stands, not free text",
        "tests/test_skill_outputs.py::test_no_decision_field_accepts_free_text",
        "2026-12-31",
    ),
    "procedures-in-skills": (
        "RB-S2: procedures live in skills, not in instruction files",
        "tests/test_entry_points.py::test_procedures_live_in_skills",
        "2026-12-31",
    ),
    "doc-type": (
        "RB-S3: a page has exactly one Diataxis type",
        "tests/test_provenance.py::test_every_docs_page_declares_a_doc_type",
        "2026-12-31",
    ),
    "freshness-per-page": (
        "RB-S4: freshness per page, a deprecated page is only a pointer",
        "tests/test_validators.py::test_deprecated_pages_are_pointers_only",
        "2026-12-31",
    ),
    # --- 2ee triage 2026-09-19: demotions from the mapping (wave 2) --------
    "agents-evidence-contract": (
        "RB-A1: the evidence clause is byte-identical in every agent definition",
        "tests/test_agents.py::test_every_agent_carries_the_evidence_contract",
        "2026-11-30",
    ),
    "agents-tool-scopes": (
        "RB-A2: read-only agents carry no shell, executors declare their scope",
        "tests/test_agents.py::test_read_only_agents_have_no_bash",
        "2026-11-30",
    ),
    "skill-outputs-transfer": (
        "RB-A3: a self-asserted verdict is recomputed by a second reader",
        "tests/test_skill_outputs.py::test_a_self_asserted_verdict_is_recomputed",
        "2026-12-31",
    ),
    "hook-behaviour-tests": (
        "RB-H1/H2/H3: guards fail closed, matchers are tool names, no silencers",
        "tests/test_hook_behaviour.py::test_no_guard_is_registered_with_a_silencer",
        "2026-11-30",
    ),
    "hooks-registered-tests": (
        "RB-H4: every hook script is registered and every registration runs",
        "tests/test_hooks_registered.py::test_every_hook_script_here_is_registered",
        "2026-11-30",
    ),
    "fehler-katalog-transfer": (
        "RB-G2: the gate level follows from the significance in the error catalogue",
        "tests/test_fehler_katalog.py::test_every_gate_reference_matches_the_significance_level",
        "2026-12-31",
    ),
    "kit-transfer": (
        "RB-G5/G6/P3: export-schema and evidence-pipeline checkers travel with the kit transfer",
        "tests/test_export_schemas.py::test_missing_schema_is_exit_2_and_stale_is_exit_1",
        "2026-12-31",
    ),
    "human-gates-transfer": (
        "RB-M4: the reconciliation report carries a signer and justified tolerances",
        "tests/test_human_gates.py::test_a_recon_report_without_a_signer_is_unsigned",
        "2026-12-31",
    ),
    "codeowners-here": (
        "RB-M7: CODEOWNERS covers every decision path with a line of its own",
        "tests/test_repo_settings.py::test_codeowners_covers_every_human_decided_path",
        "2026-11-30",
    ),
    "owner-roles-here": (
        "RB-M8: the roster resolves role to handle, never the reverse",
        "tests/test_provenance.py::test_owner_is_a_role_not_a_person",
        "2026-11-30",
    ),
    "provenance-validators": (
        "RB-P1/P2: artifact classes, sign-offs and the directory map are checked",
        "tests/test_provenance.py::test_every_in_scope_file_declares_a_class",
        "2026-11-30",
    ),
    "gate-record-validators": (
        "RB-M1: the record template is checked by a validator",
        "tests/test_validators.py::test_gate_record_template_validates",
        "2026-11-30",
    ),
}


def _regel_ventil(name: str) -> Ramp:
    was, erzwinger, frist = REGEL_VENTILE[name]
    return Ramp(
        name=name,
        condition=(f"{was} — due as soon as `{erzwinger}` exists (at the latest {frist})"),
        predicate=lambda ref=erzwinger: _enforcer_exists(ref),
        target=Level.BLOCK,
        until_then=Level.INFO,
        deadline=date.fromisoformat(frist),
    )


def valves() -> list[Ramp]:
    """All open valves. An empty list would be a finding, not a success."""
    aktiv = selected_rule_groups()
    lint = [_lint_valve(g, was) for g, was in WARTENDE_LINT_GRUPPEN.items() if g not in aktiv]
    regel = [_regel_ventil(n) for n in REGEL_VENTILE]
    return [*lint, provenance_review_valve(), *regel]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Shows the deliberately open valves and whether any is due.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    offen = valves()
    faellig = [v for v in offen if v.due]

    if args.format == "json":
        print(
            json.dumps(
                [{"name": v.name, "condition": v.condition, "due": v.due} for v in offen],
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1 if faellig else 0

    print(f"{len(offen)} open valve(s) · active in ruff.toml: {', '.join(sorted(selected_rule_groups()))}\n")
    for v in offen:
        marke = "DUE    " if v.due else "open   "
        print(f"  {marke}  {v.name}")
        print(f"           {v.condition}")
    if faellig:
        print(
            "\nAt least one valve is due: the condition holds, but the check still sits "
            "at the lower level. A rule that costs nothing any more and stays off "
            "anyway is a wasted gate."
        )
        return 1
    print("\nNo valve is due — all are still waiting for their condition.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
