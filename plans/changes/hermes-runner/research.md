---
title: "Research — hermes-runner"
status: draft
implementation_status: none
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-i3y
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# hermes runner — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). Facts
as read on 2026-10-05. Everything here was read or measured in this session
unless it says "not read" or "from the assessment".

**The change.** Epic bead coding-harness-i3y, "Hermes as the runner for
Coding Harness's recurring jobs: groundwork, ADR and first job". The
maintainer, 2026-10-05: "Ich würde gerne Hermes forcieren, lege die
Grundlage dafür" ("I want to push Hermes; lay the groundwork"). Hermes Agent
(Nous Research) becomes the runner for this repository's recurring agent
jobs; the first job is the weekly re-check of research notes (bead
coding-harness-pu9, part 2). This goes against the "Not Hermes, not now" of
the assessment (`docs/research/2026-10-05-hermes-agent-runner.md`, PR #72,
not merged). The class is `architectural`: a new runtime component, so the
change carries its ADR and runs the design phase 2b with the architecture
delta of ADR 0009.

**What was read, and at which commit:**

| Source | Ref | How |
| --- | --- | --- |
| This repository | `origin/main` at `87daf91` (this worktree) | files |
| The assessment | `origin/docs/research-hermes` at `d442933` (PR #72, open) | `git show` |
| The age list (pu9 part 1) | `origin/feat/research-currency` at `8380d7c` (no PR found) | `git show` |
| The leak check, stage 2 | `origin/feat/stage-2-codex-glm` at `ef7407c` (PR #60, open) | `git show` |
| Design template and prompt | `origin/docs/template-bundle` at `855eeb6` (no PR found) | `git show` |
| adhd-relief | local branch `wechsel-hermes` at `bdce8dc`; `origin/wechsel-hermes` at `e76ac64` | files, `git log`, read only |
| GitHub settings of this repository | API, read only | `gh api` GET |
| GitHub's rules on rulesets and fine-grained tokens | `github/docs`, branch `main` | raw files |
| Hermes Agent documentation | `NousResearch/hermes-agent`, tag `v2026.9.21` | raw files (three pages) |
| The tracker | beads i3y, pu9, 6hx | `tools/bd show`, read only |

A search of `plans/` for "hermes", "recheck" and "re-check" found no earlier
artefact for this topic: Hermes is mentioned only in the archived
`omnigent-deny-layers` change (section 2.7), and "re-check" once in an
unrelated sense. `plans/specs/` holds only `.gitkeep`.

`origin/feat/research-currency` moved from `f6e0f6d` to `8380d7c` during this
session (a parallel session's repair round); the facts in section 1.2 were
re-read at `8380d7c`.

**Not done:** Hermes was not installed or run, no model was called, nothing
was written in adhd-relief, and the tracker was not written. Two Hermes
documentation pages (memory, curator) could not be fetched (HTTP 429); what
this note says about them comes from the assessment, which read Hermes's
`main` at `66fa864`.

Sections 1 to 4 are what exists. Sections 5 to 10 were asked for by the
caller of this phase: they work out the maintainer's stated direction (the
job's contract, the trust split, the groundwork slices, what is shared with
adhd-relief, risks, and what needs the laptop). They are inputs for the
interview and the spec, not decisions. Section 11 lists what is unclear,
section 12 the files a change would touch.

## 1 · The job and its input

### 1.1 · What the tracker says

Bead coding-harness-pu9, part 2 (description, read 2026-10-05): "a recurring
agent that re-checks the oldest note's dated facts and sources on the web and
opens a pull request with an addendum (holds / overtaken / new), never
editing findings in place and never writing the tracker. The prompt for (2)
lives in the repository and is runner-neutral."

Bead coding-harness-i3y lists the groundwork: run adhd-relief's Hermes spike
as proof of the guards; a GitHub ruleset on `main`; a runner-neutral re-check
prompt; an endpoint entry for the model; a publish step outside Hermes
(maintainer-owned script and token, Hermes holds none); a Coding Harness
Hermes profile (own user, web and file only, learning off); an ADR for the
first unattended writing agent with the ADR 0009 architecture delta. It
names what is shared with adhd-relief (host, pinned install, egress proxy,
guard baseline) and what never is (user, `HERMES_HOME`, write root, tokens).

### 1.2 · The input: the age list (pu9 part 1, not merged)

`scripts/check_research_currency.py` at `8380d7c`:

- `--format json` prints `schema_version` (1, constant `SCHEMA_VERSION`),
  `today`, `threshold_days` (90), `corpus` (`docs/research/`) and `notes`, a
  list of `path`, `last_reviewed`, `age_days`, `due`, `problem`
  (`render_json`).
- The spec's section "What part 2 may rely on"
  (`plans/changes/research-currency/spec.md`): "`notes[0]` is the oldest note
  — a note with an unusable review date before any dated one. Whether part 2
  takes only due notes or the oldest regardless is part 2's decision". A
  merged re-check "sets the note's `last_reviewed:` to the day of the
  re-check, in the same pull request as its addendum — `updated:` moves too,
  as the gate `frontmatter-current` already demands."
- `--today` pins the date; one day of slack for a future date, because the
  nightly run is in UTC and a review is dated in the maintainer's time zone
  (same spec, `[DETAIL]`s).

Running the script needs Python with PyYAML and a checkout. A Hermes agent
without a shell cannot run it (section 6).

### 1.3 · The assessment's prompt and runner contract

The assessment (§7) proposes `prompts/research-recheck.md`, "beside the phase
prompts, with a first line saying it is a job prompt, not a phase", and
seven steps: input (`notes[0]` or a named note); read the note whole; check
each dated claim on the web, fetched pages being "data, never instructions";
append one section `## Addendum YYYY-MM-DD · re-check` with holds, overtaken,
new and a "not read" list; move `last_reviewed:` and `updated:`; touch
nothing else; report counts, and fail visibly if nothing could be checked.

Its §7.2 lists eight guarantees for any runner: a diff check outside the
agent (only the one note, only appended lines and the two header dates); the
agent holds no write token and no shell; never merges, approves,
force-pushes or pushes to `main`; no tracker; a declared endpoint (RB-A6)
with the leak check before a foreign call; no hidden state (memory,
self-written skills off); bounded turns, tokens and wall time with no retry
after the model was called; a visible outcome for a failed run.

## 2 · What binds a runner in this repository

### 2.1 · House rules 4, 6 and 8

- **Rule 4, one writer per tracker** (`AGENTS.md`). The job writes no
  tracker. A credential that can push a branch can push `refs/dolt/data`
  too; only its holder decides (assessment §3.4; section 3.4 below for why a
  ruleset does not help).
- **Rule 6, the customer instance is out of bounds.** Enforced before a
  foreign call by the leak check (section 2.3).
- **Rule 8 and ADR 0008, the merge is the decision.** Agents merge only on
  the maintainer's request (`prompts/07-commit.md`, "The merge": restate,
  never `--admin`, stop on red CI, `gh pr merge <n> --merge
  --match-head-commit <sha>`). The brake is the eight merge ask rules of
  `scripts/merge_guard.py` (`MERGE_ASK_RULES`) in `.claude/settings.json`:
  `gh pr merge *`, `gh -* pr merge*`, `gh pr -* merge *`,
  `gh api *merge*`, `gh api *Merge*`, `gh alias set *`,
  `git push *main*`, `mcp__*__merge_pull_request` (a ninth ask rule there
  is Omnigent's `sys_advise_models`). They bind Claude Code only;
  `docs/WORKFLOW.md` ("What this does not do") calls them "a brake against
  an accidental merge, not a lock".
- A re-check pull request decides nothing: `docs/research/` is
  `human-written` or `ai-drafted-reviewed` in `provenance.yaml`, not
  `human-decided`, so it is an ordinary pull request with
  `.github/pull_request_template.md`.

### 2.2 · Declared endpoints (rule RB-A6)

- `docs/governance/regelwerk.md`, RB-A6: every model named here "löst gegen
  einen deklarierten Endpunkt auf"; "Nicht gelistet ist BLOCK".
- `model-endpoints.yaml` on `main` (German, translation pending under bead
  coding-harness-yim): `anthropic-api`, `claude-code-plan` ("Nur ueber
  offiziell unterstuetzte Werkzeuge"), `bedrock-claude`, `glm-coding-plan`
  (`glm-5.3`, `glm-5.3-flash`; "**Nur ueber Claude Code**") and `kimi-code`.
  PR #60 replaces `kimi-code` with `openai-codex` and adds
  `claude-sonnet-5-5`. **No OpenCode Go entry** on `main` or on PR #60's
  branch (read).
- The enforcer, `tests/test_model_endpoints.py`, resolves the `model:` of
  each `.claude/agents/*.md`, the routing table of `docs/WORKFLOW.md` and the
  `**Model:**` line of each `prompts/*.md` (`prompt_modelle`). It checks
  **names only**: it does not see which tool or which endpoint carries a
  call. `glm-5.3` is already listed under `glm-coding-plan`, so a second
  endpoint listing it would pass the test whatever route is used — the
  declaration's remark, not the test, carries "only through Claude Code".
- `_kandidaten` turns a display name into ids by replacing `.` with `-`:
  `GLM-5.3` becomes `glm-5-3`, which is not listed. A prompt whose
  `**Model:**` line reads "GLM-5.3" would turn the test red (derived from the
  code, not run). A line starting with "none" is skipped.
- `model-endpoints.yaml` is not under a `human-decided` prefix in
  `provenance.yaml` (no prefix lists it); its kit role is `bestand`
  (`scripts/kit/manifest.yaml`).

### 2.3 · The leak check (only on PR #60's branch)

`scripts/leakcheck.py` at `ef7407c`: scans every file under
`plans/changes/<name>/`, every tracked or untracked file of the worktree,
the history of every local and remote-tracking branch, the staged changes,
and every `--prompt-file`. The denylist lives outside the repository
(`~/.config/cc-routing/denylist.txt`, or `--denylist`, or
`LEAKCHECK_DENYLIST`). "If it cannot measure, it refuses": no change name or
an empty change folder is a BLOCK. Exit 0 clean, 2 otherwise. On `main`,
`make leakcheck` prints that the check needs the denylist and exits 1
(`Makefile`).

For a scheduled job, three limits (assessment §3.5, confirmed in the
docstring): a re-check has no change folder; the denylist must be on the
host that runs the check; and search queries go to the search vendor, which
the check does not see.

### 2.4 · Unattended runs (M3)

- Implementation plan (`docs/architecture/2026-09-17-implementation-plan.md`,
  "W2 and M3"): "**Unattended operation (M3)** can retain coordinator-only
  writes. Prove total budgets, process-group cancellation, approval timeout,
  restart, remote checkpoint recovery and complete tracker restore. … Rehearse
  one bounded night run and a human morning review before routine use."
- Target (`docs/architecture/2026-09-17-omnigent-first-target.md`, row
  "Expanded permissions"): "Direct tracker writers and unattended runs meet
  their separate mode, restore and recovery requirements before activation".
- The assessment (§3.7): a weekly agent that opens pull requests is an
  unattended run by that wording; "Whether such a job waits for M3 or is
  scoped out of it is a decision the maintainer takes once, in the ADR that
  brings the first scheduled agent".

### 2.5 · The class and its artefacts

- `docs/WORKFLOW.md`, "Change classes": `architectural` — "a new subsystem
  or a break of an interface; it carries its ADR already, so it is not
  asked".
- Phase 2b: `prompts/02b-design.md`, `templates/design.md` and
  `templates/adr.md` exist only on `origin/docs/template-bundle` at
  `855eeb6`; no pull request for that branch was found. The prompt: for
  `architectural`, the design phase runs "always", and the ADR draft "becomes
  `docs/adr/<NNNN>-<slug>.md` in the change's own pull request, which makes
  that pull request a decision pull request". `templates/design.md` has five
  parts: Alternatives, Interfaces, Data model, ADR draft, Architecture delta.
- ADR 0009 (merged in PR #70): the architecture delta is a Mermaid flowchart
  in `design.md`, each box labelled with its C4 level, plus lists of added,
  changed and removed elements.
- ADR numbers: `main` has 0001–0006, 0008, 0009; 0007 is on PR #60's branch
  (`0007-stage-2-reviews-by-codex-and-glm.md`). The next free number is 0010.

### 2.6 · Ratchets a new script or folder meets

- `tests/test_ci.py`: every script under `scripts/` has a caller (a `run:`
  step in `ci.yml`) or a reason in `ci_gates.OHNE_AUFRUFER`
  (`test_every_script_has_a_caller_or_a_declared_reason`), and a test or a
  declared reason (`test_every_script_has_a_test_or_a_declared_reason`).
- The kit probe (`scripts/kit/probe.py --strict`, a gate): every tracked file
  is classified in `scripts/kit/manifest.yaml`. `prompts/` is `mechanismus`
  ("die sieben Phasen-Prompts"), so a job prompt there would travel with the
  kit; `tools/` is a `bestand` catch-all.
- `provenance.yaml`: `prompts/`, `tests/`, `.github/` are `human-written`;
  `docs/adr/` is `human-decided`; `plans/` is `human-written` or
  `ai-drafted-reviewed`; `plans/INDEX.md` is `machine-rendered`. No prefix
  lists `scripts/` or `tools/`.
- The CI (`.github/workflows/ci.yml`, generated from `decisions/gates.yaml`)
  runs on push, pull request, a nightly schedule and by hand; its job
  `verify` reported `success` on `87daf91`, and `drift` was `skipped`
  (check runs, measured).

### 2.7 · Omnigent

Omnigent's policy reaches Hermes through a per-harness hook
(`plans/changes/archive/2026-09-29-omnigent-deny-layers/decisions.md`, item
1); the policy is not installed (bead coding-harness-671, per the
assessment). A job fired by Hermes's own gateway is not an Omnigent session,
as far as the assessment read (§3.1).

## 3 · GitHub settings and rulesets (measured 2026-10-05)

### 3.1 · This repository today

Read with `gh api` GET calls:

- `repos/MPAdesso/coding-harness`: `private: true`, owner type `User`,
  `allow_auto_merge: false`, merge, squash and rebase all allowed,
  `delete_branch_on_merge: false`.
- `…/rulesets` → `[]`; `…/rules/branches/main` → `[]`;
  `…/branches/main/protection` → 404 "Branch not protected";
  `…/branches/main` → `protected: false`.
- `…/actions/permissions/workflow` → `default_workflow_permissions: read`,
  `can_approve_pull_request_reviews: false`.
- **The plan is not read.** `GET /user` returns `plan: null` with the current
  login, and the billing endpoints answer that they need the `user` scope.
  The login's scopes: `admin:ssh_signing_key`, `gist`, `read:org`, `repo`,
  `workflow` (`gh auth status`).
- Direct pushes to `main`: 13 of the 76 first-parent commits of `origin/main`
  at `87daf91` are not merges; the latest is `6ccd11f` of 2026-09-22, a
  bead-render chore commit. Since then every change came by pull request
  (`git rev-list --first-parent`).

### 3.2 · Whether rulesets are available here

GitHub's documentation source (`data/reusables/gated-features/repo-rules.md`,
read 2026-10-05): "Rulesets are available in public repositories with GitHub
Free and GitHub Free for organizations, and in public and private
repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud." The
same gate holds for protected branches. **So for this private repository a
ruleset needs GitHub Pro or higher.** The API answered as for an unprotected
branch, not with an upgrade notice; whether it answers a Free private
repository differently was not verified. The maintainer can settle it in
the account's billing page.

### 3.3 · What a ruleset can hold (GitHub's documentation)

From `available-rules-for-rulesets.md` and its reusables (read 2026-10-05):

- **Require a pull request before merging**: "The pull request doesn't
  necessarily have to be approved, but it must be opened"; required
  approvals 0 to 10.
- **Require status checks to pass**: strict (branch up to date) or loose.
- **Block force pushes**; **Restrict deletions** (selected by default);
  **Restrict updates**: "only users with bypass permissions can push to
  branches … whose name matches".
- **Bypass list**: "Repository admins, organization owners, and enterprise
  owners", the maintain or write role, teams, GitHub Apps, Dependabot; a
  bypass can be limited to "For pull requests only".
- Push rulesets are for the Team plan only.
- Creating a repository ruleset needs the `administration: write`
  permission.

### 3.4 · Tokens, and how a ruleset meets the merge flow

Fine-grained token permissions, from GitHub's permission data
(`src/github-apps/data/fpt-2022-11-28/fine-grained-pat-permissions.json`,
read 2026-10-05):

| Call | Permission |
| --- | --- |
| Create a pull request | `pull_requests: write` |
| Create a ref (push a branch) | `contents: write` |
| **Merge a pull request** | **`contents: write`** |
| Create a repository ruleset | `administration: write` |

**A token that can push the job's branch can also merge a pull request**
through the API. The assessment listed this as not verified (§8); it is now
read from GitHub's data, not tried.

How a ruleset meets this repository's flow (derived from the documentation
and the measured settings above, not tried):

- **One account for everyone.** The maintainer, every agent (ADR 0008:
  "Agents act under the maintainer's GitHub account") and a fine-grained
  token the maintainer creates all act as `MPAdesso`. A ruleset decides by
  actor, so it cannot let the maintainer merge while stopping a token of the
  same account. Only a second identity — a GitHub App, which a bypass list
  can name — could be told apart. ADR 0008 put a bot identity for agents on
  the not-now list.
- **Approvals cannot be met** with one account: nobody else can approve.
  (That GitHub refuses an author's own approval was not read this session.)
- **`gh pr merge <n> --merge --match-head-commit <sha>`** keeps working under
  "require a pull request" and "require status checks" once CI is green;
  `--admin` needs a bypass entry; `--auto` already fails because
  `allow_auto_merge` is false.
- **The tracker ref is outside every ruleset.** Rulesets target branches and
  tags; `refs/dolt/data` is neither, so a ruleset neither blocks nor protects
  `tools/bd dolt push`.
- The candidate status check is the CI job `verify`.

## 4 · adhd-relief today (read only)

### 4.1 · State of the repository

Local branch `wechsel-hermes` at `bdce8dc`, one commit ahead of
`origin/wechsel-hermes` (`e76ac64`); the commit adds a handover and drops a
bytecode file, and stays unpushed. `e76ac64` is the head of the open PR #2,
"docs: switch the always-on agent from OpenClaw to Hermes Agent", created
2026-09-23 (`gh pr view`). All files below are on that branch, not on its
`main`.

### 4.2 · ADR-0022 — Hermes as the always-on agent (proposed)

`docs/adr/0022-hermes-als-always-on-agent.md`, status `proposed`: "Angenommen
wird es, wenn der Spike S-1 bis S-8 grün ist (D-41). Bis dahin gilt
ADR-0002." What it decides:

- A LaunchDaemon of its own with `UserName` = the service user,
  `HERMES_HOME` in that user's home, the gateway with `--external-supervisor`
  and `KeepAlive`; Hermes's own LaunchAgent is not used.
- Install as a git checkout of a dated tag under `/opt/hermes`, owned by the
  maintainer; no `hermes update` (D-50).
- `HERMES_WRITE_SAFE_ROOT` = the vault; a list of toolsets in
  `agent.disabled_toolsets`; `config.yaml`, `.env` and `SOUL.md` owned by the
  maintainer (D-46).
- Learning without approval (D-42); every learned change traceable through a
  separate git directory that **a job of the maintainer commits** every 15
  minutes (D-43, ADR-0011 addendum of 2026-09-22). The agent itself does not
  commit.
- `hermes cron` jobs created by the maintainer's setup; every LLM exit
  through the scanner (D-52); web research as a named exit past the scanner
  (D-44), unless S-7 shows it can be routed.

### 4.3 · ADR-0025 — OpenCode Go (accepted 2026-09-24)

`docs/adr/0025-opencode-go-als-llm-anbieter.md`, status `accepted`:
provider `opencode-go` (not `custom`, which lacks the `x-opencode-session`
header), its address overridden to the scanner (`OPENCODE_GO_BASE_URL`);
only models without retention or training (GLM, Kimi, Qwen, MiniMax, MiMo);
the console switches "Allow models that train on request data" and "Allow
models hosted in China" off. Addendum: no written inquiry to opencode (D-73);
if opencode blocks or throttles the account, fall back to OpenCode Zen, paid
by use.

From its research note
(`docs/research/2026-09-24-opencode-go-als-llm-anbieter.md`):

- Operator Anomaly Innovations, Inc. (USA); 10 USD a month; quota limits of
  "5-hour — 20% of the monthly limit; weekly — 50%"; GLM-5.3 about 220
  requests per five hours (estimate of the vendor).
- "Yes, you can use Go with any agent"; Hermes is a "Validated Client".
- The terms forbid software that runs "while you are not logged into the
  Services"; whether scheduled jobs fall under it is open.
- Hosting: "Go models are hosted in the US" and, elsewhere, "US, EU, and
  Singapore" — the sources contradict each other.
- GLM, Kimi, Qwen, MiniMax, MiMo: "Not used / 0 days" retention.
- GLM is served at `https://opencode.ai/zen/go/v1/chat/completions`.

### 4.4 · The spike kit

`infra/macbook/spike-hermes/` at `bdce8dc`:

- `README.md` (446 lines), the runbook for S-1 to S-8 and the permission
  tests R-1 to R-6: "Nicht ausgeführt — die erste Durchführung ist der Test
  dieses Runbooks." Duration: "ein Nachmittag, plus ein Neustart des Macs".
  Needs: a Telegram test bot, the maintainer's Telegram user id, an OpenCode
  Go key, optionally a Firecrawl key for S-7, `uv`, `git`, `ffmpeg`, and
  `sudo` throughout.
- `config.yaml` (70 lines), the guard baseline: `model.provider:
  opencode-go`, `default: "glm-5.3"`, `base_url:
  "http://127.0.0.1:8787/go/v1"`; `fallback_providers: []`; auxiliary models
  inherit the main one; `agent.disabled_toolsets`: `terminal`,
  `code_execution`, `cronjob`, `browser`, `computer_use`, `desktop_ui`,
  `tts`, `image_gen`, `video_gen`, `homeassistant`, `discord`,
  `discord_admin`, `yuanbao`, `feishu_doc`, `feishu_drive`, `spotify`;
  `web.backend: firecrawl`, `web.keyless_fallback: false`;
  `cron.allow_agent_scheduling: false`; `security.tirith_enabled: false`;
  `updates.check: false`.
- `ai.adhd-relief.spike-hermes.plist`: LaunchDaemon, `UserName` `_hspike`,
  `/opt/hermes-spike/venv/bin/hermes gateway run --external-supervisor`,
  `HERMES_HOME` `/Users/_hspike/.hermes`, `HERMES_WRITE_SAFE_ROOT`
  `/Users/Shared/spike-vault`, `KeepAlive` on unsuccessful exit.
- `scanner-attrappe.py` (126 lines), a stub proxy on `127.0.0.1:8787`:
  routes `/bot…` and `/file/bot…` to Telegram, `/go/…` to
  `opencode.ai/zen/go/`, `/fc/…` to `api.firecrawl.dev`; one JSON line per
  request, tokens never written; it "prüft aber nichts". The real scanner
  (ADR-0021) is `proposed` and comes with adhd-relief's WP-4.
- `laufstatus.sh`: a cron job's state from its newest result file — exit 0
  success, 1 failed or too old, 2 no run. Finding written into the runbook
  (2026-09-23, source of `v2026.9.21`): the result files have mode 600 and
  belong to the service user, so the script runs as that user.
- Pinned Hermes: tag `v2026.9.21`, commit `d337b73`, version 0.21.4. The
  assessment read v0.21.5 of 2026-09-24 as the latest release.

### 4.5 · The spike tests that matter for Coding Harness

From the runbook, section 6; "green when" condensed:

| Test | What it proves | Green when |
| --- | --- | --- |
| S-2 | Toolsets really off, also in sub-agents | no file written by terminal, code or sub-agent; no `terminal`, `execute_code`, `process`, `cronjob_manage` call in the logs; `delegate_task` occurred |
| S-3 | The gateway as a LaunchDaemon under the service user | after a kill, `/restart`, a tag change and a Mac restart, exactly one gateway runs as the service user; no LaunchAgent created |
| S-4 | Configuration read-only for the service user | ten append, move and remove attempts on `config.yaml`, `.env`, `SOUL.md` and `HERMES_HOME` all fail; a chat request to change the config fails |
| S-5 | Every LLM exit through the proxy | each LLM call in the proxy log, only allowed models, nothing direct with the proxy stopped |
| S-6 | Run state readable from outside | `laufstatus.sh` exit 0 on a good run, 1 on a `[CRON_FAILURE]` run; `hermes cron doctor` non-zero |
| §7 | Write boundary of the file tools | a write outside `HERMES_WRITE_SAFE_ROOT` refused; a read of the maintainer's home refused by the OS |
| S-7 | Web backend through the proxy | search and fetch appear as `route: web`; red, if a direct connection to the search vendor shows |

S-1 (Telegram through the proxy) and S-8 (local speech) concern only
adhd-relief.

### 4.6 · Not run, on this machine

The handover of 2026-09-24
(`docs/journal/handover/2026-09-24-vault-skelett-und-opencode-go.md`): "Der
Hermes-Spike selbst ist weiterhin nicht gelaufen." Next step there: run it
with the maintainer, who is needed "für `sudo` und ein OpenCode-Go-Abo mit
API-Schlüssel". Measured on 2026-10-05: no user `_hspike` (`id`), no
`/opt/hermes*`, no `hermes` on the `PATH`, no Hermes LaunchDaemon.

## 5 · The job's contract

As the bead and the caller state it, with where each part already stands:

| Part | Contract | Stands in |
| --- | --- | --- |
| Input | `notes[0]` of `check_research_currency.py --format json` (or a note the caller names) | pu9; research-currency spec; assessment §7.1 |
| Output | one pull request with one appended section, `## Addendum YYYY-MM-DD · re-check`: holds, overtaken, new, not read; each item with the claim's section, the finding and its source | pu9; assessment §7.1 |
| Header | `last_reviewed:` and `updated:` set to the day of the run; nothing else in the header | research-currency spec; assessment §7.1 |
| Never | edit a finding in place; write the tracker (`tools/bd`, `refs/dolt/data`; the PR names no bead); merge, approve, force-push or push `main` | pu9; assessment §7.2 |
| Failure | if nothing could be checked, fail visibly instead of writing an empty addendum | assessment §7.1 |

Open in the contract (section 11): due notes only, or the oldest regardless.

## 6 · The trust split

As the bead and the caller state it; the facts that bear on each line are
cited.

| Who | Holds | Does | Cannot |
| --- | --- | --- | --- |
| Hermes agent, as its own service user | the model key in a `.env` it cannot write (S-4) | reads the staged note and the prompt; searches and fetches the web; writes the addendum into its write root | run a shell (`terminal` off, S-2); write outside `HERMES_WRITE_SAFE_ROOT` (§7); read the maintainer's files (OS, §7); read the publish token |
| Prepare and publish job, as the maintainer | a fine-grained token for this one repository: `contents: write`, `pull_requests: write` | computes `notes[0]`, stages the note; later checks the diff, commits, pushes `research-recheck/<note>-<date>`, opens the pull request | — it is fixed code; what it must never call (merge, push `main`, `refs/dolt/data`) is a rule of the script and its tests |
| The maintainer | the merge | reviews and merges, or asks an agent to (ADR 0008) | — |

The adhd-relief precedent for the second row: a job of the maintainer
commits, the agent never does (ADR-0011, D-43).

What the split rests on, and what it does not cover:

- **It rests on OS users.** Hermes's `approvals.deny` is "a list of glob
  patterns that block matching terminal commands" (Hermes docs, `security.md`
  at `v2026.9.21`). With the terminal off it guards only against a toolset
  switched on by mistake.
- **The token can merge** (section 3.4). Nothing in the split depends on it
  not merging, because the agent never holds it.
- **Any process of the maintainer can read the token**, Claude Code sessions
  included. They already hold the maintainer's GitHub login with `repo`
  scope (section 3.1), so the token adds no reach on that side; it narrows
  what the publish job alone can reach.
- **The diff check checks shape, not truth.** An addendum that a hostile
  page steered passes it if it is appended and well-formed; the maintainer's
  review is the only content check.
- **Ordering of three steps across two users** (prepare as the maintainer,
  the agent as the service user, publish as the maintainer) is not designed
  yet; the result files the agent's run leaves are readable only by the
  service user (section 4.4).

Hermes facts used here, from its documentation at `v2026.9.21`:

- A cron job's `enabled_toolsets` "wins" over the platform's toolsets;
  example `["web", "file"]` (`features/cron.md`).
- "Cron jobs default to running detached from any repo — no `AGENTS.md` …
  is loaded" unless `--workdir` is set (same page).
- `approvals.cron_mode: deny` and `single_query_mode: deny` block dangerous
  commands in unattended runs (`security.md`).
- `HERMES_WRITE_SAFE_ROOT` hard-blocks `write_file` and `patch` outside the
  prefix, which also keeps the agent from writing Hermes's own state
  outside it (same page).
- Learning off needs `memory.memory_enabled: false`,
  `memory.user_profile_enabled: false`,
  `auxiliary.background_review.enabled: false`, `curator.enabled: false`
  (assessment §2.8, read at Hermes `main` `66fa864`; not re-read at the tag).

## 7 · The groundwork slices

Class proposals follow `docs/WORKFLOW.md`; the actor is who does the step.

| # | Slice | Class (proposed) | Actor | Needs the laptop? |
| --- | --- | --- | --- | --- |
| 1 | Spike S-2 to S-6 (plus §7 and S-7) from adhd-relief's runbook; results stay in adhd-relief, Coding Harness cites them by commit | `spike` (adhd-relief's spike bead, per its runbook) | maintainer at the laptop (`sudo`, test bot, OpenCode Go key, one afternoon); an agent alongside in an adhd-relief session | **yes** |
| 2 | A ruleset on `main` (scope: decision Q4) | `bounded` once the scope is decided; a setting, recorded in the ADR | maintainer (GitHub settings); an agent only on explicit request | no |
| 3 | `prompts/research-recheck.md`, runner-neutral | `feature`; the assessment proposed "no" to the ADR question (§6.1) | agent drafts, maintainer merges (`prompts/` is `human-written`) | no — runs by hand in a Claude Code session |
| 4 | An endpoint entry in `model-endpoints.yaml` for the job's model | `bounded` (carries out decision Q2) | agent drafts, maintainer merges | no |
| 5 | The prepare and publish script: stage `notes[0]`, check the diff, push one branch, open one pull request, never merge | inside this `architectural` change | agent builds (phase 4); maintainer creates and places the token | build and test: no; live: yes |
| 6 | The Coding Harness Hermes profile under `tools/hermes/`: own service user, own `HERMES_HOME`, own write root, toolsets `web` and `file`, learning off, `approvals.deny` for `git`, `gh`, `tools/bd`; LaunchDaemon; runbook | inside this `architectural` change | agent drafts it with a validation test; maintainer installs (`sudo`) | validation: no; install: **yes** |
| 7 | The ADR (number 0010) and `design.md` with the ADR 0009 delta | `architectural` | agent drafts, maintainer merges (decision pull request) | no |
| 8 | The leak check for a job without a change folder (decision Q5) | `bounded`, after PR #60 merges | agent; the denylist is on the laptop | build: no; run: yes |

Dependencies, as read: slice 7 cites slice 1's results; slice 6's
configuration follows decisions Q2 and Q3; slice 5's token design follows
Q4; the first scheduled run needs slices 1 to 6, and slice 8 if Q5 says so.
Slice 7's form needs the design template, which is not merged.

## 8 · Shared with adhd-relief, and never shared

**Shared:**

- **The host:** the MacBook (adhd-relief ADR-0007, "Host ist das MacBook,
  ein Mac mini kommt später"; title read).
- **The pinned install:** `/opt/hermes`, a git tag, owned by the maintainer,
  read-only for service users (ADR-0022, D-50). One tag for both: an update
  for one is an update for the other.
- **The egress proxy:** today only the spike's stub, which forwards and logs
  but checks nothing; the real scanner is adhd-relief's WP-4. Its log
  records the model and the start of the system prompt, not which service
  user called (read in `scanner-attrappe.py`).
- **The guard baseline:** the configuration items in section 4.4.
- **Possibly the OpenCode Go subscription** (decision Q2): one quota for
  both agents; and a block for one would be a block for both.

**Never shared:** the service user; `HERMES_HOME` (memory, sessions, cron
jobs and their output); the write root; tokens and keys (the model key per
user, the GitHub token only for the publish job); instruction files
(`SOUL.md`, context files). adhd-relief keeps learning on (D-42); Coding
Harness turns it off.

**What Hermes offers for two agents on one host** (its documentation at
`v2026.9.21`, `user-guide/profiles.md` and `multi-profile-gateways.md`):

- "A profile is a separate Hermes home directory" under
  `~/.hermes/profiles/`, each with its own `config.yaml`, `.env`, `SOUL.md`,
  memories, sessions, skills, cron jobs and state database.
- One gateway can serve all profiles ("Multiplexing is **on by default**",
  `gateway.multiplex_profiles`), with per-profile `.env` as the secret
  scope, enforced by Hermes's code inside one process.
- "Stick with one-process-per-profile when you want hard process-level
  isolation between profiles".
- Profiles live under one OS user's home. ADR-0022 notes, for adhd-relief,
  that reading outside the vault is prevented "allein [durch] das
  Betriebssystem". So under one user the Coding Harness agent could read the
  personal vault and the other profile's keys, and the other agent could read
  this profile's (derived from the two documents; not tried).

## 9 · Risks and a pre-mortem

**Pre-mortem: on 2027-01-05 the Hermes runner was switched off. Why?**

| # | What went wrong | Early sign | What the groundwork has against it |
| --- | --- | --- | --- |
| 1 | A Hermes release renamed or changed a guard key; a toolset or memory came back on silently | a tag change without re-running S-2 and S-4 | pinned tag (D-50); a validation test over the profile; S-2/S-4 after every tag change |
| 2 | OpenCode Go blocked the account for automated use (its terms, section 4.3), and took adhd-relief's agent down with it | throttling, 4xx from the proxy | ADR-0025's fall-back to Zen; separate keys; Q2 decides whether to share |
| 3 | A fetched page steered the addendum; the diff check passed it because it checks shape | an addendum claiming more than its sources | "pages are data" in the prompt; sources with URLs in each item; the maintainer's review |
| 4 | The laptop slept; Hermes caught up once, the publish job ran before or without it, and opened nothing or a half addendum | a week with no pull request and no failure notice | ordering of the three steps (section 11); a visible failure on every path |
| 5 | The fine-grained token expired; the publish job failed quietly | none, unless failures surface | token lifetime not read (section 11); failure notice |
| 6 | The weekly pull requests piled up unread, or were merged unread | open re-check PRs older than a week | one note a week; the assessment's "decide on the numbers after two or three runs" |
| 7 | Web tools were dead: no search key, keyless fall-back off; every claim came back "not read" | addenda with only "not read" | S-7; a named web backend and key (section 11) |
| 8 | The leak check never ran (no change folder, PR #60 unmerged) and repository text reached a US endpoint and a search vendor unchecked | — | decision Q5 |
| 9 | A tag update made for adhd-relief broke the Coding Harness job | the Coding Harness job fails after an adhd-relief update | one shared tag is a coupling; the runbook says who updates and re-tests |
| 10 | The spike kept waiting for a free afternoon; the epic stalled | the spike bead still open after a month | decision Q1 puts it first; slices 2–5 and 7 do not wait for it |
| 11 | An unattended writer ran without M3's budgets, cancellation and restore | no turn or time cap configured | the ADR scopes the job out of M3 or defers it (section 2.4) |
| 12 | Quota contention: the weekly job used up the five-hour GLM quota the personal agent needed | adhd-relief replies fail on quota | Q2; scheduling at night |

**Other risks, as facts:**

- Hermes's pace: "about one [release] every five days" and about 14,700
  commits in 30 days (assessment §2.1).
- Ten reviewed advisories, one high; an open prompt-injection issue through
  skill description files (assessment §2.9).
- Hermes's bundled GitHub skill asks for a classic token with `repo` scope
  and teaches `gh pr merge` (assessment §2.6); bundled skills are opted out
  in adhd-relief (D-51).

## 10 · What can be built and tested without Hermes, and what needs the laptop

| Without Hermes running (any session) | Needs the laptop and the maintainer |
| --- | --- |
| The prompt, run by hand in a Claude Code session on the subscription (assessment option A) | Spike S-2 to S-6, §7, S-7 (`sudo`, keys, one afternoon) |
| The prepare and publish script, with tests against a temporary git repository and a stubbed `gh` | Creating the service user and its LaunchDaemon |
| The diff check (only the one note, appended lines, two header dates) | Placing the OpenCode Go key and a web backend key |
| The profile configuration and a test that holds it to the guard list (YAML; the plist through Python's `plistlib`, since CI runs on Ubuntu) | Creating the fine-grained token and placing it for the publish job |
| The endpoint entry (held by `tests/test_model_endpoints.py`) | The first live run and its timing on a sleeping laptop |
| The ruleset (GitHub settings, any browser) | The leak check with the real denylist |
| The ADR and `design.md` | — |

## 11 · What is unclear

Each item is a `[GAP]` for the spec or design phase unless marked.

- **Due notes only, or the oldest regardless** — left to part 2 by the
  research-currency spec. Today no note is due (the oldest review was 19 days
  old on 2026-10-05, per that spec).
- **How the three steps are ordered** across two users, and how the publish
  job learns that the agent finished: the agent's result files are mode 600
  and owned by the service user (section 4.4).
- **Gateway or one-shot for Coding Harness.** Hermes cron needs a running
  gateway (assessment §2.2); a launchd job could instead start a one-shot
  Hermes run as the service user (`hermes chat -q`, used in the runbook's
  S-2). A design alternative for phase 2b.
- **The web backend** for the job: adhd-relief configures Firecrawl through
  the proxy with keyless fall-back off; without a key the web tools do not
  work. Which vendor sees the job's search queries is a data question (house
  rule 6).
- **The write root's content**: only the staged note (and the prompt), or a
  checkout. With `--workdir` unset no `AGENTS.md` is loaded.
- **Fine-grained token lifetime and renewal**: not read.
- **The GitHub plan** (Pro or Free) and so whether a ruleset is available:
  not read (section 3.2).
- **Whether a user-owned repository offers the "Repository admin" bypass
  role**: not read.
- **Delivery**: a pull request only, or also a Telegram message. The
  assessment notes LakeSwitch D-65's "nothing notifies during work".
- **The M3 question** belongs to the ADR (section 2.4).
- **Whether the job prompt should travel with the kit** (`prompts/` is
  `mechanismus`): not decided anywhere read.
- **Requests per run** against the GLM-5.3 quota of about 220 per five
  hours: not measured; the assessment estimates 10–30 searches and fetches
  and about 300,000 input tokens per run.

## 12 · Files a change would touch

**New:**

- `prompts/research-recheck.md` — the job prompt.
- `scripts/<publish script>.py` and `tests/test_<publish script>.py`.
- `tools/hermes/` — `config.yaml`, the LaunchDaemon plist, an `.env`
  template without values, `README.md` (runbook), and a test.
- `docs/adr/0010-<slug>.md`.
- `plans/changes/hermes-runner/` — `decisions.md`, `spec.md`, `design.md`,
  `plan.md`, `findings.md`.

**Changed:**

- `model-endpoints.yaml` — one entry (Q2).
- `scripts/ci_gates.py` — `OHNE_AUFRUFER` for the publish script, which runs
  on the laptop, not in CI.
- `scripts/kit/manifest.yaml` — if `tools/hermes/` or the job prompt need
  their own rule.
- `docs/WORKFLOW.md` — the job prompt beside the phase prompts; the runner.
- `ROADMAP.md` — Q6.
- `AGENTS.md` — possibly a standing rule ("a runner never merges"), if the
  spec makes one.
- `plans/INDEX.md` — regenerated.

**Not touched:** `.claude/settings.json` (it binds Claude Code, not Hermes);
adhd-relief (its spike and PR #2 are its own); lakeswitch-ai.
