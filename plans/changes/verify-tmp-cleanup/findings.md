---
title: "Findings — verify-tmp-cleanup"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-tmp-cleanup

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1008 files, 3890 commits, 12 rules.

## Draft evidence — 2026-11-10

Drafted `spec.md` and `plan.md` against checkout `f035b46a`; implementation
has not started. The class remains bounded, so neither a design document nor
an ADR draft is due. No phase-2a review rows were present to resolve.

Checks run with the checkout's `.venv/bin/python3` and
`PYTHONDONTWRITEBYTECODE=1`, all exiting 0:

- `scripts/check_interview_minimums.py --change verify-tmp-cleanup`: green
  on the existing reasoned skip; no maintainer answer was added.
- `scripts/check_criterion_ledger.py`: green, including the new plan's
  not-yet-written test entries.
- `scripts/check_research_handoff.py --change verify-tmp-cleanup`: measured,
  exempt from swarm-specific obligations because no v2 evidence exists.
- `scripts/check_frontmatter_current.py`: green.
- A read-only structure check confirmed mandatory headers, eleven numbered
  criteria with refuting cases, the opening plan card and empty time section.

`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent in
this checkout. The plan follows the phase-3 prompt and existing plan form.
The full check, index regeneration, tracker-backed registry check and commit
remain the runner's work; no full verification result is claimed here.
The remote pull-request state was not read: `gh pr view` could not connect
to the GitHub API. The external session registry was not read, as this
attempt is restricted to the worktree and repository Git directory; no
tracker write was made.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-tmp-cleanup/findings.md` +28 -0
> - `plans/changes/verify-tmp-cleanup/plan.md` +158 -0
> - `plans/changes/verify-tmp-cleanup/spec.md` +169 -0
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/verify-tmp-cleanup/findings.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> plans/changes/verify-tmp-cleanup/plan.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> plans/changes/verify-tmp-cleanup/spec.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 36921 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-11: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 1011 files, 3901 commits, 12 rules.

## Draft repair evidence — 2026-11-11

Reviewed the existing spec and plan against `research.md`, `decisions.md`
and the available templates at checkout `f035b46a`. No open phase-2a rows
were present. The class, eleven criteria, decisions and plan card remain
unchanged; no design or ADR is due for this bounded change.

Updated only the spec and plan's `updated` and `last_reviewed` fields and
this findings record. Their creation dates remain 2026-11-10. The previous
attempt's frontmatter result above predates its failed post-run check;
the fresh checks below supersede that result.

Checks rerun with `.venv/bin/python3` and `PYTHONDONTWRITEBYTECODE=1`,
all exiting 0:

- `scripts/check_interview_minimums.py --change verify-tmp-cleanup`.
- `scripts/check_criterion_ledger.py`.
- `scripts/check_research_handoff.py --change verify-tmp-cleanup`:
  explicitly exempt because this change has no research-swarm/v2 evidence.
- `scripts/check_frontmatter_current.py`: every held document is current.
- A read-only structure check: required headers, eleven refuting cases,
  the opening plan card, empty time section and no open review rows.

The unavailable template and validator noted above remain unavailable.
Full verification and the commit remain the runner's work. The existing
`plans/INDEX.md` modification was left untouched. Remote pull-request and
external session-registry state were not read under the worktree-only
restriction; no tracker write or git mutation was performed.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`
