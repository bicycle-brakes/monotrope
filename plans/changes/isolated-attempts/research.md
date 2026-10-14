---
title: "Research — isolated-attempts"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: Data Architect
provenance: human-written
tags: [research]
---

# isolated attempts — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1123 commits, 12 rules.

## Runner exploration — 2026-10-14

All facts are collected. My toolset here is read-only (Glob/Grep/Read — no shell, no write), so per the repository agent rules I report the facts as prose ready to append to `research.md`; the orchestrating session commits them.

---

**Ready for `plans/changes/isolated-attempts/research.md`** — replace the placeholder body, keep the Stage-2 audit line, and set the frontmatter the skeleton itself asks for: `provenance: ai-drafted-reviewed`, `produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}`, `review: {status: pending, approved_by: null, approved_at: null}`, `tags: [research, stage-2, runner, isolation]`.

---

# isolated attempts — Research

Phase 1 for bead coding-harness-s9r, read in the worktree `isolated-attempts` (branch `explore/isolated-attempts`, opened by commit `6fd9450 docs(s9r): open change isolated-attempts`) on 2026-10-14.

## The request

The session handover of 2026-10-14 (`docs/journal/handover/2026-10-14-night-run-third.md`, sections 1 and 3) names bead coding-harness-s9r (P1) as "isolate each writing attempt", the structural answer to the fix-by-case pattern of PR #138: each phase-6 re-check found the next case of one finding class (F-8, F-10 to F-17), and the F-12 fix created F-13. F-15 to F-17 of that change stand as accepted limits by the maintainer's rule of 2026-10-13, and the handover says the new bead "closes the class structurally". What the bead's own record asks beyond that is stated nowhere in this worktree.

## What exists today — the writing attempts

