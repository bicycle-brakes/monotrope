---
title: "Draft ADR 0007 amendment — interactive sessions use the checked runner"
status: draft
implementation_status: partial
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-10
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

Status: moved on 2026-10-10 into the decision record `docs/adr/0012-interactive-stage-2-sessions-run-through-the-checked-runner.md` (ADR 0012), which the merge of its pull request accepts. This draft is kept as the change's record and is no longer edited.
Decider: maintainer. Prepared by Codex, 2026-10-07; the OpenCode Go launcher
re-pointed from the OpenCode CLI to Pi on 2026-10-09 (decisions Q-1 to Q-6).
Amends launch scope, not reviewer/model selection; supersedes no whole ADR.

## Context

Budget takeover needs interactive work without skipping the declaration, leak
check and audit required of finite phase calls. The maintainer therefore
requested an extended launch boundary, not relaxed prerequisites.

## Decision Drivers

- Preserve declared framework-only endpoints and refuse unknown transports.
- Provide an independent window with a checked handover and honest audit.
- State exactly what launch scanning and dispatch prove.
- Carry all OpenCode Go traffic through one launcher, Pi, as ADR 0011 already
  does for the review loop; the maintainer wants no OpenCode CLI.

## Considered Options

- Checked Terminal dispatch with start-only scan and audit.
- Direct TUI launch relying on a manually run prior scan.
- Supervised program-start acknowledgment with another lifecycle mechanism.
- For OpenCode Go models: Pi with a runner-supplied policy extension
  (proposed), or the OpenCode CLI with its effective-policy read-back
  (rejected by the maintainer, 2026-10-09).

## Decision

Proposed option: checked Terminal dispatch. Interactive foreign sessions start
only through `python3 scripts/stage2.py session <change> --model <id>` in the
canonical worktree. A declared framework endpoint and clean leak check over
the exact initial prompt are prerequisites. The audit records date, model,
endpoint, handover source and scan counts. Terminal acceptance is success,
not proof of CLI startup, authentication or model success.

An `opencode-go/<model>` id selects Pi: the id names the endpoint, not the
launcher. Pi starts at the pinned version only, with discovery off and one
runner-supplied policy extension that blocks file tools outside the worktree
and writes to its own file, `.stage2-sessions/` and `.pi/`, and asks before
`bash` calls that match dangerous patterns. The runner confirms the extension
loaded; its behaviour is held by tests, not read back from a live Pi. The
session signs in with the maintainer's own `~/.pi/agent`; the runner reads
nothing from it.
Codex uses workspace-write/on-request without claiming worktree-only reads.
Neither harness configuration is OS confinement.

## Consequences

- The scan covers launch only, with existing exclusions; later edits/prompts,
  approved arbitrary shell code and UI model/agent changes are not scanned.
  Another model re-enters through the runner.
- This change approves no new endpoint, credential or review order; the
  `opencode-go` declaration is ADR 0011's.
- Initial support is macOS Terminal only, with no silent fallback.
- The proof of the policy is weaker than OpenCode's read-back: a bug in the
  extension that its tests miss is not seen at launch.
- Only dangerous `bash` patterns ask; a command outside the list runs unasked.
- `~/.pi/agent` may hold other providers' credentials, so a model switched
  inside the session can leave the declared endpoint unscanned.
- `.git/` stays writable for the session.
- Bead coding-harness-0al (the OpenCode 2.x failure) is superseded: no
  `opencode` call remains.

## Validation

- Tests plant wrong worktrees, undeclared models, forbidden prompt/index data,
  hostile quoting, a Pi off the pin, extension handler faults (paths outside
  the worktree, protected paths, dangerous `bash` without a UI) and
  terminal/audit failures.
- Full `make verify` and independent review precede the decision PR.
- A real GUI/model run is named explicitly if measured; stand-ins do not
  prove live confinement, authentication or model success.
