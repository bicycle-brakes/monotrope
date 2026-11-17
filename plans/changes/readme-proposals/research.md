---
title: "Research — readme-proposals"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-7kzl
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-17", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# readme proposals — Research

Stage-2 call, 2026-11-17: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1112 files, 4538 commits, 12 rules.

## Runner exploration — 2026-11-17

Phase 1 is done — every statement below was checked in this worktree on 2026-11-17. The research follows, in English, ready to append below the existing header of `plans/changes/readme-proposals/research.md`.

Lese-Hinweis: Das Folgende ist der Artefakt-Text (Englisch, gemäß House Rule 1) zum Anhängen an `research.md`.

---

*Read cut-off: worktree `docs/readme-proposals` (per session start it carries edits only under `plans/changes/readme-proposals/` and had merged `origin/main` at `b35927ca`), files as read on 2026-11-17. No `git` command was available to this phase; commit-hash equality with `dfede341` is listed under Not checked.*

## Summary

- **The implement post-run check is the one real drift, and it is not in the README.** `docs/how-it-works.md` and `docs/testing.md` still say an implement attempt runs the full `make verify`; ADR 0025 as amended on 2026-11-12 routes implement and repair through a targeted check with the full run only as fallback (`docs/adr/0025-targeted-check-after-repair.md`, amendment section "Implement and draft amendment", decision 1; `docs/WORKFLOW.md:1026-1028`, updated 2026-11-15). README's own post-run bullets are already correct.
- **README's "Checked by tools" list overstates two gates.** No script or gate checks a spec for an open `[DECISION]` — that check belongs to the validator that is not built (`docs/WORKFLOW.md:36-38` header note; grep for `\[DECISION\]` across `scripts/` matched only the research and question-context scripts). And the repository's cited "handover schema and gate" (`docs/research/2026-10-31-architecture-reconciliation.md`, M1 row, line 166) is `tests/test_handover_entry.py`, whose own docstring says it measures "the handover injection and its trust threshold", not a content schema; only the handover header's currency is gated (`provenance.yaml:104-106`, `decisions/gates.yaml` gate `frontmatter-current`).
- **README's status cut-off contradicts itself.** The section opens with "gate counts re-read on 2026-11-03" (`README.md:225-226`) while the counts below cite `8c54b1a0`, 2026-11-12 (`README.md:231`). I re-counted `decisions/gates.yaml` on 2026-11-17: 24 gates, 20 block, 3 report, 1 advisory — unchanged.
- **Model access omits the research swarm** (ADR 0020, `status: accepted` in its frontmatter), the phase-1 route for `feature` and `architectural` changes; README names only GLM exploring "small changes" (`README.md:213-218`).
- `docs/orchestration.md:29` links a README anchor (`#working-in-parallel`) that no README heading provides — the section does not exist under that name.
- `docs/testing.md:61` presents the stop hook as running; the tree has no `.claude/hooks/` at all and the doctrine's own header note lists it as missing.
- The lead proposal for bead coding-harness-tlr4 is below, marked as such.
- Everything else checked holds: getting-started commands and paths, all links and diagram files, the phase table, the class paragraph, the "Not built yet" list (accurate against the tree), the license pair with `COMMERCIAL.md`, the model routes against `model-endpoints.yaml`, and `docs/WORKFLOW.md` itself (updated 2026-11-15) needed no correction where README summarises it.

## README.md

**Where** `README.md:9-11` — **Today**: "**A step-by-step workflow for AI coding agents. Every step leaves a file, and scripts check the agent's claims.**" — **Why stale or wrong**: not wrong, but bead coding-harness-tlr4 asks (task brief, `handover.md` in this folder) that the top lead with what the workflow *enforces* that a prompt-only workflow can only advise, with measured numbers and their cut-off. **Proposed text** (this is the tlr4 proposal, marked as such — the maintainer decides):

> **A step-by-step workflow for AI coding agents. Where a prompt-only workflow can only advise, Monotrope enforces: a repair counts only when its test failed on the code before the repair, and the runner re-runs that test itself; every call to another model passes the endpoint allowlist and the leak check, and a block stops the call with no fallback; one gate list drives the local checks and CI alike — 24 gates, 20 of them blocking (`decisions/gates.yaml`, counted 2026-11-17; last declared at `8c54b1a0`, 2026-11-12) — and a suite of 4,426 tests (2026-11-02, `98d58db9`) must be green before `main` merges a pull request.**

