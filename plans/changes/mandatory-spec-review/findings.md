---
title: "Findings — mandatory-spec-review"
category: findings
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-ttic
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — mandatory-spec-review

Stage-2 call, 2026-11-17: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1111 files, 4554 commits, 12 rules.

Stage-2 call, 2026-11-17: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1114 files, 4556 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-17

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | BLOCKER | SPEC | base | `spec.md`, criteria 3 and 5; `docs/WORKFLOW.md` §4 "The draft", steps 3–5 | [AMBIGUITY] Which spec change makes a review stale. In the documented chain, the second `draft` rewrites `spec.md` after the review to work its rows in, and then the plan card follows. Reading A: that redraft is "the spec's last change". The review is then no longer dated after it, so every change whose review had any row is refused at implement until another `spec-review` runs on the revised spec. If that review has rows too, there is another redraft and another review, so only a clean final review admits implement. Steps 4–5 of the chain and `prompts/02-spec.md` "After the spec review" would have to change. Reading B: a redraft that works the 2a rows in does not count. The chain then passes implement on its first review, but the runner needs a rule for telling such a redraft apart from any other edit, and the spec gives none. The two readings produce different runner checks and a different draft chain. | Opus | in spec | — |
| S-2 | MAJOR | SPEC | base | `spec.md`, criterion 3 ("dated after the spec's last change") | [AMBIGUITY] The spec does not say where the spec's change time comes from or how it is compared. The 2a heading carries only a day (`## Phase 2a — Opus 5.5, <date>`, `scripts/stage2.py:3668`). The spec's time could be its `updated:` header (a day, written by the author), the last commit that touches `spec.md` (a timestamp) or the file's mtime. With a strict "after" on days, a review held the same day as the draft is refused although it read the current spec. This change is that case: spec `updated: 2026-11-17`, review 2026-11-17. With "on or after", a redraft later that same day counts as reviewed, but the same redraft one day later does not. With the `updated:` header, an edit that does not bump it leaves a stale review admitted. With commit time, a timestamp is compared with a heading that has no time of day. | Opus | in spec | — |
| S-3 | MAJOR | SPEC | base | `spec.md`, criteria 1, 3 and 4 ("spec-review rows") | [AMBIGUITY] Which records count as a spec review. Findings files hold three forms: runner blocks `## Phase 2a — Opus 5.5, <date>`, Codex blocks `## Phase 2a — Codex, <date>` (`plans/changes/stage2-session/findings.md:24`, still read by `recorded_2a_session`), and hand-written SPEC rows that answer 2a's three questions under another heading after "Phase 2a was skipped" (`plans/changes/harness-decide-adr/findings.md:29`, `plans/changes/research-currency/findings.md:29`). Reading A: any `## Phase 2a` block counts. A Codex 2a then admits implement, although criterion 1 requires an Opus review. Reading B: only `Opus 5.5` blocks count. Every Codex or hand-held review is then refused at implement. Also unsaid: whether a 2a block whose answer was not six-cell rows ("answered in table lines that are not six-cell rows", `scripts/stage2.py:1630`) counts as a review. Any `[AMBIGUITY]` in such a block stands in no row, so criterion 4 cannot see it. | Opus | in spec | — |
| S-4 | MAJOR | SPEC | base | `spec.md`, criterion 4 ("open `[AMBIGUITY]`") | [AMBIGUITY] The spec does not say what makes an ambiguity row open. The runner writes Status `open` on every row (`scripts/stage2.py:1641`). The maintainer's answer goes to `decisions.md` and the spec, and the row may move to `in spec`, `rejected — …`, `resolved <date> by <source>` or `answered`. Reading A: open means the Status begins `open`. An ambiguity that is answered in `decisions.md` but whose row nobody moved still refuses. Reading B: open means no recorded answer, and the Status cell is ignored. Also unsaid: (a) which cell carries the marker. Severity is free text in the 02a prompt, so it may stand in Severity or Finding. A search over the whole row also matches a Finding that only quotes the gate phrase "no open `[AMBIGUITY]`". (b) whether only the latest 2a block is read or every block. Under "every block", an old block's never-moved `[AMBIGUITY]` refuses even after a later clean review. Under "latest", it is forgotten. | Opus | in spec | — |
| S-5 | MAJOR | SPEC | base | `spec.md`, criteria 3–6; `scripts/stage2.py:10043`; `docs/WORKFLOW.md` §4 lines 990–993 | [AMBIGUITY] The spec does not say whether `implement --stage2-off [REASON]` is subject to the new precondition. That route keeps stage 1, `spec-review` has no stage-1 route, and the doctrine says the stage-1 route skips class derivation. Reading A: the precondition applies there too. The runner must then read the class on a route documented as classless, and while stage 2 is off a bounded, feature or architectural change cannot get the runner review it needs, so it cannot implement at all. Reading B: the stage-1 route skips the check. Any such change then reaches Sonnet unreviewed just by adding the flag, which is what criterion 3's refutation describes. | Opus | in spec | — |
| S-6 | MAJOR | SPEC | base | `spec.md`, criteria 3, 6 and 8 | Hole: the spec does not say how `implement` learns the class. Today `implement` reads no class (`scripts/stage2.py:10043`). Only explore runs `declared_class` (`scripts/stage2.py:8743`), which reads `research.md` and `spec.md` and refuses when no class is stated. Whoever builds this must invent four things: which header or headers are read, and what happens when `class:` is missing, invalid, or different in the two files. Failing closed means a classless change can never implement. Failing open means a missing header exempts a change as if it were a spike. Criterion 8 reaches previously implemented changes, which are the most likely to lack a header. This change's own `research.md` states no class while its `spec.md` says `bounded`. | Opus | in spec | — |
| S-7 | MAJOR | SPEC | base | `spec.md`, criterion 7 | [AMBIGUITY] The spec does not fix which changes the handover lists. Reading A: every non-archived folder under `plans/changes/` with no 2a block, spikes included. The maintainer is then asked to decide catch-up for changes the rule exempts. Reading B: only `bounded`, `feature` and `architectural` changes. "Without a spec review" also has two readings: no 2a block at all, or no review that counts as current by criterion 3/4's standard (stale, or with an open `[AMBIGUITY]`). Under "no block at all", a change that implement would refuse for a stale review is not listed, and the maintainer first learns of it from the refusal. Also unsaid: whether changes already implemented but not yet archived count as "open". Q-1 leaves them untouched but makes a later implement call need the review. | Opus | in spec | — |
| S-8 | MAJOR | SPEC | base | `spec.md`, criteria 1 and 2 | Cannot go red as stated. The plan card is shown by the orchestrating session, and no runner verb or check observes a plan card: the only new refusal sits at implement (criterion 3). Input: a bounded change whose plan card reaches the maintainer with no 2a block. No state turns red. A bounded change reviewed after its plan card but before implement passes criterion 3 while breaking criterion 1, and nothing tells the two apart. Without a named observable (a doctrine text or a check), criteria 1 and 2 state intent, and criterion 2's "the new rule requires a spike" is no more checkable. | Opus | in spec | — |
| S-9 | MINOR | SPEC | base | `spec.md`, criterion 7 and Definition of Done | Red only on a live night run. The DoD delivers handover instructions only. The criterion is about the content of a future handover, which a session writes from prose, and no test or check is named. Refuting input: an open bounded change with no 2a block and a handover that omits it. That case exists only when a night run's handover is written after the merge, so the change can be merged without the criterion ever having been able to fail. | Opus | in spec | — |

