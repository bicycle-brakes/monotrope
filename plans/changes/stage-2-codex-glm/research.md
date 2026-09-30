---
title: "Research — stage-2-codex-glm"
status: draft
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-bc9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-30"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, stage-2, codex, glm, leak-check, model-routing]
---

# Stage 2 with Codex and GLM — Research

Phase 1 after [`prompts/01-explore.md`](../../../prompts/01-explore.md).
Measured on 2026-09-30 against `origin/main` at `1c708f7` (branch
`feat/stage-2-codex-glm`), unless a line names another commit. The sections
up to "Files a change would touch" state facts only. The last section, "Open
points for the phase 1a interview", carries options and recommendations
because the orchestrating session asked for them as input to the interview.

Nothing in this research was sent to Codex, GLM or any other foreign
endpoint, and neither was started with repository content. The only
commands run against them were `codex --version` and the local `--help`
texts. The leak-check figures below come from a local count that printed
numbers only, never a match and never a rule.

## Question

Can Coding Harness changes be reviewed by models from two other vendors
before the merge — Codex (OpenAI) for the spec review (phase 2a) and the
review (phase 6), GLM (Z.ai) in a short review loop before phase 6 — with
only framework content leaving the machine? What exists for it today, what
does the doctrine say, and how does the proposal relate to decision D-13
(the four criteria that open stage 2)?

## Input: what was decided and what is proposed

**Decided by the maintainer on 2026-09-30, relayed from the lakeswitch-ai
session** (recorded here as relayed, not heard in this session):

- Spec review (2a) on Codex, model `gpt-6.1-sol`, effort `max`.
- The same Codex agent runs the review (6), resumed with `codex exec resume`.
- Implement (4) on Sonnet 5.5, effort `medium`.
- A GLM 5.3 review loop (effort `max`) before phase 6; Sonnet adapts the
  code; at most 2 rounds.
- Codex reads GLM's findings only after it has given its own verdict.
- Kimi is dropped.
- Framework content only: customer code goes to neither vendor.

**Proposed, not approved:** the one-page plan handed over with that decision
(five work packages, one change, one pull request, appetite 6 hours; it lives
outside this repository) and its addendum of four points — routing by change
class, measuring the first three stage-2 runs, an evidence rule for review
findings, one condition per acceptance criterion. Each is taken up below.

Before creating this folder: `plans/specs/` is empty; `rg -i
"codex|glm|kimi|stage 2|leakcheck"` over `plans/changes/` finds no artefact
about stage 2. `scripts/new_change.py` listed nine "possibly related" files
by name overlap; the matches in `omnigent-deny-layers` name Codex only as one
of the harnesses Omnigent drives, none is about stage 2.

## What exists today

### 1 · The doctrine: stage 2 as written

- **Header note** (`docs/WORKFLOW.md`, top): "stage 1 is binding. Stages 2
  and 3 are prepared, not active." The "Not all of it is here yet" note
  lists, among others, `scripts/run_change.sh`, the `scripts/cc-*.sh`
  profiles, `tests/test_model_profiles.py`, `templates/findings.md` and
  `templates/plan-marking.md` as named but absent.
- **§4 "Stage 2 — adding GLM and Kimi (prepared, not active)"**: "Exactly two
  rows of the routing table change: implement moves from Sonnet 5 to GLM,
  review from Fable 5.1 to Kimi." Mechanics: six `scripts/cc-*.sh` profiles
  over one shared base, every `ANTHROPIC_*` variable set explicitly,
  `make leakcheck NAME=<change>` as "the barrier without which nothing runs",
  the denylist outside the repository and BLOCK when it is missing, plan
  markings `[FLASH]`/`[GLM5.3]`/`[SONNET]` read by `scripts/run_change.sh`.
  The closing caveat: subscriptions are limited to officially supported
  tools, and "whoever switches stage 2 on checks beforehand what stands in
  `spec.md` and `plan.md`".
- **The proposal changes GLM's role.** §4, `model-endpoints.yaml` (GLM
  `bemerkung`: "Vorgesehen fuer Phase 4 (Umsetzung)") and `prompts/03-plan.md`
  ("Model markings (stage 2 only)") all give GLM the implementation. The
  decided flow gives GLM a review loop and keeps implementation on Sonnet.
  After the change, all three would contradict the flow unless rewritten.
- **§3 "Model routing"** (stage 1): 2a and 6 on Fable 5.1, 4 on Sonnet 5.
  "One reviewer for both": phase 6 resumes the session of phase 2a
  (`--session-id` there, `--resume` here; the id stands in `findings.md`),
  and "The spec review improves the spec first" (maintainer, 2026-09-29).
  "Escalation. After two failed review rounds, move up to Fable."
- **§3 "What deliberately does not happen in stage 1"**: "No
  `ANTHROPIC_BASE_URL`, no router, no gateway."
- **§6 "The order"**: "Process, then model diversity, then orchestration."
  "Stage 1 must have run for two to three weeks in real use. The signal to
  move on: the phase gates hold without anyone thinking about them, and the
  Sonnet implementation is the noticeable cost." §6 does not carry D-13's
  four criteria (see §4 below).
- **§8, row "`ln -s AGENTS.md CLAUDE.md`"**: Claude Code's direct reading of
  `AGENTS.md` "fails with telemetry switched off, Bedrock/Vertex or an own
  `ANTHROPIC_BASE_URL` — then Claude Code reads nothing". A GLM session runs
  with its own `ANTHROPIC_BASE_URL`. Stated in the doctrine, not measured in
  this research.
