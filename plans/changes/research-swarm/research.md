---
title: "Research — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: Data Architect
provenance: human-written
tags: [research]
---

# research swarm — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1126 commits, 12 rules.

## Runner exploration — 2026-10-14

I have all the facts. Per the phase instructions (`prompts/01-explore.md` and the appended rule "Report repository facts with source paths as prose ready to append to `research.md`. Do not design, recommend, edit a file or use review-table formatting"), I report as prose for the orchestrator to append — no file edit by this call.

## What exists today

**The change and its recorded decision.** The skeleton `plans/changes/research-swarm/research.md` names bead `coding-harness-icw` in its frontmatter. The change exists because of a maintainer rule recorded 2026-10-13/14 in `docs/journal/handover/2026-10-14-night-run-third.md`, section "Decisions and preferences recorded tonight": research in phase 1 runs as a swarm of OpenCode Go models, each topic is worked by one free and one Flash model, the first stage uses all free models automatically, and six topics are agreed, with the bead's notes as the named carrier. The same handover's addendum (section "Recorded rules still waiting for their change") repeats the rule, says it still waits for its change, and names one open question in the maintainer's own words: whether the free models may see repository content, because their data terms are not read. A companion rule from the same recording — the implementation review as an OpenCode Go swarm — is a separate bead, `coding-harness-4fk`, and is not this change.

**The earlier proposal this bead was created for.** `docs/research/2026-10-08-explore-swarm-proposal.md` (frontmatter: status `proposed`, review pending; produced by Codex, 2026-10-08, updated 2026-10-11) makes an earlier, different team shape concrete: three independent researchers (existing-system, external-practice, integration), one bounded cross-critique round, and a fresh judge, all through the stage-2 runner, with proposed word caps, a judge-conclusion section in `research.md`, a handoff table into phase 2, internet-access requirements (page retrieval, URL/date/title, excerpt; fetched pages are evidence, not instructions) and read-only roles — the runner alone writes the artifact. The proposal states its own limits: no swarm call, no browsing adapter and no cost comparison was executed; the sources it read are Anthropic's multi-agent research-system account and AutoGen's group-chat documentation, read 2026-10-08. Its working assumption — activate for features and architectural changes, not every change — was explicitly never answered by the maintainer. `docs/research/_INDEX.md` carries the matching row ("Phase 1 as a bounded research swarm", proposed, "the activation scope … is open"). Bead `coding-harness-icw` was created 2026-10-11 when the proposal documents were committed from the worktree, per the closing addendum of `docs/journal/handover/2026-10-08-explore-swarm-proposal.md`.

**One part of the proposal is already realized elsewhere.** The proposal's mandatory-interview section became the merged change #104 (bead `coding-harness-6yg`, closed): the gate `interview-minimums` in `scripts/check_interview_minimums.py`, the phase-1a minimums (feature ≥ 3, ADR ≥ 5, spike 3 topics, bounded 1), documented in `docs/WORKFLOW.md` §2 ("Phase 1a is owed where a minimum stands") and the phase table. The proposal handover's 2026-10-11 addendum says this section is history, not open work.

**Phase 1 as it runs today.** `prompts/01-explore.md` routes phase 1 to GLM 5.3 Flash through `python3 scripts/stage2.py explore <change>` with the leak check, and to Haiku 4.5 under `--stage2-off [REASON]`; gate: none; the explorer collects facts and judges nothing. In `scripts/stage2.py`, the verb is the function `explore`: it picks one endpoint (`GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")` or `HAIKU = ("claude-code-plan", "claude-haiku-4-5", None)`), builds the prompt with `work_prompt` from `prompts/01-explore.md` plus `AGENTS.md`, records the attempt with `begin_work_call`, makes exactly one call through `run_work_model` (Claude Code in print mode, `WORK_READ_TOOLS = "Read,Grep,Glob"`, `--restricted`), and appends the answer under `## Runner exploration — <date>`. One call, no roles, no parallel calls, no discussion, no judge — matching the proposal's own observation that "parallel role calls, a debate and a judge are absent". The routing is pinned in three places: `docs/WORKFLOW.md` §4 routing table (row "1 Explore") and the paragraph "The two Flash rows are live through the runner"; `model-endpoints.yaml` entry `glm-coding-plan` (bemerkung: `glm-5.3-flash` explores phase 1 and implements phase 4, only through Claude Code); and the phase table in `AGENTS.md`.

