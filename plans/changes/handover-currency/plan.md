---
title: "Plan — handover-currency"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ni8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, handover, documentation, currency]
---

# Plan — handover-currency

```text
For you:     Each handover checks the architecture and front documents and refreshes your management status view.
Done when:   Missing checks fail verification, legacy records stay intact, and a real handover demonstrates the vault update.
Appetite:    4 hours of phase 4, including repairs; stop and hand over when exhausted.
Not now:     Age warnings, automatic handovers, a vault synchronizer, a new board, or backfilling old handovers.
Pre-mortem:  suppose it failed: most likely because a complete-looking record claims a check nobody performed.
Starts unless you say stop.
```

## Implementation

1. Extend the existing schema with strict configuration and body-record readers;
   keep its frontmatter helpers and channel contract compatible. Add the
   read-only command and fixture tests, then the prospective-adoption cases.
2. Add the blocking gate in the one gate list, derive CI, and bind this
   repository's targets to a pre-rule commit whose handover bodies match the
   adoption PR's starting tree. Before merge, bring the adoption PR up to date
   and include the latest pre-rule main-line handovers in this still-proposed
   snapshot; after adoption never advance it to exempt later records. The
   instance records its own full commit id, never a backdatable file date.
3. Move the authoring instructions, templates and kit classifications together.
   Run the focused tests, planted faults and full verification, then have an
   authorized writer demonstrate the actual management update. Stop on the
   appetite; do not widen into a vault integration to finish the demonstration.

The implementer needs this plan and `spec.md`; the design's necessary details
are carried below. Explore used Stage 2, GLM 5.3 Flash on `glm-coding-plan`,
attempt 1 on 2026-10-14; no Stage-1 fallback was recorded.

## Files

| Path | Operation and purpose |
|---|---|
| `scripts/handover_schema.py` | Extend the existing library with the single configuration/body-record grammar, keeping all current frontmatter and channel definitions. |
| `scripts/check_handover_currency.py` | Create the read-only CLI that discovers handovers and checks required session segments using the schema. |
| `tests/test_handover_currency.py` | Create portable fixtures and failure probes for completeness, adoption, CLI verdicts and external-access isolation. |
| `tests/test_feedback_channel.py` | Extend the template check to hold the new body example and preserve the existing direction/hash tests. |
| `tests/test_ci.py` | Add the new gate's removal/enforcement fault case following the existing gate tests. |
| `decisions/handover-check.yaml` | Create this repository's five target bindings, handover directory and fixed pre-rule commit. |
| `decisions/gates.yaml` | Add `handover-currency`, command `python3 scripts/check_handover_currency.py`, job `verify`, enforcement `block`, placement `both`, floor `false`, `needs_history: true`. |
| `.github/workflows/ci.yml` | Regenerate from the gate list; do not edit the derived steps. |
| `templates/handover.md` | Add a complete currency-section example, addendum guidance and write/read-back evidence outside the immutable findings block. |
| `templates/handover-check.yaml` | Create an unbound instance-settings example with adoption, paths and view locators requiring local values. |
| `AGENTS.md` | State the standing obligation at session end, with the configuration, completion gate and historical exemption. |
| `docs/WORKFLOW.md` | Extend the eighth-movement gate and authoring sequence, including the management projection and its relation to daily reconciliation. |
| `README.md` | Point authors and kit adopters to the handover rule and instance-configuration template. |
| `tools/claude-code/skills/handover/SKILL.md` | Add the check/update/receipt steps in the maintainer's German display language, preserving the existing first three resume sections. |
| `tools/claude-code/README.md` | Document the authoring behavior and reinstall step; no hook or status-line behavior changes. |
| `scripts/kit/manifest.yaml` | Carry the command, test and new template as `mechanismus`; explicitly keep `decisions/handover-check.yaml` as `bestand`. |
| `scripts/export/manifest.yaml` | Carry the new validator and its imported `handover_schema.py`; the template already travels, while local settings retain `drop`. |
| `tests/test_kit.py` | Hold the portable mechanism/local-binding distinction and export dependency closure. |
| `plans/changes/handover-currency/spec.md` | Preserve the criteria; update implementation status and review metadata only as earned. |
| `plans/changes/handover-currency/design.md` | Keep the proposed design aligned if a freely revisable detail changes. |
| `plans/changes/handover-currency/plan.md` | Replace implemented `not yet written` ledger entries and record measured phase-4 time and evidence. |
| `plans/changes/handover-currency/findings.md` | Retain runner evidence and record the later reviews and dispositions through the runner. |
| `plans/INDEX.md` | Let the runner regenerate the registry after artifact changes. |
| `docs/journal/handover/2026-10-14-handover-currency.md` | The authorized author creates the live-rehearsal handover with its actual check and receipt, after the worker's code step. |

