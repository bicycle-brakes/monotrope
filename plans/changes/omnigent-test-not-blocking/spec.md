---
title: "Spec — omnigent-test-not-blocking"
status: draft
implementation_status: partial
date: 2026-11-12
last_reviewed: 2026-11-12
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-i9df
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, omnigent, tests]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — omnigent-test-not-blocking

Report differences between Omnigent's installed tool names and the repository's
classification during policy installation instead of failing the ordinary test
suite on those differences (bead coding-harness-i9df — move the installed-tool
comparison out of blocking verification). Research: [research.md](research.md).
Decision: [decisions.md, Q-1](decisions.md#q-1--what-not-blocking-means).

## Problem

At baseline `7bd3d64d` (2026-11-12), the native-surface test compares the
installed Omnigent's tools with the repository's three classification lists
in both directions. An external update can therefore fail the blocking
`pytest` gate without a repository change. Research records the added tools
in the Omnigent 0.21.0 fix and the previously intended strict comparison;
the interview records the maintainer's decision to report it at installation.

The rendered-rule and policy tests check separate guarantees. Making the
whole test file or pytest gate advisory would discard those guarantees,
contrary to the answer in `decisions.md` Q-1. The old archived specification's
installed-surface requirement is replaced by this change; historical artifacts
remain unchanged.

## Terms

**Surface:** the tool names exposed by the installed Omnigent.
**Drift:** surface names absent from the repository's classification, or
classified names absent from the surface; it says nothing about how a new
tool should be classified.

## Acceptance criteria

1. When the ordinary test suite runs, equality between the classification
   lists and the locally installed Omnigent's surface is no longer a pass condition.
   *Refuted by:* adding or removing an installed tool name alone fails a test.
   *Basis:* decisions.md#Q-1.

2. When policy installation or reinstallation can read Omnigent's surface,
   its output identifies drift in each direction by tool name, or states that
   the surface matches.
   *Refuted by:* an unclassified tool or a no-longer-offered tool is omitted,
   a matching surface is reported as drift, or an unchanged reinstall omits the report.
   *Basis:* decisions.md#Q-1; research.md, "How the tests run".

3. When installation produces a surface diagnostic, that diagnostic leaves
   the installation's success or failure result unchanged.
   *Refuted by:* drift or a failed surface read makes an otherwise successful
   installation fail, or reporting turns a failed policy merge into success.
   *Basis:* decisions.md#Q-1.

4. If the surface cannot be read during an otherwise successful installation,
   the output explicitly reports that the comparison could not be performed.
   *Refuted by:* an import or discovery error is silent or is reported as a
   matching or empty surface.
   *Basis:* decisions.md#Q-1; research.md, "What is unclear about it".

5. When repository-owned classification or rendered-rule invariants are
   violated, their existing checks remain blocking.
   *Refuted by:* stale rendered policies, a missing deny or ask rule, or an
   overlapping classification becomes a skip, warning or successful check.
   *Basis:* decisions.md#Q-1.

## Non-goals

- Changing the pytest gate's enforcement, placement or membership.
- Weakening any other Omnigent test, including installed-code policy evaluation.
- Automatically classifying new tools, changing tool lists or regenerating rules.
- Installing or updating the Omnigent package, adding an upgrade watcher, or
  invoking the maintainer's real installer/configuration from this change's tests.
- Reconciling historical tool counts or completing the old live security probe.

This is the interview's `bounded` change: phase 2b and an ADR are not due.

## Protected areas

- `.claude/settings.json`, `tools/omnigent/policy.yaml` and the classification
  tables: the rule set is unchanged.
- `decisions/gates.yaml`, `.github/`, `provenance.yaml`, `AGENTS.md`, `prompts/`
  and `templates/`: no gate, governance or workflow change is needed.
- Installer terminal refusal, backups, validation before writes, foreign-policy
  preservation, restart messages, and `--check`/`--remove` semantics: only the
  install diagnostic changes; existing failures must retain their exit status.
- Archived change artifacts: historical evidence is preserved.

## Definition of Done

- Targeted checks and `make verify` are green on the implementation commit.
- Deterministic tests exercise matching, added, removed and unreadable surfaces,
  installer reporting on a no-op reinstall, and preservation of merge failure.
- `tools/omnigent/README.md` explains the install-time report and its limits;
  no models or ADR files change.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the installed-tool comparison task
  (coding-harness-i9df); its last commit carries `Closes-Bead: coding-harness-i9df`.
- No special live run is required; fake surfaces and temporary configurations
  provide regression evidence without changing the maintainer's machine.

## Open decisions

None open. The maintainer chose install-time reporting and accepted its later
notification in `decisions.md` Q-1, recorded on 2026-11-12.

[DETAIL] Keep both directions of the old comparison in the report, because
missing classified names are useful evidence too; neither direction blocks.
[DETAIL] Use deterministic stand-ins to test reporting, because a regression
test must not depend on the locally installed version reproducing drift.
[DETAIL] Set a two-hour phase-4 appetite, repairs included, because this is one
comparison relocation with no gate or policy redesign; stop and report at the limit.
