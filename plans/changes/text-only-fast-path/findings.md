---
title: "Findings — text-only-fast-path"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-is4h
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — text-only-fast-path

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5161 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1153 files, 5162 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | spec.md AC7 | [AMBIGUITY] AC7 asks for "conditions within" the required verify job. The required check is the context `verify` (tests/test_repo_settings.py:405), and in ci.yml that is the aggregator job `verify` (ci.yml:156-164). That job only tests `needs.gates.result`. pytest and leerprobe are steps of a different job, `gates` (ci.yml:79-94). Reading A: "verify job" means gates.yaml's `job: verify`, which is the ci.yml `gates` job, so an `if:` on the pytest and leerprobe steps satisfies AC7. Reading B: it means the ci.yml job named `verify`, the one that is actually required. Then no condition on the existing steps meets AC7 as written. The note would have to propose moving steps into the aggregator, or every candidate is refuted. | Opus | open | — |
| F-2 | MAJOR | SPEC | base | spec.md Terms, "no Markdown file read by a test"; AC4 | [AMBIGUITY] It is unclear whether "read by a test" covers files that a test reaches through a glob over the live tree. Reading A: only files a test opens by their own path, such as AGENTS.md. Most plans/ and docs/ PRs then stay eligible. Reading B: also every file matched by a live-tree glob, for example `PLANS.glob("*/research.md")` (tests/test_explore_provenance.py:23), `.claude/agents/*.md` (tests/test_regelwerk.py:282) and `prompts/*.md`, plus files read by a script that a test runs against the real tree. Under B, every PR that adds or edits a change's research.md is ineligible, so most change PRs drop out of the AC4 total. The two readings give very different eligible sets and totals. | Opus | open | — |
| F-3 | MINOR | SPEC | base | spec.md Terms; AC2; AC4 | [AMBIGUITY] Eligibility depends on which Markdown files tests read, but the spec does not say at which revision. Reading A: the tests at today's head, using the AC2 inventory, for every PR since 2026-11-01. Reading B: the tests at each PR's base commit. A file read only by a test added later, or no longer read today, changes a PR's eligibility. AC4's "an ineligible one is counted" cannot be judged until this is fixed. | Opus | open | — |
| F-4 | MAJOR | SPEC | base | spec.md Terms "CI minutes"; AC4 | The spec does not say which runs count toward an eligible PR's CI minutes, so the person doing the work would have to decide. Candidates: pull_request runs only; also merge_group runs (ci.yml:10-11); also the push-to-main run after the merge (ci.yml:7-8); superseded runs cancelled by `cancel-in-progress` (ci.yml:18); reruns. Another open case: runs on intermediate heads whose diff contained non-Markdown paths, in a PR whose final net diff is text-only. At job scope it is also open whether the `verify` aggregator job counts. Each choice gives a different total. AC4's refutation only checks that PRs are included and that the total can be traced, so every one of these choices passes. | Opus | open | — |
| F-5 | MAJOR | SPEC | base | spec.md AC1-AC4, AC6, AC7 | These criteria cannot go red when content is missing. Each one is triggered by the note doing the thing ("When the note inventories…", "When the note measures…", "When the note presents a recommendation…"). AC5 is triggered by unavailable data and AC8 by the budget expiring; neither requires content. Refuting input: a note finished within two hours, with CI data accessible, that has no gate inventory, no list of test reads, no measurement and no recommendation. No trigger fires, so all eight criteria stay green. Only the Definition of Done prose asks for the content. | Opus | open | — |
| F-6 | MINOR | SPEC | base | spec.md AC2, Refuted-by | [AMBIGUITY] "A discovered test read is omitted": discovered by whom? Reading A: by the note's own search. A read the search never found is then not "discovered", so an incomplete search cannot refute AC2, and the AC4 eligibility built on it cannot be challenged. Reading B: discovered by anyone, including the reviewer. Then any live-tree read missing from the note refutes AC2. | Opus | open | — |
| F-7 | MINOR | SPEC | base | spec.md AC3 | AC3 cannot go red when the list of faults is incomplete. Refuting input that does not refute: the note names one fault for each candidate, with evidence (for example, a new unclassified .md that the kit probe catches), and leaves out other documentation faults pytest catches, such as tests over `.claude/agents/*.md` or `prompts/*.md`. The refutation only covers an omitted candidate or an unsupported claim, so the note passes while understating what skipping would miss. | Opus | open | — |
| F-8 | MINOR | SPEC | base | spec.md AC7 | [AMBIGUITY] "Process gate" is not defined, and AC7's Refuted-by line only covers "another process gate or tracker hydration". Reading A: every gate except pytest and leerprobe is a process gate, so a candidate that also skips ruff-check, ruff-format, markdownlint or lychee is refuted. Reading B: only the plans and decision gates are process gates, so such a candidate passes the refutation even though the criterion text limits skipping to pytest and the kit probe. Neither reading says whether skipping the setup steps that are not gates (setup-node and setup-pi, ci.yml:40-47) is allowed. | Opus | open | — |
| F-9 | MINOR | SPEC | base | spec.md line 24; AC1-AC8 "the research note"; DoD | [AMBIGUITY] The spec never names the file the deliverable goes in. Line 24 labels `research.md` as "Research", and the criteria then say "the research note". Reading A: append to plans/changes/text-only-fast-path/research.md. Reading B: a new file `docs/research/2026-11-2x-text-only-fast-path.md`, as decisions.md specifies, with the date left open. Reading B brings that file's own frontmatter and research-currency obligations. Phase 6 checks "the research note" against the spec, which allows either. | Opus | open | — |
| F-10 | MINOR | SPEC | base | spec.md DoD, bullet 2 | [AMBIGUITY] The Definition of Done says "local `make verify` is skipped". The runner's record at plan.md:61 says "a fresh full `make verify` is still required before phase 6", and research.md:48 leaves this exact scope question open. Reading A: no full `make verify` runs for this change. Reading B: only a hand-run by the author is skipped, and the runner's full check before phase 6 still runs. The spec does not say which. | Opus | open | — |
| F-11 | MINOR | SPEC | base | spec.md AC1 | [AMBIGUITY] It is unclear what counts as reading Markdown content. Reading A: only gates that open and parse a Markdown file's bytes are classified "reads". Reading B: any gate whose result depends on a Markdown file's path, presence or git history is classified "reads", for example the kit probe's classification of every tracked file (gates.yaml:118). Under A, AC1 can list the kit probe as not reading Markdown while AC3 credits it with catching a documentation fault. The inventory then contradicts itself, and AC1 cannot be refuted on that point. | Opus | open | — |