No deletion is planned. The real rehearsal writes only the existing registered
project-status block in `~/ADHS-Vault/20-Projekte/Software/coding-harness.md`,
as identified in decisions Q-1, and creates the named handover through the
normal procedure. If the rehearsal runs on a later day, update the proposed
date-based filename in this plan and record the actual path and source commit
in the PR evidence. Before that write, the authorized author reads the repository's entry
in `~/ADHS-Vault/_agent/Vault-Repo-Abgleich.md` and resolves every registered
note, including the existing board views named there; these are checked, not
migrated. If the registration no longer names that project note, stop the live
write and record the exact existing destination rather than creating a note.
The runner's worktree-only phase-4 worker does not perform this external step;
the orchestrator with vault access does it. No private contents are copied into
repository evidence. An unavailable destination remains incomplete.

## Contract to implement

- Configuration: strict YAML `schema_version: 1`, a repository-relative
  `handover_dir`, fixed full `adoption_ref`, and nonempty `targets` with unique
  `id`, `kind: file|tree|management`, `locator`; require a management target.
  Bind this instance's architecture tree, three front documents and registered
  management views. Reject unresolved example values, duplicate keys/ids,
  unknown versions and repository file/tree paths escaping the root.
- At adoption, resolve the recorded commit's handover paths and bodies using
  read-only git. Exempt unchanged bodies; permit normal header stamps. On a
  legacy file validate only the appended body suffix and reject replacement of
  its historical body. A file absent at adoption is subject even if backdated.
  Missing config, history, directory, unreadable files or enumeration errors
  are unmeasured (exit 3); an existing empty configured directory is a measured
  zero new records, reported as such (exit 0).
- Split new bodies/suffixes at unfenced level-two headings beginning `Addendum`
  in the existing dated or dash form. Each nonempty session segment needs one
  `Documentation currency` heading at level two or three and one fenced YAML
  record. A quoted example or a section inside immutable findings is invalid.
- Record: `schema_version: 1`, timezone-bearing ISO `checked_at`, inspected
  `source_ref`, and `checks` with exactly the configured target ids. Each group
  has nonempty `documents`, individually named with `status: current|stale`
  and nonempty `detail`. Reject duplicate document locators within a group,
  empty evidence and placeholders. Stale claims require a follow-up action
  with bead and work description; a completed small correction records
  `action.kind: corrected` and the PR path/explanation, with final status current.
- A management group additionally requires `update.status: done`,
  timezone-bearing `updated_at`, repository `source_path`, source commit and
  write/read-back `evidence`. Explicit `incomplete` states produce a locating
  finding. The gate treats external locators as text and never follows them.
- The gate validates recorded inventory, not the truth or completeness of a
  claimed real-world inspection. Do not retroactively expand old records when
  new architecture documents appear. The writer/reviewer checks each current
  document and registered vault note; small fixes belong to the handover PR,
  larger ones to an existing/new bead obtained under the one-writer rule.
- Commit any substantive source corrections through ordinary green
  verification first, in the same handover PR. Refresh/read back the project
  status view with an existing committed status source (for example this change's
  plan or the roadmap) and write the complete handover with that receipt.
  Its `source_path` identifies that source document, not a handover that does
  not exist at the cited commit. Publishing the handover needs no second refresh
  when its reported status is unchanged; substantive later changes do. The
  author owns the refresh even when daily reconciliation is scheduled.
- CLI: `--root DIR`, default this checkout; sorted path/segment findings and
  explicit checked/exempt counts. Exit 0 complete, 1 findings, 3 unmeasured.
  Neither network, credentials nor external directories are needed in CI.
- Kit: fixture tests use another tree (`journal/` and different targets);
  local bindings/adoption do not travel. Keep `probe.REIST_NICHT` and its cap
  unchanged; an actual corpus/configuration assertion belongs in the gate,
  not in a new stock-dependent portable test.

## Criterion ledger

