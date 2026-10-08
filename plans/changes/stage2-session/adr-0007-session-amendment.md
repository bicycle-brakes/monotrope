---
title: "Draft ADR 0007 amendment — interactive sessions use the checked runner"
status: draft
implementation_status: partial
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr-draft, stage-2, session]
---

# Draft ADR 0007 amendment — interactive sessions use the checked runner

Status: proposed in the decision PR, not an accepted ADR 0007 edit.
Decider: maintainer. Prepared by Codex, 2026-10-07. Amends launch scope,
not reviewer/model selection; supersedes no whole ADR.

## Context

Budget takeover needs interactive work without skipping the declaration, leak
check and audit required of finite phase calls. The maintainer therefore
requested an extended launch boundary, not relaxed prerequisites.

## Decision Drivers

- Preserve declared framework-only endpoints and refuse unknown transports.
- Provide an independent window with a checked handover and honest audit.
- State exactly what launch scanning and dispatch prove.

## Considered Options

- Checked Terminal dispatch with start-only scan and audit.
- Direct TUI launch relying on a manually run prior scan.
- Supervised program-start acknowledgment with another lifecycle mechanism.

## Decision

Proposed option: checked Terminal dispatch. Interactive foreign sessions start
only through `python3 scripts/stage2.py session <change> --model <id>` in the
canonical worktree. A declared framework endpoint and clean leak check over
the exact initial prompt are prerequisites. The audit records date, model,
endpoint, handover source and scan counts. Terminal acceptance is success,
not proof of CLI startup, authentication or model success.

OpenCode starts with a dedicated checked policy denying external directories
and asking before shell execution; an unresolved effective override blocks.
Codex uses workspace-write/on-request without claiming worktree-only reads.
Neither harness configuration is OS confinement.

## Consequences

- The scan covers launch only, with existing exclusions; later edits/prompts,
  approved arbitrary shell code and UI model/agent changes are not scanned.
  Another model re-enters through the runner.
- Go activation still requires the separate approved endpoint declaration;
  this change approves no new endpoint, credential or review order.
- Initial support is macOS Terminal only, with no silent fallback.

## Validation

- Tests plant wrong worktrees, undeclared models, forbidden prompt/index data,
  hostile quoting, permission overrides and terminal/audit failures.
- Full `make verify` and independent review precede the decision PR.
- A real GUI/model run is named explicitly if measured; stand-ins do not
  prove live confinement, authentication or model success.
