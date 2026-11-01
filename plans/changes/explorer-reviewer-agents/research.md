---
title: "Research — explorer-reviewer-agents"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-9ll
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "stage-2 explore, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
---

# explorer reviewer agents — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 801 files, 2934 commits, 12 rules.

## Runner exploration — 2026-10-31

The exploration is complete. Here is the research, ready to append to `plans/changes/explorer-reviewer-agents/research.md`.

---

## What exists today

**The change itself is a skeleton.** The folder holds only `research.md` (frontmatter: `bead: coding-harness-9ll`, `status: draft`, `implementation_status: none`, `provenance: human-written`) with an empty body and this run's audit line. The bead's own text was not read: the tracker is the Dolt database under `.beads/` and carries no rendered copy in the tree (`AGENTS.md`, house rule 2), so the change's exact mandate is an open question, not a fact. What the tree says is the name: the opening commit (`dfa06b1f`, "chore(plans): open change explorer-reviewer-agents") and the `plans/INDEX.md` row for `changes/explorer-reviewer-agents/research.md` (draft, 2026-10-31, coding-harness-9ll). The name matches the one piece the doctrine promises and the tree provably lacks: the two sub-agent definitions `.claude/agents/explorer.md` and `.claude/agents/reviewer.md`.

**The doctrine promises the two definitions twice.** The header notice of `docs/WORKFLOW.md` ("Not all of it is here yet.", checked 2026-10-27 against the tree at `e61554b0`) lists as absent from this repository: `scripts/validate_change_artefacts.py`, "the sub-agents `.claude/agents/explorer.md` and `reviewer.md`", and the stop hook `.claude/hooks/session-stop/check-tests-green.sh`; where the text names one of the missing pieces it describes the target, not this tree. The §3 stage-1 table ("What stands in the repository for it") carries the row "Sub-agents | `.claude/agents/explorer.md`, `reviewer.md` | read-only, model pinned". Neither file exists in this worktree (Glob over `.claude/**` and the tree); `.claude/agents/` holds seven different definitions: `code-generation-orchestrator.md`, `consistency-auditor.md`, `entity-builder.md`, `entity-deployer.md`, `migration-supervisor.md`, `preconditions-gate-runner.md`, `reconciliation-orchestrator.md` — all German, each with frontmatter `name`, `model`, `tools` (for example `code-generation-orchestrator.md` pins `model: claude-sonnet-5`, `tools: Read, Write, Edit, Grep, Glob, Bash`) and the Regelwerk's RB-A1 evidence contract in the body.

**A test pins the notice to keep them absent.** `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands` (its docstring says "Criterion 8") asserts `.claude/agents/explorer.md` and `reviewer.md` stand in the *absent* half of the notice, while `.claude/commands/`, `docs/governance/gate-catalog.md`, `make change` and `make index` stand in the *supplied* half. Building the agents therefore moves both the notice and this test; the notice must keep its check date and commit (`plans/changes/workflow-promises/spec.md`, criterion 8).

**The predecessor change deliberately left them out.** `plans/changes/workflow-promises/` (bead coding-harness-i0l, class `bounded`, `implementation_status: partial`) supplied the gate catalog, `make change`, `make index` and `/workflow-start` (`.claude/commands/workflow-start.md` exists and only opens the folder: "Phase 1 (explore) is a separate step"). Its Non-goals name "missing agents" among the mechanisms not built, and its `research.md` ("Promised and absent", item 2) records today's state of `.claude/agents/`: seven definitions, German, carrying the RB-A1 clause "byte-gleich" per `docs/governance/regelwerk.md` §6, and — observed in the files — `reconciliation-orchestrator.md` declares `tools: Read, Write, Grep, Glob, Bash`, not the read-only pair the §3 table describes. The same research names `.claude/agents/explorer.md` and `reviewer.md` in "Which files a change would have to touch" and states the intended form: "a follow-up bead per missing piece is the night-run plan's stated form for everything this change only reports."

**Governance a new agent definition runs into (all enforced today, over every `*.md` in the directory):**

