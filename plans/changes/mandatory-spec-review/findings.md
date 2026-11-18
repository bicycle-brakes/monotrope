---
title: "Findings — mandatory-spec-review"
category: findings
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-18
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