Stage-2 call, 2026-11-18: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4595 commits, 12 rules.

Stage-2 call, 2026-11-18: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1114 files, 4601 commits, 12 rules.

Stage-2 call, 2026-11-18: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1114 files, 4610 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-18

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-10 | MAJOR | SPEC | base | `spec.md`, Terms "Qualifying review" ("identifiable clean result"); criteria 6 and 8 | [AMBIGUITY] The spec does not say what identifies a clean result. The runner writes `Opus reported no finding.` for every answer that has no table line, then quotes the answer below it (`scripts/stage2.py:1629-1635`). So three different answers get the same line: exactly `No finding.`, a prose refusal ("I cannot read spec.md"), and a prose paragraph that raises an `[AMBIGUITY]` outside a table. The two instructions also conflict. The 02a prompt asks for "one sentence" that names what was checked, while the runner's answer format asks for exactly `No finding.`. Reading A: the runner's no-finding line is the clean result. A refusal or a prose ambiguity then admits implement, and there is no row the refusal could name. Reading B: only an answer of exactly `No finding.` is clean, as phase 6 already rules (`rejected_review_block`, `scripts/stage2.py:3697-3698`). Every other answer without rows is then unreadable and fails closed. That includes a reviewer who followed the 02a one-sentence instruction. Legacy blocks would have to be judged by their quoted answer. | Opus | in spec | — |
| S-11 | MAJOR | SPEC | base | `spec.md`, criterion 10 | [AMBIGUITY] "The spec bytes read by the reviewer" is not something the runner can observe. The reviewer opens `spec.md` from disk with its own tools. `phase_prompt` sends only the prompt and the change name (`scripts/stage2.py:1962-1969`). Reading A: the runner hashes `spec.md` at the start of the call, or at the end. An edit made while the review runs (for example by the orchestrating session while the review runs in the background) then records a fingerprint for bytes the reviewer never read, or misses bytes it did read. Reading B: the runner puts the spec bytes into the prompt and hashes those. That changes the input of the 02a call, and the reviewer can still open the file on disk and see other bytes. Neither reading says whether a start hash that differs from an end hash fails the call. The refuting case "identifies different bytes" cannot be built until one of these is fixed. | Opus | in spec | — |
| S-12 | MAJOR | SPEC | base | `spec.md`, Terms "Qualifying review" ("runner-written"); criteria 6 and 12 | [AMBIGUITY] The spec defines neither "legacy" nor the mark that makes a block runner-written. Anyone can type a heading and its rows by hand. Reading A: legacy means any block that lacks a fingerprint, whatever its date. A hand-typed `## Phase 2a — Opus 5.5, <today>` block with rows then admits implement on the by-day reader, which is exactly what criterion 6's "hand-written" refutation forbids. Reading B: only blocks dated before this change merges are legacy, and a later block without a fingerprint fails closed. Even under B, nothing separates a hand-written block that carries a correct sha256 from a runner block. Refuting input for criterion 6's hand-written clause: a hand-written block under the runner's heading. Without a named mark, no state turns that case red. | Opus | in spec | — |
| S-13 | MAJOR | SPEC | base | `spec.md`, Terms "Qualifying review" ("declared fallback block"); criteria 13 and 15; Open decisions, third [DETAIL] | [AMBIGUITY] "Declared fallback block" reads two ways once the single configured value changes, and Q-6 asks for that switch to be easy. Reading A: a block counts whenever it is marked as fallback, whichever model wrote it. A review by a model later dropped from the declaration (terms lapsed or excluded) keeps admitting implement. Reading B: a block counts only while its model is the one configured now. One switch of the value then disqualifies every existing fallback review: implement refuses those changes, and the inventory moves them from the re-check list to the refused list. The spec also does not say whether the block records which model wrote it, and reading B needs that. | Opus | in spec | — |
| S-14 | MAJOR | SPEC | base | `spec.md`, criterion 13 | [AMBIGUITY] "Opus is unreachable" is not defined, and the runner has no such category today. `run_work_model` treats any non-zero exit or empty answer as one failed call (`scripts/stage2.py:5626-5633`). Reading A: every failed Opus call counts, whether usage limit, auth expiry, timeout, crash or empty answer. Each of these then sends the review to DeepSeek 30 seconds later, including failures that a later Opus attempt would have cleared. Reading B: only connection or availability failures count. The runner then needs a way to classify Claude CLI failures that the spec does not supply, and every other failure ends the verb with no review. The spec is also silent on whether an Opus answer that is unreadable or not clean (S-10) triggers the retry and the fallback. | Opus | in spec | — |
| S-15 | MAJOR | SPEC | base | `spec.md`, criterion 3; Terms "Qualifying review" | [AMBIGUITY] The spec does not say where the draft–review loop ends. Reading A: "clean review" means a review that reported no finding, matching the Terms' "clean result". A re-review whose remaining rows are all rejected with a reason, and which needs no spec edit, is then not clean. The workflow must review the unchanged bytes again, which will likely raise the same rows, so the loop never ends. Meanwhile implement already admits that review, because only an open `[AMBIGUITY]` refuses (criterion 8), so doctrine and runner disagree. Reading B: the loop ends at the first review of the current spec whose rows need no spec edit. The card may then follow a review that still has rows, as long as each one was rejected with a reason. The two readings put different text into `docs/WORKFLOW.md` and `prompts/02-spec.md`, and they decide when the card is shown. | Opus | in spec | — |
| S-16 | MINOR | SPEC | base | `spec.md`, criterion 17 | [AMBIGUITY] The spec does not say when a change leaves the re-check list. Reading A: the change is listed whenever its findings hold any fallback block. An Opus re-check then never removes it. Reading B: the change is listed only while its newest current qualifying block is a fallback block. An Opus review of the same bytes removes it. If the spec changes after the fallback review, that review is stale, the change moves to the refused list, and its "Opus re-check" entry disappears. "By day" also reads two ways: "in daytime", or "grouped by date". | Opus | in spec | — |
| S-17 | MINOR | SPEC | base | `spec.md`, criterion 12; Open decisions, first [DETAIL] | [AMBIGUITY] "Last committed spec-change day" names no git date. The block heading carries the runner's local date (`today()`, `scripts/stage2.py:712-714`). Reading A: the committer date. A rebase or amend moves that date to the rebase day, so every legacy review on a rebased branch turns stale although the spec bytes did not change. Reading B: the author date. A spec commit that is cherry-picked or rebased in after a review keeps its older author day, so the review counts as current over a spec it never read. Neither reading fixes the timezone of the commit day (the commit's own offset or the runner's local zone). Near midnight, the commit then falls on a different day from the heading. | Opus | in spec | — |
| S-18 | MINOR | SPEC | base | `spec.md`, criteria 1–3 | [AMBIGUITY] "The workflow text" does not say which texts it covers. `AGENTS.md` marks 2a `*(optional)*` in its phase table (line 20), and the prompts also describe the draft chain. Reading A: `docs/WORKFLOW.md` alone. A change that leaves `AGENTS.md`'s "(optional)" or the chain wording in `prompts/02-spec.md` untouched then passes criteria 1–3, while those texts still allow a card before the review. Reading B: every doctrine text that describes phase 2a or the draft chain, so any one of them allowing the card refutes the criterion. The choice decides which files a test for criteria 1–3 reads. | Opus | in spec | — |
| S-19 | MINOR | SPEC | base | `spec.md`, criteria 4 and 16 | Hole: criterion 16 lists bounded, feature, architectural and classless changes that fail "the same review check as implement". It says nothing about changes that implement refuses through criterion 4 rather than the review check. (a) A change whose class is invalid, or whose class differs between `research.md` and `spec.md`, belongs to none of the four listed groups. It is either left out or listed under a heading the spec does not give. (b) A classless change with a current clean review passes the review check, so it is not listed, yet implement refuses it for having no class. The maintainer learns of that refusal only at implement, which is what Q-8 set out to avoid. The refutation "a qualifying refused change" does not say whether a class refusal counts as refused. | Opus | in spec | — |

