---
title: "Research — definitive-refusal"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-2ym2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# definitive refusal — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3377 commits, 12 rules.

## Runner exploration — 2026-11-06

Die Exploration ist fertig. Der Tracker (Bead-Beschreibung) ist aus dieser Lese-Sitzung nicht lesbar — das ist als offene Frage vermerkt. Hier ist die Research-Fassung, bereit zum Anhang an `plans/changes/definitive-refusal/research.md`:

---

## definitive refusal — phase-1 findings (explorer, 2026-11-06)

**Proposed header addition:** `neighbours: [plans/specs/implementation-verification/spec.md, plans/changes/loop-until-clean/spec.md, plans/changes/review-verdict-validated/spec.md, plans/changes/restore-symlink-parent/spec.md, plans/changes/ledger-marker/spec.md]`

### Scope note — the change's own first open question

- The change folder was opened 2026-11-06 (commit `0c3a5f5a`, "chore(definitive-refusal): open the change folder", bead `coding-harness-2ym2`); `plans/changes/definitive-refusal/research.md` held only the skeleton and the stage-2 route line before this run. The bead's description is **not read**: the tracker lives in the Dolt database (`.beads/metadata.json` names backend `dolt`, database `coding_harness`); no rendered copy is committed (ADR 0004), `.beads/interactions.jsonl` does not name the bead (grep, no match), and this explorer has read-only tools and runs no command, so `tools/bd show` was not run. Grep for `2ym2` over the tree finds exactly two hits, both this change's own files (`plans/INDEX.md`, the research header). Everything below researches the name "definitive refusal" against the tree; the bead's exact wording decides the scope and is the first interview question.

### What exists today

**1. The runner's refusal machinery is uniform and terminal.**
- `scripts/stage2.py` defines `class Refused` ("The runner refuses before any call: exit 2"), `class CallFailed` (exit 1) and `class CleanStop` — a finished loop is told apart from a refusal by exit code 3 (`CLEAN_CODE`; the comment cites R-11 of the review-swarm review, where both used to be 2). Function `main` prints `refused: <reason>` on stderr and returns 2; `RestorationRefused` carries its own exit code.
- About 90 `raise Refused(...)` sites cover the leak check ("the leak check is not clean; the call does not start."), class declarations ("the stated classes disagree", "--class … is none of …", flag exclusivity such as "--stage2-off applies only to …"), endpoint and model admission ("model-endpoints.yaml declares no endpoint …", "pi … is not the pinned …; no call starts", "the launch of … carries no checked destination; no model request starts."), loop records (lost record, overlapping release, repair brake), credential scrubbing and the git helpers.
- Doctrine matches the code: "a leak-check BLOCK stops without a fallback" (`docs/WORKFLOW.md` stage-2 section; ADR 0015 and ADR 0017 each state it in their decisions), and "missing, invalid or disagreeing declarations refuse before any model call" (`docs/WORKFLOW.md` model-routing section; AGENTS.md stage-2 section).
- Writes after a refusal are forbidden by runner review R-4, with one dated, documented exception — the no-round bookkeeping line (`docs/WORKFLOW.md`, lost-record section; the checkpoint comment in `scripts/stage2.py` reads "A `Refused` stop … is never followed by a write (runner review R-4)").

**2. The one refusal the repository itself documents as NOT definitive: the permission brake.**
- `.claude/settings.json` (read in full) `permissions.ask` holds ten rules: `Bash(gh pr merge *)`, `Bash(gh -* pr merge*)`, `Bash(gh pr -* merge *)`, `Bash(gh api *merge*)`, `Bash(gh api *Merge*)`, `Bash(gh alias set *)`, `Bash(git push *main*)`, `mcp__*__merge_pull_request`, `Bash(codex *)`, `mcp__omnigent__sys_advise_models`. `permissions.deny` holds 27 Omnigent tools by name plus `Edit(//**/.omnigent/config.yaml)`. The only configured hook is `SessionStart` → `tools/claude-code/hooks/beads-start.sh`.
- Four places state the gap in so many words:
  - AGENTS.md house rule 8: "asks before every merge command it recognises — a brake, not a lock: another spelling passes."
  - `docs/WORKFLOW.md` §2 "What this does not do": the ask rules match a command's text and another spelling passes them, enumerating curl against the API, the web page, `gh` through `sh -c '…'`, an absolute path, a script file, a flag moved before `merge`, a GraphQL merge mutation read from a file, and `gh alias import`.
  - `docs/WORKFLOW.md` stage-2 section: `Bash(codex *)` is "a brake, not a lock: `sh -c`, an absolute path or a script file passes it, as it does for the merge rules in §2". The runner records the same rule as constant `CODEX_ASK_RULE` with its reason ("codex typed directly skips the leak check and the declaration; the runner is the way in").
  - `docs/research/2026-10-31-architecture-reconciliation.md` row T38 ("bypass must be seen to fail"), disposition Partial: "The harmless-probe experiment was never run; no bypass-failure evidence exists." Row T27 records that the injected-instruction fixture "is not found in tree".
