---
title: "Research — commit-hook-stamp"
status: draft
implementation_status: none
date: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-23", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# commit hook stamp — Research

Stage-2 call, 2026-11-23: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1184 files, 5518 commits, 12 rules.

## Runner exploration — 2026-11-23

Exploration complete. Here is the research, prose ready to append to `plans/changes/commit-hook-stamp/research.md`.

---

## What exists today

**The stamp and the gate behind it.** `scripts/check_frontmatter_current.py` (module docstring) holds every Markdown file whose longest `provenance.yaml` prefix declares `frontmatter: required` to one rule: its `updated:` date is not earlier than the date of the file's last change. The reference date of a clean file is the committer date (in the commit's own offset) of the newest non-merge commit that touched it; an untracked or modified file must reach today; a shallow clone is refused, not guessed at (`preflight`). `--stamp` sets `updated:` to today by editing exactly that one line (`stamped` is the pure writer, `stamp` raises `CannotStamp` for non-UTF-8 input); the stampable findings are `missing`, `unreadable`, `stale` and `future` (`STAMPABLE`), while `no-frontmatter` and `duplicate` are left for a hand edit. The clock reads are `date.today()` (local) and `datetime.now(UTC).date()` in `main`. The held set comes from `provenance.yaml` `paths:` — today that is `docs/journal/handover/`, `docs/journal/planning/`, `docs/lessons/`, `docs/catalog/`, the three governance quality files, `docs/adr/`, `docs/architecture/`, `docs/research/`, `docs/governance/`, `docs/how-to/`, `docs/WORKFLOW.md` and all of `plans/` except `plans/INDEX.md` (`frontmatter: none` there); `excluded: docs/archive/`.

**Where the gate runs.** `decisions/gates.yaml` entry `frontmatter-current` (title "Every held document's updated date is current"): `job: verify`, `enforcement: block`, `placement: both`, `subsets: [docs]`, `needs_history: true`. It is rendered into `.github/workflows/ci.yml` (step `frontmatter-current`, `run: python3 scripts/check_frontmatter_current.py`, no `--stamp`; the verify job checks out with `fetch-depth: 0`, so history is measurable in CI) and is row 64 of `docs/governance/gate-catalog.md`. CI therefore measures currency but never stamps.

**Three stamp writers exist today, none of them a commit hook.**

1. *By hand:* `python3 scripts/check_frontmatter_current.py --stamp`, documented as a duty in `docs/WORKFLOW.md` §4 hand repairs: "After local midnight the stamps follow the local date. `scripts/check_frontmatter_current.py --stamp` runs before a commit after local midnight: the `updated:` field takes the local date, which differs from UTC in the hours after midnight in Europe/Berlin." Night-run handovers repeat it (`docs/journal/handover/2026-10-23-night-run.md`, `2026-10-30-three-lane-night.md`).
2. *The stage-2 runner at write time:* `scripts/stage2.py` imports `check_frontmatter_current`; `stamp_updated` (wrapper around `check_frontmatter_current.stamp` with `clock_now().local_date`) is called after findings writes and evidence inserts (including `insert_before_time`), the atomic research append embeds `stamped()`, and `prepare_derived` stamps every changed held document before verification and then renders the index. The living spec `plans/specs/implementation-verification/spec.md` (bead coding-harness-mfv) fixes this contract: "Modified or new held documents get today's updated stamp" (criterion 2) and "Stamping precedes index rendering, which precedes make verify on every attempt" (criterion 3). `scripts/harness.py`'s time-log `publish` stamps through `check_frontmatter_current.stamped` before an atomic write.
3. *Nobody at commit time.* No hook stamps today; see below.

**What a stamp touches and what it does not.** `plans/INDEX.md` renders `last_reviewed:` into its "last reviewed" column (`scripts/plans_registry.py`, `REQUIRED` tuple and `render_index`), so moving `updated:` cannot invalidate the index. `scripts/check_research_currency.py` measures age from `last_reviewed:` only — its header comment excludes `updated:` from that measure. The runner's work measurement explicitly discounts stamp-only edits (`docs/WORKFLOW.md` §4: "discounting the generated index and stamp-only changes in any document"; "Replacing only an existing `updated:` value does not count as work").