Stage-2 call, 2026-11-18: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4626 commits, 12 rules.

Stage-2 call, 2026-11-18: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1114 files, 4629 commits, 12 rules.

Stage-2 call, 2026-11-18: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1114 files, 4633 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-18

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-20 | MAJOR | SPEC | base | `spec.md`, Terms "Qualifying review" ("readable rows") and "Open ambiguity"; criterion 7; `scripts/stage2.py:1620-1636` | [AMBIGUITY] The spec does not say whether a block is readable when some of its rows parse and some lines do not. The runner keeps the six-cell rows and quotes every other line of the answer below them, including table lines it could not parse (`answer_parts`). Example input: an answer with one valid row and one `[AMBIGUITY]` row that has an unescaped pipe, so that row splits into seven cells. Reading A: the block has readable rows, so it counts as a review. The ambiguity is then in no row. Criterion 7 cannot see it, and implement starts a model. Reading B: one table line that cannot be read makes the whole block unreadable, and it fails closed. A whole review is then lost to one stray pipe. The spec also does not say whether prose next to the rows that raises an `[AMBIGUITY]` counts. The plan's "fail closed on malformed blocks" does not settle which of these "malformed" means. The two readings give different implement results for the same block. | Opus | in spec | — |
| S-21 | MAJOR | SPEC | base | `spec.md`, criteria 10, 11, 16 and 18; `docs/WORKFLOW.md:1828`; `plans/_README.md:49-50`, `:87` | [AMBIGUITY] The spec does not say whether the header fields at the top of `spec.md` (`status`, `implementation_status`, `last_reviewed`) count as "spec bytes". These fields live in `spec.md`, and the orchestrator changes them by hand ("An approval or an implementation transition stays the orchestrator's act"). Six open changes already read `implementation_status: partial`, and `last_reviewed` has to be refreshed as it ages. Reading A: the fingerprint covers the whole file. Moving `implementation_status` after implement, changing `status`, or refreshing `last_reviewed` then makes the review stale even though the spec text did not change. Every change implemented under the new rule then shows up on the morning list as refused for review (criterion 16), and the later implement call of criterion 18 needs a new Opus round. Reading B: the header fields are left out. The runner then needs a rule for which bytes it hashes, and the spec gives none. The fingerprint would also no longer match "the spec bytes included in the review prompt", which criterion 10 names. Q-2 chose "every change" over the option of not counting a redraft that only works the review rows in. Edits that touch only these header fields were not part of that question. | Opus | in spec | — |
| S-22 | MAJOR | SPEC | base | `spec.md`, criteria 3, 6, 7 and 11; Open decisions, fourth [DETAIL] | [AMBIGUITY] The spec does not say what happens after the third round to a row that needs a spec edit and cannot become a plan limit. That is a BLOCKER, or an `[AMBIGUITY]` whose answer changes the spec. The fourth [DETAIL] turns only non-BLOCKER rows into plan limits, and it keeps criterion 7's refusal for an open ambiguity. Any spec edit then makes every review stale (criterion 11), and implement refuses until another review exists (criterion 6). Reading A: after round three the spec is frozen. The BLOCKER or the answer goes into `decisions.md` or a plan limit, and the row's Status moves without a spec edit. Plan and code then follow a spec that does not contain the answer, although `prompts/02-spec.md` makes the revised spec the measure for plan, code and review. Reading B: such a row edits the spec and a fourth review runs. That is the "requires another round after the third" that criterion 3 names as its failure case. The workflow text differs under each reading, and criterion 3 cannot be judged for a BLOCKER found in round three. | Opus | in spec | — |
| S-23 | MAJOR | SPEC | base | `spec.md`, criterion 13; `scripts/stage2.py:3666`, `:5626-5633`, `:10689` | Gap: two of criterion 13's failure kinds are not observable in the runner today. (a) Timeout: the spec-review call runs with no runner timeout (`run_work_model(..., timeout=None)`), so a hung Opus call waits forever. The retry and the fallback then never start, which is the stalled night run that Q-6 set out to prevent. Whoever builds this must invent the limit, and decide whether it belongs in the central configuration next to the pause. (b) Usage limit, authentication and connection failure: `run_work_model` raises the same `CallFailed` for every non-zero exit, and nothing classifies Claude CLI failures. (`rate_limited` only serves the free Pi swarm members.) Whoever builds this must invent the patterns that recognise each kind. The spec also does not say what a non-zero exit that matches none of the five kinds does: retry and fall back, or end the verb with no review. Without a named signal for a connection failure, the test for criterion 13 cannot be built for that kind. | Opus | in spec | — |
| S-24 | MINOR | SPEC | base | `spec.md`, criteria 3 and 17 | [AMBIGUITY] The spec does not say whether the Opus re-check of a fallback review counts as a review round. Reading A: it counts. A fallback review in round three then makes the required re-check a fourth round, which criterion 3 names as its failure case. Reading B: it does not count. The spec then does not say what happens to re-check rows that need a spec edit: either the loop restarts outside the three-round limit, or the rows are dropped. A change the night run has already implemented on a fallback review also has no stated path when the day re-check raises a BLOCKER. The only thing that happens is that criterion 18 refuses its next implement call. | Opus | in spec | — |
| S-25 | MINOR | SPEC | base | `spec.md`, Terms "Qualifying review" ("its matching … audit line"); criterion 6; `scripts/stage2.py:1925-1936`, `:3668` | Gap: "matching" does not say which fields must match. `begin_call` writes the audit line with the date at the start of the call. The block heading takes `today()` after the answer comes back. Reading A: any `spec-review` audit line directly above the block matches. A block marked as fallback under an Opus audit line then counts, and so does an Opus block under a DeepSeek audit line. Reading B: the date and the model or endpoint must agree with the heading. A real call that runs past local midnight then carries a start date one day before its heading, and it fails closed. The test for criterion 6's "unaudited" case depends on which reading is built. | Opus | in spec | — |
| S-26 | MINOR | SPEC | base | `spec.md`, Terms "Legacy block"; criterion 12 | Gap: "dated before this change merges" names a moment the runner cannot know when it is built, and block headings carry only a local day. Whoever builds this must invent the cutoff. One option is a fixed day written into the code at implementation time. Blocks the old runner writes between implementation and merge, or on the merge day itself, then land on either side, depending on the day chosen and on whether "before" is strict. The other option is to look up the commit that brought in the fingerprint writer, and squash or rebase merges move that commit. A cutoff set too late lets a hand-typed block without a fingerprint count by day, which is the case the Terms rule out. A cutoff set too early refuses real reviews written before the merge. Criterion 12's failure case cannot be built until the cutoff is fixed. | Opus | in spec | — |
| S-27 | MINOR | SPEC | base | `spec.md`, criterion 16 | [AMBIGUITY] The spec does not say whether a change folder that has not reached its spec yet counts for the morning list. Three open folders (`ci-bead-summary`, `handover-at-95`, `loop-structure-first`) hold only a `research.md` with no `class:`. This change's own runner-written `research.md` also has none, because explore can take the class from its `--class` argument alone. Reading A: every non-archived folder counts. Each of these folders then shows up every day in the class group, and a folder that has a class but no draft yet shows up as refused for review. The maintainer is then asked to catch up reviews that are not due yet. Reading B: only folders with a `spec.md` (or a `plan.md`) count. The list then needs that rule, and the spec does not give it. The test for criterion 16 needs different fixtures under each reading. | Opus | in spec | — |

