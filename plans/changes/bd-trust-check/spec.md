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

**Trusted repository:** one whose nonempty Git origin URL exactly equals a nonblank line in the tracker trust list. The list is `${XDG_CONFIG_HOME:-$HOME/.config}/coding-harness/trusted-repositories`.

## Acceptance criteria

1. When a repository is not trusted, the status line, handover hook and repository start hook do not execute its local `tools/bd`, directly or indirectly.
   *Refuted by:* a marker written by that wrapper after any of the three paths runs, including start reconciliation.
2. When a repository is trusted and its local `tools/bd` is executable, each of the three paths uses that wrapper for its tracker operation.
   *Refuted by:* a trusted wrapper receives no expected list or prime invocation.
3. When a repository is untrusted, a usable `bd` on `PATH` outside that repository may provide the tracker operation; otherwise the operation is skipped without executing the repository wrapper.
   *Refuted by:* an unavailable fallback causes local wrapper execution, or an available external fallback cannot provide the operation.
4. If the tracker trust list is absent, unreadable, contains only blank lines, or the origin is missing, the repository is untrusted.
   *Refuted by:* any such case authorizes its wrapper.
5. When the tracker trust list contains a nonblank origin, only an exact match authorizes that origin.
   *Refuted by:* a partial match, a regular-expression metacharacter interpretation, or a different origin authorizes the wrapper.
6. When the handover content trust file contains blank lines, those lines do not authorize any origin and nonblank regular expressions retain their existing matching behavior.
   *Refuted by:* a blank line exposes an untrusted handover, or a matching nonblank pattern no longer exposes the trusted handover.
7. When the display is installed or checked, the common tracker trust selection is available to both installed scripts and the repository start hook.
   *Refuted by:* an installed script cannot perform the same trust decision, or a missing installed dependency is silently treated as trust.

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
