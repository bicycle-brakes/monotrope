---
title: "Spec — enqueue-pr"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-va1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, merge-queue]
class: bounded
adr_files: []
---

# Spec — enqueue-pr

A single guarded command admits an eligible pull request to the merge queue (bead `coding-harness-va1l`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-25 the research found that direct merge commands require approval, so an unattended orchestrator cannot use the stated queue-admission grant. No existing script checks the pull request, phase-6 review, required checks and closure trailer together. The grant cited in the research was not present in the checked-out `AGENTS.md`; its exact wording was not read. Existing instructions require an exact head and a maintainer request for merging.

## Terms

**Head:** the pull request's current commit. **Admission:** placing that head in an enabled merge queue; admission is not proof of a merge.

## Acceptance criteria

1. When a non-draft, same-repository pull request targeting `main` is open, not already queued, and satisfies criteria 3–10, the command admits its verified head to the merge queue.
   *Refuted by:* an eligible head is refused or not queued.
2. When a request is closed, targets another branch, is a draft, or comes from a fork, admission is refused.
   *Refuted by:* any such request reaches admission.
3. When the last `## Phase 6` block in the head's findings file neither explicitly reports no findings nor has every finding row marked `fixed` or `rejected`, admission is refused, regardless of severity.
   *Refuted by:* an absent, ambiguous, open, taken or unrecognised latest verdict is admitted.
4. When the head has more or fewer than one `Closes-Bead` trailer, or its bead is unknown or closed, admission is refused.
   *Refuted by:* an absent, multiple, unknown or closed declaration reaches admission.
5. When the pull request diff does not touch exactly one change folder whose `bead` matches the head trailer, admission is refused.
   *Refuted by:* zero or multiple matching folders reach admission.
6. When the latest phase-6 block lacks a reviewed commit, or the reviewed commit is not an ancestor of the head, admission is refused.
   *Refuted by:* missing or unrelated review evidence reaches admission.
7. When a commit after the reviewed commit is neither a record-only commit inside that change folder, an empty commit, nor a merge of main, admission is refused.
   *Refuted by:* a subsequent code change reaches admission.
8. When a required check from the applicable `main` ruleset is absent, pending, failed, or has a conclusion other than SUCCESS, SKIPPED or NEUTRAL on the verified head, admission is refused.
   *Refuted by:* a missing or failing required check reaches admission, or a permitted conclusion is rejected.
9. When a pull request has the `decision` label or touches `docs/adr/`, the script refuses admission with that reason.
   *Refuted by:* such a request reaches admission.
10. When any prerequisite or the applicable ruleset cannot be read or established unambiguously, admission is refused.
    *Refuted by:* unreadable, ambiguous or missing evidence reaches admission.
11. When admission is attempted, the GraphQL `enqueuePullRequest` mutation receives the verified head as `expectedHeadOid`.
    *Refuted by:* a direct merge, administrative bypass, or mutation with another or missing head is issued.
12. When the mutation rejects a moved head, the command reports `head-moved` and does not retry.
    *Refuted by:* the command retries or fails to identify the changed head.
13. When phase 6 records a verdict, the runner records the commit reviewed in that block.
    *Refuted by:* a newly recorded verdict has no reviewed commit or names a different commit.
14. When admission succeeds, the command exits 0 and reports queued, not merged.
    *Refuted by:* success reports merged or returns a nonzero exit status.
15. When a request is already queued, the command reports that state and exits 0 without another admission.
    *Refuted by:* a retry enqueues again or reports an error.
16. When a prerequisite fails, the command exits 1 and reports each independently determinable failure on stderr using its condition identifier.
    *Refuted by:* a failed condition is omitted, has no identifier, or the command exits 0.
17. When invocation is invalid or admission fails after verification for a reason other than a moved head, the command exits 2.
    *Refuted by:* a usage or admission failure exits 0 or 1.
18. When the checkout's admission script differs from `origin/main`, the script refuses before any admission call.
    *Refuted by:* the unmodified script admits after its own blob differs from `origin/main`.
19. While Claude Code is used, the guarded script is allowed and direct merge commands remain subject to approval, or denial under the existing night policy.
    *Refuted by:* the guarded script is not allowed or a direct merge is allowed without the existing control.
20. When the documented merge procedure admits a request, it names the guarded script as the admission path.
    *Refuted by:* the procedure or decision-PR template directs admission through a direct merge command.

## Non-goals

- Direct merges, administrative bypass, closing beads, changing required checks, or treating queue admission as a completed merge.
- Codex and Antigravity permission enforcement is follow-up work (bead `coding-harness-r7zc`); this change makes no claim that external policies are installed.
- A design or ADR is not due for a bounded change.

## Protected areas

Tracker data and other changes' findings are read-only; their writers retain ownership.

## Definition of Done

- `make verify` green; the criterion ledger demonstrates the criteria.
- The admission command, phase-6 runner, tests, Claude Code permission and merge procedure move together.
- The pull request closes bead `coding-harness-va1l` and its last commit carries `Closes-Bead: coding-harness-va1l`.
- Special runs: none.

## Open decisions

[DETAIL] Match the trailer to exactly one changed folder, read its findings at the head, and take the last phase-6 heading in file order; this makes the reviewed evidence reproducible. Explicit no-findings text must state that the reviewer reported no finding; a bare verdict with no rows is not enough.

[DETAIL] Report all independently determinable failures with stable identifiers (`request-state`, `base`, `draft`, `fork`, `already-queued`, `trailer`, `change`, `phase-6`, `reviewed-commit`, `post-review`, `checks`, `decision`, `evidence`, `script-integrity`, `head-moved`); this makes unattended results actionable. A dependent check whose input is unavailable is not invented.

[DETAIL] The self-check in criterion 18 detects accidental changes only: an edited script can remove its own check, and mutable imports are not protected. It is not a security boundary against a hostile checkout.

[DECISION]

Thema: Einreihen von Entscheidungs-Pull-Requests.
Absicht: Die bestehende Entscheidung zur Zurückweisung und die Entscheidung für einen einzigen Einreihungsweg müssen zusammen ausführbar sein.
Heute: Die Antwort in `decisions.md#Q-5` sagt, dass das Skript Entscheidungs-Pull-Requests zurückweist und die Maintainerin oder der Maintainer sie einreiht. `decisions.md#Q-6` bestimmt das Skript als einzigen Einreihungsweg für alle; der Prüfungsbefund S-10 nennt zusätzlich eine ausdrückliche Option für die Maintainerin oder den Maintainer, die Q-5 nicht ausdrücklich beantwortet.
Repository-Änderung: Der Plan muss festlegen, ob das Skript bei ausdrücklicher menschlicher Aktion eine Ausnahme anbietet oder eine andere Regel gilt.
Architekturänderung: Die Wahl bestimmt, ob eine Ausnahme im einzigen Einreihungsweg existiert; die übrigen Prüfungen bleiben bestehen.

Ziel in einem Satz: Entscheidungs-Pull-Requests sollen auf einem eindeutig festgelegten Weg eingereiht werden.
Option 1 — Ausdrückliche menschliche Ausnahme im Skript: Die Maintainerin oder der Maintainer reiht über das Skript ein; Nachteil: eine zusätzliche Ausnahme muss zuverlässig vor unbeaufsichtigter Nutzung geschützt werden.
Option 2 — Skript weist immer zurück: Die Maintainerin oder der Maintainer nutzt einen anderen freigegebenen Weg; Nachteil: das Einreihen hat mehr als einen Weg.
Empfehlung: Option 1, weil sie den festgelegten einzigen Einreihungsweg erhält.
Wenn du „ok“ sagst: Das Skript bietet eine ausschließlich ausdrücklich menschlich freigegebene Ausnahme für Entscheidungs-Pull-Requests; die übrigen Voraussetzungen gelten weiter.
Was verloren geht: Option 2 würde die Ausnahme im Skript vermeiden.
Akzeptierter Nachteil: Option 1 erfordert eine geschützte Ausnahme; Option 2 erfordert einen weiteren Einreihungsweg.

Welche Option und welchen zugehörigen Nachteil akzeptierst du?
