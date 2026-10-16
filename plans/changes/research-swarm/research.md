---
title: "Research — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
neighbours: [plans/changes/interview-context/spec.md, plans/changes/haiku-5-5/spec.md]
---

# research swarm — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
runner preserved the GLM exploration below; Codex added the dated repository
evidence at the end while drafting, without changing that report's wording.

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

## Supplementary repository evidence — 2026-10-14

Read within this worktree at `1e29f6e384a3942c1003b8449465bbe830ddd355`; the
earlier exploration above is retained as evidence of what was known then.

- **Interview closes the original intent gaps.** The five answered records
  supply the free/Flash ids, six topics, public-only free-model boundary,
  activation for feature/architectural work and Opus 5.5 as judge. Q-3
  explicitly leaves replacement of repository-bound free seats to the spec.
  These answers supersede the corresponding "unclear" observations in the
  earlier report (`decisions.md`, Q-1 to Q-5).
- **The architectural class owes no ADR-question answer file.** Only a
  `feature` owes that answer; an `architectural` change carries its ADR
  already. The earlier last bullet's suggestion that every architectural
  change also needs an answer file is incorrect (`docs/WORKFLOW.md`, "Change
  classes, the ADR question and decision pull requests").
- **Early class input is absent.** `explore` preflights `research.md`, not
  `spec.md`, and does not read a class. `main` exposes no `--class` argument;
  `--model` and `--handover` belong to `session`. The doctrine explains that
  current explore routing is not class-dependent because the spec comes
  later (`scripts/stage2.py`, `explore`, `preflight`, `main`;
  `docs/WORKFLOW.md`, "Which change gets what").
- **Public authorization needs a separate data class.** `declaration_problem`
  checks `framework` and declared residency on every current call. The
  endpoint tests recognize billing only as `token` or `abonnement`, require
  nonempty permission/model lists, and accept permissions only from declared
  data classes. No public-only endpoint or free-model id is currently
  declared (`scripts/stage2.py`, `declaration_problem`;
  `tests/test_model_endpoints.py`, `ABRECHNUNGEN`,
  `test_every_endpoint_states_operator_residency_and_billing`,
  `test_only_a_declared_data_class_may_be_seen`; `model-endpoints.yaml`).
- **Existing launch helpers provide some, not all, boundaries.**
  `run_reviewer` uses a fresh home/config, disables discovery and retries,
  but launches from the repository with `read,grep,find,ls` tools. The
  runner's own documentation says those reads are unconfined. Its tools
  contain no public search/fetch facility (`scripts/stage2.py`,
  `run_reviewer`, `PI_TOOLS`, "Reads").
- **Routing group labels require actual resolution.** The model-line
  readers inspect root phase prompts and bold routing-table cells; only
  `the ladder` currently has a declared-group exception. A new swarm label
  cannot be silently skipped (`tests/test_model_endpoints.py`,
  `prompt_modelle`, `routing_models`,
  `test_every_model_in_the_routing_table_resolves`).
- **The new runtime helpers remain local under current kit classification.**
  No specific `stage2.py` rule exists in the kit manifest, so the `scripts/`
  and `tests/` stock catch-alls apply to its new helpers/tests too; the
  `prompts/` prefix already covers subdirectories. No classification change
  is needed for this scope (`scripts/kit/manifest.yaml`).
- [GAP] **Free transport and live web support are not qualified.** Q-1
  records model ids seen in Pi, but no source read in this worktree maps
  them to a Pi provider or service address. No public search/fetch adapter
  exists here. Actual availability, the pinned runtime's tool/event contract
  and page retrieval must be measured before claiming live support; this
  drafting call made no external reads or live probes.
- [GAP] **The named change-artifact validator is not present.** The file
  `scripts/validate_change_artefacts.py` is absent, as the workflow still
  anticipates its future delivery. `templates/` contains spec/design/ADR
  forms but no plan template; phase 3's prompt defines that file's shape
  (`docs/WORKFLOW.md`, "Change classes"; `prompts/03-plan.md`;
  worktree file inventory). Existing interview and criterion-ledger gates
  can be measured; the runner owns the derived index and full verification.


## Redraft repository evidence — 2026-10-15

Read inside this worktree at `6e80ded42785cc3a53ebb1c3f0a7f557fcd8d6e9`
(branch `explore/research-swarm`). This adds current facts without rewriting
historical exploration or claiming that the amended swarm has run.

- **The interview now amends the original shape.** Q-7 records the locator
  trio/Opus merge, eight repository topics and three online topics, identical
  initial perspectives, report template, claim-based scoring, neighbour
  headers, research/interview/spec links and concurrent provider queues.
  Q-8 records the maintainer's Pi free-tier 403 observation and selects Go
  through Pi instead; Q-9 fixes the online trio as DeepSeek, MiMo and Qwen
  Flash. These supersede the old free roster and six-topic pairing; the
  drafting call performed no external read or provider probe (`decisions.md`,
  Q-7–Q-9, including the dated addenda and complete topic walk-through).
- **The implemented earlier slice has six pairs and differing angles.**
  `TOPICS` contains 1–6; `ANGLES`, `repository_prompt`, `topic_pairs` and
  `run` dispatch the former pair assignments, with sequential loops and
  buffered Flash output. `swarm_problems`/`swarm_roles` validate the fixed
  free roster and focuses; `free_transport` inventories Pi providers. There
  is no finder stage, eight-topic trio or provider queue in the read source
  (`scripts/stage2_swarm.py`, named symbols). Existing citation, deadline,
  partial-output and public-tools corrections are retained rather than
  evidence that the new graph already works.
- **The declaration still reflects the earlier slice.** It has
  `opencode-free`, `free_roster`, `free_focuses`, `topic6_free`, `flash_pair`
  and paid author/judge fields, with no Qwen research role. The Go `modelle`
  list is also the review ladder, so adding a research model there would
  change review ordering/membership (`model-endpoints.yaml`, `research_swarm`
  and `opencode-go`; `scripts/stage2.py`, `ladder`).
- **The current fallback already selects Haiku 5.5.** `HAIKU` is
  `claude-haiku-5-5`; restoring the older spec's 4.5 wording would contradict
  the read neighbouring version-change spec (`scripts/stage2.py`, `HAIKU`;
  `plans/changes/haiku-5-5/spec.md`, criteria 1–3).
- **Research obligations are not currently checked.** The interview prompt
  counts minimum answers and preserves context, but has no research item/claim
  link fields. The spec prompt has no criterion-basis or neighbour-header
  rule. Existing `interview-minimums`, `question-context` and
  `criterion-ledger` checks have different contracts; none of the entries in
  the read gate list checks research decision coverage (`prompts/01a-interview.md`,
  `prompts/02-spec.md`, `decisions/gates.yaml`; headers/docstrings of
  `scripts/check_interview_minimums.py` and `scripts/check_criterion_ledger.py`).
- **Two neighbours were read for this redraft.** The context-form change
  requires truthful retained context and keeps minimum counts unchanged;
  the Haiku version change fixes the fallback at 5.5. The new trace links
  must coexist with those contracts, without backfilling old answers or
  changing their meaning (`plans/changes/interview-context/spec.md`,
  criteria 4, 8 and 10; `plans/changes/haiku-5-5/spec.md`, criteria 1–3).
  Other named worktree changes from the night handover (central models,
  loop-until-clean, isolated attempts) have no spec at the queried paths in
  this worktree; their other worktrees and current PR states were not read.
- **A new gate needs kit and generated-CI integration.** The one gate list
  generates CI, while existing checker/tests travel by explicit mechanism
  entries; the catch-all for runtime scripts alone is not sufficient for a
  newly travelling gate (`decisions/gates.yaml`, schema commentary;
  `scripts/kit/manifest.yaml`, entries for the existing interview/context/
  ledger checkers; `tests/test_ci.py`, gate ratchets).
- **An earlier pre-merge blocker remains.** F-1 is the attended offline
  real-Pi isolation capture; its recorded disposition says it remains a
  pre-merge requirement. No phase-2a open table row was found in the current
  findings. Phase-6 rows and runner audits are historical evidence, not
  newly closed spec-review findings (`findings.md`, Phase 6).
- **ADR numbering and checks.** The highest existing ADR file is 0018;
  local HEAD removed the earlier 0019 draft specifically before redrafting.
  Exactly one new draft is therefore due, numbered 0020 since ADR 0019 went
  to the pi-pin change (renumbered 2026-10-15). The named
  `scripts/validate_change_artefacts.py` remains absent. The registry's real
  tracker path calls `bead_render.render_pfad()`, which may resolve outside
  this worktree; the drafting call leaves that check and full verification
  to its runner (`scripts/plans_registry.py`, `_bead_export_path`).

[DETAIL] The three-agent finder, two Opus preparatory roles, 24 repository
contributions, nine online contributions and final Opus judge total 39
invocations under Q-7–Q-9 (calculation, 2026-10-15). This is a planned graph,
not a measured run duration, token count or cost saving. The contract and
its test ledger live in the revised spec/design/plan; no v2 research reports,
maintainer answers or runtime qualification evidence are fabricated here.


## Go free-model redraft evidence — 2026-10-16

Read only within this worktree at `6146fdea58194fbb358a69f91f5a275b5e72faee`.
Earlier observations above remain historical, including the old 39-call graph.

- **The new answer adds Go free models, not Zen.** Q-10 records the
  maintainer's approval for online topics 9–11 only, in addition to Q-9's
  fixed Flash trio. Its context requires a live Pi catalog before every run,
  provider `opencode-go`, ids ending `-free`, and include/exclude declaration
  lists. The recorded examples are observations dated 2026-10-16, not a
  permanent roster or availability measured by this drafting call
  (`decisions.md`, Q-10). No human answer is changed by this redraft.
- **The code still rejects Go as a free provider.** `free_transport` removes
  the paid provider from inventory candidates, while `swarm_roles` still
  loads `free_roster` and `free_focuses`. The declaration retains the Zen
  `opencode-free` entry. These cannot implement Q-10 simply by adding new
  ids to the old list (`scripts/stage2_swarm.py`, `free_transport`,
  `swarm_roles`; `model-endpoints.yaml`, `research_swarm`).
- **The actual pin is now 1.2.0.** The repository package pins this exact
  runtime; ADR 0019 and its real-Pi offline contracts are present. Historical
  findings about 1.1.0 remain evidence of that version, not qualification of
  the amended online/free path (`tools/pi/package.json`,
  `docs/adr/0019-repository-pinned-pi-and-contract-tests.md`,
  `tests/test_pi_contract.py`, module contract and `provider_data`).
- **A listing is not proof of a live refresh.** The locally installed pinned
  source exposes `ModelRuntime.refresh` with `allowNetwork`, `providers` and
  `force`, and returns errors/abort state. Its remote catalog provider has a
  four-hour freshness window, fetches a provider shard from Pi's catalog,
  and merges the shipped baseline with a remote overlay. New selection must
  distinguish fresh remote identities from stale shipped ones and inspect
  the refresh outcome rather than assume a successful CLI exit proves it
  (`tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/`:
  `model-runtime.js`, `ModelRuntime.create`/`refresh`;
  `remote-catalog-provider.js`, `withRemoteCatalog`/`requestCatalog`;
  `tools/pi/node_modules/@earendil-works/pi-ai/dist/models.d.ts`,
  `ModelsRefreshOptions`). These installed-source paths are local evidence,
  not files proposed for editing or shipping as new kit content.
- **The sole ADR draft is already numbered correctly.** Read-only comparison
  with the local `origin/main` reference shows only ADR 0020 added; ADR 0019
  is present on the merged base. Updating the existing proposal preserves
  the one-new-ADR rule. No fresh remote PR query was made under this call's
  worktree-only read restriction.
- **Review evidence remains open where appropriate.** No phase-2a rows with
  open status exist in the read findings. Phase-6 F-1 still requires the
  maintainer-attended real-Pi offline capture before merge; it is neither
  waived nor marked fixed here (`findings.md`, Phase 6). The artifact
  validator is still absent; the drafting call uses the existing interview
  and ledger checks and leaves full verification to the runner.

[DETAIL] With `N` selected Go free models frozen before model dispatch, the
planned graph has `39 + 3N` invocations (calculation, 2026-10-16). Default
include/exclude lists are empty, selecting all eligible Go free chat ids;
filters, a measured zero and catalog failure have distinct outcomes in the
spec. The earlier 12-hour implementation stop and 150-minute run deadline
remain. No catalog request, external model invocation, offline canary capture,
live availability measurement or cost measurement was performed here.

## Draft retry evidence — 2026-10-16

Read only this worktree at `6146fde`; no provider, user configuration or
other checkout was read. The supplied first-attempt diagnostics report 46
swarm-test failures before contribution dispatch: the real Pi wrapper cannot
find `dirname` under the fixture's restricted PATH, then reports a missing
Node declaration relative to scratch. This retry did not rerun that suite.

- `scripts/stage2.py::require_pi` launches the absolute `PI_WRAPPER`, while
  `tests/test_stage2_swarm.py::sworld` supplies only a PATH-based `pi` and
  does not patch that constant. In contrast, `tests/test_stage2.py::world`
  injects a separately named `pin-pi` wrapper. This explains why merely
  putting a stand-in on PATH no longer intercepts the version check.
- `scripts/stage2_swarm.py::free_transport`, `pi_public_call` and
  `pi_repository_call` still construct bare-Pi commands. The amended plan
  must align these with the repository pin and inject that same seam in
  orchestration tests; adding system directories to the unit fixture's PATH
  alone would conceal the mismatch rather than ensure a stand-in is used.
- Real-runtime catalog tests and the attended isolation capture must retain
  actual pinned Pi. A unit fixture repair cannot qualify either boundary.
  The supplied diagnostics establish a red verifier for the earlier attempt,
  not a reason to weaken any criterion, discard F-1 or claim this retry green.

[GAP] Resolved from the sources above: the launcher mismatch belongs in the
implementation sequence. No maintainer answer, criterion or runtime policy
needs changing. The drafting scope permits no test or runner repair here.

## Third draft attempt evidence — 2026-10-16

The runner's third draft attempt (route glm, model glm-5.3) followed two
failed Codex attempts. That session has no command tool: it ran no gate, no
test and no git command, and read nothing outside this worktree (branch
explore/research-swarm, latest listed commit `6146fde`).

- Every criterion-ledger line of `plan.md` was checked against the test
  files by reading them: each named test is defined in its file
  (`tests/test_stage2_swarm.py`, `tests/test_stage2_research_tools.py`,
  `tests/test_stage2.py`), each `not yet written` function is undefined,
  and `tests/test_research_handoff.py` and
  `tests/test_stage2_research_catalog.py` do not exist. The one ledger
  section covers spec criteria 1–42 with no entry outside them.
- `scripts/stage2.py:196` defines `PI_WRAPPER` as the absolute `tools/pi/pi`
  path, confirming the diagnosis above: a PATH stand-in cannot intercept it,
  and the 46 swarm-test faults stand until plan step 1 repairs the seam. A
  drafting attempt cannot make that repair inside its scope.
- The neighbour paths named in the headers of `research.md` and `spec.md`
  exist in this worktree. No maintainer answer, criterion, class, appetite
  or ADR claim changed in this attempt; ADR 0020 remains the sole claimed
  ADR file and is unapproved.

## Phase-2a incorporation evidence — 2026-10-16

Read in this worktree at e1b54de. The recorded S-1–S-20 rulings in decisions.md
settle the phase-2a rows; earlier statements that no such open rows existed
are historical, not the current review state.

[GAP] Pinned Pi 1.2.0's local pi-ai/dist/types.d.ts defines chat as
`type?: "chat"` (absent defaults to chat) and declares `input` modalities,
but its Model interface has no dedicated tool-support boolean. The local
remote-catalog-provider.js parseCatalog retains extra raw metadata and
merges baseline/overlay; it does not qualify a raw capability field as proof
of tool support. No remote catalog was read here. Phase 4 must qualify and
record the raw capability mapping; absent/negative support excludes a free
seat as no-tool-support rather than assuming chat implies tool support.
This retains ruling S-3's explicit-support requirement without inventing a
pinned API field or claiming live availability. All other edits implement
the recorded rulings, not new maintainer answers or runtime measurements.

## Incorporation-round attempt 3 evidence — 2026-10-16

Read only this worktree (branch explore/research-swarm, latest listed commit
e1b54de) and the uncommitted incorporation revisions under review; no
provider, user configuration or other checkout was read. This session has no
command tool: it ran no gate, no test and no git command.

- The retained artifacts were reviewed against the recorded S-1–S-20 rulings
  and kept: spec, design, plan and ADR 0020 wording agree, and no defect was
  found that a drafting attempt may repair. One wording choice is recorded in
  the spec's Open decisions instead of being reworded after the rulings.
- Every criterion-ledger entry of `plan.md` was checked against the test tree
  by reading it: all seventeen named tests are defined
  (`tests/test_stage2_swarm.py`, `tests/test_stage2_research_tools.py`,
  `tests/test_stage2.py`), every `not yet written` function is undefined
  anywhere under `tests/`, and `tests/test_research_handoff.py` and
  `tests/test_stage2_research_catalog.py` do not exist. The one ledger covers
  spec criteria 1–42 with no entry outside them, in the three entry forms
  `scripts/check_criterion_ledger.py` holds.
- `scripts/stage2.py` still resolves `PI_WRAPPER` to the absolute
  `tools/pi/pi` path while `tests/test_stage2_swarm.py::sworld` offers only a
  PATH-based stand-in, so the 46 red swarm tests of the supplied diagnostics
  remain the known seam fault; plan step 1 owns the repair, and a drafting
  attempt still cannot make it inside its scope.
- No maintainer answer, criterion, class, appetite or ADR claim changed in
  this attempt; ADR 0020 remains the sole claimed ADR file and unapproved,
  and findings rows S-1–S-20 stay `in spec`, none open.
