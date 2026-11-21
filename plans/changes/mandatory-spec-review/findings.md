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

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1114 files, 5024 commits, 12 rules.

Stage-2 call, 2026-11-21: review-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1114 files, 5025 commits, 12 rules.

Loop attempt: 2026-11-21 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base

Stage-2 call, 2026-11-21: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 5030 commits, 12 rules.

## Phase 6 — Codex, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `scripts/stage2.py:4200` | Wenn das neueste Review zwei offene `[AMBIGUITY]`-Zeilen enthält und nach der dritten Runde nur die erste durch eine Antwort der Person geklärt ist, lässt die Zulassung die Implementierung starten: Sie prüft nur die erste Zeile und übersieht die zweite offene Mehrdeutigkeit. Jede offene Mehrdeutigkeit muss die Implementierung zurückhalten. [Kriterium 7] | Codex | fixed — tests/test_stage2.py::test_each_open_ambiguity_needs_its_own_settlement | — |
| F-2 | MAJOR | SPEC | base | `scripts/stage2.py:4220`, `scripts/stage2.py:4508` | Ein aktuelles Fallback-Review mit offener Mehrdeutigkeit oder offenem BLOCKER wird in der Morgeninventur als abgelehnt aufgeführt, aber nicht für die Opus-Nachprüfung genannt. Die Inventur muss auch dieses aktuelle Fallback-Review für die Nachprüfung ausweisen. [Kriterium 17] | Codex | fixed — tests/test_stage2.py::test_inventory_lists_refused_current_fallback_for_recheck | — |
| F-3 | MAJOR | SPEC | base | `scripts/stage2.py:4448` | Wenn nach einem Fallback in Runde drei auch die Opus-Nachprüfung zweimal fehlschlägt und erneut der Fallback antwortet, markiert der Runner das neue Fallback als Nachprüfung. Beim nächsten Aufruf verweigert er wegen des Rundenlimits eine weitere Opus-Nachprüfung, obwohl weiterhin ein aktuelles Fallback-Review vorliegt. Die Opus-Nachprüfung muss in derselben Runde möglich bleiben. [Kriterium 17] | Codex | fixed — tests/test_stage2.py::test_fallback_replacing_recheck_respects_round_cap | — |