- `tests/test_regelwerk.py::test_rb_a1_clause_is_present_verbatim` globs all of `.claude/agents/*.md` and requires the evidence-contract clause of `docs/governance/regelwerk.md` §6 byte-identical in each; the Regelwerk §6 gives the reason ("fourteen slightly different versions would be fourteen rules") and §6 declares itself normative, copied not retold. A new `explorer.md` or `reviewer.md` must carry the clause byte-equal or this test goes red.
- `tests/test_regelwerk.py::test_agent_definitions_carry_no_instance_terms` refuses instance vocabulary (`DV2`, `DLT`, `SDP`, `Oracle`, `ANSPRMENGE`, `exacs`, `wdp`, `Hub/Sat/Link`) in any agent definition.
- `tests/test_model_endpoints.py::test_every_agent_model_resolves_to_a_declared_endpoint` parametrizes over `agent_modelle()` and requires every definition's `model:` line to name a model declared in `model-endpoints.yaml` (RB-A6, "not listed is BLOCK"). Declared today under `anthropic-api` and `claude-code-plan`: `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-5-5`, `claude-opus-5-5`, `claude-sonnet-5-5`; under `glm-coding-plan`: `glm-5.3`, `glm-5.3-flash`; under `openai-codex`: `gpt-6.1-sol`; plus the `opencode-go` ladder set.
- `provenance.yaml` (prefix `.claude/agents/`) allows `human-written` and `ai-drafted-reviewed` and holds `frontmatter: none` — the agent frontmatter is Claude Code configuration, not a document header (comment in the map, bead coding-harness-qd7). The directory is not `human-decided`; `docs/governance/regelwerk.md` is, but a new definition copies §6 instead of editing it.
- `scripts/kit/manifest.yaml` classifies `.claude/agents/` as `mechanismus`: every definition carries the RB-A1 clause byte-equal and a `model:` against `model-endpoints.yaml`, committed so a parallel session's deletion is loud — the kit transports the directory into new instances.
- `docs/WORKFLOW.md` §7 ("What survives each stage"): `.claude/agents/` survives stage 1 and stage 2 unchanged and is replaced by YAML in stage 3.

**How the doctrine describes the two agents as targets, and what really runs today.** The §3 sub-agent row says "read-only, model pinned"; §3 also states a sub-agent takes its effort from its own frontmatter (`effort: xhigh`) and that a new definition is read only when a session starts. §3's "Check after setup" records an unresolved measurement: "There are reports that the `model:` field in sub-agent definitions is ignored and sub-agents run on the parent model. Look once with `/status`" — and §9 lists the same check as outstanding ("does the sub-agents' model assignment take hold?"). Nothing found in the tree records that this check happened. The reviewer side already has one documented sub-agent use as a fallback: §4 "Night runs" rule 1 sends a phase-6 re-check "through a read-only Sonnet 5.5 sub-agent whose rows the orchestrator records unchanged" when Codex is at capacity — run ad hoc, without a definition file. The explorer side runs today through the runner, not a sub-agent: `prompts/01-explore.md` routes phase 1 through `scripts/stage2.py explore` (GLM 5.3 Flash; Haiku 5.5 with `--stage2-off`; the research swarm for `feature`/`architectural`, ADR 0020), and `scripts/stage2.py` defines `EXPLORER_ROLE` (constant near the `names_a_repository_file` function), the runner's statement that the explorer is read-only (Read, Grep, Glob) and not the orchestrator — added by the `explore-role` change (bead coding-harness-e7m, `implementation_status: partial`). `AGENTS.md` records the general sub-agent orchestration rule ("Sub-agents survive a budget pause": each commits and pushes after every green step, ends with a `Resume:` line), and the 2026-10-31 handover records a phase-1 run "through a Haiku sub-agent" in the `go-access-point` worktree — sub-agents are in real use without repository definitions.

**Language.** The seven existing definitions are German throughout; `AGENTS.md` house rule 1 makes the repository English and sends remaining German to translation pull requests of its own (its list names "mainly `scripts/`, `tests/` and `docs/governance/`", not `.claude/agents/`).

## Where it lives

Promise sites: `docs/WORKFLOW.md` header notice ("Not all of it is here yet.") and §3 stage-1 table (Sub-agents row); the pinning test `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands`. The predecessor audit: `plans/changes/workflow-promises/research.md` (promised-and-absent item 2) and `spec.md` (criterion 8, Non-goals). Governance holders: `docs/governance/regelwerk.md` §6 (the clause, human-decided), `tests/test_regelwerk.py`, `tests/test_model_endpoints.py`, `model-endpoints.yaml`, `provenance.yaml` (`.claude/agents/` prefix), `scripts/kit/manifest.yaml` (kit transport). The seven existing definitions: `.claude/agents/*.md`. The other two absent pieces the same notice names — `scripts/validate_change_artefacts.py` and `.claude/hooks/session-stop/check-tests-green.sh` — are also not in this worktree (Glob finds neither), and the same test holds them in the absent list.