- A second enforcement layer is **proposed but not built**: `docs/research/2026-09-30-decision-pull-requests.md` section (f) "Optional second layer (proposed)" describes a PreToolUse hook under `.claude/hooks/pre-tool-use/` (Python, `shlex` parsing, per rule RB-H3) that recognises every spelling, refuses an unbound merge (a merge command without `--match-head-commit` is denied with a reason), fails closed — and notes it stays "still a brake" against a script written to a file and run later.
- Presence checks, kept apart: `.claude/hooks/` is **not there** (glob over `.claude/**` returns only `agents/`, `commands/workflow-start.md`, `settings.json`). `tools/claude-code/hooks/` holds five informational hooks (beads-start.sh, handover.sh, parallel-sessions.sh, recap.sh, session-scan.sh), and `parallel-sessions.sh` deliberately warns rather than refuses (header comment: "the model is asked to warn the person before changing files, not to refuse"). The session-stop refusal is promised and absent, pinned absent: `tests/test_workflow_entry.py` asserts `.claude/hooks/session-stop/check-tests-green.sh` sits on the absent list; its explore (bead coding-harness-788, `feat/stop-hook`) stands before its interview per the 2026-11-03 handover. `provenance.yaml` reserves `.claude/rules/` as `human-decided` — the directory is **not there**; `.claude/settings.json` carries **no** reservation in `provenance.yaml` (not found in the reservations read).