Stage-2 call, 2026-11-18: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4641 commits, 12 rules.

Stage-2 call, 2026-11-18: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1114 files, 4645 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/mandatory-spec-review/plan.md` +18 -18
> - `scripts/stage2.py` +506 -12
> - `tests/test_stage2.py` +491 -9
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`, `tests/test_stage2.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> >       seed_spec_review(world, answer="| A1 | [AMBIGUITY] | SPEC | base | spec.md:1 | which bytes make it stale |")
>
> tests/test_stage2.py:28727: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2.py:28581: in seed_spec_review
>     fingerprint = stage2.spec_body_fingerprint(stage2.spec_body_bytes(folder / "spec.md"))
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> spec = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1831/popen-gw5/test_implement_names_open_revi0/repo/plans/changes/demo/spec.md')
>
>     def spec_body_bytes(spec: Path) -> bytes:
>         """The spec's body bytes: everything after the front matter header (criteria 10 and 11).
>     
>         A front-matter-only edit leaves the body untouched, so a review over the
>         body stays current (criterion 11's refuted case).
>         """
>         data = spec.read_bytes()
> >       match = FRONT_MATTER.match(data)
> E       TypeError: cannot use a string pattern on a bytes-like object
>
> scripts/stage2.py:3697: TypeError
> _______________________ test_stage2_off_enforces_review ________________________
> [gw10] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1831/popen-gw.../44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1831/popen-gw10/test_stage2_off_enforces_revie0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x10a6123c0>
>
>     def test_stage2_off_enforces_review(world: World, capsys: pytest.CaptureFixture[str]) -> None:
>         # Criterion 9. Planted fault: the flag bypasses the class or the review precondition.
>         gate_demo(world)
>         successful_implementation(world)
>         assert world.run("implement", "demo", "--stage2-off", "Z.ai outage") == 2
>         assert "has no spec review" in capsys.readouterr().err
>         assert world.calls("claude") == []
> >       seed_spec_review(world)
>
> tests/test_stage2.py:28754: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2.py:28581: in seed_spec_review
>     fingerprint = stage2.spec_body_fingerprint(stage2.spec_body_bytes(folder / "spec.md"))
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> spec = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1831/popen-gw10/test_stage2_off_enforces_revie0/repo/plans/changes/demo/spec.md')
>
>     def spec_body_bytes(spec: Path) -> bytes:
>         """The spec's body bytes: everything after the front matter header (criteria 10 and 11).
>     
>         A front-matter-only edit leaves the body untouched, so a review over the
>         body stays current (criterion 11's refuted case).
>         """
>         data = spec.read_bytes()
> >       match = FRONT_MATTER.match(data)
> E       TypeError: cannot use a string pattern on a bytes-like object
>
> scripts/stage2.py:3697: TypeError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_legacy_review_currency_by_day[on-cutoff-day]
> FAILED tests/test_stage2.py::test_morning_inventory_uses_review_admission - T...
> FAILED tests/test_stage2.py::test_legacy_review_currency_by_day[predates-commit]
> FAILED tests/test_stage2.py::test_implement_refuses_missing_stale_or_unreadable_review[unaudited]
> FAILED tests/test_stage2.py::test_implement_rechecks_previously_implemented_change
> FAILED tests/test_stage2.py::test_implement_refuses_missing_stale_or_unreadable_review[stale]
> FAILED tests/test_stage2.py::test_a_failed_spec_review_call_writes_no_rows[empty-answer]
> FAILED tests/test_stage2.py::test_fallback_review_is_marked - TypeError: cann...
> FAILED tests/test_stage2.py::test_fallback_spec_review_honours_leak_check - T...
> FAILED tests/test_stage2.py::test_a_review_whose_bytes_change_mid_call_writes_no_block
> FAILED tests/test_stage2.py::test_legacy_review_currency_by_day[legacy-current]
> FAILED tests/test_stage2.py::test_spec_review_retries_then_falls_back - TypeE...
> FAILED tests/test_stage2.py::test_implement_refuses_missing_stale_or_unreadable_review[codex]
> FAILED tests/test_stage2.py::test_implement_refuses_missing_stale_or_unreadable_review[unreadable]
> FAILED tests/test_stage2.py::test_morning_inventory_names_fallback_rechecks
> FAILED tests/test_stage2.py::test_legacy_review_currency_by_day[dirty-body]
> FAILED tests/test_stage2.py::test_implement_accepts_current_review - TypeErro...
> FAILED tests/test_stage2.py::test_a_failed_spec_review_call_writes_no_rows[non-zero-exit]
> FAILED tests/test_stage2.py::test_an_answer_that_is_not_rows_is_kept - TypeEr...
> FAILED tests/test_stage2.py::test_review_currency_rejects_changed_bytes - Typ...
> FAILED tests/test_stage2.py::test_spec_review_fingerprints_reviewed_bytes - T...
> FAILED tests/test_stage2.py::test_implement_names_open_review_ambiguity - Typ...
> FAILED tests/test_stage2.py::test_stage2_off_enforces_review - TypeError: can...
> 23 failed, 10 passed in 12.87s
> ```