Phase 6 verdict: codex 01a1fcb2-8670-78b2-a4bf-15ec1739ab9b, 2026-11-21
Reviewer session: codex 01a1fcb2-8670-78b2-a4bf-15ec1739ab9b — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | correctness | base | `scripts/stage2.py:legacy_currency_problem` | `spec_last_commit_day` asks git for the last commit touching `spec.md`, so a committed front-matter-only edit makes a legacy block fail `written < committed`. That contradicts the added comment that front matter edits never invalidate a review; currency should measure the last committed body change. | hy4-flash-free | fixed — tests/test_stage2.py::test_legacy_currency_ignores_committed_header_edit | yes — tests/test_stage2.py::test_legacy_currency_ignores_committed_header_edit | agree |
| L1-2 | MAJOR | correctness | base | `scripts/stage2.py:spec_last_commit_day` | `git log --format=%cI` returns the committer date with its timezone offset; slicing `line[:10]` gives the committer's local calendar day, not the UTC day required by the docstring and criterion. Reviews or commits near midnight in a non UTC timezone are compared against the wrong date. | hy4-flash-free | fixed — tests/test_stage2.py::test_spec_commit_day_uses_utc | yes — tests/test_stage2.py::test_spec_commit_day_uses_utc | agree |
| L1-3 | MINOR | robustness | base | `scripts/stage2.py:spec_review_call_config` | `yaml.safe_load` can return a non mapping, but the code only validates the `spec_review` value after calling `data.get`. A top level list or scalar in `model-endpoints.yaml` raises `AttributeError` instead of the intended `Refused` diagnostic. | hy4-flash-free | fixed — tests/test_stage2.py::test_spec_review_config_refuses_non_mapping | yes — tests/test_stage2.py::test_spec_review_config_refuses_non_mapping | agree |
| L1-4 | MAJOR | test | base | `tests/test_stage2.py:minus_seeded_review` | The helper rebuilds the seeded block with `opus_review_block(world)`, whose default fingerprint is the current spec body. In the fixture secret draft test, the draft run has just changed the spec body, so the generated string no longer matches the seeded block and is not removed; the assertion then counts the seed's own `leak check clean` line. | hy4-flash-free | fixed — not a test — the helper removes the originally recorded seeded block | no — not a test | agree |
| L2-1 | MAJOR | MAINT | base | `scripts/stage2.py:3822` against `scripts/stage2.py:4072` | The runner accepts a review row whose Severity is any word — its own answer instruction says the severity cell is free text — renders it into the block, and the stored-block reader then requires BLOCKER, MAJOR, MINOR or an `[AMBIGUITY]` prefix and declares the whole table unreadable. So `spec-review` writes the block, prints "1 rows appended" and exits 0, while `implement` refuses that same block as "no readable review"; re-running the review appends another block that is unreadable in the same way, so the change is stuck with no diagnosis pointing at the severity word. Either reader must treat any six-cell row as a row, or the verb must refuse the non-conventional severity before writing. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_spec_review_answer_the_stored_reader_rejects_fails_the_call | no | agree |
| L2-2 | MAJOR | SPEC | base | `scripts/stage2.py:3948` and `scripts/stage2.py:4033` | `qualifying_reviews` discards every legacy block that fails the by-day currency test and `review_admission` counts rounds from the survivors, so a change whose three review rounds were written before the fingerprint rule and whose spec body was then edited counts zero rounds: the three-round exception never fires and `implement` refuses it as unreviewed. This change is that case — its three blocks are dated 2026-11-17 and 2026-11-18, its spec body's last committed change is 2026-11-19, so its next `implement` call is refused with "no qualifying spec review exists" although three rounds ran, which is exactly what the round-three exception was decided to allow. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_stale_legacy_blocks_still_count_as_rounds | no | agree |
| L2-3 | MAJOR | SPEC | base | `scripts/stage2.py:4072` with `scripts/stage2.py:1179` | An answer carrying one readable row plus an `[AMBIGUITY]` row of more than six cells (a stray unescaped `\|`) is accepted as a review: `parse_rows` widens only rows whose severity is BLOCKER, MAJOR or MINOR, so the ambiguity line lands in the "not a row" text, `readable_review` returns the remaining row, and the block is written with the ambiguity as quoted prose. `open_ambiguity_row` reads rows only, so `implement` starts a model instead of refusing and naming the row, and the plan's "fail closed if any table line is malformed" holds only on the stored side. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_an_overwide_ambiguity_row_reads_and_reads_back_open | no | agree |
| L2-4 | MINOR | SPEC | base | `scripts/stage2.py:4096` | `fourth_round_authorized` is a case-insensitive substring test for "fourth" and "authoriz" anywhere in `decisions.md`, so a note that declines a fourth round ("the maintainer does not authorize a fourth round") admits one, and a single recorded authorization keeps admitting rounds four, five and beyond. The three-round limit is described as staying hard with one maintainer-decided exception, and neither the wording nor the count is checked. | deepseek-v4.1-flash | fixed — tests/test_stage2.py::test_one_authorization_releases_exactly_one_extra_round | no | agree |
| L2-5 | BLOCKER | MAINT | base | `scripts/stage2.py:3850` (`spec_review_blocks`), `scripts/stage2.py:1231` (`append`), `plans/changes/mandatory-spec-review/findings.md:24-26` | Qualification requires the `Stage-2 call … spec-review` line to be the line immediately above the heading, but `append` — the runner's only writer — always separates appended blocks with one blank line, and the old `spec_review` wrote call line and heading in two appends. Every block that exists in the repository therefore has a blank line between call line and heading (findings.md:24 blank, :26 heading), and no `Spec fingerprint:` line exists anywhere under `plans/`, so no real-world block can ever qualify: `review_admission` answers "no qualifying spec review exists" for this change despite its three Opus reviews (findings.md:26, :46, :67), a later `implement` on it refuses, and the morning inventory lists every change holding a spec as review-missing. The whole legacy machinery (`LEGACY_SPEC_REVIEW_DAY`, `legacy_currency_problem`, `spec_last_commit_day`) is unreachable, because a legacy block must pass the same adjacency test first — the spec's "Legacy block" term, criterion 12 and S-26's named limit ("old-runner blocks between implementation and merge need a new review" implying earlier ones count) are defined over an empty set. The tests seed the adjacent layout themselves (`review_audit_line`, `tests/test_stage2.py:7872`), so none of them reads the file layout the old runner actually produced. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_a_blank_line_between_call_line_and_heading_still_qualifies | no | agree |
| L2-6 | MAJOR | SPEC | base | `scripts/stage2.py:4072` (`readable_review`), `scripts/stage2.py:1179` (`parse_rows`), `scripts/stage2.py:3803` (`_stored_rows`), `scripts/stage2.py:1620` (`answer_parts`) | A successful call can write a review block that qualifies as nothing, and nothing then retries or falls back. Call time accepts any six-cell line as a row — the runner's own answer format calls the severity cell "free text (BLOCKER, MAJOR or MINOR is the convention)" — but the stored block is read back by `_stored_rows`, which marks the whole block unreadable when one row's Severity is anything outside BLOCKER/MAJOR/MINOR or an `[AMBIGUITY]` prefix (an empty severity, "CRITICAL", "MAJOR (contract)", lowercase `[ambiguity]`). For such an answer `spec-review` exits 0 and prints "N rows appended" (the rendered table plus prose is written), while criterion 13 and the accepted S-20 rule ("an unreadable answer … the runner retries or falls back") never fire — the unreadability is only discovered later, when implement refuses "no qualifying spec review exists" even though findings.md visibly holds the review's rows. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_spec_review_with_an_unreadable_severity_retries_then_falls_back | no | agree |
| L2-7 | MAJOR | SPEC | base | `scripts/stage2.py:1179` (`parse_rows`), `scripts/stage2.py:3875` (`open_ambiguity_row`), criterion 7, decisions.md S-20 | An open ambiguity in the answer can be dropped into prose where the gate never reads it, so the model starts. An `[AMBIGUITY]` row whose Severity cell carries the mark and that contains one unescaped ` \| ` anywhere splits into more than six cells; `parse_rows` folds such rows only when the second cell is one of BLOCKER/MAJOR/MINOR, so the ambiguity row goes into `rest`, is quoted under `NOT_ROWS_NOTE` in the block, and at read-back `_stored_rows` skips it because quoted lines are not table lines. The block still qualifies (its other rows parse), `open_ambiguity_row` sees no marked row, and implement starts the model — exactly the refutation case S-20 names ("an ambiguity hidden in an unparsed line would start a model"), which that decision closed by making one unparseable table line void the whole block. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_an_overwide_ambiguity_row_reads_and_reads_back_open | no | agree |
| L2-8 | MAJOR | SPEC | base | plan.md criterion ledger row 1; `tests/test_stage2.py:8007-8049`; `AGENTS.md:20`; `docs/WORKFLOW.md:995-998` | Criterion 1's refuting state is the repository's current state, yet its ledger test is green. `AGENTS.md:20` still marks the phase `Spec-Review *(optional)*`, `docs/WORKFLOW.md:997` still says a bounded change "may skip the spec review, which is optional there", and `:995` still claims "Nothing checks a change's class beyond explore" — now false, since `implement` reads `declared_class`. The plan defers those held-path edits to the orchestrator, but the anchored test `test_doctrine_requires_review_before_card` cannot fail on this state: `spec_review_doctrine_problems` only checks that a spec-review step stands before the plan-card step in the chain and that two rows keep their order, never the optional/mandatory wording, so the criterion's own refutation ("the workflow permits a card without a current review") turns it red only in a planted variant that removes the chain step. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_doctrine_requires_review_before_card | yes — tests/test_stage2.py::test_doctrine_requires_review_before_card, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L2-9 | MINOR | MAINT | base | `scripts/stage2.py:4096` (`fourth_round_authorized`) | The fourth-round exception is two substring matches anywhere in decisions.md — `"fourth"` and `"authoriz"` — with no link to a decision about this change: an answer that merely records or quotes the rule (the criterion's own wording quotes it too) unlocks a fourth review round silently, and a British "authorised" spelling never matches. Criterion 3 asks for the maintainer's recorded authorization, not the words appearing somewhere in the file. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_fourth_round_is_not_released_by_wording | no | agree |
| L2-10 | MINOR | MAINT | base | `scripts/stage2.py:4130` (`run_fallback_review`), `scripts/stage2.py:3215` (`run_reviewer`), `prompts/02a-spec-review.md:7` | The declared fallback reviewer runs with `free=True`, which per `run_reviewer`'s own docstring means `--no-tools` and a scratch directory outside the worktree. The substitute for the Opus review therefore cannot read `research.md` or `decisions.md`, the inputs the 02a prompt declares, and the prompt's `READ_REQUEST` ("Read nothing outside this worktree and the repository's git directory") is unsatisfiable from that directory; only the spec body carried in the prompt reaches it, while its block otherwise looks like a full review. Nothing in the block records that the declared inputs were unreachable. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_fallback_review_has_worktree_read_access | no | agree |
| L2-11 | MAJOR | SPEC | base | `AGENTS.md:20`; `docs/WORKFLOW.md` (§1 phase table, §4 draft chain, verb list); `prompts/02-spec.md` "After the spec review"; `prompts/02a-spec-review.md` | The change promises that the workflow itself requires the spec review before the card and repeats draft and review until a current review settles the rows (spec criteria 1 and 3), but the diff touches no workflow text: `AGENTS.md` still marks phase 2a `*(optional)*`, `docs/WORKFLOW.md` carries no three-round rule, no re-review after a spec edit, no maintainer authorization for a fourth round and no final-draft exception (no occurrence of "three rounds"/"round three" anywhere in it), and `prompts/02-spec.md` still describes the chain as one review then one redraft then the card with no re-review step. The plan defers these edits to a held-path step after the accepted attempt, but if the change merged as it stands, criteria 1 and 3 are false in the merged tree while the runner-side machinery exists. | glm-5.3-flash | fixed — tests/test_stage2.py::test_doctrine_repeats_review_after_edit | yes — tests/test_stage2.py::test_doctrine_repeats_review_after_edit, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L2-12 | MAJOR | MAINT | base | `tests/test_stage2.py:8007-8029` (`spec_review_doctrine_problems`, `spec_review_repeat_problems`) | The tests for criteria 1–3 cannot go red for the refuting cases the criteria name. Criterion 1's test checks only that the 2a row stands before Plan in `AGENTS.md` and that the chain names the step before the card — it accepts the live `*(optional)*` marker that permits a card without a current review, which is exactly the S-18 reading ("any one of them allowing the card refutes the criterion"). Criterion 3's test greps for two prose patterns ("fourth … runs without … authoriz", "final draft … still requires … review"); the live texts fail none of them, so a merge that never adds the promised rule text stays green, and a later edit that removes the spec-review step from the chain but leaves the ordering intact can also pass. | glm-5.3-flash | fixed — tests/test_stage2.py::test_doctrine_repeats_review_after_edit | yes — tests/test_stage2.py::test_doctrine_repeats_review_after_edit, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L2-13 | MAJOR | MAINT | base | `scripts/stage2.py`, `fourth_round_authorized` (new, in the spec-review section) | The fourth-round gate is two substring searches: `decisions.md` must contain "fourth" and "authoriz" anywhere. The pair already occurs in decision text that only records the rule rather than authorizing a round — this change's own `decisions.md` (Q-9) contains "releases a fourth round, which is recorded in decisions.md" and "authorizes a fourth round" — so any change whose decisions.md quotes the Q-9 doctrine, or whose history mentions a rejected authorization, passes the gate without the maintainer deciding anything. The orchestrating session writes `decisions.md`, so the agent the gate constrains can satisfy it by writing two words; unlike `triage`, nothing ties the match to a structured maintainer decision, and no test plants a decisions.md that mentions a fourth round without granting one. | glm-5.3-flash | fixed — tests/test_stage2.py::test_fourth_round_is_not_released_by_wording | no | agree |
| L2-14 | MINOR | SPEC | base | `scripts/stage2.py`, `spec_review_inventory` (the class/review/recheck grouping) | A change that fails both the class check and the review check is listed only in the class group: the code uses `if class_problem … elif review_problem … elif recheck`, so a change with a missing or disagreeing class and no qualifying review never appears in the "review missing" group, although criterion 16 says the inventory lists bounded/feature/architectural changes that fail the same review check as implement and separately lists class-refused ones. The maintainer reading the class group does not learn that the review is also missing, and the review group under-reports. | glm-5.3-flash | fixed — tests/test_stage2.py::test_the_inventory_lists_a_change_in_every_failing_group | no | agree |
| L2-15 | MINOR | MAINT | base | `scripts/stage2.py`, `spec_review_prompt` (`body.decode("utf-8")` uncaught) | A spec body that is not valid UTF-8 makes `spec-review` crash with a raw traceback instead of the runner's clean refusal: the admission path wraps spec reads in `UnicodeDecodeError` handling, but the review call decodes the body bytes outside any handler. The same bytes pass admission silently (the fingerprint hashes bytes without decoding), so a change can be implement-admitted yet unable to review. | glm-5.3-flash | fixed — tests/test_stage2.py::test_spec_review_refuses_a_spec_body_that_is_not_utf8 | no | agree |
| L2-16 | MINOR | MAINT | base | `scripts/stage2.py`, `spec_last_commit_day`, `legacy_currency_problem`, `qualifying_reviews`, `review_admission`, `spec_review_inventory` | Currency for legacy blocks re-walks the spec's full commit history with one `git show` subprocess per commit, once per legacy block per admission check, and the morning inventory runs a full admission for every change folder with a spec — so a repository with long spec histories pays O(blocks × commits × changes) subprocesses in one `--spec-review-inventory` run, and the result is recomputed on every implement call. No test bounds this cost and no caching exists. | glm-5.3-flash | rejected — accepted limit: the inventory runs once per morning; its subprocess cost is named in the PR, not optimized here (provisional agent decision, autonomous run 2026-11-19) |  | disagree — Die Zeile nennt keinen gemessenen Aufwand oder konkreten Fall, in dem die Inventur dadurch unbrauchbar wird. |
| L2-17 | MINOR | MAINT | base | `scripts/stage2.py`, `_run` (the comment above the verb choice check, new in the diff) | The comment claims "argparse validates an explicit verb against `choices`, and its default against them too, so a verb-less call … would never parse; the one verb check stands here instead" — but the same diff removes `choices=` from the verb argument, so argparse validates nothing and the stated reason for moving the check into `_run` is false; a maintainer reading the parser sees no `choices` and a comment describing a mechanism that no longer exists. | glm-5.3-flash | fixed — not a test — the comment above the verb check in _run now states only that verbs are validated there, after the verb-less inventory option; it no longer claims argparse choices | no | disagree — Die Zeile beschreibt einen falschen Kommentar ohne konkreten Verhaltensfehler. |
| L3-1 | BLOCKER | SPEC | base | `scripts/stage2.py`, `review_rounds` (~line 3925) and `_review_part`'s `if stale is not None and rounds < 3` (~line 4108); `tests/test_stage2.py::test_stale_legacy_blocks_still_count_as_rounds` | The three-round exception that admits a changed spec without a new review is keyed on a lifetime count of every qualifying block the change ever had, so as soon as a change has held three spec reviews at any point in its history, criteria 6, 11 and 18 stop having any effect for it for ever: any later edit of `spec.md` — a month later, by a different lane, for an unrelated reason — is admitted on review evidence that is arbitrarily old, and the named test asserts exactly that ("legacy blocks the spec body outgrew still count; three admit the edited spec"). Q-10 and criterion 19 grant the exception to *the final draft of the review loop*, a bounded episode, not to every future spec edit; nothing resets the count when the spec is rewritten, so the gate the change exists to build is permanently off for precisely the heavily reviewed changes. | qwen3.8-flash | fixed — tests/test_stage2.py::test_stale_legacy_blocks_still_count_as_rounds | yes — tests/test_stage2.py::test_stale_legacy_blocks_still_count_as_rounds | agree |
| L3-2 | BLOCKER | SPEC | base | `model-endpoints.yaml` (top level: `schema_version`, `datenklassen`, `endpunkte`, `research_swarm`, `ausgeschlossen` — no `spec_review:` block); `scripts/stage2.py` `spec_review_call_config` default `"fallback_model": None` and `run_fallback_review`'s first branch | Criterion 13 promises that a failed Opus review "retr[ies] once after a centrally configured pause before using its centrally declared DeepSeek fallback through Pi", and the spec's third Open decision fixes the initial declared value as `deepseek-v4.1-flash` on OpenCode Go. The shipped declaration file names no `spec_review` block at all, so `spec_review_call_config` returns `fallback_model: None` and every real `spec-review` whose two Opus attempts fail ends in `CallFailed("no fallback model is declared …")` with no block written; the whole Q-6 purpose — a night run not stopped by an unreachable Opus — is unmet as delivered, and criteria 14 and 15 are unreachable code. No test notices, because every fallback test writes its own fixture configuration (`pin_spec_review`) and none reads the repository's declaration file. | qwen3.8-flash | fixed — tests/test_stage2.py::test_repository_declares_the_spec_review_fallback | yes — tests/test_stage2.py::test_repository_declares_the_spec_review_fallback, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L3-3 | MAJOR | SPEC | base | `AGENTS.md:20` (`\| 2a \| Spec-Review *(optional)* \| …`), `docs/WORKFLOW.md:977` (`\| \`bounded\` \| Opus 5.5, where one is held \|`), `docs/WORKFLOW.md:995-998` ("**Nothing checks a change's class beyond explore.** … one stated as `bounded` may skip the spec review, which is optional there") | The mandatory part of the change never reaches the workflow texts it is supposed to change. The spec's Terms name `AGENTS.md`'s phase table and `docs/WORKFLOW.md` as Workflow texts, and criterion 1 is refuted by "The workflow permits a card without a current review", which is exactly what the unchanged `(optional)` marker and "where one is held" still say. `docs/WORKFLOW.md:995` now also states something the runner contradicts: implement derives the class and refuses on it (criterion 4), and the same section's `--stage2-off` sentence still promises that the route "skips class derivation and class/neighbour header checks" while criterion 9 requires the class precondition there. | qwen3.8-flash | fixed — tests/test_stage2.py::test_doctrine_requires_review_before_card | yes — tests/test_stage2.py::test_doctrine_requires_review_before_card, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L3-4 | MAJOR | SPEC | base | `docs/WORKFLOW.md:1465-1467` (draft chain steps 4 and 5), `prompts/02-spec.md` "After the spec review" (lines 128-140) | Q-2 decided the chain becomes draft → review → second draft → **re-review** until a review is clean, and criterion 3 requires the workflow to "repeat draft and review" until settled or round three. The chain as it stands still runs step 4 ("A second `draft <change>` works the review's open rows in") straight into step 5 ("The plan card reaches the maintainer unchanged"), and `prompts/02-spec.md` still ends the phase with "The revised `spec.md` is the one yardstick" with no re-review. So the doctrine a night run follows tells it to show the card on bytes no review has read, while the runner refuses the very implement that follows — doctrine and gate disagree, which is the state S-15 was raised to settle. | qwen3.8-flash | fixed — tests/test_stage2.py::test_doctrine_repeats_review_after_edit | yes — tests/test_stage2.py::test_doctrine_repeats_review_after_edit, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L3-5 | MAJOR | MAINT | base | `tests/test_stage2.py::spec_review_doctrine_problems` (~8008), `test_doctrine_requires_review_before_card`, `test_doctrine_exempts_spike`, `test_doctrine_repeats_review_after_edit` (8032-8090) | The three tests that are supposed to anchor criteria 1-3 stay green against the untouched doctrine, so nothing in `make verify` detects the missing edits of L3-3 and L3-4. They assert only that the chain *mentions* a `spec-review` step before the card line and that `AGENTS.md`'s ` \| 2a \| ` row precedes the ` \| 3 \| Plan` row — both true today — and that regex-planted sentences in a copied-out string would be noticed ("final draft … still requires … review", "a fourth review round runs without … authoriz"). There is no assertion that any live text calls the review mandatory or that no live text still calls it optional, so a reviewer's wording check can only ever go red for a sentence nobody would write. | qwen3.8-flash | fixed — tests/test_stage2.py::test_doctrine_requires_review_before_card | yes — tests/test_stage2.py::test_doctrine_requires_review_before_card, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L3-6 | MAJOR | MAINT | base | `prompts/02a-spec-review.md:57-60` ("## If you find nothing / Say so, in one sentence, and name what you checked"), used by `scripts/stage2.py` `spec_review_prompt` → `phase_prompt` (the file body is sent first, `SPEC_REVIEW_ANSWER_FORMAT` appended last), read back by `readable_review` | The prompt a reviewer is given still asks for a one-sentence clean result, while the new reader accepts a clean review only as the answer equal to exactly `No finding.` and raises `CallFailed("the answer is neither six-cell findings nor exactly \`No finding.\`")` otherwise, and S-10 made prose without rows fail closed. A reviewer that follows the file's own section therefore burns the initial call and the retry (2 × 30-minute limit) on a clean spec, then reaches the undeclared fallback of L3-2 and writes no block at all — leaving implement refused with "no qualifying spec review exists" for a spec that was reviewed and found clean. | qwen3.8-flash | fixed — tests/test_stage2.py::test_spec_review_prompt_states_the_strict_answer_format | yes — tests/test_stage2.py::test_spec_review_prompt_states_the_strict_answer_format, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L3-7 | MAJOR | SPEC | base | `scripts/stage2.py` `FOURTH_ROUND_TITLE` / `FOURTH_ROUND_GRANT` and `fourth_round_authorized` (~4155-4175); criterion 3 of `spec.md` | The only escape from the three-round cap is gated on an invented literal form: a record of this change whose heading title begins `Fourth spec-review round` and whose `answer:` field begins with the English word `authorized` (`["\` \s]*authori[sz]ed\b`). Criterion 3 says only that the maintainer "authorizes a fourth round in `decisions.md`", and every answer this repository records is the maintainer's wording or an option letter — `decisions.md` of this very change holds `"jaja"`, `"C"`, `"A"`, `"A: Du entscheidest (Empfohlen)"`, `"C: Nach Runde 3 frei"` — none of which matches, so an authorization the maintainer actually gave releases nothing, the change silently falls to re-slicing, and the failure looks like a maintainer decision. | qwen3.8-flash | fixed — not a test — the form that authorizes a fourth round is now declared in `spec.md` under Open decisions. It is a `Q-<n> · Fourth spec-review round` question in `decisions.md`, answered by the maintainer with an answer beginning `authorized`. The runner's refusal already names the same form. | no — not a test | disagree — Die aktuelle Spezifikation legt genau diese Form für die Freigabe einer vierten Runde fest. |
| L3-8 | MAJOR | MAINT | base | `scripts/stage2.py` `spec_review` rounds guard (~4277: `if not recheck and rounds >= 3 and not (rounds == 3 and fourth_round_authorized(...))`) together with `_review_part`'s ambiguity refusal (~4097) | Once three qualifying blocks exist the `spec-review` verb refuses to run, but the gate keeps demanding evidence it can no longer be given: for a change whose newest block holds an unsettled row, implement answers "the newest qualifying spec review … still has the open ambiguity row …; settle the row and **review the spec again** before a model starts", and the named command then refuses with "3 spec-review rounds have run … a fourth round runs only when …". A maintainer following the runner's own instruction has no route left except the authorization of L3-7, and past four rounds even that is closed ("no round runs after the fourth"), so the change is bricked rather than re-sliced by a rule nobody wrote down. | qwen3.8-flash | fixed — tests/test_stage2.py::test_an_ambiguity_with_no_round_left_is_settled_in_decisions | yes — tests/test_stage2.py::test_an_ambiguity_with_no_round_left_is_settled_in_decisions | agree |
| L3-9 | MINOR | MAINT | base | `scripts/stage2.py` `legacy_currency_problem` (`head = spec_body_of(_git_output(root, "show", f"HEAD:…").encode("utf-8"))`) beside `spec_last_commit_day` (`_git_output(root, "show", …, preserve_newlines=True).encode("utf-8")`) | The committed spec body is read two incompatible ways in adjacent functions: the disk/HEAD comparison goes through `run_git` in text mode with `errors="replace"`, so a committed body containing a byte that is not valid UTF-8 arrives as U+FFFD and can never equal the exact disk bytes, and every legacy review of such a spec is reported "the spec body changed on disk without a commit after it" — a permanent refusal with a message that misattributes it to the operator. The same file's bytes read in the sibling function go through `os.fsdecode` and are re-encoded with plain `"utf-8"`, which raises `UnicodeEncodeError` on the surrogate escapes instead of refusing, so `spec-review`/implement tracebacks (exit 1) where the change elsewhere promises `refused:` (exit 2) — see `test_spec_review_refuses_a_spec_body_that_is_not_utf8` for the byte-exact handling this path lacks. | qwen3.8-flash | fixed — tests/test_stage2.py::test_a_committed_spec_body_that_is_not_utf8_reads_byte_exact | yes — tests/test_stage2.py::test_a_committed_spec_body_that_is_not_utf8_reads_byte_exact | agree |
| L3-10 | MINOR | SPEC | base | `tools/claude-code/skills/handover/SKILL.md` (contains no mention of `stage2.py`, of an inventory or of spec reviews), `scripts/stage2.py` `spec_review_inventory`, `plan.md` step 3 | The new `--spec-review-inventory` has no caller. Q-8 and criterion 16 exist so that the maintainer learns which changes implement would refuse *before* a refusal, and `plan.md` step 3 says the morning handover skill "instructs … to run `python3 scripts/stage2.py --spec-review-inventory` and include its output", but the instruction is nowhere in the skill, and no test reads the live file (the tests only invoke the function with `stage2.main([...])`). As shipped, the list exists only if someone remembers the flag, which is the state the change was written to end. | qwen3.8-flash | fixed — tests/test_stage2.py::test_morning_handover_runs_the_spec_review_inventory | yes — tests/test_stage2.py::test_morning_handover_runs_the_spec_review_inventory, red first by hand against the old texts (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | agree |
| L4-1 | MINOR | MAINT | base | `scripts/stage2.py`, `body_edits_after_review` | After three spec-review rounds an uncommitted-only body change is refused instead of admitted: when `spec.md` has no committed version the fingerprint matches none of the (empty) version list, so the function returns `None` and the post-three-round single-edit exception (criterion 19) never applies, defeating the admission for a spec that lives only on disk. | hy3 | fixed — tests/test_stage2.py::test_final_draft_with_uncommitted_only_spec | yes — tests/test_stage2.py::test_final_draft_with_uncommitted_only_spec, red first by hand against HEAD's scripts/stage2.py (orchestrator hand repair, 2026-11-20) | agree |
| L4-2 | MINOR | MAINT | base | `scripts/stage2.py`, `spec_review_inventory` | The morning inventory aborts the whole list on the first non-read error raised while measuring one change (e.g. a git launch failure surfacing from `review_admission` → `spec_body_versions`), although its contract states a change that cannot be read is reported, never silently omitted. | hy3 | fixed — tests/test_stage2.py::test_inventory_continues_after_measurement_error | yes — tests/test_stage2.py::test_inventory_continues_after_measurement_error, red first by hand against HEAD's scripts/stage2.py (orchestrator hand repair, 2026-11-20) | agree |
| L4-3 | MINOR | MAINT | base | `prompts/02a-spec-review.md` vs `scripts/stage2.py` (`open_ambiguity_row`, `review_severity`) | The prompt instructs the reviewer that the `[AMBIGUITY]` mark belongs in the Severity cell, but the admission code also treats a Finding cell beginning with `[AMBIGUITY]` as an open ambiguity; the prompt understates the rule, so the prompt and the matching code drift and a maintainer editing one would mis-state the other. | hy3 | fixed — not a test — prompts/02a-spec-review.md names both places an open [AMBIGUITY] may stand, the start of the Severity cell or the start of the Finding cell (plan step 3 applied by the orchestrator, maintainer 2026-11-20) | no — not a test | agree |
| L5-1 | MAJOR | MAINT | base | `scripts/stage2.py:3843` (`_stored_rows`) | A Phase 2a block that holds a table line with a single cell (a hand-written note line such as `\| note \|`) makes the reader index `cells[1]` on a one-element list and raise `IndexError`, instead of treating the block as unreadable. The new `docs/WORKFLOW.md` section promises that one table line which does not parse makes the whole block unreadable, and an unreadable block is a plain refusal; here `implement` and `--spec-review-inventory` die with a traceback instead. Every other row reader (`parse_rows`) checks the cell count before it reads the severity cell; this one does not, and a seeded one-cell line in a 2a block shows it. | minimax-m3.1-flash | fixed — tests/test_stage2.py::test_single_cell_review_line_refuses_without_traceback | yes — tests/test_stage2.py::test_single_cell_review_line_refuses_without_traceback | agree |
| L5-2 | MAJOR | SPEC | base | `scripts/stage2.py:4146` (`open_ambiguity_row` only), `scripts/stage2.py:4427` (`spec_review_inventory`), `docs/WORKFLOW.md` "The spec review before the plan card" | The promised maintainer decision for a BLOCKER after the third round has no runner surface. The workflow, `spec.md` criterion 3 and `decisions.md` Q-9 send "a BLOCKER, or an `[AMBIGUITY]` whose answer changes the spec" to the maintainer, who authorizes a fourth round or re-slices the change; the gate checks only the `[AMBIGUITY]` mark, so a change whose newest qualifying review still carries an open BLOCKER row is admitted by `implement`, and the morning inventory lists only changes whose review is missing, unreadable, stale or ambiguous, so such a change is named in no group and never reaches the maintainer's list. | minimax-m3.1-flash | fixed — tests/test_stage2.py::test_open_third_round_blocker_refuses_implement_and_inventory | yes — tests/test_stage2.py::test_open_third_round_blocker_refuses_implement_and_inventory | agree |
| L5-3 | MINOR | MAINT | base | `scripts/stage2.py:3806` | A stored Opus block qualifies only when the audit line above it names the model id the declaration holds today (`OPUS[1]`), while the heading carries only the label "Opus 5.5". Switching the Opus model in the declaration therefore stops every stored 2a block from qualifying, and each change is then refused at `implement` with "no qualifying spec review exists" and no hint that the model id moved. The fallback block records its own model in its heading and survives such a switch; the Opus block does not. | minimax-m3.1-flash | rejected — Accepted limit, named in the PR: a model-id switch in the declaration is a deliberate maintainer change that re-qualifies reviews; no switch is planned (provisional agent decision, night run 2026-11-20-a). |  | disagree — Ein Wechsel der Opus-Modellkennung ist ein hypothetischer künftiger Konfigurationswechsel; die Zeile belegt keinen aktuellen Fehler. |
| L5-4 | MINOR | MAINT | base | `model-endpoints.yaml` | The declared `fallback_endpoint` is a knob that can hold only one legal value: the runner refuses any endpoint but `opencode-go`, and it does so only after both Opus calls have failed, as a `CallFailed` that names no remedy. `model-endpoints.yaml` presents the value as switchable ("Switching it is one value"), so a maintainer who points it elsewhere gets a dead fallback rather than a working one. | minimax-m3.1-flash | fixed — orchestrator hand edit 217adb13 (model-endpoints.yaml comment names the one admitted fallback endpoint; the runner does not commit that file) | no | disagree — Die aktuelle Konfiguration nennt OpenCode Go als einzige unterstützte Route und erklärt die Einschränkung. |
| L5-5 | MINOR | MAINT | base | `scripts/stage2.py:4151` and `scripts/stage2.py:4366` (the refusal messages), `scripts/stage2.py:4223` and `scripts/stage2.py:4257` (the readers) | The refusal messages name a `decisions.md` form that the readers take more strictly than the message says. `maintainer_answers` counts a record only when it carries `status: answered`, `answered_by: maintainer`, a non-empty `asked` and a non-empty `answer`; the ambiguity message asks only for "a question headed `Q-<n> · Ambiguity S-1` and an answer", and the fourth-round message names the heading and the answer but never the status field. A maintainer who writes the named heading and answer and leaves the record's status at `draft` is refused again with the same message and no hint of the field that is missing. | minimax-m3.1-flash | fixed — tests/test_stage2.py::test_review_refusals_explain_required_decision_fields | yes — tests/test_stage2.py::test_review_refusals_explain_required_decision_fields | agree |
| L5-6 | MINOR | MAINT | base | `scripts/stage2.py:9624` (`declared_class`), `scripts/stage2.py:10862` (`implement`), `scripts/stage2.py:12268` (the `--class` refusal) | The class refusal the implement gate prints offers `--class` as its first remedy, but the implement verb refuses that option ("--class belongs to the explore and prepare-explore verbs alone"). The operator is pointed at a flag the route rejects; only the second half of the sentence works, and it names `research.md` alone, although the class may equally be stated in `spec.md`, which the same reader reads as well. | minimax-m3.1-flash | fixed — tests/test_stage2.py::test_implement_missing_class_remedy_names_valid_headers | yes — tests/test_stage2.py::test_implement_missing_class_remedy_names_valid_headers | agree |
| L6-1 | MAJOR | SPEC | base | `plans/changes/mandatory-spec-review/spec.md`, Terms "Open ambiguity", criterion 7 and decision Q-5 | The yardstick contradicts the gate it judges. The Terms say an answer alone does not close an ambiguity row, criterion 7 refuses implement whenever the newest qualifying block holds one and is refuted by "the model starts", and one detail note repeats that an open ambiguity still refuses under criterion 7. The runner, however, admits the change once no review round can run and `decisions.md` holds any maintainer-answered question mentioning the row (`ambiguity_settled` in `scripts/stage2.py`), matching the workflow text and a second detail note; decision Q-5 recorded the opposite ("an answer recorded in decisions.md does not count until its row's Status is moved"). A phase-6 reviewer measuring the gate against criterion 7 finds the code refutes the criterion's own refutation clause. | mimo-v2.6-pro | fixed — not a test — Spezifikation beschreibt die Ausnahme für eine beantwortete Mehrdeutigkeit; die historische Entscheidung bleibt erhalten. | no — not a test | disagree — Die aktuelle Spezifikation nennt die Ausnahme für eine Antwort der Person ausdrücklich in den Begriffen und in Kriterium 7. |
| L6-2 | MAJOR | SPEC | base | `plans/changes/mandatory-spec-review/spec.md`, criterion 19 | The one-final-draft limit lives outside the criterion. Criterion 19 accepts review evidence after three rounds "when the spec body changes", and its refuted-by forbids a refusal caused by the changed body after three rounds; the runner refuses a second body version after round three (`body_edits_after_review` / `edits > 1` in `review_admission`), the workflow text and test `test_a_later_spec_edit_after_the_final_draft_needs_a_review_again` agree, and `plan.md` step 1 promises admission of "a changed spec body" with no cap. The cap ("one body version after the reviewed one") appears only in a detail note, so the built gate matches the criterion's refutation and criterion 19 cannot be used to judge it. | mimo-v2.6-pro | fixed — not a test — Kriterium und Plan begrenzen den letzten Entwurf auf eine Fassung. | no — not a test | disagree — Kriterium 19 begrenzt die Ausnahme inzwischen ausdrücklich auf eine abschließende Version. |
| L6-3 | MINOR | MAINT | base | `scripts/stage2.py`, `ambiguity_settled` | The settlement reader is looser than the documented form `Q-<n> · Ambiguity <row id>`: it searches "ambiguity <row id>" anywhere in a question's title and accepts any non-empty maintainer answer. A question that merely mentions the row (e.g. "Why the Ambiguity R1 wording was chosen") whose answer declines to settle it counts as settlement and unblocks implement. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_ambiguity_settlement_requires_exact_question_title | yes — tests/test_stage2.py::test_ambiguity_settlement_requires_exact_question_title | agree |
| L6-4 | MINOR | MAINT | base | `scripts/stage2.py` | A question id is counted once, first occurrence winning (the interview-minimum rule imported into the round count). A re-asked or reissued `Q-<n> · Fourth spec-review round` record under an id already answered "no" leaves the later `authorized` answer invisible; the refusal names the heading form but never says the id must be unused, so the change stalls at "re-slice" with no visible cause. | mimo-v2.6-pro | rejected — Accepted limit, named in the PR: a question id is answered once; a re-asked fourth-round question takes a new id. (provisional agent decision, night run 2026-11-20-a) |  | agree |
| L6-5 | MINOR | MAINT | base | `scripts/stage2.py`, `SPEC_REVIEW_ANSWER_FORMAT` | The strict severity instruction is spliced into the shared answer format by a literal `str.replace` of one sentence of `ANSWER_FORMAT`. Any rewording of that sentence silently drops the strict instruction while `readable_review` still fails the call on any other severity: the reviewer is told severity is free text, answers CRITICAL, the call fails twice, and a night run falls back for no real outage. No test pins the replace target to `ANSWER_FORMAT`. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_spec_review_severity_splice_refuses_changed_shared_instruction | yes — tests/test_stage2.py::test_spec_review_severity_splice_refuses_changed_shared_instruction | agree |
| L6-6 | MINOR | MAINT | base | `scripts/stage2.py` | The endpoint check that keeps the fallback on the single admitted endpoint runs only inside `run_fallback_review`, i.e. after Opus has already failed twice mid-outage; `spec_review_call_config` accepts any `fallback_endpoint` string, so a typo in `model-endpoints.yaml` (whose comment says the runner refuses any other endpoint, without saying when) is discovered only on the night the fallback is needed. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_spec_review_config_refuses_unadmitted_fallback_endpoint | yes — tests/test_stage2.py::test_spec_review_config_refuses_unadmitted_fallback_endpoint | agree |
| L7-1 | MAJOR | SPEC | base | `scripts/stage2.py` | The fallback review block is always headed `## Phase 2a — fallback <model>, <date>` and never carries the `Opus re-check of the fallback review, same round` marker, so `review_rounds` counts it as one round more; and `review_round_open` returns true whenever the newest qualifying block is a current fallback (`recheck or rounds < 3 or …`), so the three-round cap does not apply on that path at all. When the Opus re-check of a fallback fails twice, the fallback writes a plain fallback block: a change whose third round was a fallback reaches four qualifying blocks, i.e. a fourth spec-review round no maintainer authorized, and while the newest block stays a fallback the verb keeps running, so “at most three rounds, a fourth only by a recorded maintainer answer, no round after the fourth” never bites. No test covers a fallback that replaces a failed re-check. | minimax-m3 | fixed — tests/test_stage2.py::test_fallback_replacing_recheck_respects_round_cap | yes — tests/test_stage2.py::test_fallback_replacing_recheck_respects_round_cap | agree |
| L7-2 | MINOR | MAINT | base | `scripts/stage2.py` | The verb reads the change’s `findings.md` with a bare `read_text(encoding="utf-8")` and the spec body with `spec_body_bytes`, neither guarded, while the admission’s `_review_part` guards exactly these two reads and answers “cannot be read”. A `findings.md` that is not UTF-8 (or a spec file that disappears between the preflight and the read) therefore ends `spec-review` in an unhandled `UnicodeDecodeError`/`OSError` traceback instead of the runner’s refusal, even though the same files are read defensively a few hundred lines above. | minimax-m3 | fixed — tests/test_stage2.py::test_spec_review_refuses_files_unreadable_after_preflight | yes — tests/test_stage2.py::test_spec_review_refuses_files_unreadable_after_preflight | agree |
| L7-3 | MINOR | SPEC | base | `scripts/stage2.py` | For a legacy (undigested) review the runner measures currency and the number of later body versions with two different rules, and they disagree: the currency check calls the review stale when its heading day lies before the last committed spec-change day, while the counter drops the oldest committed body version unconditionally (`versions[1:]`) on the assumption that it already existed when the review was written. A legacy review whose spec was committed only after the review day is thus reported stale and counted as zero edits at the same time, and after three rounds the admission follows the counter and lets the change implement on a review the runner has just called stale — the case the spec’s criterion 12 names as refuted. | minimax-m3 | fixed — tests/test_stage2.py::test_legacy_body_versions_count_from_review_day | yes — tests/test_stage2.py::test_legacy_body_versions_count_from_review_day | agree |
| L8-1 | MAJOR | MAINT | base | `scripts/stage2.py`, `spec_review_answer_format` | The spec-review answer format is built by replacing a literal, multi-line severity paragraph copied from `ANSWER_FORMAT`. If a later change rewords that shared text, `stage2.py` will crash at import with `ValueError: shared severity instruction must appear exactly once`; the coupling should be broken by a marker or by composing the format explicitly. | kimi-k2.7-code | rejected — As designed: the import-time ValueError is the loud guard L6-5 asked for; a reworded shared paragraph must fail at once, never drop the strict instruction silently. (provisional agent decision, night run 2026-11-20-a) |  | disagree — Die Prüfung verweigert eine widersprüchliche Anweisung ausdrücklich; die Zeile nennt keinen konkreten Fehler im aktuellen Verhalten. |
| L8-2 | MINOR | MAINT | base | `scripts/stage2.py`, `LEGACY_SPEC_REVIEW_DAY` | The legacy-review cutoff is a hard-coded date (`2026-11-19`). If the merge is delayed, runner-written blocks from between that day and the merge will be rejected unless they already carry a fingerprint, and the only fix is to edit the constant by hand. | kimi-k2.7-code | rejected — Accepted limit, named in the PR: the legacy cutoff day is a constant; if the merge slips past it the constant moves in the merge PR. (provisional agent decision, night run 2026-11-20-a) |  | disagree — Die aktuelle Spezifikation legt den festen Stichtag und die Folge für ältere Runner-Blöcke bis zum Merge ausdrücklich fest. |

Rounds run: 8

Record digest: sha256:f03ade8dac8c02fb77de324df9099db8e445aaab9698eb72af93476e3095b0ec

Record identity: sha256:58bdafb7067b924607489fe60a2a57c6e662c7252f7f4277c02bfb1e2c0f0da5

Cut rounds: 1, 2, 3, 4, 5, 6, 7, 8

Loop state: {"availability": {"checked_at": "2026-11-19T21:54:58+00:00", "failed": {"deepseek-v4-pro": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "glm-5.3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "grok-4.7": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "hy4-preview": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "kimi-k3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated.\"}", "qwen3.8-max": "pi call failed: exit 1: 403 {\"type\":\"error\",\"error\":{\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}}"}, "reachable": ["hy4-flash-free", "deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "glm-5.2": "absent from the fresh provider catalog", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "qwen4-max": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 \"thinking.type.enabled is not supported for this model; use thinking.type.adaptive\" (a Pi adapter setting, bead coding-harness-36za evidence))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": []}, "consumed": ["free", "flash", "rung:qwen3.8-flash", "rung:hy3", "rung:qwen3.7-plus", "rung:minimax-m3.1-flash", "rung:mimo-v2.6-pro", "rung:minimax-m3", "rung:kimi-k2.7-code", "rung:step-5-preview"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-fable-5-2", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "gemini-4-carbon", "provider": "opencode"}, {"model": "gemini-4-hydrogen", "provider": "opencode"}, {"model": "gemini-4-neon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "gpt-6.2-astra", "provider": "opencode"}, {"model": "gpt-6.2-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "hy4-flash-free", "provider": "opencode"}, {"model": "iceman-free", "provider": "opencode"}, {"model": "inkling-2-small-free", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "longcat-2.5-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-ember-1.0", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "tidepool-alpha-free", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-flash-free", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "qwen4-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-19T21:47:21+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1795124840296, "etag": "W/\"cc2f04cbfe8260c9f7e1aa3de29586be\"", "lastModified": 1795094589000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash 1017", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "hy4-flash-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4 flash Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 1048576, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 1048576, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "LongCat 2.5 Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.075, "cacheWrite": 1.875, "input": 1.5, "output": 4.5}, "id": "qwen4-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Qwen4 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": ["opencode-go/gemini-4-argon: wire api \"google-generative-ai\" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base"], "overlay": ["beam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-flash-free", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "longcat-2.5-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "qwen4-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-11-13", "id": "longcat-2.5-free", "reason": "The maintainer took the longcat models out for good on 2026-11-13 (\"das scheint ein sehr langsames modell zu sein\"): longcat-2.0 timed out on all three online topics of that day's research swarm run; the free longcat id goes with it (bead coding-harness-363r.2)."}, {"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": ["hy4-flash-free"], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"], "rungs": ["qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.
> Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor, qwen4-max.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the free diff of scripts/stage2.py was cut at 400 lines; the free diff of tests/test_stage2.py was cut at 400 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> mimo-v2.6-flash wrote 1 row(s) with more than six cells; the cells after the fifth were joined into the finding, so an unescaped `|` before it moves the columns.
> The diff was cut: the change diff was cut at 2000 of 2993 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> qwen3.8-flash wrote 1 row(s) with more than six cells; the cells after the fifth were joined into the finding, so an unescaped `|` before it moves the columns.
> The diff was cut: the change diff was cut at 2000 of 3444 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 4143 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> ## Stage failed — rung:qwen3.7-plus (qwen3.7-plus)
> qwen3.7-plus answered twice without a written round (2026-11-20); retired on the maintainer's standing authorisation for this lane, night run 2026-11-20-a
> The stage is retired by the maintainer: no round of it counts, and the loop continues with the next stage.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 4225 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 4330 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 4376 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 4573 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> ## Stage failed — rung:step-5-preview (step-5-preview)
> step-5-preview was stopped by the 45-minute round limit (2026-11-21); retired by the orchestrator in night run 2026-11-20-a (provisional agent decision)
> The stage is retired by the maintainer: no round of it counts, and the loop continues with the next stage.

<!-- End of released loop record -->

Stage-2 call, 2026-11-21: review (loop marks) · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 5030 commits, 12 rules.

Stage-2 call, 2026-11-21: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 5033 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +24 -16
> - `tests/test_stage2.py` +32 -1
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 68 lines of this gate left out …]
> ........................................................................ [ 73%]
> ........................................................................ [ 75%]
> ........................................................................ [ 76%]
> ........................................................................ [ 77%]
> ........................................................................ [ 78%]
> ........................................................................ [ 79%]
> ........................................................................ [ 80%]
> ........................................................................ [ 81%]
> ........................................................................ [ 82%]
> ........................................................................ [ 84%]
> ........................................................................ [ 85%]
> ........................................................................ [ 86%]
> ........................................................................ [ 87%]
> ........................................................................ [ 88%]
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
> ................                                                         [100%]
> =================================== FAILURES ===================================
> ___________ test_an_overwide_ambiguity_row_reads_and_reads_back_open ___________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/.venv/bin/python3
>
>     def test_an_overwide_ambiguity_row_reads_and_reads_back_open() -> None:
>         """L2-3, L2-7: an `[AMBIGUITY]` row with an extra unescaped pipe folds like any row and stays an open row."""
>         answer = rows(1) + "\n| A1 | [AMBIGUITY] scope | SPEC | criterion 2 | spec.md:2 | one | two |"
>         parsed = stage2.readable_review(answer)
>         assert [row[0] for row in parsed] == ["X1", "A1"]
>         stored = stage2.answer_block(parsed, answer, "Opus")
>         block = stage2.spec_review_blocks(f"## Phase 2a — Opus 5.5, {FIXED_REVIEW_DAY}\n\n{stored}\n")[0]
>         assert block.table_readable and [row["id"] for row in block.rows] == ["X1", "A1"]
> >       assert stage2.open_ambiguity_row(block) == "A1"
> E       AttributeError: module 'stage2' has no attribute 'open_ambiguity_row'. Did you mean: 'open_ambiguity_rows'?
>
> tests/test_stage2.py:8549: AttributeError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=65654) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/mandatory-spec-review/tests/test_stage2.py:24902: DeprecationWarning: This process (pid=65648) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_an_overwide_ambiguity_row_reads_and_reads_back_open
> 1 failed, 6406 passed, 17 skipped, 5 warnings in 536.32s (0:08:56)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 47450 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/mandatory-spec-review/stage2/attempts/mandatory-spec-review/attempt-1-20261121T060355213835Z-74424b42.md
> ````

Stage-2 call, 2026-11-21: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1114 files, 5034 commits, 12 rules.

Runner restoration, 2026-11-21: repair · attempt 2 · route codex-repair — lifecycle fields: plans/changes/mandatory-spec-review/plan.md, plans/changes/mandatory-spec-review/spec.md — unchanged

Stage-2 call, 2026-11-21: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1114 files, 5059 commits, 12 rules.

## Phase 6 — Codex, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-4 | MAJOR | SPEC | base | `scripts/stage2.py:4015` (`body_edits_after_review`) | Wenn nach drei Review-Runden eine bereits früher commitete Spezifikation mit uncommitteten Änderungen geprüft und danach genau einmal für den finalen Entwurf geändert wird, verweigert der Runner die Implementierung. Er findet den Fingerabdruck der geprüften Fassung nicht in der Git-Historie und kann die eine erlaubte Änderung deshalb nicht zählen. Diese erste geänderte Fassung muss zugelassen werden. [Kriterium 19] | Codex | open | — |

Phase 6 verdict: codex 01a1fdb9-3073-7871-adfd-16a1354fe7e8, 2026-11-21
Reviewer session: codex 01a1fdb9-3073-7871-adfd-16a1354fe7e8 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