**The runner's own relationship between stamps and commits.** `checkpoint` (`scripts/stage2.py`, def `checkpoint`) classifies changed held files whose diff is stamp-only via `derived_leftover` and restores exactly those paths from the baseline (`git restore --source=<baseline> --staged --worktree`) before `git add -A` and the checkpoint commit — its comment states "A protected document's derived stamp may enter the run, but must not enter its commit." The checkpoint commit disables only signing and identity (`-c commit.gpgsign=false -c user.name=stage2-runner -c user.email=stage2-runner@invalid`); it does not touch `core.hooksPath`, so git hooks would fire on runner checkpoint commits as things stand.

**Existing hooks and who disables them.** The only tracked hooks are the tracker's five shims under `.beads/hooks/` (`pre-commit`, `prepare-commit-msg`, `pre-push`, `post-checkout`, `post-merge`), each a `BEADS INTEGRATION v1.1.2` managed section with a repository preamble that prepends `tools/beads/bin` to PATH so the shimmed `bd` resolves to the pinned wrapper; the preamble comment says it is kept outside the managed section "so `bd hooks install` preserves it". They reach `.git/hooks` through the beads installer — the fresh-clone prerequisite is `tools/beads/install.sh && tools/bd bootstrap --yes` (`AGENTS.md` house rule 2; `docs/adr/0004-tracker-render-is-the-contract.md`, "Decision"). `tools/beads/install.sh` installs only the pinned bd binary, not hooks. No general-purpose hook infrastructure exists: there is no `.githooks/` directory, no tracked `core.hooksPath` configuration, and no pre-commit-framework config — this confirms the earlier finding in `plans/changes/harness-decide-adr/research.md` (addendum item 1): "the only tracked commit hook is the tracker's `.beads/hooks/prepare-commit-msg`." Four script paths deliberately run git with hooks off (`-c core.hooksPath=/dev/null`): `scripts/pr_sync.py` (its merge/ff-only steps), `scripts/research_capture.py` (its git wrapper), `scripts/stage2_research_history.py` (its clone handling) — commits made through those paths bypass any commit-side hook by construction. Claude Code's hook settings (`.claude/settings.json`) carry exactly one hook, SessionStart → `tools/claude-code/hooks/beads-start.sh`; no PostToolUse or other editor-side hook exists. The archived change `plans/changes/archive/2026-09-29-frontmatter-current/research.md` posed the origin question in its open points: "Auto-stamp implementation: Should this be a PostToolUse hook (Claude Code only), a Git pre-commit hook (all editors), or a CI stamp-on-merge step?" — the CI branch is settled in the negative by the gate's placement (measure only), the other two are not.

**Recorded incidents of the manual duty failing** (facts from records, not judgement): `docs/journal/handover/2026-11-11-night-run-twelve-lanes.md` records three runs red only on the stamp gate after local midnight and a hand edit after midnight that did not move the stamp costing a lane; `docs/journal/handover/2026-11-11-day-decisions-six-lanes.md` records a round red only on the stamp gate. The archived change `plans/changes/archive/2026-11-16-midnight-stamp-test/` (bead coding-harness-bxxt.5) fixed the sibling class — tests comparing a captured date against a later runner-written stamp — and its research maps the whole runner stamp path as of 2026-11-10; it explicitly did not touch the manual stamp duty.

**Where the bead sits.** `coding-harness-yv9i.2` is a child of epic `coding-harness-yv9i` "Runner robustness and attempt safety", P1, rank 3 of 15 (`docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md`, priority table and cluster-epic note; `docs/research/2026-11-09-make-verify-long-term.md` also places beads under this epic). The change folder was opened by commit `f1097071` "docs(commit-hook-stamp): open the change for coding-harness-yv9i.2".

## Where it lives

