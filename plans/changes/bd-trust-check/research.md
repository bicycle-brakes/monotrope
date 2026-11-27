---
title: "Research — bd-trust-check"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-5ane.2
owner: Data Architect
provenance: human-written
tags: [research]
---

# bd trust check — Research

## Topic (bead coding-harness-5ane.2)

Class: bounded. Why (audit S-5, confirmed and understated):
`tools/claude-code/statusline.sh:157` runs `"$beads_root/tools/bd"` whenever
`.beads` exists, `hooks/handover.sh:151` and `hooks/beads-start.sh:149` run
`"$root/tools/bd"`; installed user-wide, they execute the `tools/bd` of any
repository a session opens, so a cloned untrusted repository runs its own
script. `handover.sh:199-204` matches the trust file with `grep -qE -f`, where
a blank line matches everything. What: run a repository-local `tools/bd` only
for repositories on an explicit trusted list (harness-neutral location),
otherwise the `bd` on `PATH` or nothing; ignore blank lines in the trust file.
Acceptance: tests with a temporary untrusted repository whose `tools/bd`
writes a marker: no marker after status line, start hook and handover hook;
trusted repository still works. Source: PR #437 (full codebase audit, base
`24632499`), re-verified against main `b9ce3ac0` on 2026-11-24.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
