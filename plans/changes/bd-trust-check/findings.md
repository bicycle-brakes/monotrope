---
title: "Findings — bd-trust-check"
category: findings
status: draft
implementation_status: none
date: 2026-11-27
created: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-5ane.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — bd-trust-check

Stage-2 call, 2026-11-27: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1320 files, 6136 commits, 12 rules.

Stage-2 call, 2026-11-27: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1323 files, 6138 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-27

Spec fingerprint: sha256:63d047524dde621f19036cf29fbbc88915ceed740bd47bd4878dfb454fb410fb

Spec review commit: a7413ac9be63b93facf9b2da921156dd3076b71a

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, AC3 ("a usable `bd` on `PATH`") | Reading A: "usable" is any executable `bd` on `PATH`. In an untrusted repository that pins its tracker (this one, before its origin is listed), the status line's `list` and the start hook's `prime` then run whatever `bd` is installed against that store. That bypasses the pin `tools/bd` enforces, and `tools/bd:27-28` says a newer `bd` migrates a store's schema on open, one way. Reading B: "usable" means compatible with the repository's pin (`tools/beads/VERSION`, read as data), otherwise skip. A test with a version-mismatched `bd` on `PATH` passes under one reading and fails under the other. | Opus | in spec — reading B (pin-compatible external bd only) in Terms, AC3 and [DETAIL] S-1..S-8 (bounded standing grant) | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md, AC2; `tools/claude-code/statusline.sh:148` | The status line's beads block runs only when `command -v bd` finds a `bd` on `PATH`. Reading A: that gate stays. A trusted repository with an executable `tools/bd` but no `bd` on `PATH` then shows no beads line and its wrapper gets no `list` call, which AC2 counts as red. Reading B: a trusted executable wrapper is enough, so the gate has to change. The spec does not say whether AC2's precondition includes a `bd` on `PATH`. The handover hook (`handover.sh:152`) checks only the selected executable, so the two installed paths already differ here. | Opus | in spec — reading B (trusted wrapper suffices without bd on PATH) in AC2 and [DETAIL] S-1..S-8 | — |
| S-3 | [AMBIGUITY] | SPEC | base | spec.md, Terms ("Git origin URL"); AC5 | Reading A: the output of `git remote get-url origin` (what `handover.sh:202` uses), which expands `url.<base>.insteadOf` rules from the user's global Git config. Reading B: the raw `remote.origin.url` value. Under an `insteadOf` rule the two strings differ. The same list line then trusts a repository under one reading and not the other, and the README would have to tell users to write a different string. | Opus | in spec — reading A (git remote get-url origin) in Terms and [DETAIL] S-1..S-8 | — |
| S-4 | MAJOR | SPEC | base | spec.md, AC3 ("outside that repository"); AC1 Refuted-by | "Outside that repository" is undefined for: a linked worktree whose tracker root is the main worktree (`statusline.sh:145`); a `bd` symlink that resolves inside the repository; relative or empty `PATH` entries resolved against the working directory; and repository-internal shims such as `tools/beads/bin/bd`. Whoever builds this has to pick a rule. Nothing can go red for this clause either. AC1's marker detects only `tools/bd`, and AC3's refutation names only an unavailable fallback and an available external one. So a repository-internal `bd` on `PATH` that does not pass through `tools/bd` can run without any criterion failing. | Opus | in spec — "outside" defined by resolved real path in Terms; AC3 refutation names symlink and shim cases | — |
| S-5 | MAJOR | SPEC | base | spec.md, AC7 | The spec does not say what happens when the shared trust selection is missing or unreadable: untrusted with the `PATH` fallback, skip, a visible warning, or a non-zero `--check`. It also does not say where installed scripts may load it from. Loading it from the repository being displayed would execute that repository's code, and AC1 would not notice because it is not `tools/bd`. Because the refutation says "silently treated as trust", a missing dependency that grants trust and prints a warning still passes. | Opus | in spec — missing or unreadable selection means untrusted plus a warning; never loaded from the shown repository (AC7) | — |
| S-6 | MAJOR | SPEC | base | spec.md, AC3 ("otherwise the operation is skipped"); decisions DETAIL 3 | The spec does not say what each path reports when the operation is skipped or reconciliation is withheld for trust reasons. Status line: the beads line is hidden, or shows a trust note. Handover: `beads_json` currently leaves `beads_state=unread`, which renders as "keine Antwort in 4 s", a false timeout claim. Start hook: today a missing wrapper exits 1, which is a session-start error. The spec does not say whether an untrusted skip exits 0 or 1. Nor does it say whether the withheld reconciliation is folded into the prime JSON as a note, which the hook's own contract (`beads-start.sh:21-24`) requires for skips. | Opus | in spec — new AC8: plain trust-skip reports per path, start hook exits 0 | — |
| S-7 | MINOR | SPEC | base | spec.md, Terms ("exactly equals a nonblank line"); AC4, AC5 | The spec does not say whether lines are compared verbatim or trimmed (leading or trailing spaces, the CR of a CRLF file), whether a whitespace-only line counts as blank, or whether comment lines exist. Compared verbatim, an entry with trailing whitespace never trusts and nothing says why; trimmed, it matches. AC5 tests come out differently under each choice. | Opus | in spec — entries trimmed (CR included), blank and # lines are no entries (Terms) | — |
| S-8 | MINOR | SPEC | base | spec.md, AC7; Definition of Done | The spec does not say whether `install.sh` creates, seeds or reports the absent tracker trust list (on install or `--check`). Once this ships, this repository is itself untrusted on every machine until a line is added. Its own start hook then stops reconciling and the status line falls back. Whether that default is intended, and how the user learns of it, is left to whoever builds it. | Opus | in spec — install.sh --check reports an absent list with the line to add; no seeding (AC7) | — |