Stage-2 call, 2026-11-18: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1114 files, 4655 commits, 12 rules.

Stage-2 call, 2026-11-18: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM via Z.ai refused with claude-code:unrecognized_model glm-5.3-flash since about 16:07; the saved Flash tree crashed the runner's own admission, so this attempt starts from the plan · leak check clean over 1114 files, 4667 commits, 12 rules.

Stage-2 call, 2026-11-18: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM via Z.ai refuses glm-5.3-flash (bead coding-harness-b5pu); the previous Sonnet call ended at claude exit 1; starts from the plan · leak check clean over 1114 files, 4679 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/mandatory-spec-review/plan.md` +18 -18
> - `scripts/stage2.py` +441 -9
> - `tests/test_stage2.py` +465 -9
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`, `tests/test_stage2.py`.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 189 lines of this gate left out …]
>                     f"line {call.lineno} handles Git failure with bare exit codes instead of diagnostic patterns"
>                 )
>                 for code, pattern in zip(value.keys, value.values, strict=True):
>                     assert isinstance(code, ast.Constant) and type(code.value) is int and code.value != 0
>                     assert not isinstance(pattern, ast.Constant) or isinstance(pattern.value, str), (
>                         f"line {call.lineno} needs an expected diagnostic pattern for each handled Git failure"
>                     )
>     
>         for function in (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)):
>             if function.name == "run_git":
>                 continue
>             for assignment in (node for node in ast.walk(function) if isinstance(node, ast.Assign)):
>                 call = assignment.value
>                 if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "run_git"):
>                     continue
>                 names = {target.id for target in assignment.targets if isinstance(target, ast.Name)}
>                 reads_status = any(
>                     isinstance(node, ast.Attribute)
>                     and node.attr == "returncode"
>                     and isinstance(node.value, ast.Name)
>                     and node.value.id in names
>                     for node in ast.walk(function)
>                 )
>                 if reads_status:
>                     assert any(keyword.arg == "allow" for keyword in call.keywords), (
>                         f"{function.name}:{call.lineno} handles Git status without explicit allowed exit codes"
>                     )
>                     for raised in (node for node in ast.walk(function) if isinstance(node, ast.Raise) and node.exc):
> >                       assert any(
>                             isinstance(node, ast.Attribute)
>                             and node.attr == "diagnostic"
>                             and isinstance(node.value, ast.Name)
>                             and node.value.id in names
>                             for node in ast.walk(raised.exc)
>                         ), f"{function.name}:{raised.lineno} builds a Git failure without its diagnostic"
> E                       AssertionError: spec_last_commit_day:3830 builds a Git failure without its diagnostic
> E                       assert False
> E                        +  where False = any(<generator object test_every_git_launch_of_the_runner_goes_through_run_git.<locals>.<genexpr> at 0x10b27a500>)
>
> tests/test_stage2.py:25204: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=19916) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/tests/test_stage2.py:23767: DeprecationWarning: This process (pid=19917) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_round_calls_its_rung_from_the_entry - Ass...
> FAILED tests/test_stage2.py::test_every_git_launch_of_the_runner_goes_through_run_git
> 2 failed, 6356 passed, 17 skipped, 5 warnings in 591.81s (0:09:51)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 46999 earlier lines left out …]
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
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-19: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4762 commits, 12 rules.