- **The findings process** (§2): the table form lives in
  `templates/findings.md` (absent here); columns in use
  (`plans/changes/omnigent-deny-layers/findings.md`): ID, Severity,
  Dimension, Origin, Where, Finding, Status — no column naming which
  reviewer raised a finding. "Two consecutive rounds of `fix-r` origin are an
  escalation, not a third round." "Disagreements are recorded, not
  resolved."

### 2 · The phase prompts

- `prompts/02a-spec-review.md`: model Fable 5.1; input `spec.md`,
  `research.md`, `decisions.md`, not the author's reasoning; three questions
  (two readings → `[AMBIGUITY]`; holes; criteria that cannot go red); the
  session is started with a fixed id (`claude --model claude-fable-5-1
  --session-id <uuid>`) written under the table in `findings.md`.
- `prompts/06-review.md`: model Fable 5.1; resumes the 2a session
  (`--resume <uuid>`); measures against the revised `spec.md`; dimensions
  `SPEC` and `MAINT` ("error handling, edge cases, contracts facing outward,
  security — finds what the spec is silent about"); "A finding already
  rejected in an earlier round may only reappear with new evidence
  attached."
- `prompts/04-implement.md`: model Sonnet 5; stop and report on a departure
  from the plan; a test with its counterpart for every change.
- `prompts/02-spec.md`: "Each [criterion] comes with what would refute it."
  No spec template exists (`templates/` holds `gate-record.yaml` and
  `handover.md` only); `scripts/validate_change_artefacts.py` does not exist
  (both measured by listing).
- `prompts/03-plan.md`: section "Model markings (stage 2 only)" with
  `[FLASH]`, `[GLM5.3]`, `[SONNET]`.

### 3 · The endpoint declaration

`model-endpoints.yaml` (German keys and comments; house rule 1 keeps the
translation of existing German for a pull request of its own):

- Data classes: `framework` ("dieses Repository … keine Residenzauflage"),
  `kundencode`, `kundendaten`.
- Endpoints: `anthropic-api`, `claude-code-plan`, `bedrock-claude` (models
  include `claude-sonnet-5`, `claude-opus-5-5`, `claude-fable-5-1` — **no
  Sonnet 5.5**); `glm-coding-plan` (Zhipu AI, `residenz: anbieter-erklaert`,
  `abrechnung: abonnement`, `darf_sehen: [framework]`, models `glm-5.3`,
  `glm-5.3-flash`); `kimi-code` (Moonshot AI, same shape, models `k3`,
  `kimi-for-coding`). **No OpenAI endpoint.** The file's rule: "Nicht
  gelistet ist BLOCK."
- The stage-2 comment: enforcement of `darf_sehen: [framework]` is "nicht
  durch diese Zeile, sondern durch `make leakcheck` vor jeder Sitzung an
  einem Fremdendpunkt".
- **The personal-use declaration** (section "Nutzungszweck"): both
  subscriptions above (GLM and Kimi) are declared personal use, "Stand
  2026-09-10: vom Eigentuemer erklaert". To be obtained again when the
  project is run commercially, `lakeswitch-ai` goes public, or a client pays
  for work that runs through these endpoints. On 2026-09-30 both
  `coding-harness` and `lakeswitch-ai` are private on GitHub (`gh repo view`).
  The ChatGPT subscription behind Codex is not covered.
- `ausgeschlossen:` entries carry `was`, `klasse`, `grund`; nothing tests
  their shape.

`tests/test_model_endpoints.py` (RB-A6) resolves every model named in
`.claude/agents/`, in the routing table of `docs/WORKFLOW.md` and in the
`**Model:**` line of each prompt against the declared model ids. Measured by
calling its helpers on 2026-09-30:

- A display name is turned into candidate ids by lower-casing and replacing
  spaces **and dots** with dashes: "GLM 5.3" → `glm-5-3`, "gpt-6.1-sol" →
  `gpt-6-1-sol`, "Sonnet 5.5" → `claude-sonnet-5-5`. With the ids spelled
  `glm-5.3` and `gpt-6.1-sol` (as the proposal and the file spell them), a
  prompt naming either model **does not resolve**, and the test goes red. So
  does "Sonnet 5.5" until `claude-sonnet-5-5` is listed.
- The routing-table regex matches only rows whose phase is a single digit
  and one word (`| 4 Implement |`); rows `1a`, `2a` are not checked. The
  prompt check covers `02a-spec-review.md` and `06-review.md`.

### 4 · Decision D-13 and its four conditions

- **Where it is recorded.** `docs/architecture/target-architecture.md` §9.1
  (interview of 2026-09-16, "Against the recommendation? no"): "Four measured
  criteria open stage 2 and thereby M2: ≥ 3 full seven-phase runs with
  metrics in coding-harness; lakeswitch's disclosure decision written; leak
  check green in every run; the foreign reviewer's endpoint declared with
  residency. Implement-phase cost is measured, not a switch." That document
  is `status: superseded`, but says "the decisions below remain a dated
  record until individual ADRs replace them". The current target
  (`docs/architecture/2026-09-17-omnigent-first-target.md`, `status:
  proposed`) carries D-13 forward as **Retain**. The implementation plan
  (`docs/architecture/2026-09-17-implementation-plan.md`, `status: proposed`)
  adds: "Real foreign-model calls still require every D-13 condition and
  instance permission, even in an optional trial", and "Foreign model calls
  are not permitted before D-13 qualification". It also says the three D-13
  runs "can use a fresh-context same-lineage reviewer". No ADR under
  `docs/adr/` (0001–0006) records D-13; `docs/WORKFLOW.md` §6 does not carry
  its numbers.
- **How an interview decision is amended here.** The gate
  `decision-continuity` (`decisions/gates.yaml`, `enforcement: block`,
  `floor: true`; `scripts/check_decision_continuity.py`) requires every
  decision D-1 to D-17 to appear in the current target's "Decision
  continuity" table, and every ADR in its hand-kept map `AMENDMENT_ADRS` to
  exist and to name the decision it amends. D-3, D-4, D-7 and D-17 were
  amended that way (ADRs 0001, 0003, 0004, 0006). D-13 is not in the map. An
  amendment of D-13 would follow the same path: an ADR naming D-13, its row
  in the table changed from "Retain" to "Amend", and a `"D-13"` entry in
  `AMENDMENT_ADRS`. The gate does not detect an "Amend" row without a map
  entry; the map is kept by hand.
- **Its coupling.** D-13 opens "stage 2 and thereby M2" — M2 being the
  Omnigent step "Feature and cross-vendor operation". The proposal runs stage
  2 without Omnigent, as separate CLI processes.
- **Criterion by criterion, on 2026-09-30:**

| # | Criterion | State | Evidence | What the proposal does |
|---|---|---|---|---|
| 1 | ≥ 3 full seven-phase runs with metrics in coding-harness | **not met** | Bead coding-harness-kw0 ("Stage-2 entry measurement") is open, depends on coding-harness-9qo (template bundle, open) and bo0 (closed). Its acceptance asks per phase for tokens, wall time, human minutes and gate outcomes, "generated rather than typed". No script in `scripts/` generates such metrics (`rg -i "wall time\|human minutes\|metrics"` found none). Changes that ran most phases (`frontmatter-current`, `omnigent-deny-layers`, the archived `reproducible-bead-export`) carry no metrics. | Nothing. Addendum point 2 (measure the first three stage-2 runs) measures *after* switching on, not before. |
| 2 | lakeswitch-ai's disclosure decision written | **not read** | Not found in this repository (`rg -i disclosure`). Not read in `lakeswitch-ai`. Its meaning is stated nowhere here beyond the name; by its wording it concerns lakeswitch content. | Nothing. "Framework content only" means lakeswitch content is not sent. |
| 3 | leak check green in every run | **not possible yet** | `make leakcheck` exists only as a stub that prints a message and exits 1 (`Makefile`, target `leakcheck`); its message says "see AGENTS.md", and `AGENTS.md` says nothing about a leak check. | Work package 2 ports the leak check; the runners refuse without a green one. |
| 4 | the foreign reviewer's endpoint declared with residency | **met for GLM, not for Codex** | `glm-coding-plan` is declared with `residenz: anbieter-erklaert`; no OpenAI endpoint exists. | Work package 1 declares `openai-codex`. The residency value is not stated in the proposal. |

- **Relation, as a fact:** the proposal satisfies criterion 4 and builds what
  criterion 3 needs. It does not satisfy criterion 1, and criterion 2 is
  unknown. Its work packages 3 and 4 each end in "one real run" — a real
  foreign-model call, which the implementation plan's wording does not permit
  before all four criteria hold. The maintainer's decision of 2026-09-30, as
  relayed, does not mention D-13.

### 5 · House rule 6 and "framework content only"

- `AGENTS.md`, house rule 6: "The customer instance is out of bounds … no
  filename, field name, entity or layer name from there appears in a
  framework artifact."
- What enforces "framework content only" today: the declaration
  (`darf_sehen: [framework]` for GLM) and nothing else in this repository.
  The leak check is a stub. `permissions.deny` in `.claude/settings.json`
  holds only Omnigent rules.
- **Local count against the denylist, 2026-09-30** (script in the session
  scratchpad, counts only; the denylist `~/.config/cc-routing/denylist.txt`
  exists, mode 600, 12 rules, its content not read):

| Scope | Size | Hit lines |
|---|---|---|
| tracked files at `1c708f7` | 160 files | 0 |
| `git log -p HEAD` | 200 commits, 42,981 lines | 0 |
| `tools/bd prime --hook-json` (what the project's SessionStart hook injects) | 6,482 bytes | 0 |
| `tools/bd list --all --json` | 47 issues (default limit not checked) | 0 |

A zero count says the 12 rules do not match; whether the 12 rules cover
every customer identifier was not read and cannot be judged here.

- **What a foreign agent can see beyond the change folder and the diff:**
  both runners, as proposed, start an agent with tools inside the worktree.
  It can read
  `AGENTS.md`, `docs/`, the git history and the tracker (through hooks, see
  §6 and §7). The leak check as ported from portfolio scans only
  `plans/changes/<name>/` and `git diff <base>...HEAD` (section 8). Whether
  the agents' sandboxes allow reading outside the worktree (sibling
  repositories) was not tested.

### 6 · Codex CLI on this machine

Measured on 2026-09-30 by `codex --version`, `codex exec --help`, `codex
exec resume --help`, `codex exec review --help`, and by reading key names in
`~/.codex/` (no session content, no memory content read):

- **Version** `codex-cli 0.159.2` (matches the proposal).
- **Model and effort.** The local model cache lists `gpt-6.1-sol` with
  efforts `low`, `medium`, `high`, `xhigh`, `max` and `ultra` ("Maximum
  reasoning with automatic task delegation"); its default effort is `low`.
  `~/.codex/config.toml` sets `model = "gpt-5.6-sol"` and
  `model_reasoning_effort = "xhigh"` — so a call that does not pin both runs
  on another model at another effort. That `gpt-6.1-sol` answers at `max` is
  the proposal's measurement, not repeated here.
- **stdin.** `codex exec` help: "If stdin is piped and a prompt is also
  provided, stdin is appended as a `<stdin>` block". Consistent with the
  proposal's `< /dev/null` for background shells; not re-run.
- **Resume.** `codex exec resume [SESSION_ID] [PROMPT]` exists, with `-m`,
  `-c`, `--json`, `-o`, `--ephemeral`, `--ignore-user-config`. It lists **no
  `-s/--sandbox` option** (`codex exec` has `-s read-only|workspace-write|
  danger-full-access`). Whether `-c sandbox_mode=…` works on resume, and
  whether model and effort carry over from the first call, was not tested.
- **Session id.** `codex exec` has no option to set the session id up front
  (Claude Code's `--session-id` has no counterpart). How the id is captured
  for `findings.md` (from `--json` events or the session files) was not
  tested. `--ephemeral` runs "without persisting session files" and would,
  by its wording, leave nothing to resume.
- **`codex exec review`** exists (`--base`, `--uncommitted`, `--commit`, a
  custom prompt). The proposal does not use it; whether it can continue a
  2a session was not tested.
- **What a Codex session in this repository loads besides the prompt:**
  - `AGENTS.md` (Codex's own convention; not measured in a run).
  - The tracked `.codex/config.toml` (`[features] hooks = true`) and
    `.codex/hooks.json`: four hooks (SessionStart on `startup|resume|clear`,
    UserPromptSubmit, PreCompact, PostCompact) that call `tools/bd
    codex-hook …` — tracker context. The user config holds hook-trust
    entries for the main checkout's path; whether the hooks run from a
    worktree path, and what `codex-hook` injects, was not tested.
  - `~/.codex/AGENTS.md`: not present.
  - `~/.codex/memories_1.sqlite` exists. Whether the memory feature is on
    and what it would add to a prompt was not read. 27 session files exist
    under `~/.codex/sessions`; none was started in the customer instance
    (their recorded working directory), 15 mention its repository name.
- **Login.** The proposal says ChatGPT login; `~/.codex/auth.json` exists
  (not read).

### 7 · GLM through Claude Code on this machine

- The proposal: a separate `claude -p` process against
  `https://api.z.ai/api/anthropic`, key `GLM_KEY` from
  `~/.config/cc-routing/secrets.env`, empty `CLAUDE_CONFIG_DIR` so the
  maintainer's global instructions and hooks stay home. `glm-5.3` and
  `glm-5.3-flash` answer (proposal's measurement). **Not tested: whether
  Z.ai honours effort `max`.**
- Measured here: `secrets.env` exists (mode 600, 4 non-comment lines, not
  read). Claude Code is `2.1.285`; its help lists `--effort
  low|medium|high|xhigh|max`, `--bare` ("skip hooks … LSP, plugin sync"),
  `--setting-sources user,project,local`, `--disallowedTools`,
  `--session-id`, `--resume`, `--permission-mode` (`acceptEdits`, `auto`,
  `bypassPermissions`, `manual`, `dontAsk`, `plan`).
- An empty `CLAUDE_CONFIG_DIR` keeps the user's hooks out, not the
  project's: `.claude/settings.json` has a SessionStart hook
  `tools/bd prime --hook-json`, so the tracker context reaches a GLM session
  unless hooks are skipped (0 hits in the count above).
- Per `docs/WORKFLOW.md` §8, a session with its own `ANTHROPIC_BASE_URL`
  does not read `AGENTS.md`; the reviewer's prompt would have to carry what
  it needs. Not measured.

### 8 · The pieces in portfolio-agentic-engineering (read-only)

Read at `20a279c` (2026-09-23). The four files were last changed on
2026-09-13 (`5f99f0b`), not 2026-09-10 as the proposal says;
`_cc-common.sh` and `cc-glm.sh` are commented in English, `leakcheck.py`
and its tests in German.

- `scripts/_cc-common.sh` (69 lines): loads `secrets.env` (override
  `CC_SECRETS`); `run_cc <base> <token> <model> <small> [prompt]` sets every
  `ANTHROPIC_*` variable explicitly (base URL removed when empty) and starts
  `claude -p "<prompt>" --permission-mode acceptEdits` headless, else
  interactive; `require_leakcheck` refuses without `CC_CHANGE` and runs
  `make leakcheck NAME=<change>`. It does **not** set `CLAUDE_CONFIG_DIR`,
  and `acceptEdits` lets the model edit files — for a reviewer, both differ
  from the proposal.
- `scripts/cc-glm.sh` (11 lines): requires `GLM_KEY`, calls
  `require_leakcheck`, runs `glm-5.3` (override `GLM_MODEL`) for phase 4.
- Siblings not in scope: `cc-claude.sh`, `cc-sonnet.sh`, `cc-glm-flash.sh`,
  `cc-kimi.sh`, `cc-kimi-k3.sh`, `run_change.sh`.
- `scripts/leakcheck.py` (257 lines): scans every non-binary file under
  `plans/changes/<name>/` and `git diff <base>...HEAD`. Default base from
  `git symbolic-ref refs/remotes/origin/HEAD` (here: `origin/main`,
  measured), fallback `origin/master`. BLOCK on a hit; on a missing, empty,
  unreadable or invalid denylist; on a missing or empty change folder; on an
  unreadable file; on an undeterminable diff. It reports file, line, rule
  name, match length and character class — never the match. It imports
  `_verdict.Verdict` and uses `block`, `info`, `render`, `exit_code`; all four
  exist in this repository's `scripts/_verdict.py`. Not covered by its
  design: uncommitted changes (the diff is commit-to-commit), and anything
  the agent reads on its own.
- `tests/test_leakcheck.py` (188 lines, 12 tests): clean passes; planted
  secret blocks; the output never carries the secret or a part of it;
  missing, empty or broken denylist blocks; missing or empty change blocks;
  the diff is scanned; the CLI scans the diff without `--base`; an unusable
  base blocks; the CLI returns the exit code. Five tests assert German
  message substrings ("sauber", "fehlt", …) and change with a translation.
- portfolio's `Makefile` target: `leakcheck` needs `NAME`, passes `BASE`.

### 9 · The overlapping change `feat/harness-decide-adr` (not merged)

Read with `git show origin/feat/harness-decide-adr:<path>` at `1c161d0`; no
pull request is open for it on 2026-09-30 (`gh pr list`).

- It adds to `docs/WORKFLOW.md` §2 "Change classes, the ADR question and
  decision pull requests": four classes `spike`, `bounded`, `feature`,
  `architectural` in the spec header; only a `feature` owes an answer to the
  ADR question (`decisions/answers/<change>/adr.yaml`, gate `adr-answers`);
  an `architectural` change "carries its ADR already, so it is not asked".
  Its interview decided "No further class duties" (Q3). "Nothing checks
  that the class is right." It does not touch §3's routing table or §4.
- **Decision pull request** = one that "adds, changes or removes a file
  `provenance.yaml` reserves for `human-decided` — an ADR, an ADR answer, the
  rule set". `model-endpoints.yaml` has no entry in `provenance.yaml`
  (measured), so a change to it alone is not a decision PR by that
  definition; a new ADR under `docs/adr/` makes one.
- It adds house rule 8 to `AGENTS.md` (merge only on the maintainer's
  request), ask rules for merge commands to `.claude/settings.json`, the gate
  `adr-answers` to `decisions/gates.yaml` and `ci.yml`, entries to
  `scripts/kit/manifest.yaml`, a paragraph to `prompts/02-spec.md` (class and
  `adr_question` in the header), "The merge" to `prompts/07-commit.md`.
- The proposal's "decision PR (label `decision`, title `decide(<scope>):
  …`)" depends on this branch being merged.
- No new ADR on that branch; `docs/adr/` ends at 0006 on both.

### 10 · Repository bookkeeping a new script meets

- `scripts/kit/manifest.yaml`: "eine nicht klassifizierte Datei ist ein
  BLOCK"; each new script and test needs a role (`mechanismus` or
  `bestand`). `scripts/kit/probe.py` caps its `REIST_NICHT` list at
  `DECKEL = 32`.
- `scripts/ci_gates.py`, `OHNE_AUFRUFER`: a script without a CI step needs an
  entry with a reason (`tests/test_ci.py` holds it). A leak check that must
  not run in CI (its denylist is outside the repository) is such a script.
- `scripts/export/manifest.yaml`: prefix verdicts for what travels to
  lakeswitch-ai; `model-endpoints.yaml` travels as an empty shell
  (`geruest`); everything unlisted is `drop`.
- `provenance.yaml`: `prompts/`, `tests/`, `templates/` are `human-written`;
  `docs/adr/` is `human-decided`; `docs/WORKFLOW.md`, `plans/` allow
  `ai-drafted-reviewed`; `model-endpoints.yaml` and `scripts/` are unmapped.

### 11 · The tracker

- Bead coding-harness-bc9 ("Stage 2: Codex and GLM review Coding Harness
  changes before the merge"): feature, P2, in progress, claimed by
  `coding-harness-e0`; related to coding-harness-kw0.
- Bead coding-harness-kw0 (the D-13 entry measurement): task, P2, open.
- Bead coding-harness-9qo (template bundle: spec template with class and
  Definition of Done, design phase 2b, findings and plan-marking templates):
  task, P1, open.

## What is unclear

Each is sorted by the question protocol; the list of open points below
repeats them with their weight.

1. Whether the maintainer's decision of 2026-09-30 was meant to amend D-13,
   or to be built and switched on only once D-13 holds. **[DECISION]**
2. The model id of Sonnet 5.5 (`claude-sonnet-5-5` by the file's pattern)
   — not verified. **[GAP]**
3. The residency value for a ChatGPT-subscription Codex endpoint, and the
   account's data-use setting — vendor documentation and the account, not
   this repository. **[GAP]**
4. Whether Z.ai honours `--effort max`. **[GAP]** (needs one run, after the
   leak check exists)
5. Codex on resume: sandbox, model, effort; the session-id capture;
   memories; hooks from a worktree; read scope of the sandbox. **[GAP]**
6. What lakeswitch-ai's disclosure decision is and whether it is written.
   **[GAP]** (lakeswitch-ai not read)
7. The study behind addendum point 2 (arXiv 2607.21656) — not read; its
   figures are the addendum's.

## Files a change would touch

Measured against `1c708f7`; ✱ marks a file `feat/harness-decide-adr` also
changes.

| File | What would happen there |
|---|---|
| `model-endpoints.yaml` | add an OpenAI/Codex endpoint (`darf_sehen: [framework]`, residency, `abonnement`, official Codex CLI only); move Kimi to `ausgeschlossen` with date and reason; GLM's `bemerkung` from phase 4 to the review loop; add `claude-sonnet-5-5`; the personal-use declaration for the ChatGPT subscription; model ids that resolve (dots, see §3) |
| `tests/test_model_endpoints.py` | only if the id resolver changes instead of the ids |
| `scripts/leakcheck.py`, `tests/test_leakcheck.py` | new: ported from portfolio, in English |
| `Makefile` | the `leakcheck` stub becomes the real target |
| `scripts/codex-review.sh` (name per plan) | new: the Codex runner for 2a and 6 |
| `scripts/cc-glm.sh`, `scripts/_cc-common.sh` (names per plan) | new: the GLM review-loop runner |
| `docs/WORKFLOW.md` ✱ | header note, "Not all of it is here yet", §3 routing table and "One reviewer for both", §4 rewritten (Codex and GLM, Kimi gone), §6 or §4 the D-13 relation |
| `prompts/02a-spec-review.md`, `prompts/06-review.md` | model line and session commands for Codex; the order Codex verdict, then GLM findings |
| `prompts/04-implement.md` | model line Sonnet 5.5 |
| a new prompt for the GLM loop (e.g. `prompts/04b-…`) | new phase text, and a row in the phase table |
| `prompts/03-plan.md` | the "Model markings (stage 2 only)" section no longer matches |
| `docs/adr/0007-…md` | new, if the ADR is decided |
| `docs/architecture/2026-09-17-omnigent-first-target.md`, `scripts/check_decision_continuity.py` | only if D-13 is amended: its continuity row to "Amend", and `"D-13"` into `AMENDMENT_ADRS` |
| `scripts/kit/manifest.yaml` ✱, `scripts/ci_gates.py` (`OHNE_AUFRUFER`), possibly `scripts/export/manifest.yaml` | classify each new script and test |
| `decisions/answers/stage-2-codex-glm/adr.yaml` | only if the class is `feature` and the other branch is merged |
| `AGENTS.md` ✱ | possibly one line where the leak check is named (the Makefile stub points there) |
| `.claude/settings.json` ✱ | only if a direct `codex` call outside the runner is to be asked or denied |

Not touched by this change as proposed: `prompts/02-spec.md` ✱ (unless the
EARS-lite sentence comes in), `prompts/07-commit.md` ✱,
`decisions/gates.yaml` ✱ and `ci.yml` ✱ (the leak check does not run in CI).

## Size

- The proposal: 6 hours, one session, five work packages.
- Measured additions since: the id resolver (§3), Sonnet 5.5's id, the
  English port and a scan of uncommitted changes (§8), a read-only reviewer
  instead of `acceptEdits` (§8), session-id capture and resume flags for
  Codex (§6), the ADR, the manifest and `OHNE_AUFRUFER` bookkeeping (§10),
  and the `03-plan.md` markings section.
- **Estimate: about 9–11 hours, two sessions.** Endpoint and tests 0.75 h;
  leak check 2 h; Codex runner 2 h; GLM loop 2 h; doctrine and prompts 2 h;
  ADR and bookkeeping 1–1.5 h. Real runs are extra and depend on the D-13
  answer.
- **Smallest useful version (about 5–6 hours):** endpoint declaration, the
  leak check, the Codex runner for 2a and 6 as one agent, the ADR, and the
  doctrine for Codex. The GLM loop follows as a change of its own. Smaller
  still, and sending nothing (about 3.5 hours): endpoint, leak check and ADR
  only — the barrier without the capability.

## Open points for the phase 1a interview

Recommendations here were requested by the orchestrating session; the facts
they rest on are above. Scope-changing decisions first.

### [DECISION] 1 · How this change relates to D-13

- **Goal:** decide whether review by other vendors may start before D-13's
  four criteria hold.
- **Options:**
  1. *Amend D-13 in this change's ADR, for framework content.* Criteria 3
     (leak check) and 4 (declared endpoint) stay hard, and the runners
     enforce them on every call. Criterion 2 is stated to govern
     lakeswitch-ai content, which this change never sends. Criterion 1 is
     replaced by measuring the first three stage-2 runs (addendum point 2)
     with a stop rule. Consequence: real calls start with this change; bead
     coding-harness-kw0 is re-scoped; "process first, then diversity"
     (WORKFLOW §6) is knowingly shortened.
  2. *Build now, switch on later.* Everything is built and tested offline;
     no real call until kw0 has three measured runs and the disclosure
     decision is written. Consequence: the capability waits on kw0, which
     waits on the template bundle (9qo) and on a metrics generator that does
     not exist yet; the "one real run" acceptance moves to the switch-on.
  3. *Build and run without touching D-13.* Consequence: the architecture
     documents and the practice contradict each other — a `[DIVERGENT]`
     finding at review.
- **Recommendation:** option 1 — the two criteria that protect data stay
  hard and become enforced rather than written; the two that measure
  readiness are the ones the maintainer's routing decision already
  answered in substance.
- **If "ok":** ADR 0007 records the amendment with its date and is mapped
  for D-13 in the gate `decision-continuity`; the runners
  refuse without a green leak check and a declared endpoint; the first three
  runs are recorded (see decision 5).
- **What is lost:** the measured stage-1 baseline before any foreign call.

### [DECISION] 2 · One change or two

- **Goal:** fix the scope of this pull request.
- **Options:** 1. all five work packages in one change (about 9–11 h, two
  sessions); 2. the smallest useful version now (endpoint, leak check, Codex
  for 2a and 6, ADR, doctrine; about 5–6 h), the GLM loop as its own change;
  3. the barrier only (endpoint, leak check, ADR; about 3.5 h).
- **Recommendation:** option 2 — the Codex half delivers the decided review
  path on its own, and the GLM loop adds the open questions about effort and
  permissions that one change should not carry together.
- **What is lost:** the GLM loop arrives in a second pull request.

### [DECISION] 3 · Stage 2 by change class (addendum point 1)

- **Goal:** decide whether the class chooses how much of stage 2 runs.
- **Options:** 1. in this change, doctrine only: one table (spike and
  one-sentence changes: nothing; bounded: GLM loop only, review on Fable;
  feature and architectural: Codex 2a, GLM loop, Codex 6), nothing enforces
  it; 2. later, its own change; 3. not at all — every stage-2 change runs
  the full path.
- **Facts that bear on it:** the class field exists only on the unmerged
  branch; its interview decided "no further class duties"; nothing checks
  that a class is right, so a feature marked bounded skips Codex.
- **Recommendation:** option 1, after `feat/harness-decide-adr` merges —
  one table, no gate, and the misclassification risk stated beside it.

### [DECISION] 4 · The ADR (proposal: yes)

- **Goal:** decide whether this change records its decision as an ADR.
- **Options:** 1. yes, ADR 0007: where framework content may flow, Kimi
  dropped, the D-13 relation — the pull request becomes a decision PR
  because it adds a file under `docs/adr/`; 2. no ADR: the decision lives in
  `model-endpoints.yaml` and the doctrine, and the pull request is an
  ordinary one (that file is not `human-decided`).
- **Recommendation:** option 1 — every earlier amendment of an interview
  decision went through an ADR that the gate `decision-continuity` maps
  (D-3, D-4, D-7, D-17); amending D-13 by prose alone would be the silent
  rewrite that gate exists to catch. If decision 1 is option 2, the ADR
  still records the routing and Kimi's removal.

### [DECISION] 5 · Measuring the first three stage-2 runs (addendum point 2)

- **Goal:** decide what is recorded and what stops stage 2.
- **Options:** 1. in this change: per finding, reviewer, taken or rejected,
  and whether a taken finding turned a green test red; after three runs a
  short evaluation, and stage 2 falls back to Fable if taken findings broke
  tests; 2. leave it to kw0.
- **Recommendation:** option 1 if decision 1 is option 1 (it then is the
  replacement for criterion 1); otherwise option 2.

### [DECISION] 6 · The personal-use declaration for the ChatGPT subscription

- **Goal:** cover the use of the ChatGPT subscription for this repository.
- **Options:** 1. declare personal use, dated 2026-09-30, with the same three
  expiry conditions as the GLM declaration; 2. use a token-billed OpenAI API
  key instead — no subscription question, paid per call, and not through the
  ChatGPT login the proposal measured; 3. do not declare — Codex stays
  unusable.
- **Recommendation:** option 1, and record the account's data-use setting
  beside it (not read here).

### [DECISION] 7 · The evidence rule for review findings (addendum point 3)

- **Goal:** decide when Sonnet takes a Codex or GLM finding.
- **Options:** 1. as written — taken only when a test demonstrates it or the
  spec supports it, otherwise rejected with a reason; 2. not now.
- **Fact that bears on it:** `MAINT` findings are by definition those the
  spec is silent about, so under option 1 each needs a test; a `MAINT`
  finding no test can show (a documentation gap, a security posture) is
  rejected.
- **Recommendation:** option 1, applied to every repair round, with that
  consequence written beside the rule; rejected findings stay in
  `findings.md` as disagreements.

### [DECISION] 8 · Sonnet 5.5 for implement: stage 2 only, or everywhere

- **Goal:** settle which changes implement on Sonnet 5.5 at `medium`.
- **Options:** 1. every change (same vendor, same data class, one routing
  table); 2. stage-2 changes only.
- **Recommendation:** option 1 — as with the 2026-09-29 routing decisions,
  which held for the whole repository.

### [DECISION] 9 · One condition per acceptance criterion (addendum point 4)

- **Goal:** confirm where the EARS-lite sentence goes.
- **Recommendation:** not in this change — it touches `prompts/02-spec.md`,
  which the other branch also edits, and belongs with the spec template
  (bead coding-harness-9qo) or a small change of its own after that merge.

### [GAP]s — answer by reading or measuring, not by asking

- Sonnet 5.5's model id.
- The residency value to declare for Codex under a ChatGPT subscription
  (vendor documentation).
- Whether Z.ai honours `--effort max` (one run after the leak check).
- Codex: sandbox and effort on `exec resume`; how the session id is
  captured; whether memories are on and what they inject; whether the
  tracked `.codex/hooks.json` runs from a worktree; whether the read-only
  sandbox reads outside the worktree.
- lakeswitch-ai's disclosure decision (read in that repository).
- The study behind addendum point 2.

### [DETAIL]s — the agent decides and writes the reason down

- Model ids that resolve in `tests/test_model_endpoints.py`: list the dashed
  form, or teach the resolver dots — one of the two, reason in the plan.
- The ported leak check scans uncommitted changes too, or the runner
  refuses a dirty tree.
- The GLM reviewer runs without write permission, and without project and
  user hooks (`--bare` or `--setting-sources`), with the house rules in its
  prompt because it does not read `AGENTS.md`.
- Codex model and effort pinned on every call, `< /dev/null` in background
  shells, no `--ephemeral`.
- GLM's findings stay where Codex cannot read them until Codex's verdict is
  written, since Codex can read the whole worktree.
- A reviewer column (Codex, GLM, Fable) in `findings.md`; the escalation
  target when the reviewer is Codex ("move up to Fable" today).
- New values in `model-endpoints.yaml` in English inside the German-keyed
  schema; the translation of the rest stays a pull request of its own.
- ADR number 0007; kit manifest, `OHNE_AUFRUFER` and export-manifest
  entries; the `03-plan.md` markings section marked retired or rewritten.
- The change's class (`architectural` carries its ADR; `feature` answers
  the ADR question) follows decision 4.

## Corrections after verification

Phase 2, 2026-09-30, against `origin/main` at `ba940fb` unless a line names
another commit. Where these lines disagree with the text above, they hold.

1. **Pull request #54 is merged.** Section 9 read `feat/harness-decide-adr`
   at `1c161d0` when no pull request was listed. The branch was then opened
   as pull request #54 and merged on 2026-09-30 at 14:55 UTC (merge commit
   `ba940fb`); the merged tree equals the branch tip `76c8239` (`git diff
   origin/feat/harness-decide-adr origin/main` is empty). This branch still
   stands on `1c708f7` and does not contain it.
2. **The kit probe's exception list is full.** Section 10 gives `DECKEL =
   32`. On `origin/main` the cap is 31 (lowered on 2026-09-30) and
   `REIST_NICHT` in `scripts/kit/probe.py` holds exactly 31 entries. Eight of
   them are parametrised ids of `tests/test_model_endpoints.py` that carry a
   prompt's file name and model display name (for example
   `[04-implement.md-Sonnet 5]`); a changed model line changes its id, and a
   new prompt with a model line adds one entry.
3. **The model lists differ per endpoint.** Section 3 groups them. In
   `model-endpoints.yaml`, `bedrock-claude` lists only `claude-opus-5` and
   `claude-sonnet-5`; `claude-opus-5-5` and `claude-fable-5-1` stand in
   `anthropic-api` and `claude-code-plan` only.
4. **Files a change would touch.** `prompts/02-spec.md` is touched
   (decisions.md, answer 9). `decisions/answers/stage-2-codex-glm/adr.yaml`
   is not needed: the change carries its ADR, so its class is
   `architectural`, which the gate `adr-answers` does not hold to an answer.
5. **The routing-table check needs the model name alone in bold.** Its
   pattern reads the whole bold text of the second cell as the display name;
   a cell such as `**Codex gpt-6.1-sol**` would be read as one name and not
   resolve.

## Gaps closed in phase 2

Read on 2026-09-30. Nothing was sent to Codex or GLM; neither was started.

1. **Sonnet 5.5's model id is `claude-sonnet-5-5`.** Source: the Claude API
   reference bundled with Claude Code 2.1.285 (its model table, cached
   2026-09-25): "Claude Sonnet 5.5 | `claude-sonnet-5-5`", effort levels
   `low` to `max`, default `high`. The same table confirms `claude-opus-5-5`
   and `claude-fable-5-1`.
2. **Codex under a personal ChatGPT plan: residency is declared by the
   provider, not selectable.** OpenAI's own pages (help.openai.com,
   openai.com) answered a direct fetch with HTTP 403, so the pages were not
   read; what follows rests on search-result summaries of them. Data
   residency is offered to eligible ChatGPT Enterprise, Edu, Healthcare and
   API customers, not to personal plans. The Europe privacy policy names
   OpenAI Ireland Limited as the controller for the EEA and states that
   personal data is processed and stored in the United States and where
   OpenAI's affiliates and service providers are, under Standard Contractual
   Clauses. On a personal plan the setting "Improve the model for everyone"
   also applies to Codex tasks. The value that fits the file's vocabulary is
   `residenz: anbieter-erklaert`, as for GLM.
3. **Codex non-interactive mode** (learn.chatgpt.com/docs/non-interactive-mode,
   the page `developers.openai.com/codex/noninteractive` redirects to, read
   directly): `--json` turns stdout into JSON Lines; the event
   `thread.started` carries `thread_id`; `codex exec resume <SESSION_ID>`
   continues a run, and the page does not say which settings carry over;
   `codex exec` runs in a read-only sandbox by default; `--ephemeral` does not
   persist session files; `-o <path>` writes the final message to a file;
   `--ignore-user-config` skips `$CODEX_HOME/config.toml`.
4. **A resume can silently start a new thread.** openai/codex issue 15538
   (closed, no fix named): resuming a session started with `--ephemeral`
   produced a different `thread_id` and no prior context, without an error.
   A runner that compares the resumed `thread_id` with the recorded one sees
   this; one that does not, cannot.
5. **Codex's read-only sandbox reads the whole disk.** Search results (openai/codex
   issue 7657 and a write-up of the sandbox) say the sandbox limits writes
   and network, not reads. The current documentation
   (learn.chatgpt.com/docs/permissions, read directly) describes permission
   profiles with `deny` rules for reads (`default_permissions`,
   `[permissions.<name>.filesystem]`). Whether Codex CLI 0.159.2 supports
   them on macOS was not measured.
6. **The customer instance is on this disk.** Its checkout sits beside the
   other repositories in the maintainer's home directory (existence checked
   with `ls`; nothing in it was read). A reviewer that can read the whole
   disk can reach it.
7. **lakeswitch-ai's disclosure decision is not written.** At lakeswitch-ai
   `09c9d62`, `docs/workflow.md` §4 says that sending specification prose, a
   plan derived from it or a diff over `src/` to a third-party endpoint is a
   disclosure, and that before stage 2 is switched on somebody decides, as a
   recorded decision, which trees may leave. `git grep -i disclosure` finds
   no such record. It concerns lakeswitch-ai's own trees, as answer 1 of
   `decisions.md` reads criterion 2.
8. **The implementation plan already names the stop rule's direction.**
   `docs/architecture/2026-09-17-implementation-plan.md`, M2: "reviewer
   regressions revert to the qualified same-lineage path while the cause is
   resolved" — the same direction as answer 5 (fall back to Fable).
9. **D-16 and model names.** The target's continuity row for D-16 retains
   "No fixed model names in doctrine"; `docs/WORKFLOW.md` §3 has named models
   since before this change. A fact for the reader, not a gap this change
   closes.

Still open, carried to the plan: whether Z.ai honours effort `max`; which
settings carry over on `codex exec resume`; how Codex hooks and memories are
switched off and shown to be off; whether the reviewers' reads can be
confined to the worktree. The study behind the addendum's point 2 stays not
read; answer 5 of `decisions.md` does not rest on its figures.