- 1: not yet written tests/test_handover_currency.py::test_new_handover_requires_every_configured_target — no section, empty checks or an omitted target accepted
- 2: not yet written tests/test_handover_currency.py::test_document_records_require_individual_status_and_detail — a document without current/stale or a named inventory accepted
- 2: not a test — phase-6 review compares the rehearsal's individual inventory and judgments with every architecture/front document and registered repository vault note at its cut-off; an omission or date-only judgment refutes it
- 3: not yet written tests/test_handover_currency.py::test_stale_document_requires_a_specific_detail — empty stale explanation accepted; the live review also rejects a non-specific claim
- 4: not yet written tests/test_handover_currency.py::test_corrected_document_requires_pr_evidence — claimed correction without its PR path accepted
- 4: not a test — phase-6 review checks each rehearsal correction against the handover PR diff; a missing small fix refutes it
- 5: not yet written tests/test_handover_currency.py::test_remaining_stale_claim_requires_follow_up_bead — stale claim without bead/work description accepted
- 5: not a test — the orchestrator shows the referenced bead and tracker ownership for each larger correction; missing work or an unauthorized tracker write refutes it
- 6: not yet written tests/test_handover_currency.py::test_management_refresh_requires_done_and_readback_evidence — a promise, incomplete update or empty receipt accepted
- 6: not a test — an authorized author performs and reads back the real project-status update for the rehearsal, even if unchanged; deferred reconciliation or a fixture-only claim refutes it
- 7: not yet written tests/test_handover_currency.py::test_management_receipt_requires_view_time_source_path_and_commit — any evidence identifier absent accepted
- 8: not yet written tests/test_handover_currency.py::test_unavailable_target_is_incomplete — an explicit read/write failure accepted as complete
- 9: not yet written tests/test_handover_currency.py::test_legacy_body_is_exempt_without_a_new_section — untouched historical body fails or is rewritten
- 10: not yet written tests/test_handover_currency.py::test_legacy_addendum_needs_its_own_check — legacy path exempts a new unchecked suffix
- 10: not yet written tests/test_handover_currency.py::test_each_new_session_segment_needs_one_real_section — another session's check, an example or immutable finding substitutes for the required section
- 11: not yet written tests/test_handover_currency.py::test_backdating_a_new_file_does_not_exempt_it — header or filename date grants exemption
- 12: not yet written tests/test_handover_currency.py::test_cli_locates_incomplete_and_unmeasured_handovers — broken input gives exit 0 or loses the file/segment
- 12: not yet written tests/test_ci.py::test_handover_currency_gate_blocks_locally_and_in_ci — removal, report enforcement or missing history requirement is undetected
- 13: not yet written tests/test_handover_currency.py::test_another_repository_uses_its_own_paths_and_adoption — fixture inherits this repository's documents or commit
- 13: not yet written tests/test_kit.py::test_handover_check_travels_without_instance_bindings — missing validator/schema/template or copied local settings undetected
- 14: not yet written tests/test_handover_currency.py::test_verification_never_opens_the_management_view_or_writes — external access, network use or a changed byte is undetected
- 15: not yet written tests/test_feedback_channel.py::test_currency_example_satisfies_the_schema — the template's example is incomplete while its test stays green
- 15: not a test — phase-6 review reads AGENTS, WORKFLOW, template and reinstalled handover skill against the obligation; a deferred update or absent completion step refutes it

## Verification

Run within the checkout's existing activated `.venv` (otherwise `make venv`
once, then `source .venv/bin/activate`), verbatim:

```bash
python3 scripts/ci_gates.py --generate-ci
python3 -m pytest tests/test_handover_currency.py tests/test_feedback_channel.py tests/test_ci.py tests/test_kit.py -q
python3 scripts/check_handover_currency.py
python3 scripts/check_interview_minimums.py --change handover-currency
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

Demonstrate red against fixture faults: remove the required section/target,
strip the management receipt, append an unchecked legacy session, backdate a
new file, remove the snapshot commit and weaken the gate to report. Record the
fault, failing test and restored green result. The real authoring rehearsal
adds the actual source commit and write/read-back evidence; it is not performed
by CI. Reinstall the changed authoring skill through
`tools/claude-code/install.sh` on the authorized writer's machine.

## Do not touch

Do not backfill the corpus, change historical claims or hashes, change the
status line/hooks, implement the 95-percent trigger, change the daily vault
reconciliation, migrate boards, modify another repository, or repair unrelated
architecture content/translation. No ADR or ADR answer is written by this
implementation; the maintainer's answer remains a pre-merge workflow step.

## Draft handoff — 2026-10-14

Drafted on `explore/handover-currency` at `d9cbe20`; no commit or implementation
was performed here. Interview minimums and the criterion ledger pass. The
runner owns derived files, full verification and its one commit. The named
change-artifact validator is absent; the plans registry's tracker-dependent
check is left to the runner because this draft may not read outside the
worktree/git directory. Current remote PR state, tracker ownership and the live
vault were not read. No phase-2a rows exist to dispose of. Resume: let the
runner verify and commit this draft, then show the unchanged card and route
the spec review; record only the maintainer's eventual ADR answer.

## Time used