Stage-2 call, 2026-11-19: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM via Z.ai refuses glm-5.3-flash (bead coding-harness-b5pu) · leak check clean over 1114 files, 4766 commits, 12 rules.

Stage-2 call, 2026-11-19: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1114 files, 4770 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/mandatory-spec-review/plan.md` +1 -1
> - `scripts/stage2.py` +674 -10
> - `tests/test_stage2.py` +675 -33
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>     self.exit(2, _('%(prog)s: error: %(message)s\n') % args)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> self = ArgumentParser(prog='-c', usage=None, description='stage2.py - the one way this repository starts a foreign model.\n\n...2 refused.\n', formatter_class=<class 'argparse.RawDescriptionHelpFormatter'>, conflict_handler='error', add_help=True)
> status = 2
> message = "-c: error: argument verb: invalid choice: 'demo' (choose from draft, explore, implement, prepare-explore, prepare-loop, probe, release-loop, repair, review, review-loop, session, spec-review, triage)\n"
>
>     def exit(self, status=0, message=None):
>         if message:
>             self._print_message(message, _sys.stderr)
> >       _sys.exit(status)
> E       SystemExit: 2
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/argparse.py:2637: SystemExit
> ----------------------------- Captured stderr call -----------------------------
> usage: -c [-h] [--stage2-off [REASON]] [--model MODEL]
>           [--class {spike,bounded,feature,architectural}]
>           [--availability-reported ID] [--seats TRIO=MODELS]
>           [--handover HANDOVER] [--stage-failed MODEL] [--reason TEXT]
>           [--restart] [--spec-review-inventory]
>           [{draft,explore,implement,prepare-explore,prepare-loop,probe,release-loop,repair,review,review-loop,session,spec-review,triage}]
>           [change] [ROW=STATUS] [REASON]
> -c: error: argument verb: invalid choice: 'demo' (choose from draft, explore, implement, prepare-explore, prepare-loop, probe, release-loop, repair, review, review-loop, session, spec-review, triage)
> ____________ test_spec_review_retries_then_falls_back[empty-answer] ____________
> [gw7] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2181/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2181/popen-gw7/test_spec_review_retries_then_0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10835ff80>
> step = {'stdout': ''}
> capsys = <_pytest.capture.CaptureFixture object at 0x108713ef0>
>
>     @pytest.mark.parametrize(
>         "step",
>         [{"exit": 1}, {"stdout": ""}, {"stdout": "A refusal in prose."}],
>         ids=["nonzero-exit", "empty-answer", "unreadable-answer"],
>     )
>     def test_spec_review_retries_then_falls_back(
>         world: World, monkeypatch: pytest.MonkeyPatch, step: dict, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         """Criterion 13 (spec): one retry after the configured pause, then the declared fallback through Pi."""
>         defaults = stage2.spec_review_call_config(world.root)
>         assert defaults["timeout_seconds"] == 30 * 60 and defaults["pause_seconds"] == 30
>         assert defaults["fallback_model"] is None, "no fallback is declared before the configuration names one"
>         pin_spez_review(world)
>         waits: list[int] = []
>         monkeypatch.setattr(stage2, "pause", waits.append)
>         world.script(claude=[step, step], pi=[rows(1)])
> >       assert world.run("spec-review") == 0
> E       AssertionError: assert 2 == 0
> E        +  where 2 = run('spec-review')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2181/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2181/popen-gw7/test_spec_review_retries_then_0/state')).run
>
> tests/test_stage2.py:8260: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 30 files, 3 commits, 1 rules, 1 prompt texts
> spec-review: the Opus call produced no readable review (claude call failed: the answer is empty); one retry follows after 30 seconds.
> INFO  (1):
>   - leak check clean: 30 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2181/popen-gw7/test_spec_review_retries_then_0/bin/pin-pi --version ended 1; it is not the pinned 1.5.0; no call starts:                              ^^^^^^^^^^^^^^^^^^^^
>   File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2181/popen-gw7/test_spec_review_retries_then_0/bin/pin-pi", line 205, in fits
>     return step_.get("model") is None or model_of(a) == step_["model"]
>            ^^^^^^^^^
> AttributeError: 'str' object has no attribute 'get'.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_an_answer_that_is_not_rows_is_kept - Assert...
> FAILED tests/test_stage2.py::test_explore_uses_flash_read_only_and_appends_research
> FAILED tests/test_stage2.py::test_morning_inventory_uses_review_admission - S...
> FAILED tests/test_stage2.py::test_fallback_review_is_marked[same-declaration]
> FAILED tests/test_stage2.py::test_fallback_review_is_marked[changed-declaration]
> FAILED tests/test_stage2.py::test_spec_review_retries_then_falls_back[nonzero-exit]
> FAILED tests/test_stage2.py::test_morning_inventory_names_fallback_rechecks
> FAILED tests/test_stage2.py::test_the_morning_inventory_reports_a_clean_world
> FAILED tests/test_stage2.py::test_spec_review_retries_then_falls_back[unreadable-answer]
> FAILED tests/test_stage2.py::test_the_morning_inventory_takes_no_verb - Syste...
> FAILED tests/test_stage2.py::test_spec_review_retries_then_falls_back[empty-answer]
> 11 failed, 117 passed in 13.24s
> ```