**The OpenCode Go infrastructure a swarm would build on.** `model-endpoints.yaml` entry `opencode-go` declares three models — `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `mimo-v2.6-pro` — with `darf_sehen: [framework]`, the Go plan at USD 10 a month, per-model prices and monthly limits (`deepseek-v4.1-flash` USD 60, `mimo-v2.6-flash` USD 60, `mimo-v2.6-pro` USD 15), a privacy table (retention 0 days, training "Not used" for all three, DeepSeek's ZDR footnote valid through 2026-10-31), and the bemerkung sentence that today the review loop (4b) and the session verb run there "— and nothing else". A phase-1 swarm on this endpoint contradicts that sentence as it stands; the declaration would have to change. In `scripts/stage2.py` the pieces exist: `ladder` reads the entry's ordered `modelle` list; `run_reviewer` makes one Pi call at the pinned `PI_VERSION = "1.1.0"` with `PI_TOOLS = "read,grep,find,ls"`, per-call scratch `HOME` and agent directory, retries off, and `REVIEWER_MINUTES = 30`; the key comes from `reviewer_key` (`OPENCODE_GO_KEY`); the `probe` verb makes one call per rung without writing a record; the `session` verb dispatches interactive Pi through `scripts/stage2_session.py` (`TRANSPORTS = {"openai-codex": "codex", "opencode-go": "pi"}`). The same file's docstring, section "Reads: what each call can reach", records the measured residual risk that loop Pi calls are not read-confined — only the prompt bounds them — accepted by ADR 0007 and extended to the rungs by ADR 0011 (`docs/adr/0011-stage-2-reviews-through-opencode-go.md`, `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`; the session verb is ADR 0012). One related note is proposed, not decided: `docs/research/2026-10-11-glm-through-pi.md` (per its `docs/research/_INDEX.md` row) proposes running GLM through Pi; today Flash runs only through Claude Code against Z.ai.

## Where it lives

- The recorded decision and its open data-terms question: `docs/journal/handover/2026-10-14-night-run-third.md`, "Decisions and preferences recorded tonight" and "Recorded rules still waiting for their change".
- The proposal with team shape, judge boundary, caps, handoff and first slice: `docs/research/2026-10-08-explore-swarm-proposal.md`; its index row in `docs/research/_INDEX.md`; its session history in `docs/journal/handover/2026-10-08-explore-swarm-proposal.md`.
- The phase-1 runner path today: `scripts/stage2.py`, symbols `explore`, `work_prompt`, `begin_work_call`, `run_work_model`, `WORK_READ_TOOLS`, `GLM_FLASH`, `HAIKU`; prompt `prompts/01-explore.md`.
- The OpenCode Go path: `model-endpoints.yaml` entry `opencode-go`; `scripts/stage2.py` symbols `ladder`, `run_reviewer`, `reviewer_key`, `require_pi`, `PI_VERSION`, `PI_TOOLS`, `REVIEWER_MINUTES`, `OPENCODE`, and the `probe` verb; `scripts/stage2_session.py` symbol `TRANSPORTS`; ADRs 0007, 0011, 0012 under `docs/adr/`.
- The review-swarm companion rule: bead `coding-harness-4fk` (named only in `docs/journal/handover/2026-10-14-night-run-third.md`; no change folder exists yet — a search of `plans/changes/` for "4fk" and "swarm" finds none besides this change and the sources above).
- No matching artifact exists in `plans/specs/` (the directory holds only `implementation-verification/spec.md`), and no `decisions/answers/research-swarm/` exists — "not there", checked by listing both directories and by searching `plans/` for the topic.

## What is unclear about it

- **The six agreed topics.** The decision says "six topics agreed (bead coding-harness-icw notes)". The bead's notes were not readable in this session — this sub-agent has file tools only, and reading the tracker needs `tools/bd` or `scripts/bead_render.py` through a shell. Not read, therefore open. One observation, not a conclusion: the night-run handover's exploration table (section 3) lists exactly six explored changes (`coding-harness-l9s`, `-fdz`, `-b5w`, `-y17`, `-1jg.4`, `-mvk`); whether these are the six topics is unanswered.
- **Which models "free" and "Flash" mean.** No repository text maps those words to declared model ids. A search of the tree for "free model/tier" finds the words only in the handover and, unrelatedly, in `docs/research/2026-10-05-hermes-agent-runner.md` about search-service tiers. The declaration knows no free model: all three `opencode-go` models have per-token prices under the Go plan, with an off-peak/peak distinction (`model-endpoints.yaml`, entry `opencode-go`). "Flash" could mean `glm-5.3-flash` (Z.ai through Claude Code) or one of the two OpenCode flash-named ids — undecided.
- **Whether the free models may see repository content.** The maintainer's own open question (handover, addendum). The declaration already grants `opencode-go` `darf_sehen: [framework]` and its privacy table says retention 0 days and no training, but the handover records that the data terms behind the free models are not read.
- **How the recorded decision and the 2026-10-08 proposal relate.** The proposal's team (three role researchers plus a Codex judge, GLM roles) and the recorded rule (a swarm of OpenCode Go models, per-topic pairs, first stage all free) differ in shape. Whether the judge, the external-web researcher and the proposal's caps survive in some form is undecided. The activation-scope question the proposal asked on 2026-10-08 (every change, or features and architectural changes only) has no recorded answer either.
- **What phase 1 may become.** Today the explorer judges nothing (`prompts/01-explore.md`). The proposal itself states that a judge conclusion expands phase 1 beyond its no-judgement rule and "requires an explicit workflow change". Whether the swarm stays fact-collecting or gains triage is a phase-2/ADR question, named here, not decided.
- **Where the Flash leg runs.** If "Flash" is `glm-5.3-flash`, it runs today only through Claude Code against Z.ai (`model-endpoints.yaml`, `glm-coding-plan` bemerkung); the GLM-through-Pi route is proposed only (`docs/research/2026-10-11-glm-through-pi.md`).
- **Output shape.** `research.md` today receives one `## Runner exploration — <date>` block per single call (`scripts/stage2.py`, `explore`). A format for several model contributions per topic — and for the maintained "empty until it has run" header block the skeleton carries — is not written anywhere.