**3. Delivered refusal precedents a change could pattern-match (each with its test).**
- Restore refusal: a restore path resolving outside the worktree must be refused — "nothing written, path named, run ends without fallback" (night plan 2026-10-22 item 6, bead coding-harness-10w; the parked-PR note on #228 in `docs/research/2026-10-27-parked-runner-prs.md` records the pre-fix behavior that unlinked a symlinked parent and went on). Change folder: `plans/changes/restore-symlink-parent/`.
- Alias refusal: the ledger clearing refuses a symlinked, alias-resolving or hard-linked plan before any write (`plans/changes/ledger-marker/spec.md` criterion 4; `tests/test_stage2.py::test_clearing_the_ledger_refuses_an_aliased_parent_or_a_hard_link`).
- Storage refusals, the newest change: `scripts/verify_duration.py` defines refusal as "diagnostic on stderr, exit code 2" (module docstring), with delivered tests for substituted history, unsupported event version, hard-linked history and append I/O failure (loop rows L1-2, L1-3, L1-8, L1-12 in `plans/changes/verify-duration/findings.md`, fixed 2026-11-05).
- Verify-lock admission: readings below the memory floor for 60 minutes refuse the entry, naming floor and last reading; unusable lock state "refuses the entry before any protected work instead of running unlocked" (`docs/WORKFLOW.md` verify-lock section; the behavior description is from WORKFLOW — `scripts/verify_lock.py` itself **not read** here, its existence named by the reconciliation report T22 and `tests/test_verify_lock.py`).
- Answer refusal: "an empty, refused or malformed phase-6 answer is not a finished review" was delivered as `plans/changes/review-verdict-validated/` (its spec lists empty output, refusal prose, header-only tables; release refuses without a genuine verdict).
- Row-id refusal: "Row ids that are not L<n>-<m> are refused, not reported clean" (weekend plan 2026-10-24 item B0; delivered on `fix/review-loop-row-ids` per that plan).
- Tracker wrapper: `tools/bd` refuses `init`, `migrate`, `upgrade` (AGENTS.md house rule 3; the wrapper's text **not read** here).

### Where it lives

- Enforcement in the tree today: `.claude/settings.json` (`permissions.ask`, `permissions.deny`, `hooks.SessionStart`) — the only layer; nothing else inspects commands.
- The refusal engine: `scripts/stage2.py` (`Refused`, `CleanStop`, `CallFailed`, `RestorationRefused`, `main`, `CODEX_ASK_RULE`).
- The brake documentation: AGENTS.md house rule 8; `docs/WORKFLOW.md` §2 and the stage-2 permission section; `docs/research/2026-09-30-decision-pull-requests.md` (f); `docs/research/2026-10-31-architecture-reconciliation.md` T27/T38.
- Hook homes: `tools/claude-code/hooks/` (five display hooks, installed by `tools/claude-code/install.sh`), `.claude/hooks/` (absent), `.claude/rules/` (reserved in `provenance.yaml`, absent in the tree).

### What is unclear (interview questions)

1. **The bead's intent** — the description was not readable in this phase; it decides which refusal "definitive" names.
2. **Which refusal is the target**: the merge/codex ask-brake (the only refusal documented as passable by another spelling), the absent session-stop refusal, a runner stop with a residual fallback, or something outside these candidates.
3. **What "definitive" means operationally**: a deny where an ask stands; spelling-complete recognition (a shlex-parsed hook) instead of text patterns; refusing unbound merges (no `--match-head-commit`); or fail-closed on unreadable state. The research note itself names the residual limit (a script file run later stays unseen) — where the maintainer's tolerance lies is a human question.
4. **The enforcement layer**: a Claude Code PreToolUse hook, the reserved-but-absent `.claude/rules/`, a gate in `decisions/gates.yaml` (that file is `human-decided`; a new gate id is a decision PR), or branch protection outside the tree. Not decidable from the tree.
5. **Whether bypass-failure evidence is in scope** (T38's never-run harmless-probe experiment) or the change is code-only.

### Which files a change would have to touch

- `.claude/settings.json` — the ask/deny rules; any re-spelling of the brake.
- A new hook file and its install path — `.claude/hooks/pre-tool-use/…` per the proposed layer, or `tools/claude-code/hooks/…` with `tools/claude-code/install.sh`.
- `tests/` — the entry test pins supplied and absent pieces (`tests/test_workflow_entry.py`); a gate joining needs its known-bad/mutation case (rule RB-G4, `scripts/mutation_evidence.py` exists).
- `docs/WORKFLOW.md` §2 and the stage-2 permission section, AGENTS.md house rule 8 — if the brake/lock wording changes, both describe today's gap and a lock would make them false.
- Possibly `decisions/gates.yaml` and `docs/governance/gate-catalog.md` (both `human-decided` — decision PR), and `provenance.yaml` if a new path reservation is wanted (decision PR per house rule 8).

---

Kurzum für dich: Der Explorer-Lauf hat die komplette Refusal-Landschaft kartiert. Die stärkste dokumentierte Lücke zum Namen „definitive refusal" ist der Merge-/Codex-Brems块 in `.claude/settings.json` („a brake, not a lock: another spelling passes" — vier Belege inkl. ungebautem Hook-Vorschlag). **Nächster Schritt:** Interview-Frage 1 an dich — die exakte Bead-Beschreibung (`tools/bd show coding-harness-2ym2`) entscheidet, welcher Refusal gemeint ist; ich konnte sie aus dieser Phase nicht lesen.

## Scope correction and repository gap check — 2026-11-06

The answered interview record settles the earlier scope questions: this is a
bounded change to paid review-loop rungs, not to permission hooks
(`decisions.md#Q-1`). The tracker description remains not read in this draft.
The following observations were read at commit `4a80673c` on 2026-11-06:

- `scripts/stage2.py::run_reviewer` turns a nonzero Pi exit into `CallFailed`
  through `fail`; the message keeps only the last nonempty stderr line,
  scrubbed and cut to 200 characters. It does not distinguish HTTP 403/410.
- `run_swarm` preserves each member's exception; `Refused` from admission
  propagates rather than becoming a replaceable provider failure.
- `_review_round` replaces failed Flash members down the pinned paid ladder,
  but a failed single rung reaches the all-failed `CallFailed` branch. No
  round or stage consumption is written. `review_loop` only continues within
  the same invocation for `FreeStageUnavailable`, not a failed paid rung.
- `retire_stage`, used by `release-loop --stage-failed`, already persists a
  quoted `Stage failed` block and consumption together through `write_round`
  and atomic `replace_record`. This does not invent a completed round.
- Existing offline fixtures and tests in `tests/test_stage2.py` cover manual
  retirement after release, quoted failure text, failed Flash replacement,
  and an all-failed attempt leaving the stage unconsumed. These are the
  regression boundary for automatic retirement of definitive paid-rung errors.
- `docs/WORKFLOW.md` describes manual retirement and says an all-failed
  attempt consumes no stage. It needs the interview's narrow automatic
  retirement exception; the no-round bookkeeping must remain truthful.

No live provider call or captured 403/410 response was read. Detection must
therefore use explicit HTTP failure evidence from a failed Pi call, with
offline fixtures for accepted forms and false positives; successful reviewer
prose and a bare model number are not evidence of an HTTP refusal.

The worktree has `templates/spec.md` and `templates/design.md`, but no
`templates/plan.md`; existing change plans and `prompts/03-plan.md` supply the
plan form. `scripts/validate_change_artefacts.py` is absent at this commit;
the available interview and criterion-ledger checks can be run separately.