Stage-2 call, 2026-11-19: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1114 files, 4796 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/mandatory-spec-review/plan.md` +1 -1
> - `scripts/stage2.py` +28 -17
> - `tests/test_stage2.py` +17 -14
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 935 lines of this gate left out …]
>         world.findings.write_text(before, encoding="utf-8")
>         world.script(
>             claude=[
>                 {
>                     "stdout": "implemented",
>                     "plant": {
>                         "src/app.py": "value = 2\n",
>                         "plans/changes/demo/findings.md": before.replace(
>                             "title: Findings\n", "title: Findings\n" + injected
>                         ),
>                     },
>                 }
>             ],
>             make=[{"stdout": "green\n"}],
>         )
> >       assert world.run("implement") == 0
> E       AssertionError: assert 2 == 0
> E        +  where 2 = run('implement')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/verify-runs-501/32652/pytest-of-mikypik...zwyfjptgm40000gn/T/verify-runs-501/32652/pytest-of-mikypiky/pytest-1/popen-gw1/test_implement_cannot_forge_lo2/state')).run
>
> tests/test_stage2.py:24167: AssertionError
> ----------------------------- Captured stderr call -----------------------------
> refused: no qualifying spec review exists for demo: run `python3 scripts/stage2.py spec-review demo` first - a review qualifies as an Opus 5.5 or declared-fallback block with readable rows or the exact `No finding.` answer and its matching runner call line directly above it.
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=34444) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/tests/test_stage2.py:24405: DeprecationWarning: This process (pid=34439) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_fixture_secret_in_a_failed_draft_check_allows_a_clean_retry
> FAILED tests/test_stage2.py::test_a_refused_attempt_keeps_the_findings_a_human_touched
> FAILED tests/test_stage2.py::test_each_repair_attempt_leaves_an_audit_line_the_count_reads
> FAILED tests/test_stage2.py::test_quoted_reader_lines_count_for_no_reader - A...
> FAILED tests/test_stage2.py::test_repair_starts_no_review_call - AssertionErr...
> FAILED tests/test_stage2.py::test_baseline_cleanup_refuses_reinstated_external_parent[direct-run]
> FAILED tests/test_stage2.py::test_baseline_cleanup_refuses_reinstated_external_parent[baseline-chain-run]
> FAILED tests/test_stage2.py::test_the_probe_checks_discovered_and_paid_models_once
> FAILED tests/test_stage2.py::test_the_probe_continues_after_member_failures[unavailable-first-free]
> FAILED tests/test_stage2.py::test_the_probe_continues_after_member_failures[unavailable-first-paid]
> FAILED tests/test_stage2.py::test_the_probe_continues_after_member_failures[unavailable-last-paid]
> FAILED tests/test_stage2.py::test_the_probe_continues_after_member_failures[empty-answer-first-free]
> FAILED tests/test_stage2.py::test_the_probe_continues_after_member_failures[empty-answer-first-paid]
> FAILED tests/test_stage2.py::test_the_probe_continues_after_member_failures[empty-answer-last-paid]
> FAILED tests/test_stage2.py::test_passing_full_fallback_repair_keeps_scope_only_in_plan
> FAILED tests/test_stage2_fail_fast.py::test_findings_restore_notice_matches_the_verdict
> FAILED tests/test_stage2.py::test_implement_cannot_forge_loop_lines_in_the_frontmatter[release]
> FAILED tests/test_stage2.py::test_implement_cannot_forge_loop_lines_in_the_frontmatter[round]
> FAILED tests/test_stage2.py::test_implement_cannot_forge_loop_lines_in_the_frontmatter[metadata]
> 19 failed, 6339 passed, 17 skipped, 5 warnings in 633.07s (0:10:33)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 47090 earlier lines left out …]
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
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-19: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1114 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1114 files, 4816 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1114 files, 4818 commits, 12 rules.

Stage-2 call, 2026-11-19: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4818 commits, 12 rules.

Runner restoration, 2026-11-20: repair · attempt 1 · route codex — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1114 files, 4834 commits, 12 rules.

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1114 files, 4834 commits, 12 rules.

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1114 files, 4834 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4839 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files none; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/mandatory-spec-review/stage2/attempts/mandatory-spec-review/attempt-1-20261120T062051723502Z-5c0cb71e.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1114 files, 4839 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +11 -9
> - `tests/test_stage2.py` +33 -0
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - L2-1: no fixed line
> - L2-2: no fixed line
> - L2-3: no fixed line
> - L2-4: no fixed line
> - L2-6: no fixed line
> - L2-7: no fixed line
> - L2-9: no fixed line
> - L2-13: no fixed line
> - L2-14: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/mandatory-spec-review/stage2/attempts/mandatory-spec-review/attempt-2-20261120T062051723502Z-5c0cb71e.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1114 files, 4847 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/check_interview_minimums.py` +31 -0
> - `scripts/stage2.py` +94 -33
> - `tests/test_stage2.py` +119 -2
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/stage2.py:3964:24: ARG001 Unused function argument: `root`
>      |
> 3964 | def qualifying_reviews(root: Path, change: str, text: str) -> tuple[list[SpecReviewBlock], str]:
>      |                        ^^^^ ARG001
> 3965 |     """The change's qualifying spec-review blocks, in findings order, and the blocks left out.
>      |
>
> scripts/stage2.py:3964:36: ARG001 Unused function argument: `change`
>      |
> 3964 | def qualifying_reviews(root: Path, change: str, text: str) -> tuple[list[SpecReviewBlock], str]:
>      |                                    ^^^^^^ ARG001
> 3965 |     """The change's qualifying spec-review blocks, in findings order, and the blocks left out.
>      |
>
> Found 2 errors.
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/mandatory-spec-review/stage2/attempts/mandatory-spec-review/attempt-3-20261120T062051723502Z-5c0cb71e.md
> ```

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1114 files, 4854 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4857 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files none; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/mandatory-spec-review/stage2/attempts/mandatory-spec-review/attempt-1-20261120T081453994758Z-ad24d19a.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1114 files, 4858 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files none; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/mandatory-spec-review/stage2/attempts/mandatory-spec-review/attempt-2-20261120T081453994758Z-ad24d19a.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1114 files, 4858 commits, 12 rules.

Runner restoration, 2026-11-20: repair · attempt 3 · route stage-1 — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model hy3 · leak check clean over 1114 files, 4888 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4893 commits, 12 rules.

Runner restoration, 2026-11-20: repair · attempt 1 · route codex — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged; plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1114 files, 4917 commits, 12 rules.

Loop attempt: 2026-11-20 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1114 files, 4924 commits, 12 rules.

Loop attempt: 2026-11-20 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1114 files, 4969 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 4974 commits, 12 rules.

Runner restoration, 2026-11-21: repair · attempt 1 · route codex — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged; plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged

Stage-2 call, 2026-11-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 5002 commits, 12 rules.

Runner restoration, 2026-11-21: repair · attempt 1 · route codex — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1114 files, 5018 commits, 12 rules.

Stage-2 call, 2026-11-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 5020 commits, 12 rules.

Runner restoration, 2026-11-21: repair · attempt 1 · route codex — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1114 files, 5021 commits, 12 rules.

Stage-2 call, 2026-11-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 5023 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +17 -7
> - `tests/test_stage2.py` +52 -0
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 82 lines of this gate left out …]
> ........................................................................ [ 89%]
> ........................................................................ [ 90%]
> ........................................................................ [ 91%]
> ........................................................................ [ 93%]
> ........................................................................ [ 94%]
> ........................................................................ [ 95%]
> ........................................................................ [ 96%]
> ........................................................................ [ 97%]
> ........................................................................ [ 98%]
> ........................................................................ [ 99%]
> .............                                                            [100%]
> =================================== FAILURES ===================================
> _ test_stale_legacy_blocks_still_count_as_rounds[three-rounds-one-final-draft] _
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/verify-runs-501/6071/pytest-of-mikypiky...---|---|---|---|---|---|---|\n| R1 | MAJOR | SPEC | criterion 1 | spec.md:1 | FB1 unique body | Opus 5.5 | open | — |')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10950a120>
> rounds = 3, edits = 1, admitted = True
>
>     @pytest.mark.parametrize(
>         ("rounds", "edits", "admitted"),
>         [(3, 1, True), (3, 2, False), (2, 1, False)],
>         ids=["three-rounds-one-final-draft", "three-rounds-later-edit", "two-rounds"],
>     )
>     def test_stale_legacy_blocks_still_count_as_rounds(
>         world: World, monkeypatch: pytest.MonkeyPatch, rounds: int, edits: int, admitted: bool
>     ) -> None:
>         """L2-2, L3-1: legacy blocks still count; three admit one final draft, a later edit needs a review again."""
>         cutoff = stage2.LEGACY_SPEC_REVIEW_DAY
>         day = (cutoff - dt.timedelta(days=10)).isoformat()
>         world.write_findings(*[opus_review_block(world, day=day, fingerprint=None) for _ in range(rounds)])
>         for step in range(edits):
>             commit_at(world, monkeypatch, cutoff - dt.timedelta(days=4 - step))
>         admission = stage2.review_admission(world.root, "demo")
>         assert admission.rounds == rounds
>         if admitted:
> >           assert admission.review_problem is None
> E           assert "the newest qualifying spec review of demo is stale: it predates the spec's last committed change of 2026-11-15. 3 spe...d admits one spec body edit only; the maintainer authorizes a fourth round in decisions.md or the change is re-sliced." is None
> E            +  where "the newest qualifying spec review of demo is stale: it predates the spec's last committed change of 2026-11-15. 3 spe...d admits one spec body edit only; the maintainer authorizes a fourth round in decisions.md or the change is re-sliced." = ReviewAdmission(klass='bounded', class_problem=None, review_problem="the newest qualifying spec review of demo is stal...aintainer authorizes a fourth round in decisions.md or the change is re-sliced.", left_out='', rounds=3, recheck=F [… 20 characters left out …]
>
> tests/test_stage2.py:8571: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=7561) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/tests/test_stage2.py:24869: DeprecationWarning: This process (pid=7557) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_stale_legacy_blocks_still_count_as_rounds[three-rounds-one-final-draft]
> 1 failed, 6403 passed, 17 skipped, 5 warnings in 544.86s (0:09:04)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 47236 earlier lines left out …]
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
> make: *** [verify] Error 1
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/mandatory-spec-review/stage2/attempts/mandatory-spec-review/attempt-1-20261121T041812401261Z-dd2de221.md
> ````

Stage-2 call, 2026-11-21: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1114 files, 5023 commits, 12 rules.

Runner restoration, 2026-11-21: repair · attempt 2 · route codex-repair — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