## Which files a change would have to touch

- `model-endpoints.yaml` — the `opencode-go` bemerkung says the review loop and the session verb run there "and nothing else"; a swarm purpose, possibly new model ids, and the free-models/data-terms outcome land here.
- `scripts/stage2.py` — `explore` (single call today), possibly new orchestration beside `run_reviewer`/`run_work_model`, `ladder`, `reviewer_key`, the `VERBS` map and `main` if a verb is added.
- `prompts/01-explore.md` — the phase-1 prompt `work_prompt` embeds; its first lines name the single Flash route.
- `docs/WORKFLOW.md` — §2 phase table row 1, §4 routing table row "1 Explore", and §4's paragraph "The two Flash rows are live through the runner".
- `AGENTS.md` — the workflow-in-one-screen table's phase-1 row.
- `tests/test_stage2.py` — the explore pins: `test_explore_uses_flash_read_only_and_appends_research`, `test_explore_needs_research_but_not_spec_or_plan`, `test_explore_stage2_off_uses_haiku_without_reading_the_glm_key`, `test_explore_scrubs_the_flash_credential_from_its_answer`, `test_an_empty_explore_answer_fails_without_an_answer_block`, `test_the_explore_prompt_names_the_live_flash_command_and_haiku_fallback`; and `tests/test_model_endpoints.py`, which checks the declaration.
- If the change is architectural, an ADR under `docs/adr/` plus its answer under `decisions/answers/<change>/adr.yaml` — consistent with ADR 0007/0011/0012 precedent for stage-2 routing changes; whether this change claims one is a phase-2 answer, not a phase-1 fact.