## What is unclear (open questions, not guesses)

- The bead coding-harness-9ll's title, description, class and label: not read — the tracker is a Dolt database and this phase reads no tracker. The `research.md` frontmatter carries no `class:` field, so the routing class (spike, bounded, feature, architectural) was not seen anywhere in the tree.
- Whether the change covers only the two agent definitions or also the stop hook and the validator named in the same notice sentence: not derivable from the tree; the change name covers the agents alone. A maintainer question.
- Which models `explorer.md` and `reviewer.md` should pin: not found anywhere in the tree. The doctrine says only "read-only, model pinned" (`docs/WORKFLOW.md` §3); the runner routes for the same phases name GLM 5.3 Flash, Haiku 5.5, Opus 5.5, Codex and the Go ladder (`prompts/01-explore.md`, `prompts/02a-spec-review.md` route, `prompts/06-review.md` route, `docs/WORKFLOW.md` §4), and §3 leaves the `model:`-field-works check open. Not there: any statement naming a model for these two files.
- The Regelwerk changelog counts ("sechzehn Agent-Definitionen lösen auf; vierzehn pinnen eine ältere Generation", and "byte-gleich in allen vierzehn Agent-Definitionen, seit PR #88") do not match this tree's seven files; whether those counts included user-level definitions outside the tree (compare the user-level `~/.claude/agents/spec-planner.md` named in `plans/changes/codex-drafts/research.md`) and which version headings those entries carry was not read.
- Whether the sub-agent `model:` field takes effect in this Claude Code version: §3 "Check after setup" and §9 demand the check; no record of it was found in the tree.

## Which files a change would have to touch

New files `.claude/agents/explorer.md` and `.claude/agents/reviewer.md` (RB-A1 clause byte-equal from `docs/governance/regelwerk.md` §6; a `model:` line that resolves in `model-endpoints.yaml` against `tests/test_model_endpoints.py`; no instance vocabulary; no document frontmatter per `provenance.yaml`; English per house rule 1). The notice in `docs/WORKFLOW.md` ("Not all of it is here yet.") loses the two agents from its absent list and re-dates its check with its commit; `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands` moves with it. `plans/INDEX.md` regenerates through `scripts/plans_registry.py --index` (`make index`). The parametrized endpoint test picks up new `model:` lines automatically; `scripts/kit/probe.py` maps the existing parametrize ids for the kit's reduced suite and may need the new ids. The seven existing definitions and `docs/governance/regelwerk.md` are held by tests and the human-decided map respectively and are not free to edit.

## Draft follow-up — 2026-11-01

[GAP] **Adding the definitions also changes the kit's endpoint-test set.**
Checked against `544cb659` on 2026-11-01: `scripts/kit/manifest.yaml` classifies
`.claude/agents/` as `mechanismus`, but `model-endpoints.yaml` as `bestand`.
`tests/test_model_endpoints.py::agent_modelle` discovers every Markdown agent's
model, and `test_every_agent_model_resolves_to_a_declared_endpoint` is
parameterized over that inventory. The kit therefore gains cases ending
`[explorer.md-claude-haiku-5-5]` and `[reviewer.md-claude-opus-5-5]` while its
endpoint declaration remains absent. This is a consequence of the readers,
not a measured kit run with the proposed files installed.

An AST read of `scripts/kit/probe.py` on 2026-11-01 measured 42 existing
`REIST_NICHT` entries and `DECKEL = 42`. `pruefe` blocks unexplained red cases,
entries with no collected case, and cap overruns; `decisions/gates.yaml`
runs that probe as a blocking gate. The existing agent-model exceptions use
`braucht-die-vollstaendige-suite`. Thus simply installing the pair is expected
to require two additional named exceptions and a visible cap change, or an
independently specified change to the portable checking mechanism. Neither
is among the three delivery files permitted by the scope note in
`decisions.md`; the draft records this conflict as an open scope decision,
without changing that note or inferring a maintainer answer.

The workflow notice is historical: it explicitly describes the tree at
`e61554b0` on 2026-10-27. Updating its inventory is companion maintenance,
not evidence that its past check was false. Its supplied/absent assertions
are in `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands`.
No additional sibling spec or plan for this pair was found by a search of
`plans/specs/` and live `plans/changes/` on 2026-11-01. There is no plan template
under `templates/`; `prompts/03-plan.md` and the existing change-plan form
supply the card, ledger and time section instead.