Stamp script `scripts/check_frontmatter_current.py`; gate definition `decisions/gates.yaml` (entry `frontmatter-current`); rendered gate `.github/workflows/ci.yml`; provenance map `provenance.yaml`; runner stamp call sites `scripts/stage2.py` (`stamp_updated`, `prepare_derived`, `checkpoint`, `derived_leftover`); harness stamp `scripts/harness.py` (`publish`); tracker hooks `.beads/hooks/*`; beads install `tools/beads/install.sh` and the `bd bootstrap` prerequisite (`AGENTS.md` house rule 2, `README.md`); Claude Code hooks `.claude/settings.json` and `tools/claude-code/hooks/beads-start.sh`; doctrine `docs/WORKFLOW.md` §4 (hand-repair stamp rule, stamp-only discounts); tests `tests/test_frontmatter_current.py` plus the stamp-path tests in `tests/test_stage2.py` (catalogued in the midnight-stamp-test research); kit carriage `scripts/kit/manifest.yaml` (entry `scripts/check_frontmatter_current.py`, role `mechanismus` — the script travels into kit copies, so its hook dependencies would travel questions with it).

## What is unclear

- The bead's own description and done-condition: `coding-harness-yv9i.2` lives in the Dolt tracker, which this phase cannot read, and no rendered copy is committed (house rule 2). Not read — recorded as an open question for the interview, not a guess.
- The change class: the research skeleton's frontmatter (`plans/changes/commit-hook-stamp/research.md`) declares no `class:` field; per the ADR-0020 routing the runner reads class from `--class` or the `research.md`/`spec.md` headers, and missing or disagreeing declarations refuse before any model call. The archived midnight-stamp-test research header is the tree precedent carrying `class:` and `neighbours:`.
- Whether hooks are actually installed in current checkouts: `.git/hooks` sits in the main checkout's git directory, outside this worktree's read scope. Not read.
- How `bd hooks install` treats an unknown, non-beads hook beside its managed sections: only the managed section's preservation is documented in the shim comments; the installer's behaviour toward foreign hooks is not documented anywhere in the tree (`plans/changes/bd-1-3-4/research.md` records related open questions about managed-section rewrites).
- The timezone of `updated:` has no deciding doctrine text: the gate compares against the committer date in the commit's offset (script docstring), stamps read the local date (`date.today()`; `clock_now().local_date` in the runner), and `docs/WORKFLOW.md` §4 ties the duty to the local date ("Europe/Berlin"). The midnight-stamp-test research flagged the same gap.
- Whether the runner's `checkpoint` carve-out ("a derived stamp must not enter its commit") would interact with a commit-time stamping hook is unstated anywhere — no text in `docs/WORKFLOW.md` or the specs speaks to commit-side stamping.

## Which files a change would have to touch

The hook itself and its installation story (today no repository-owned hook install path exists — the tracked-hook pattern is `.beads/hooks/*` plus `bd hooks install`, and `tools/beads/install.sh` installs only the binary); the stamp implementation it would invoke, `scripts/check_frontmatter_current.py` (`stamped`/`stamp`/`--stamp`); the doctrine that states the duty today, `docs/WORKFLOW.md` §4; `docs/governance/gate-catalog.md` if the gate's story moves; `AGENTS.md` if a new standing rule results; tests beside `tests/test_frontmatter_current.py` and the runner stamp tests in `tests/test_stage2.py`; `scripts/kit/manifest.yaml` if the hook or its installer must travel with the kit. `decisions/gates.yaml` is not touched unless a gate entry changes (it is `human-decided`, `frontmatter: none`).

## Neighbours

- `plans/changes/archive/2026-09-29-frontmatter-current/` (bead coding-harness-qd7) — created the gate, the stamp, and the unanswered auto-stamp hook question.
- `plans/changes/archive/2026-11-16-midnight-stamp-test/` (bead coding-harness-bxxt.5) — the midnight stamp gate behaviour and the full runner stamp-path map.
- `plans/specs/implementation-verification/spec.md` (living spec, bead coding-harness-mfv) — the derived-preparation contract that stamps before verify on every attempt.
- `docs/research/2026-11-09-make-verify-long-term.md` — where the yv9i epic's work sits relative to verify cost.

---

**Fazit in einem Satz:** Es gibt heute drei Schreibstellen für den `updated:`-Stempel (Hand, Runner, Harness) und genau einen dokumentierten Anlass, sie per Commit-Hook zu automatisieren — die offene Detailfrage des archivierten frontmatter-current-Change —, während die Bead-Beschreibung (`coding-harness-yv9i.2`) und die Hook-Installationslage die beiden offenen Punkte für das Interview sind.
