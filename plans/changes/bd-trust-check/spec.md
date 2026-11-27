---
title: "Spec — bd-trust-check"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, security, tracker]
class: bounded
adr_files: []
---

# Spec — bd-trust-check

The status line and start and handover hooks run a repository's tracker wrapper only when its origin is explicitly trusted (bead `coding-harness-5ane.2`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- The status line and handover hook select an executable repository-local `tools/bd` without a trust check; both are installed user-wide (`research.md`, 2026-11-27).
- The repository start hook also runs that wrapper without such a check; its reachability in a newly cloned repository was not established (`research.md`, 2026-11-27).
- A blank pattern in the handover content trust file matches every origin under the current matching operation (`research.md`, 2026-11-27).

## Terms

**Wrapper repository:** a repository whose tracker root (the repository top, or the main worktree's top when the tracker lives there) holds an executable `tools/bd`. Only wrapper repositories are affected by this change; a repository with `.beads/` but no executable `tools/bd` keeps today's behaviour and uses the `bd` on `PATH`, because no repository code runs (maintainer 2026-11-28, S-18).

**Trusted repository:** a wrapper repository whose nonempty Git origin URL exactly equals an entry of the tracker trust list. The list is `${XDG_CONFIG_HOME:-$HOME/.config}/coding-harness/trusted-repositories`.

**Git origin URL:** the output of `git remote get-url origin` in the repository, the same value `handover.sh` reads today (S-3, reading A; `insteadOf` rules apply).

**Entry:** a line of the list after removing leading and trailing whitespace, including a carriage return; a line that is then empty, or whose first character is `#`, is no entry (S-7).

## Acceptance criteria

1. When a wrapper repository is not trusted, the status line, handover hook and repository start hook run no `bd` at all for it: neither its local `tools/bd` nor a `bd` on `PATH`, directly or indirectly (maintainer 2026-11-28: no fallback).
   *Refuted by:* a marker written by that wrapper, or by a recording `bd` on `PATH`, after any of the three paths runs, including start reconciliation.
2. When a wrapper repository is trusted, each of the three paths uses its `tools/bd` for its tracker operation, also when no `bd` is on `PATH` (the status line's `command -v bd` gate no longer decides alone; S-2, reading B).
   *Refuted by:* a trusted wrapper receives no expected list or prime invocation, with or without a `bd` on `PATH`.
3. A repository with `.beads/` but no executable `tools/bd` behaves exactly as before this change, whether or not it is on the trust list.
   *Refuted by:* such a repository shows `bd: not trusted`, loses its beads line or prime output, or runs a different `bd` than today.
4. If the tracker trust list is absent, unreadable, contains no entry, or the origin is missing, a wrapper repository is untrusted.
   *Refuted by:* any such case authorizes its wrapper.
5. When the tracker trust list contains an entry, only an exact match authorizes that origin.
   *Refuted by:* a partial match, a regular-expression metacharacter interpretation, or a different origin authorizes the wrapper.
6. When the handover content trust file contains blank lines, those lines do not authorize any origin and nonblank regular expressions retain their existing matching behavior.
   *Refuted by:* a blank line exposes an untrusted handover, or a matching nonblank pattern no longer exposes the trusted handover.
7. The common tracker trust selection is available to both installed scripts and the repository start hook. Installed scripts load it only from their installed location, never from the repository being shown; the start hook, which is repository code wired by `.claude/settings.json`, loads it from beside itself (S-11, reading A). When the selection is missing or unreadable, a wrapper repository is untrusted (AC1) and the warning appears once per run of each path: the status line's text `bd: trust check unavailable` in place of the beads line, one line in the handover hook's `systemMessage`, one stderr line of the start hook (S-5, S-14, S-16). `install.sh --check` reports an absent tracker trust list as a note with its path and the exact line to add (this repository's origin URL); its exit status still reflects only file and settings drift (S-12, reading B). `install.sh` does not create or seed the list (S-8).
   *Refuted by:* an installed script cannot perform the same trust decision; a missing or unreadable selection grants trust, with or without a warning; the installed scripts load the selection from the shown repository; the warning is missing or repeated within one run; `--check` stays silent about an absent list, omits the line to add, or exits non-zero for it alone; or `install.sh` writes or seeds the list.
8. When an untrusted wrapper repository is skipped, each path says so plainly and exits as before: the status line shows `bd: not trusted` instead of the beads line; the handover hook renders the tracker state as `nicht vertraut` in its `systemMessage` and states "beads not read: repository not trusted" in its measured `additionalContext` (never a timeout or "keine Antwort"); the start hook prints one stderr line naming the trust list and exits 0, and its held-back reconciliation is part of that one report (S-6, S-17, S-20).
   *Refuted by:* a trust skip is shown as a timeout or as no answer, hides silently, is reported more than once, or makes the start hook exit non-zero.
9. Trust is decided before either path reads the beads cache (`$TMPDIR/claude-statusline/beads-<key>.json`): for an untrusted wrapper repository, a cached beads line is neither shown nor injected (S-13, reading A).
   *Refuted by:* a pre-written cache for an untrusted wrapper repository appears in the status line or as read in the handover.

## Non-goals

- Changing the existing handover content trust list into the tracker trust list, or automatically trusting its entries for executable code.
- Changing the Antigravity hook's separate ancestry check, general workspace trust, or the tracker itself.
- Guaranteeing safety if a user runs a malicious repository's own hook or other arbitrary repository code; this change guards tracker selection by these paths.

## Protected areas

Leave `.agents/hooks/session-start.sh` and its ancestry policy unchanged: it belongs to a separate hook.

## Definition of Done

- `make verify` green; the tracker trust behavior and the handover content trust format are documented in `tools/claude-code/README.md`.
- Protected areas remain untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes bead `coding-harness-5ane.2` and its last commit carries `Closes-Bead: coding-harness-5ane.2`.
- Special runs: none.

## Open decisions

- [DETAIL] Use exact origin URL lines in the XDG configuration file above: literal matching makes an explicit authorization auditable and avoids accidental regular-expression matches. Keep the existing handover content list separate because permission to read text does not authorize code execution.
- [DETAIL] Retain Antigravity's existing ancestry check unchanged: its independent policy is outside the three named paths.
- [DETAIL] Skip start-hook reconciliation and prime for untrusted wrapper repositories: reconciliation can invoke the local wrapper indirectly, and no external `bd` runs for them (scope narrowed 2026-11-28).
- [DETAIL] Spec-review S-1..S-8 (round 1, decided by the orchestrator under the bounded standing grant, 2026-11-27): S-1 reading B — an external `bd` is used only when pin-compatible, because a newer `bd` migrates a store one way (`tools/bd`); S-2 reading B — a trusted executable wrapper suffices without a `bd` on `PATH`; S-3 reading A — `git remote get-url origin`, as `handover.sh` already reads it; S-4 — "outside" by resolved real path against the repository and main-worktree tops, empty and relative `PATH` entries skipped; S-5 — a missing or unreadable trust selection means untrusted plus one warning, and installed scripts never load it from the shown repository; S-6 — trust skips are reported as such (new AC8) and the start hook exits 0; S-7 — entries are trimmed (CR included), blank and `#` lines are no entries; S-8 — `install.sh --check` reports an absent list with the line to add, nothing is seeded. All are reversible.
- [DETAIL] Spec-review S-9..S-15 (round 2, orchestrator under the bounded standing grant): S-9 A — the trust notice only when the operation is really skipped; S-10 A — only the first `bd` on `PATH` is a candidate; S-11 A — the start hook loads the selection from beside itself; S-12 B — an absent list is a `--check` note, not drift; S-13 A — trust before the cache read (new AC9); S-14 — warning texts, places and once-per-run refutations in AC7; S-15 — exact version comparison as `tools/bd`, empty or unreadable `VERSION` skips (fail closed). All reversible.
- [DETAIL] Scope narrowed by the maintainer (2026-11-28, answer "ja" to the orchestrator's question after spec-review round 3): only wrapper repositories are affected; an untrusted wrapper repository runs no `bd` at all, so the external-`bd` fallback, its pin-compatibility and candidate rules and the `bd version` probe are dropped. This supersedes the [DETAIL] entries for S-1, S-4, S-9, S-10 and S-15 above and resolves S-16..S-21.