(Number sources: gate count recounted from `decisions/gates.yaml` on 2026-11-17, matching the declared citation in `docs/how-it-works.md:291-293`; test count from `docs/how-it-works.md:335-337`, which carries its own cut-off and the caveat "one change ahead of `main`"; red-first from `docs/WORKFLOW.md` §4 and `docs/testing.md` layer 2; leak check from `scripts/leakcheck.py`, called by the runner per the `Makefile:32` comment "Runs before a foreign call (`scripts/stage2.py` runs it itself)".)

**Where** `README.md:240-241` — **Today**: "- The interview minimums per class, an open `[DECISION]` in a spec, the presence of a question's context and the handover schema are gates." — **Why stale or wrong**: two of the four items have no tool behind them today. `decisions/gates.yaml` (read in full, 2026-11-17) contains `interview-minimums` and `question-context`, but no gate for a spec's open `[DECISION]` and none for a handover schema; a grep for `\[DECISION\]` over `scripts/` matched only `scripts/stage2_research_report.py`, `scripts/stage2.py`, `scripts/research_handoff.py`, `scripts/check_research_handoff.py`, `scripts/check_question_context.py`. The open-`[DECISION]` check belongs to the phase-2 validator, which the doctrine's own header note lists as not in the tree (`docs/WORKFLOW.md:36-38`: "`scripts/validate_change_artefacts.py` and the stop hook … are **not** in this repository"; confirmed by glob on 2026-11-17: `scripts/validate*.py` no match). For the handover schema: the repository names `tests/test_handover_entry.py` as its "handover schema and gate" (`docs/research/2026-10-31-architecture-reconciliation.md`, M1 row), but that file's docstring (`tests/test_handover_entry.py:1-8`) says it measures "the handover injection and its trust threshold (bead hit, part 2)" — the session-start injection, not the file's structure. What is actually gated on handovers is the header: `provenance.yaml:104-106` declares `docs/journal/handover/` `frontmatter: required`, enforced by the `frontmatter-current` gate (`decisions/gates.yaml`, gate `frontmatter-current`). **Proposed text**:

> - The interview minimums per class, the presence of a question's context,
>   and the currency of a handover file's header are gates. An open
>   `[DECISION]` in a spec and the handover's section schema are rules the
>   phase prompts carry, with no tool behind them yet (see
>   [Not built yet](#not-built-yet)).

**Linked files that must change with it**: none; this bullet exists only here.

**Where** `README.md:46-48` — **Today**: "A session ends with a dated *handover* file under `docs/journal/handover/`, checked against a schema and delivered as a pull request." — **Why stale or wrong**: same evidence as above; a content-schema check is not found in `scripts/` or `tests/` (grep for `handover[ -]schema` across the repository matched prose only: the reconciliation note, handover files, `README.md` itself, `docs/architecture/target-architecture.md` — no script or test file). **Proposed text**:

> A session ends with a dated *handover* file under `docs/journal/handover/`,
> whose header a gate holds current, and is delivered as a pull request.

**Linked files that must change with it**: none.

**Where** `README.md:225-226` — **Today**: "Status as stated on 2026-11-01 against `main` at `ac11da5d`; gate counts re-read on 2026-11-03 at `b424be3a`." — **Why stale or wrong**: the same section's first bullet cites newer evidence, "`8c54b1a0`, 2026-11-12" (`README.md:231`), so the section's own cut-off sentence is older than the numbers it introduces; and the counts still hold — I re-counted `decisions/gates.yaml` on 2026-11-17: 24 gates; enforcement `block` 20, `report` 3 (`docs-links`, `markdownlint`, `research-currency`), `advisory` 1 (`lychee`). **Proposed text** (commit id left to the maintainer, who can resolve it):

> Status as stated on 2026-11-17 against `main`; gate counts unchanged since
> `8c54b1a0` (2026-11-12), re-counted on 2026-11-17: 24 gates, 20 block,
> 3 report, 1 advisory.

**Linked files that must change with it**: none (docs/how-it-works.md:291-293 carries the same counts with the same `8c54b1a0` citation and stays correct).

**Where** `README.md:213-218` — **Today**: "- **The runner's routes to other vendors** need your own accounts, set up on your machine: OpenAI Codex (drafts, repairs, final review), GLM through Z.ai (exploring small changes, implementing) and OpenCode Go (the review swarms, through the pinned Pi agent). …" — **Why stale or wrong**: as an addition rather than a falsified sentence — the phase-1 route for `feature` and `architectural` changes is the research swarm (ADR 0020, frontmatter `status: accepted`; `docs/WORKFLOW.md:1009-1010` routing table; `model-endpoints.yaml` `research_swarm:` block), and the README describes it nowhere; a reader learns phase 1 has one explorer. "Exploring small changes" matches the `glm-coding-plan` note ("since ADR 0020 only for a `bounded` or `spike` change", `model-endpoints.yaml`, `glm-coding-plan.bemerkung`) but leaves the other half of phase 1 undocumented. **Proposed text**:

> - **The runner's routes to other vendors** need your own accounts, set up on
>   your machine: OpenAI Codex (drafts, repairs, final review), GLM through
>   Z.ai (implementing; exploring a `bounded` change or a `spike`), and
>   OpenCode Go (the review swarms, and part of the research swarm, through
>   the pinned Pi agent). A `feature` or `architectural` change is explored
>   by a *research swarm*: several models in declared seats
>   ([`model-endpoints.yaml`](model-endpoints.yaml), `research_swarm`),
>   reconciled by one fresh context, before you are asked anything. For
>   `explore`, `implement` and `repair`, `--stage2-off [REASON]` runs the
>   verb on Anthropic models instead and records why; the other runner verbs
>   have no such route.

**Linked files that must change with it**: none (docs/how-it-works.md "Research swarm" section already documents it correctly).

**Where** `README.md:19-20` — **Today**: "Claude Code is the only fully supported orchestrating agent today." — **Why possibly stale (low stakes, wording)**: the doctrine itself names a second orchestrating conversation in running text — "the main Claude Code or Codex conversation" reports the availability preparation (`docs/WORKFLOW.md:1220` and `:1563`), and `AGENTS.md:37` says the same. "Fully supported" hedges this, so the sentence is defensible; it is listed so the maintainer can decide whether to acknowledge the Codex conversation. **Proposed text** (optional):

> Claude Code is the orchestrating agent this repository documents end to
> end; runner availability reports may land in a Codex conversation instead.

**Linked files that must change with it**: none.

**Checked and current — no change proposed** (each verified on 2026-11-17): the getting-started block — `tools/beads/install.sh`, `tools/bd`, `make venv` (`Makefile:42`), `bash tools/pi/install.sh`, `make verify` (`Makefile:18`), `make change NAME=<name> BEAD=<id>` (`Makefile:62-65`, NAME and BEAD required on the command line), `/workflow-start` (`.claude/commands/workflow-start.md` exists, its content not read); the post-run-check bullets (`README.md:150-165` match ADR 0025 as amended and `docs/WORKFLOW.md:1026-1028`, `:1346-1348`); the class paragraph including "Nothing checks yet that the class itself is right" (`README.md:132-137` vs `docs/WORKFLOW.md:995-998`, which states it verbatim); the "Not built yet" list (`README.md:258-266` — accurate: no `scripts/validate*.py`, no `.claude/hooks/**` in the tree; the validator is a class of check, the stop hook `.claude/hooks/session-stop/check-tests-green.sh` both named missing in `docs/WORKFLOW.md:36-38`); the stage-1 citation (`README.md:211` → `docs/WORKFLOW.md:520`, "§3 · Stage 1 — only Claude Code, only Anthropic"); all Learn-more links and anchors (`#runner-details` resolves — `docs/how-it-works.md:133`, "### Runner details"); the four diagram PNGs and the banner under `docs/assets/`; the license section against `COMMERCIAL.md` (PolyForm Noncommercial 1.0.0, Apache grant for pre-2026-10-20 releases, contact via `https://github.com/MPAdesso`); `README.md` as human-written (`provenance.yaml:286-288`, `prefix: "README.md"`, `allowed: [human-written]`).

## AGENTS.md

No change proposed. Read in full as the reference the README summarises. One observation for the record, so future README edits do not inherit it: the phase table's gate column names "validator green" (phases 2, 2b, 3 — `AGENTS.md` workflow table) and "stop-hook blocks on a red tree" (phase 5) as if built, while `docs/WORKFLOW.md:36-38` lists both pieces as not in the tree and my tree checks on 2026-11-17 agree. The doctrine carries a banner for exactly this ("Where the text below says one of the missing pieces does something, it describes the target, not this tree", `docs/WORKFLOW.md:42-44`); `AGENTS.md` carries no such note. Whether it needs one is the maintainer's call — outside this change's file list.

## docs/how-it-works.md

**Where** `docs/how-it-works.md:150-156` ("Runner details", the fail-fast bullet) — **Today**: "An implement attempt then runs the full `make verify`." — **Why stale or wrong**: ADR 0025's amendment of 2026-11-12 ("Implement and draft amendment — the targeted check covers more verbs, 2026-11-12", decision 1: "Implement takes the targeted check of decision 1 on every route, with the full fallback of decision 2") and the doctrine both state the targeted check for implement, with the full run only as fallback (`docs/WORKFLOW.md:1026-1028`: "the post-run check (the targeted check, or the admitted full `make verify` as its fallback)"; `:1346-1348`). The page's own rule gives the doctrine precedence ("Where this page and the doctrine disagree, the doctrine holds", `docs/how-it-works.md:17-19`). The repair and draft parts of the same bullet are correct. **Proposed text** (replacing the bullet's second and third sentences):

> The post-run check is targeted: the touched and linked test files and the
> gates their file kinds need — for implement and repair alike (ADR 0025, as
> amended 2026-11-12). The full `make verify` runs instead when that
> selection cannot cover the attempt safely, and always before the final
> review. A draft runs only its document gates, outside the machine-wide
> verify lock.

**Linked files that must change with it**: `docs/testing.md:62` (same claim in the `make verify` row, see below). The README needs nothing — `README.md:151-158` already states the current rule.

**Where** `docs/how-it-works.md:198-201` (after the verb flowchart) — **Today**: "The post-run check is the document gates for a draft, the full `make verify` for an implement attempt, and the targeted check or its full fallback for a repair." — **Why stale or wrong**: same evidence; the middle clause is the pre-amendment state. **Proposed text**:

> The post-run check is the document gates for a draft, and for implement and
> repair the targeted check — the touched and linked tests and the gates
> their file kinds need — with the full `make verify` as the fallback when
> that selection cannot cover the attempt safely; one fresh full
> `make verify` precedes the final review (ADR 0025).

**Linked files that must change with it**: `docs/testing.md:62`.

## docs/orchestration.md

**Where** `docs/orchestration.md:29` ("What a lane is", first bullet) — **Today**: "Each item is one bead, one branch and one worktree ([Working in parallel](../README.md#working-in-parallel))." — **Why stale or wrong**: the link target is a dead anchor. README's headings (read in full, 2026-11-17) are: *What it checks*, *How a change runs*, *Getting started*, *Current status and limits*, *Learn more*, *Contributing*, *License*; no section named "Working in parallel" exists, so `../README.md#working-in-parallel` resolves to the page top. **Proposed text**:

> Each item is one bead, one branch and one worktree ([Working rules,
> followed by the agent](../README.md#working-rules-followed-by-the-agent)).

(The alternative — restoring a "Working in parallel" section to the README — is the maintainer's call; the link fix is the smaller change.) **Linked files that must change with it**: none.

Otherwise current: `python3 scripts/machine_facts.py` exists (`scripts/machine_facts.py`, glob 2026-11-17), `make report CHANGE=<name>` exists (`Makefile:75-76`, backed by `scripts/run_report.py`), and the enforced/kept-by-hand table matches `decisions/gates.yaml` and `scripts/verify_lock.py`-backed admission as described (`docs/how-it-works.md:162-166`).

## docs/testing.md

**Where** `docs/testing.md:61` ("Where tests run" table, Stop-hook row) — **Today**: "| Stop hook | at the end of an agent's turn, only when Python changed since `HEAD` | comfort: an agent does not hand back a red tree. It is not the enforcement. |" — **Why stale or wrong**: the row reads as a running mechanism; the tree has no `.claude/hooks/` at all (glob 2026-11-17: no match), and the doctrine's header note names the stop hook `.claude/hooks/session-stop/check-tests-green.sh` as not in the repository (`docs/WORKFLOW.md:36-38`, checked there on 2026-11-01 at `8ae99e50`; still missing on 2026-11-17 here). README states the same truth correctly in its "Not built yet" list. **Proposed text** (marker added, row otherwise unchanged):

> | Stop hook *(described, not built)* | would run at the end of an agent's turn, only when Python changed since `HEAD` | comfort: an agent does not hand back a red tree. It is not the enforcement — and it is not in this tree yet (`docs/WORKFLOW.md`, header note). |

**Linked files that must change with it**: none.

**Where** `docs/testing.md:62` (same table, `make verify` row, "When" cell) — **Today**: "… inside every implement attempt after the attempt's cheap checks (ruff, its own tests) are green, inside a repair attempt when its targeted check cannot cover the repair safely, and before the final review" — **Why stale or wrong**: "inside every implement attempt" is the pre-ADR-0025-amendment state; since 2026-11-12 an implement attempt runs the targeted check, and the full suite only when the selection cannot cover it safely (ADR 0025 amendment, decision 1 and 2; `docs/WORKFLOW.md:1026-1028`). **Proposed text**:

> … inside an implement or repair attempt when its targeted check cannot
> cover the attempt safely (both run the targeted check first — ADR 0025 as
> amended), and before the final review …

**Linked files that must change with it**: `docs/how-it-works.md:150-156` and `:198-201` (the same drift, proposed above).

## docs/WORKFLOW.md

No change proposed. Read where the README summarises or cites it: the header note (`docs/WORKFLOW.md:30-53`, the missing-pieces list), the phase table (`:80-92`), §3's heading (`:520`, matching the README's stage-1 citation), §4's routing table (`:1007-1019`, matching README's model claims, with Codex as `gpt-6.1-terra` also in `model-endpoints.yaml:161-163`), the class-refusal paragraph (`:985-998`) and the post-run-check paragraphs (`:1024-1040`, `:1346-1348`). Its frontmatter says `updated: 2026-11-15` — the freshest document in the set, and the reference the other pages lag. The parts beyond these sections (roughly 2,200 of its lines) are not read; see Not checked.

## tools/claude-code/README.md

No change proposed. Read in full; it matches what the README claims about it (`README.md:290-292`): the status line, the session entry (`hooks/handover.sh start`), the parallel-session warning (`hooks/parallel-sessions.sh`), the handover safety net (`hooks/recap.sh`), and the night profile — display and reminders, no gate, which agrees with `docs/testing.md:61`'s framing for hooks and with the file's own text. Its claim that `hooks/beads-start.sh` is the repository's own SessionStart hook, not part of the user-level install, is consistent with the install list ("the eight files", `tools/claude-code/README.md:87` — count not verified against the directory; see Not checked).

## model-endpoints.yaml

No change proposed. Read in full against the spots where the README names models, routes or terms: `openai-codex` with model `gpt-6.1-terra` (replaced `gpt-6.1-sol` on 2026-11-15, per the file's own comment at the `modelle:` list), `glm-coding-plan` (`glm-5.3-flash` explores a `bounded`/`spike` change and implements; no review phase routes to it since ADR 0011), `opencode-go` (review loop, the `session` verb, and the research swarm's Go seats), the data classes (`datenklassen:` block) behind the README's allowlist sentence, and the subscription `modelle_terms` (`valid_until`) behind "A paid model whose terms reading has expired gets no calls" (`README.md:239-240`). One dated remark for the maintainer's awareness, not a README finding: the `public-web` class and the `research_swarm:` block still carry "vorgeschlagen bis zum Merge" comments (`model-endpoints.yaml:38-39` and `:676`) while ADR 0020's frontmatter reads `status: accepted` — the comment in the YAML may be ready to drop; that edit belongs to a change of its own, not to this README pass.

## COMMERCIAL.md

No change proposed. Read in full; the README's license section (`README.md:311-318`) and contribution paragraph (`README.md:305-309`) match it: PolyForm Noncommercial License 1.0.0, the Apache-2.0 grant remaining for releases published before 2026-10-20 (stated identically in both files), contact via `https://github.com/MPAdesso`, and the three-point contributor agreement, whose substance ("may be distributed under the project's license and, if needed, under a commercial license") the README states as an agreement by opening a pull request while `COMMERCIAL.md` requires it before merge — the same rule at the same boundary, worded for different readers.

## Not checked

- The exact commit identity of this worktree's HEAD and per-file equality with `dfede341`: no `git` command was available to this phase. Per the session's start state, the branch carries edits only under `plans/changes/readme-proposals/`, so the checked files should equal the merged `origin/main` content — stated, not proven.
- "The first commit is from 2026-09-16" (`README.md:22-23`): consistent with `docs/journal/handover/2026-09-16-coding-harness-bootstrap.md` existing (glob 2026-11-17), not proven from git history.
- The commit hashes `ac11da5d` and `b424be3a` in `README.md:225-226`: hashes not resolvable without git.
- The live merge state of ADR 0025's 2026-11-12 amendment (its text says it takes effect on merge of its own decision pull request; `docs/WORKFLOW.md`, updated 2026-11-15, already carries the amended rule, which is why this research treats it as in force).
- Whether `/workflow-start` accepts `--bead <id>` in exactly the form `README.md:190-192` shows: `.claude/commands/workflow-start.md` found, not read.
- The "eight files" install count in `tools/claude-code/README.md:87`: not counted against the directory listing.
- `docs/WORKFLOW.md` beyond the sections the README summarises or cites (roughly lines 105-519, 521-907, 1029-1219, 1221-1562, 1564-2141 and the sections after 2200): not read.
- That every gate in `decisions/gates.yaml` has its mutation test or listed reason (`README.md:232-234`): `docs/governance/gate-catalog.md` and the mutation-evidence list behind `scripts/mutation_evidence.py` (file exists, glob 2026-11-17) not read.
- Which free models the `free_stage` rule would select today, and which Go models are reachable: runtime questions, out of scope for a document pass.
