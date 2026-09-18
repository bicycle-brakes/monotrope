---
title: "Agent Skills assessment for the coding harness"
category: research
status: proposed
created: 2026-09-18
last_reviewed: 2026-09-18
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex-sol
  version: "2026-09-18"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [agent-skills, skills, workflow, evaluation]
---

# Agent Skills assessment

**Decision proposed:** selectively adapt a few techniques as harness-owned guidance and evaluation fixtures. Do not install the complete pack into the harness or ship it in the kit. Its lifecycle largely duplicates the seven phases, while its interaction, task, and gate defaults would create competing authorities.

**Source cut-off:** inspected the public `addyosmani/agent-skills` repository on 2026-09-18. The [Codex plugin manifest](https://github.com/addyosmani/agent-skills/blob/main/.codex-plugin/plugin.json) reports version `0.6.9`; the [tag page](https://github.com/addyosmani/agent-skills/tags) dates tag `0.6.9` to 2026-09-05 at commit prefix `84ee506`. File links below point to moving `main` and should be rechecked against a full pinned commit before any text is copied. The [license](https://github.com/addyosmani/agent-skills/blob/main/LICENSE) is MIT, copyright 2025 Addy Osmani. Adapted substantial text would retain the copyright and permission notice, plus a source and revision note. Release tags and a substantial commit history indicate active maintenance, but do not establish compatibility or efficacy in this harness. This was a documentation and source review; no upstream code, hooks, installation commands, or behavioral evaluations were run.

## Fit with the harness

| Harness movement | Relevant upstream material | Assessment |
|---|---|---|
| 1 Explore, optional 1a Interview | [`idea-refine`](https://github.com/addyosmani/agent-skills/blob/main/skills/idea-refine/SKILL.md), [`interview-me`](https://github.com/addyosmani/agent-skills/blob/main/skills/interview-me/SKILL.md) | The one-question-with-a-guess technique may reduce effort for a human answering a real intent question. Its automatic trigger, approximate 95% confidence loop, demand for an explicit yes, and optional `docs/intent/` file conflict with human-called 1a, `[DECISION]`/`[GAP]`/`[DETAIL]`, and the change artefacts. Adapt the technique only inside the existing optional interview prompt. |
| 2 Spec, 3 Plan | [`spec-driven-development`](https://github.com/addyosmani/agent-skills/blob/main/skills/spec-driven-development/SKILL.md), [`planning-and-task-breakdown`](https://github.com/addyosmani/agent-skills/blob/main/skills/planning-and-task-breakdown/SKILL.md) | Acceptance criteria and small, independently verifiable steps are compatible. Upstream PRD and task formats cannot replace `spec.md`, `plan.md`, change class, protected areas, design 2b, stable plan IDs, or Beads status. |
| 4 Implement | [`incremental-implementation`](https://github.com/addyosmani/agent-skills/blob/main/skills/incremental-implementation/SKILL.md), [`test-driven-development`](https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md) | Thin slices and visible test evidence suit the plan. Upstream's commit-after-each-slice instruction is a heuristic: the coordinator controls candidate assembly, worker branches and commits in M0. A universal red-green-refactor or test-ratio mandate should not override task class or the instance's gate manifest. |
| 5 Verify, 6 Review | [`debugging-and-error-recovery`](https://github.com/addyosmani/agent-skills/blob/main/skills/debugging-and-error-recovery/SKILL.md), [`code-review-and-quality`](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) | Reproduce/localize/reduce/fix/guard and concrete review evidence are useful. Map any findings into the harness's SPEC/MAINT, base/fix-rN, BLOCKER/MAJOR/MINOR and `[DIVERGENT]` contract. Upstream's Critical/Nit/Optional/FYI labels must not become a second merge vocabulary. |
| 7 Commit and session handover | [`git-workflow-and-versioning`](https://github.com/addyosmani/agent-skills/blob/main/skills/git-workflow-and-versioning/SKILL.md), [`shipping-and-launch`](https://github.com/addyosmani/agent-skills/blob/main/skills/shipping-and-launch/SKILL.md) | Generic branch and release advice does not own the human final merge, current CI evidence, Beads closure trailer, or durable handover. Shipping checklists are instance-specific, not kit baseline. |

The [upstream README](https://github.com/addyosmani/agent-skills) advertises nine slash commands and 25 skills, including a meta-skill that routes work to other skills. Its `/build auto` approves one plan then executes tasks. Those commands and the [meta-skill's default assumption and stop-to-ask rules](https://github.com/addyosmani/agent-skills/blob/main/skills/using-agent-skills/SKILL.md) would compete with the harness's seven-phase entry points and question protocol. In particular, a repo-answerable `[GAP]` should be explored and a reversible `[DETAIL]` decided by the agent; neither should become a routine human interruption. The one-human owner is asked only for open intent decisions and owns the final merge.

The [constraint skill](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md) has a valuable rule: watch for weakened thresholds, skipped tests and suppressions, and require owner/date on exceptions. Its separate `CONSTRAINTS.md` and `check:fast`/`check:task`/`check:full` command tiers would duplicate the harness rule ladder and sole gate manifest. Extract candidate bad-case fixtures and enforce them through the canonical verifier, with a dated valve where needed. A skill's checklist is an instruction to an agent; a check only becomes a hard gate when trusted code or CI rejects a known-bad case and binds its result to the reviewed candidate. Upstream's own [evaluation guide](https://github.com/addyosmani/agent-skills/blob/main/evals/README.md) distinguishes structural checks, lexical trigger tests and on-demand behavioral agent tests; lexical routing is explicitly an approximation, and behavioral claims still need local qualification.

The [context skill](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md) correctly favors layered, task-relevant context. Its long instruction and example rules files should not enter always-loaded context. The target retains a 200-line instruction import budget and a small generated resume packet with decisions, scopes, SHAs and remaining run budget. Supporting guidance can be loaded only for a matching phase. Measure actual packet occupancy; do not infer a token saving from the phrase “progressive disclosure.” The [README](https://github.com/addyosmani/agent-skills) acknowledges that per-skill installs omit shared `references/`, a concrete portability defect for kit copies.

Upstream [agent orchestration guidance](https://github.com/addyosmani/agent-skills/blob/main/docs/agents.md) endorses parallel fan-out for independent review perspectives. That is a useful review pattern, not an M0 implementation topology: the harness starts with two independent coding workers, one fenced coordinator, disjoint worktrees, one candidate branch, one tracker writer and a human final merge. Generic slash commands and personas cannot confer worktree, endpoint, tracker, spending or policy authority. The M0 trust, cancellation and freshness tests remain required.

## Adoption boundary and bounded pilot

1. **Adapt:** add a concise, optional interview question pattern to the existing phase 1a prompt; add one review evidence checklist mapped to the existing findings schema; and add known-bad fixtures for gate weakening and skipped tests to the canonical verifier. These are candidate changes, subject to the ordinary spec, plan, rule-ladder and gate review.
2. **Evaluate before promoting:** in a disposable synthetic repository, run one Bounded task with the current prompts and one comparable task with only the three adapted techniques. Freeze acceptance cases first. Compare escaped defects, false review findings, human minutes, total model cost, gate verdicts and resume accuracy. Include a clean control and a seeded fault. The Omnigent M0 pilot still needs its separate two-worker isolation, writer, freshness, budget and cancellation evidence.
3. **Defer:** full plugin/pack installation, `/build auto`, a new `CONSTRAINTS.md`, upstream task state or severity labels, and any shipping or security gate that lacks an instance-owned enforcer. Reconsider an individual skill only after it names a gap in the harness and a test demonstrates improvement without an extra authority.

If text is later imported, pin a full upstream commit, audit referenced files and executable hooks, record local modifications and the MIT notice, and use a reviewable kit update with rollback and a fresh-instance probe. A tag or plugin version alone does not freeze moving `main` links or transitive install behavior. The [implementation plan](../architecture/2026-09-17-implementation-plan.md) already supplies the M0/M1 qualification path; this pilot adds evidence to it and does not waive any entry or exit condition.