`run_attempts` (function in `scripts/stage2.py`) is the attempt loop the three work verbs share. Each attempt is one model call, then the post-run checks of `verify_attempt` (ruff's safe fixes and formatter on changed Python files, `make verify`, a measured line under `## Time used`), then exactly one checkpoint commit when everything passes; a failed attempt leaves its diagnostics and its changed files quoted below its audit line in the change's `findings.md` (`attempt_block`, `attempt_files`). The routes, literally in the verb functions:

- `implement`: Flash, one Flash repair, Sonnet 5.5 on stage-1; under `--stage2-off` Sonnet alone.
- `draft`: Codex (`gpt-6.1-sol`, effort `max`), one fresh Codex attempt carrying the first one's diagnostics, then `glm-5.3` on stage-1 (ADR 0016).
- `repair`: Codex, one fresh Codex attempt with the first one's diagnostics, Sonnet 5.5 at effort `medium` on stage-1 (ADR 0017). Repair is the only verb that passes `snapshot_findings`/`restore_findings` into `run_attempts`, so only repair puts `findings.md` back after a failed attempt (phase-6 F-2).

## What exists today — what confines an attempt

- **The worktree.** Every call runs inside the change's dedicated worktree; the session verb names the shape (`<main checkout>/.claude/worktrees/<change>`, `scripts/stage2.py` docstring, `session` verb). `docs/WORKFLOW.md` §3, "What isolation consists of here — three things": the worktree separates files, the harness's sandbox separates execution (a property of the environment, nothing in this repository), and `permissions.deny` in `.claude/settings.json` is a brake against accidents. The same section says isolation between sessions "is a working agreement, not a wall", naming `docs/architecture/2026-09-17-gap-analysis.md`.
- **Codex.** `run_codex` starts `codex exec` with `-c sandbox_mode="workspace-write"` for draft and repair, `read-only` for reviews, with hooks and memories disabled and no bypass flag. Both the module docstring ("the tests do not measure that confinement") and `docs/WORKFLOW.md` §4 ("the tests show the configured call, not the CLI's confinement") state that no test measures the sandbox's real confinement.
- **Claude Code calls** (explore, the draft's GLM attempt, implement, spec-review, the Sonnet fallbacks) start with `--restricted` and no `--add-dir`; the docstring and §4 "Reads" both mark this as the CLI's documented behaviour, not measured.
- **Pi loop calls** get a fresh agent directory and home per call, with extensions, MCP servers, skills, context files, prompt templates and themes off, tools `read,grep,find,ls` (`PI_TOOLS`), the version pinned by `require_pi`/`PI_VERSION` (1.1.0). The flags were measured once by hand on the pinned version; their reads are not confined — the residual risk ADR 0011 extends from ADR 0007.
- **The environment.** `foreign_env` builds each call's environment from the `ENV_ALLOW` allow-list, never the caller's.
- **The runner's only out-of-repository write** is the loop record at `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md` (`record_dir`; verified as the only such target by `plans/changes/attempt-diagnostics/research.md`, "Runner exploration — 2026-10-11").

## What exists today — what an attempt leaves behind

- After a failed *model call*, `restore_baseline` puts every path but the change's `findings.md` back at the baseline (`git restore --source=<baseline> --staged --worktree`, `git clean -fdq`, plus removal of ignored paths the attempt created, told apart by the `ignored_snapshot` mtime/size pairs).
- After failed *post-run checks* the tree stays: verified by `plans/changes/attempt-diagnostics/research.md` — "A later attempt therefore builds on the earlier attempt's half-done tree".
- Before each next attempt, the snapshotted prompt inputs are restored byte-for-byte at the end of `run_attempts`; the F-12 fix makes that loop remove whatever stands at a path "without being followed" and write anew, and `tests/test_stage2.py::test_repair_retry_restores_aliased_and_directory_inputs_without_following` pins it (F-13/F-14).
- The runner's own derived writes (INDEX render, frontmatter stamps, ruff format, the `## Runner route` block in `plan.md`) stay in the worktree after a failed run — recorded in the handover §3 as bead coding-harness-b5w's subject; that exploration lives on branch `explore/derived-leftovers`, not in this worktree.

## The findings class this change is the structural answer to

From the merged phase-6 table of `plans/changes/codex-repairs/findings.md` (all MAJOR, status open as accepted limits, origin "base"):

- **F-15** — the input restoration of `run_attempts` checks only the leaf: if a completed attempt replaces `prompts/` with a symlink to an external directory, the retry restoration unlinks and overwrites a file outside the worktree.
- **F-16** — repair's `restore_findings` callback (`ctx.findings.write_text(...)` in `repair`) writes through a symlink planted at `findings.md`; `prepare_derived` refuses an aliased held document ("refusing an aliased document path"), but the restoration callback has no such check.
- **F-17** — `findings.md` standing as a directory makes the same callback raise an uncaught `IsADirectoryError` before diagnostics are recorded or the fresh Codex retry starts.

Beyond the class, `docs/WORKFLOW.md` §4 ("The draft") and ADR 0017's consequences state what the runner cannot see at all: which paths a draft's or repair's Codex call reads, whether its sandbox in fact confines its writes, and everything `git restore`/`git clean` never touch — ignored files, paths outside the worktree, and the repository's git directory (`.git`: hooks, config). ADR 0016's residual risks for ignored files, external paths and the git directory are retained by ADR 0017.

## Prior changes and research in the same area

- `plans/changes/attempt-diagnostics/` (bead coding-harness-cit, `implementation_status: partial`, `plans/INDEX.md`): made per-attempt diagnostics durable. Its research verified the route and restoration mechanics cited above; it is the direct predecessor in code area and method.
- `plans/changes/codex-repairs/` (bead coding-harness-0ga, merged as PR #138; ADR 0017): the findings F-15–F-17, the fresh-Codex-attempt semantics, and the accepted-limits rule.
- Earlier runner changes by the index: `stage2-repair` (coding-harness-g2f), `stage2-format` (coding-harness-52r), `criterion-test-ledger` (coding-harness-909).
- `docs/research/2026-09-26-kubernetes-gate-runner.md` (status `proposed`): a pinned verifier container for the gates as a Kubernetes Job — a desk review, nothing built; the only on-file infrastructure note for stronger execution isolation.
- `docs/research/2026-10-05-hermes-agent-runner.md`: "Not Hermes, not now."
- `plans/specs/` holds exactly one spec (`implementation-verification`); no spec matches this topic, and no research artefact for it existed beyond this change's skeleton.

## What the tests pin

`tests/test_stage2.py` pins today's restoration behaviour with stand-ins, never a real CLI: `test_repair_retry_restores_aliased_and_directory_inputs_without_following` (the "wrote through the symlink" assertion), `test_a_failed_flash_process_restores_the_baseline_so_stage2_off_can_proceed`, `test_a_failed_model_call_names_what_was_restored`, `test_a_restore_after_a_dead_model_keeps_the_earlier_blocks`, `test_a_failed_repair_process_restores_the_baseline_without_a_further_attempt`, `test_a_codex_repair_that_commits_findings_restores_statuses_and_records_diagnostics`. `docs/WORKFLOW.md` §4 records the maintainer's decision of 2026-09-30 (ADR 0007) that the CLI settings are "configured on every call, not measured by any test", and that "the suite starts no real Pi".

## What is unclear

- **The bead's acceptance text** — not read (see below). The handover's one phrase "isolate each writing attempt" is all this worktree says of the goal.
- **Which boundary "isolate" names** is a `[DECISION]` for the interview: per-attempt confinement of the model process (OS level — the unmeasured property both docstrings name), a fresh scratch/worktree per attempt so one attempt's writes cannot reach the next, or only hardening the runner's restoration paths (the F-15–F-17 class). The facts above are the material; this file recommends nothing.
- **Scope of verbs**: the work verbs (`draft`, `implement`, `repair`) are `run_attempts`' only users; the interactive `session` verb also writes (`workspace-write`, `scripts/stage2_session.py` `cli_argv`) and its terminal permissions "confine nothing at the operating-system level" (module docstring). Whether it is in scope is not stated anywhere here.
- **Whether unconfined reads** (Codex and Pi; ADR 0007/0011 residual risks) belong to this change, or only the write-and-restoration class.
- **Overlap with bead coding-harness-b5w** (derived leftovers after a failed run): same area, separate bead; its research is on another branch and was not read here.
- **How per-attempt isolation interacts with the audit line and leak check**, which must keep observing the real worktree's `findings.md` in this repository — a shape question phase 2 owns.

## Which files a change would have to touch

- `scripts/stage2.py` — `run_attempts` (the loop, the input restoration, the findings callbacks), `restore_baseline`, `run_codex` (sandbox flags), `run_work_model`, the `repair` verb's `restore_findings` callback, `ENV_ALLOW`/`foreign_env` if the environment allow-list changes.
- `scripts/stage2_session.py` — `cli_argv`, if the interactive session is in scope.
- `tests/test_stage2.py` (the pinned tests above; any new isolation behaviour needs stand-in tests here), `tests/test_stage2_session.py` if the session verb changes.
- `docs/WORKFLOW.md` — §3 "What isolation consists of here" and §4's draft/repair paragraphs.
- `docs/adr/` — an ADR draft when the isolation boundary is decided, if the change is architectural; a decision answer under `decisions/answers/` if the `adr-answers` gate demands one.
- A new helper script would additionally have to satisfy `test_every_script_has_a_test_or_a_declared_reason` (`tests/test_ci.py`) or stand with a reason in `ci_gates.OHNE_TEST`.

## Not read here

- **The bead record coding-harness-s9r**: the tracker is the Dolt database read through `tools/bd`, and this session has no shell; the handover and `plans/INDEX.md` (row `changes/isolated-attempts/research.md`, bead coding-harness-s9r) are the only in-tree sources about it.
- **The six night explorations** (coding-harness-l9s, fdz, b5w, y17, 1jg.4, mvk): their `research.md` files live on their own branches, not in this worktree; their content is known only as the handover §3 summarizes it.
- **`~/.local/state/coding-harness/`**: outside this worktree, not read; what the runner writes there is stated from `record_dir` and the docstrings.
- **The real confinement of the Codex sandbox, `--restricted`, and the Pi flags**: not measured by any test and not measured here; the statements above quote the repository's own documentation of that gap.

---

*Orchestrator notes:* this file (`plans/changes/isolated-attempts/research.md`) is the phase's whole result — no gate on phase 1. Suggested next step: commit this on `explore/isolated-attempts`, then run the phase-1a interview (`prompts/01a-interview.md`) against bead coding-harness-s9r — the class minimums apply, and the `[DECISION]` questions above are the interview's starting material.

## Container tool comparison — 2026-10-14

Desk research by an Opus 5.5 sub-agent with web search, asked by the
orchestrating session after the maintainer's answer Q-1 (a container per
attempt) and the request for "the best option that may also work on Windows".
Nothing was installed or measured locally; no container tool is installed on
the maintainer's Mac (checked 2026-10-14 18:40). Sources read 2026-10-14.

| Tool | macOS (Apple silicon) | Windows 11 | Linux/CI | Licence | Isolation | CLI | Status |
|---|---|---|---|---|---|---|---|
| Podman (+ Desktop) | yes, VM via libkrun/applehv | yes, via WSL | native | Apache-2.0, free | containers share one machine VM | Docker-compatible, rootless default | v6.1.4, 2026-10-12 |
| Docker Desktop | yes | yes (WSL2) | Docker Engine | free only below 250 employees and $10M revenue | one shared VM | reference | mature |
| Docker Sandboxes (`sbx`) | not verified | not verified | not verified | CLI free, also commercial | microVM per sandbox, host proxy enforces network policy | own CLI | maturity not stated |
| Apple `container` | yes, supported on macOS 26 | no | no | Apache-2.0 | VM per container | own, Docker-like flags | 1.5.0, "under active development" |
| OrbStack | yes | no | no | commercial $8/user/month | lightweight VM | Docker | mature |
| Colima / Rancher Desktop | yes | Rancher yes (WSL2) | yes | MIT / Apache-2.0 | one shared VM | Docker or nerdctl | maintained |

Findings:

- Only Apple `container` and Docker Sandboxes give each attempt its own
  kernel; the others share one Linux VM between attempts (still a hard
  boundary against the host).
- No tool offers a single-host egress allow-list as a flag: each needs an
  internal network plus a filtering proxy (the pattern Claude Code's sandbox
  and Docker Sandboxes use) or a firewall inside the container.
- Lighter sandboxes do not confine reads portably: Claude Code's sandbox
  covers shell commands only; `@anthropic-ai/sandbox-runtime` confines reads
  but is a beta preview without native Windows; the Codex sandbox documents
  write bounds, read confinement not verified; `sandbox-exec` is deprecated.
- Start times: no authoritative measurement found (forum and blog figures of
  0.2 to 0.9 s, methods not verified).
- Pitfalls: anything readable in the container can leave through an allowed
  host; pass a long-lived token as a variable rather than mounting a home
  directory; Claude Code refuses its permission-skip flag as root, so run as a
  non-root user; on Windows keep worktrees on the WSL filesystem and pin LF
  line endings.

Ranked by the sub-agent: (1) Podman — free for companies, rootless, one CLI on
macOS, Windows (WSL) and Linux CI; (2) Docker Sandboxes — best fit on paper
(microVM per attempt, built-in network policy, credentials outside the VM),
platforms not verified, worth a timed trial; (3) Apple `container` — strongest
per-attempt wall on the Mac, macOS only, egress control undocumented, macOS 27
not verified. Portable design: the runner calls one configurable binary
(`podman` | `docker` | `container`) with the common flag subset, an internal
network and one proxy container that allow-lists the provider's API host.

A minimal live boundary test (proposed): sentinel files outside the worktree
and in the home directory must not be readable from inside; exactly one
credential variable in the environment; the provider host reachable only
through the proxy, any other host and any direct route refused; no attempt
container left after exit.

Sources: github.com/apple/container (README, docs/technical-overview.md,
docs/command-reference.md, releases); github.com/containers/podman and
releases; podman-desktop.io/docs/podman/creating-a-podman-machine;
docs.podman.io podman-machine-init; docs.docker.com/subscription/desktop-license;
docs.docker.com/ai/sandboxes and its architecture page; docs.orbstack.dev/faq;
lima-vm.io/docs/config/mount; github.com/abiosoft/colima;
github.com/rancher-sandbox/rancher-desktop; docs.rancherdesktop.io/faq;
code.claude.com/docs/en/sandboxing, sandbox-environments, devcontainer;
learn.chatgpt.com/docs/sandboxing; gvisor.dev/docs;
github.com/firecracker-microvm/firecracker;
learn.microsoft.com/en-us/windows/wsl/filesystems. Secondary sources marked as
such in the sub-agent's report were not relied on for a ranking reason.

Open: start times measured on this Mac; which platforms `sbx` supports and
whether it runs Codex and Pi; how `--internal` blocks egress in Podman and
Apple `container`.
