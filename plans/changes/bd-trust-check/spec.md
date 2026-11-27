---
title: "Spec — bd-trust-check"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
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

**Trusted repository:** one whose nonempty Git origin URL exactly equals an entry of the tracker trust list. The list is `${XDG_CONFIG_HOME:-$HOME/.config}/coding-harness/trusted-repositories`.

**Git origin URL:** the output of `git remote get-url origin` in the repository, the same value `handover.sh` reads today (S-3, reading A; `insteadOf` rules apply).

**Entry:** a line of the list after removing leading and trailing whitespace, including a carriage return; a line that is then empty, or whose first character is `#`, is no entry (S-7).

**Outside the repository:** a `bd` found on `PATH` counts as outside only when its resolved real path (symlinks followed) lies under neither the repository's top-level directory nor its main worktree's top-level directory; empty and relative `PATH` entries are skipped (S-4).

**Pin-compatible:** the external `bd` reports the version the repository pins in `tools/beads/VERSION` (read as data, never executed) exactly as `tools/bd` compares it: `bd version <pin>` followed by whitespace or end of line, the pin trimmed of surrounding whitespace. The file is read from the tracker root (the main worktree's top when the tracker lives there). An empty or unreadable `VERSION` file is a pin no `bd` matches, so the operation is skipped; only a missing file accepts any external `bd` (S-1 reading B, S-15).

**Candidate `bd`:** only the first `bd` that `command -v bd` finds; when it is inside the repository or not pin-compatible, there is no fallback (S-10, reading A).

## Acceptance criteria

1. When a repository is not trusted, the status line, handover hook and repository start hook do not execute its local `tools/bd`, directly or indirectly.
   *Refuted by:* a marker written by that wrapper after any of the three paths runs, including start reconciliation.
2. When a repository is trusted and its local `tools/bd` is executable, each of the three paths uses that wrapper for its tracker operation, also when no `bd` is on `PATH` (the status line's `command -v bd` gate no longer decides alone; S-2, reading B).
   *Refuted by:* a trusted wrapper receives no expected list or prime invocation, with or without a `bd` on `PATH`.
3. When a repository is untrusted, a pin-compatible `bd` on `PATH` outside that repository may provide the tracker operation; otherwise the operation is skipped without executing the repository wrapper. A repository without `tools/beads/VERSION` accepts any external `bd`.
   *Refuted by:* an unavailable fallback causes local wrapper execution; an external `bd` with a different version than the pin, a `bd` symlink resolving inside the repository, or a repository-internal shim such as `tools/beads/bin/bd` is used; or an available pin-compatible external fallback cannot provide the operation.
4. If the tracker trust list is absent, unreadable, contains only blank lines, or the origin is missing, the repository is untrusted.
   *Refuted by:* any such case authorizes its wrapper.
5. When the tracker trust list contains a nonblank origin, only an exact match authorizes that origin.
   *Refuted by:* a partial match, a regular-expression metacharacter interpretation, or a different origin authorizes the wrapper.
6. When the handover content trust file contains blank lines, those lines do not authorize any origin and nonblank regular expressions retain their existing matching behavior.
   *Refuted by:* a blank line exposes an untrusted handover, or a matching nonblank pattern no longer exposes the trusted handover.
7. When the display is installed or checked, the common tracker trust selection is available to both installed scripts and the repository start hook. Installed scripts load it only from their installed location, never from the repository being shown; when it is missing or unreadable, the repository is untrusted (AC3 then applies) and one warning names the missing file. `install.sh --check` reports an absent tracker trust list with the line to add for this repository; `install.sh` does not create or seed the list (S-5, S-8).
 The repository start hook, which is repository code wired by `.claude/settings.json`, loads the selection from beside itself in the repository, so it works without an install (S-11, reading A). `--check` reports the absent list as a note: it prints the path and the exact line to add (this repository's origin URL) and its exit status still reflects only file and settings drift (S-12, reading B). The warning for a missing or unreadable selection appears once per run of each path: as the status line's text `bd: trust check unavailable` in place of the beads line, as a line in the handover hook's `systemMessage`, and as one stderr line of the start hook (S-14).
   *Refuted by:* an installed script cannot perform the same trust decision; a missing or unreadable dependency grants trust, with or without a warning; the installed scripts load the selection from the shown repository; the warning is missing or repeated within one run; `--check` stays silent about an absent list, omits the line to add, or exits non-zero for it alone; or `install.sh` writes or seeds the list.
8. When a tracker operation is skipped for trust reasons (not when a pin-compatible external fallback provided it; S-9, reading A), each path says so plainly and exits as before: the status line shows `bd: not trusted` instead of the beads line; the handover hook renders the tracker state as not trusted (never as a timeout); the start hook prints one line on stderr and exits 0 (S-6).
   *Refuted by:* a trust skip is shown as a timeout or as no answer, hides silently, or makes the start hook exit non-zero; or a successful fallback is reported as not trusted.
9. Trust is decided before either path reads the beads cache (`$TMPDIR/claude-statusline/beads-<key>.json`): for an untrusted repository without a usable fallback, a cached beads line is neither shown nor injected (S-13, reading A).
   *Refuted by:* a pre-written cache for an untrusted repository without fallback appears in the status line or as read in the handover.

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
- [DETAIL] Skip start-hook reconciliation for untrusted repositories: it can invoke the local wrapper indirectly, while prime may use the external fallback.
- [DETAIL] Spec-review S-1..S-8 (round 1, decided by the orchestrator under the bounded standing grant, 2026-11-27): S-1 reading B — an external `bd` is used only when pin-compatible, because a newer `bd` migrates a store one way (`tools/bd`); S-2 reading B — a trusted executable wrapper suffices without a `bd` on `PATH`; S-3 reading A — `git remote get-url origin`, as `handover.sh` already reads it; S-4 — "outside" by resolved real path against the repository and main-worktree tops, empty and relative `PATH` entries skipped; S-5 — a missing or unreadable trust selection means untrusted plus one warning, and installed scripts never load it from the shown repository; S-6 — trust skips are reported as such (new AC8) and the start hook exits 0; S-7 — entries are trimmed (CR included), blank and `#` lines are no entries; S-8 — `install.sh --check` reports an absent list with the line to add, nothing is seeded. All are reversible.
- [DETAIL] Spec-review S-9..S-15 (round 2, orchestrator under the bounded standing grant): S-9 A — the trust notice only when the operation is really skipped; S-10 A — only the first `bd` on `PATH` is a candidate; S-11 A — the start hook loads the selection from beside itself; S-12 B — an absent list is a `--check` note, not drift; S-13 A — trust before the cache read (new AC9); S-14 — warning texts, places and once-per-run refutations in AC7; S-15 — exact version comparison as `tools/bd`, empty or unreadable `VERSION` skips (fail closed). All reversible.
