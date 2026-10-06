---
title: "Spec — hermes-runner"
status: draft
implementation_status: none
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-i3y
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, hermes, runner, research-recheck, ruleset]
class: architectural
appetite: 11  # hours of phase 4 over the five agent slices, repair rounds included; 9.5 before the key barrier of 2026-10-06
---

# Spec — hermes-runner

After this change, Coding Harness has everything a weekly research re-check
needs to run unattended under Hermes Agent, except what only the maintainer
can do at the laptop: a runner-neutral job prompt, a declared endpoint for
its model, a script the maintainer owns that stages the note, checks the
agent's diff and opens one pull request, a Hermes profile of its own, an ADR
for the first unattended writing agent, and a ruleset on `main` as the
backstop (epic bead coding-harness-i3y; the job is bead coding-harness-pu9,
part 2). Research: `research.md`, with its section 13 read in this phase.
Decisions: `decisions.md` (the six answers of 2026-10-05, and the key
barrier of 2026-10-06 in its addendum of that day). Design:
`design.md` (phase 2b, mandatory for `architectural`).

## Problem

Read on 2026-10-05 at `87daf91` unless a line says otherwise.

- **Research ages without anyone noticing.** The age list of research notes
  exists only on an unmerged branch (pull request #73), and nothing
  re-checks a note's dated facts (bead coding-harness-pu9; `research.md`
  1.1, 1.2).
- **No runner exists for a recurring agent job.** Nothing in the repository
  starts an agent on a schedule; the maintainer chose Hermes Agent for it
  against the assessment's "not now" (`research.md`, introduction; pull
  request #72).
- **Hermes's guards are unproven on this laptop.** adhd-relief's spike has
  not run; no service user, no install, no LaunchDaemon exist
  (`research.md` 4.6).
- **An agent that publishes would need a write credential, and that
  credential can merge.** A token that pushes a branch also merges a pull
  request through the API (`contents: write`; `research.md` 3.4).
- **`main` has no protection at all.** No ruleset, no branch protection
  (`research.md` 3.1); the target calls branch protection "the security
  boundary" (`research.md` 13).
- **The model the maintainer chose is not declared.** No OpenCode Go entry
  in `model-endpoints.yaml`; "not listed is BLOCK" (rule RB-A6;
  `research.md` 2.2).
- **No ADR covers an unattended writing agent,** and the milestone for
  unattended runs (M3) has not been reached (`research.md` 2.4).
- **The agent can read its own keys.** The profile as built in slice 5
  installs the OpenCode Go and Firecrawl keys in `$HERMES_HOME/.env`, which
  the service user reads so that Hermes can load it; only Hermes's own file
  guard, which Hermes calls "not a security boundary", stands between a
  fetched page and those keys (`findings.md`, F-14 and F-26; read on
  2026-10-06 at `f5494b6`).

## Terms

- **The job** — the recurring re-check of one research note.
- **The note** — the one file under `docs/research/` a run re-checks.
- **The list** — the output of `python3 scripts/check_research_currency.py
  --format json` (pull request #73, schema version 1); `notes[0]` is its
  first entry.
- **The run date** — the calendar date, in the maintainer's time zone, on
  which a run starts, written `YYYY-MM-DD`.
- **The base** — the commit of `origin/main` a run starts from.
- **The addendum** — the one section a run appends at the end of the note:
  the heading `## Addendum <run date> · re-check`, then the four
  subsections `### Holds`, `### Overtaken`, `### New`, `### Not read`, in
  this order. An item is a line beginning with a dash and a space. A
  subsection without items holds the single item `- none`.
- **A checked item** — an item under Holds, Overtaken or New other than
  `- none`.
- **The orchestrator** — `scripts/research_recheck.py`, run as the
  maintainer.
- **The agent step** — one Hermes one-shot run as the service user, started
  by the orchestrator through the wrapper `tools/hermes/recheck-agent.sh`.
- **The service user** — the macOS user of Coding Harness's Hermes agent,
  `_chhermes`; not adhd-relief's.
- **The publish token** — a fine-grained personal access token for this one
  repository with `contents: write` and `pull_requests: write`, in a file
  only the maintainer can read.
- **The two keys** — the service user's own OpenCode Go key and Firecrawl
  key, in the variables Hermes reads, `OPENCODE_GO_API_KEY` and
  `FIRECRAWL_API_KEY`.
- **The key file** — `~/.config/coding-harness/hermes-keys` in the
  maintainer's home, mode 600 in a directory of mode 700, holding exactly
  the two lines `OPENCODE_GO_API_KEY=<value>` and `FIRECRAWL_API_KEY=<value>`;
  the service user cannot read it.
- **The key handover** — the key file's two lines on the wrapper's standard
  input, once per agent step (decisions, addendum of 2026-10-06).
- **The ruleset** — the rules on `main` of decisions Q4: pull request
  required (no approval), required status check `verify`, force pushes
  blocked, deletion restricted, no bypass.
- **The profile** — the files under `tools/hermes/`.
- **The spike** — adhd-relief's runbook tests S-2 to S-6, its write
  boundary test (§7) and S-7, together with the Coding Harness part that
  the profile's runbook describes.

## Slices

Each slice merges on its own. Agent slices come first; the last two need
the maintainer. "Laptop" means the maintainer at this MacBook.

| # | Slice | Who | Laptop | Decision PR | Appetite | Needs first |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | The job prompt `prompts/research-recheck.md`, its paragraph in `docs/WORKFLOW.md`, its kit rule; this change folder | agent | no | no | 1 h | — |
| 2 | The `opencode-go` entry in `model-endpoints.yaml` | agent | no | no — no `provenance.yaml` prefix maps the file | 0.5 h | 1 |
| 3 | ADR 0010, and the D-7 row it amends | agent drafts, maintainer merges | no | **yes** | 1 h | 1 |
| 4 | The orchestrator `scripts/research_recheck.py` and its tests, the ruleset check included; the key handover with the profile's side of it (criteria 60–70) | agent | no | no | 5.5 h | 1, 5 |
| 5 | The profile `tools/hermes/`: config, wrapper, launchd and sudo files, runbook with the Coding Harness spike part, and its test | agent | no | no | 3 h | 2 |
| 6 | The ruleset on `main` | maintainer, in GitHub's settings | no — any browser | no | 15 min | — |
| 7 | The spike, the Coding Harness part and the install, results recorded | maintainer, an agent alongside | **yes** | no | one afternoon and a restart | 4, 5 |

"Needs first" counts slice 1 because it brings this change folder to
`main`, which every later session reads. The first scheduled run needs all
seven slices and pull request #73 merged. Slice 6 can be done today, in any
order. Slice 5 was built before slice 4 (`plan.md`, "Notes, slice 5"); since
2026-10-06 slice 4 also changes slice 5's files for the key handover, so it
follows slice 5's merge, and slice 7 follows slice 4's: no laptop is
installed while the keys would still sit in `.env` (F-31).

## Acceptance criteria

### Slice 1 — the job prompt

1. When an agent opens `prompts/research-recheck.md`, its first line says
   that it is a job prompt and not one of the seven phases.
   *Refuted by:* a first line that does not say both.
2. When the prompt states its input, it takes exactly one note path and
   the run date, and names `notes[0]` of the list as where a runner
   usually takes the note from.
   *Refuted by:* a prompt that asks for several notes, lets the agent
   choose the note, or omits the run date.
3. When the prompt states its output, the output is the addendum as
   "Terms" defines it, appended after the last line of the note, with
   each checked item naming the claim's section, the finding and its
   source URL.
   *Refuted by:* a prompt that allows another heading form, a second
   section, a checked item without a URL, or text placed above the end.
4. When the prompt states the header change, it sets `last_reviewed:` and
   `updated:` to the run date and changes no other header line.
   *Refuted by:* a prompt that lets the agent change any other header line.
5. If no claim could be checked, the prompt tells the agent to leave the
   note unchanged, write no addendum and say so in its answer.
   *Refuted by:* a prompt that allows an addendum without a checked item.
6. When the prompt lists what never happens, it forbids changing or
   deleting an existing line, writing any other file, any tracker command
   or bead id (`tools/bd`, `bd`, `refs/dolt/data`), and any git or GitHub
   action (commit, push, merge, approve).
   *Refuted by:* one of these not forbidden.
7. When the prompt speaks of fetched pages, it says that their content is
   data and never instructions.
   *Refuted by:* that sentence missing.
8. When `tests/test_model_endpoints.py` reads the prompt, its `**Model:**`
   line starts with "none", so it names no model.
   *Refuted by:* a model name in that line, or a red RB-A6 test or kit
   probe.
9. When the prompt is searched for a runner, it names none as a
   requirement.
   *Refuted by:* `grep -niE 'hermes|claude code|opencode'
   prompts/research-recheck.md` printing a line.
10. When `docs/WORKFLOW.md` describes the prompts, one paragraph says that a
    job prompt is not a phase, runs outside the seven phases, writes no
    tracker and ends in a pull request, and names
    `prompts/research-recheck.md`.
    *Refuted by:* no such paragraph.
11. When the kit probe classifies `prompts/research-recheck.md`, a rule of
    its own in `scripts/kit/manifest.yaml` gives it the role `mechanismus`
    with an English reason.
    *Refuted by:* no rule of its own, or `python3 scripts/kit/probe.py
    --strict` red.

### Slice 2 — the endpoint entry

12. When `model-endpoints.yaml` is read, it declares an endpoint named
    `opencode-go` with the operator Anomaly Innovations, Inc., billing
    `abonnement`, `darf_sehen: [framework]` and the models exactly
    `[glm-5.3]`.
    *Refuted by:* the entry missing, another data class, another or a
    further model.
13. When the entry's remark is read, it states that the endpoint is used
    only by Coding Harness's Hermes runner through the egress proxy with
    the service user's own key; that no leak check runs before its calls
    (the maintainer, 2026-10-05); that the vendor's hosting statements
    contradict each other; that its terms forbid software running while
    the user is not logged in, and whether a scheduled job falls under
    that is open; and the fall-back that adhd-relief's ADR-0025 names.
    *Refuted by:* one of the five statements missing.
14. While the entry exists, every test of `tests/test_model_endpoints.py`
    passes.
    *Refuted by:* a red test.

### Slice 3 — ADR 0010

15. When slice 3's pull request is opened, it adds
    `docs/adr/0010-hermes-first-unattended-writing-agent.md` with the text
    of the ADR draft in `design.md`, and the pull request has a title
    `decide(adr): …`, the label `decision` and the block of
    `.github/PULL_REQUEST_TEMPLATE/decision.md`.
    *Refuted by:* the file, the title form, the label or the block missing.
16. When the ADR is read, it states how the job relates to M3, the trust
    split between the agent and the orchestrator, the ruleset as the
    backstop with what it cannot do, and the departure from a leak check
    before foreign calls.
    *Refuted by:* one of the four missing.
17. If the ADR amends D-7, `python3 scripts/check_decision_continuity.py`
    is green with the ADR listed under D-7 in `AMENDMENT_ADRS`, and the
    D-7 row of the continuity table names ADR 0010.
    *Refuted by:* the gate red, or the row not naming ADR 0010.

### Slice 4 — the orchestrator

18. When a run starts without `--note`, the orchestrator takes `notes[0]` of
    the list read at the base.
    *Refuted by:* a test in which another note is staged.
19. When a run starts with `--note <path>`, the orchestrator takes that
    note and reads no list.
    *Refuted by:* a test in which the list is read or another note staged.
20. If `notes[0]` carries a `problem`, the run stages nothing and ends
    `failed` with that problem as its reason.
    *Refuted by:* a staged note, or another outcome.
21. If the list's `schema_version` is not 1, the run stages nothing and
    ends `failed`.
    *Refuted by:* a staged note with schema version 2.
22. If a branch `research-recheck/<note stem>-*` exists on the remote, the
    run stages nothing and ends `nothing-to-do`, naming that branch.
    *Refuted by:* a second branch or pull request for the same note.
23. When the orchestrator stages a run, the run directory holds the job
    file, the query (the prompt at the base followed by the run's inputs)
    and a copy of the note, and no other file of the repository.
    *Refuted by:* any other file in the run directory before the agent
    step.
24. If the agent step runs past the wall-time cap, the orchestrator ends
    the agent's whole process group and the run ends `failed`.
    *Refuted by:* a fake agent that sleeps past the cap and is still alive
    afterwards, or a run that publishes.
25. If the agent's event stream names a tool other than `web_search`,
    `web_extract`, `read_file`, `write_file`, `patch` or `search_files`,
    the run publishes nothing and ends `failed`, naming the tool.
    *Refuted by:* a fixture stream with a `terminal` call that publishes.
26. If the agent step exits non-zero, or its stream has no `result` event,
    the run publishes nothing and ends `failed`.
    *Refuted by:* a fixture of either kind that publishes.
27. If the work directory holds any file other than the note after the
    agent step, the run publishes nothing and ends `failed`, listing the
    files.
    *Refuted by:* a fixture with an extra file that publishes.
28. When the diff check compares the staged note with the note at the
    base, it passes only if the header is unchanged except
    `last_reviewed:` and `updated:`, both set to the run date, the body of
    the base is an unchanged prefix, and exactly one addendum follows it.
    *Refuted by,* each a fixture that passes the check: a changed or
    deleted line of the base, a third header line changed, a header date
    other than the run date, two addenda, an addendum not at the end, a
    heading of another form, the four subsections out of order.
29. If the addendum holds no checked item, the run publishes nothing and
    ends `failed` with the reason "nothing could be checked".
    *Refuted by:* a fixture with four `- none` subsections that publishes.
30. If a checked item names no `http://` or `https://` URL, the diff check
    fails.
    *Refuted by:* a fixture with such an item that passes.
31. If the addendum is longer than 300 lines, the diff check fails.
    *Refuted by:* a 301-line addendum that passes.
32. If the date at commit time differs from the run date, the run
    publishes nothing and ends `failed`.
    *Refuted by:* a test with a clock moved past midnight that publishes.
33. When the run publishes, the remote gains exactly one ref,
    `refs/heads/research-recheck/<note stem>-<run date>`, whose commit has
    the base as its only parent and changes only the note; every other ref
    of the remote — `main`, other branches, tags, `refs/dolt/*` — is
    unchanged.
    *Refuted by:* a bare test remote on which any other ref moved.
34. When the run publishes, it opens exactly one pull request from that
    branch against `main`; its body follows the shape of
    `.github/pull_request_template.md`, says "Beads: none" and says that no
    leak check ran before the run's model and search calls.
    *Refuted by:* a stub `gh` log with no `pr create`, two, another base,
    or a body without these statements.
35. While the orchestrator runs, it calls `gh` only for `pr create` and for
    the GET request on `repos/<repo>/rules/branches/main`, and it never
    calls `tools/bd` or `bd`.
    *Refuted by:* a stub that records any other `gh` call (`pr merge`,
    `pr review`, a non-GET `api` call) or a call of `bd`.
36. If the rules on `main` lack one of `pull_request`,
    `required_status_checks` naming `verify`, `non_fast_forward` or
    `deletion`, the run pushes nothing and ends `failed`, naming each
    missing rule.
    *Refuted by:* a stub answer missing one rule after which a ref appears
    on the remote.
37. When the maintainer runs `python3 scripts/research_recheck.py
    check-ruleset`, it prints each of the four rules as present or missing
    and exits 0 only if all four are present.
    *Refuted by:* exit 0 with a rule missing, or exit 1 with all present.
38. If the token file is missing, empty, or readable by group or others,
    the orchestrator stops before any network call and ends `failed`.
    *Refuted by:* a stub `gh` or `git` remote call recorded after such a
    token file.
39. When the orchestrator calls `gh` or a git remote, it passes the publish
    token through the environment only — never in an argument — and turns
    off every other git credential helper.
    *Refuted by:* a stub that records the token in its arguments, or a git
    call without the empty `credential.helper`.
40. When a run ends, it writes a record with its outcome (`published`,
    `dry-run`, `nothing-to-do` or `failed`), the step, the reason, the
    note, the base, the branch, the pull request's URL, the agent's exit
    code and token counts; it exits 0 for the first three outcomes and 1
    for `failed`.
    *Refuted by:* a record without one of these fields, or an exit code
    that does not match the outcome.
41. When `--dry-run` is given, the run does everything except the push and
    the pull request, and its record names the branch it would push.
    *Refuted by:* a ref on the remote after a dry run.
42. When the commit is made, its message names the note, the run date, the
    base, the runner and the model, and it carries no `Closes-Bead:`
    trailer and no bead id.
    *Refuted by:* a commit message without one of the five, or with a
    bead id.
43. When `pytest` runs the orchestrator's tests, they need no network: the
    remote is a bare repository in a temporary directory, and `gh`, the
    agent and the list are stubs.
    *Refuted by:* a test that fails with the network off.
44. While the orchestrator has no CI caller, `scripts/ci_gates.py` names it
    in `OHNE_AUFRUFER` with its reason, and `tests/test_ci.py` passes.
    *Refuted by:* a red `tests/test_ci.py`.

#### Added 2026-10-06 — the key handover

From the maintainer's decision of 2026-10-06 (`decisions.md`, addendum of
that day). Numbered after criterion 59, so no earlier number moves.

60. If the key file is missing, empty, or readable by group or others, the
    orchestrator stops before the agent step and before any network call,
    and ends `failed`.
    *Refuted by:* a fake agent started, or a stub `gh` or git remote call
    recorded, after such a key file.
61. When the orchestrator starts the agent step, the key file's two lines
    reach the agent command on its standard input and by no other way — no
    argument and no variable of the command's environment carries a key
    value.
    *Refuted by:* a fake agent whose standard input is not exactly the key
    file's two lines, or a key value in its arguments or environment.
62. If the agent's event stream or the staged note holds the value of
    either key, the run publishes nothing and ends `failed`, naming the key,
    never its value.
    *Refuted by:* a fixture with a key value in the stream or in the note
    after which a ref appears on the remote, a pull request is opened, or
    the record's reason holds the value.
63. When a run ends, no file the orchestrator wrote — under the run
    directory or the log directory, the saved event stream included — and
    no argument of a command it ran holds a key value.
    *Refuted by:* a key value found in such a file, or in an argument that a
    stub `gh`, a stub `git` remote or the fake agent recorded.

### Slice 5 — the profile

45. When `tests/test_hermes_profile.py` reads `tools/hermes/config.yaml`,
    `agent.disabled_toolsets` holds every core toolset of Hermes's toolsets
    reference at the pinned tag except `web`, `file` and `search`.
    *Refuted by:* one of them missing from the list.
46. When the test reads the config, `memory.memory_enabled`,
    `memory.user_profile_enabled`, `auxiliary.background_review.enabled`,
    `auxiliary.title_generation.enabled` and `curator.enabled` are all
    `false`.
    *Refuted by:* one of them true or absent.
47. When the test reads the config, `approvals.mode` is not `off`;
    `approvals.cron_mode`, `approvals.single_query_mode` and
    `approvals.unattended_mode` are `deny`; and `approvals.deny` holds
    patterns that match `git`, `gh`, `bd` and `tools/bd` commands.
    *Refuted by:* one of these not so.
48. When the test reads the config, the provider is `opencode-go`, the
    model `glm-5.3`, the base URL on `127.0.0.1`, `fallback_providers` is
    empty, and every model the file names is listed under `opencode-go` in
    `model-endpoints.yaml`.
    *Refuted by:* one of these not so.
49. When the test reads the config, `web.backend` is `firecrawl`,
    `web.keyless_fallback`, `cron.allow_agent_scheduling` and
    `updates.check` are `false`.
    *Refuted by:* one of these not so.
50. When the test reads the wrapper, it starts Hermes with `chat
    --oneshot`, `--query-file`, `--toolsets web,file`, `--ignore-rules`,
    `--format stream-json` and `--max-turns`, never with `--yolo` or
    `--worktree`, sets `HERMES_HOME` to the service user's home and
    `HERMES_WRITE_SAFE_ROOT` to the run's work directory, and bounds
    Hermes's wall time with an alarm of its own.
    *Refuted by:* one flag, variable or the alarm missing, or a forbidden
    flag present.
51. When the test reads the launchd files, the maintainer's job runs the
    orchestrator once a week without `KeepAlive`, and no file of the
    profile starts a Hermes gateway.
    *Refuted by:* `KeepAlive`, a schedule other than weekly, or `gateway`
    in a launchd file.
52. When the test reads the sudo rule, it lets the maintainer run exactly
    the installed wrapper as the service user, without a password, and
    nothing else; the same file pins sudo's input logging off for that
    wrapper, so the keys on its standard input reach no I/O log (F-33).
    *Refuted by:* a second command, `ALL` as the command, another target
    user, or the file without `!log_input` and `!log_stdin` for the wrapper.
53. When the test reads the profile's config, wrapper, launchd, sudo and env
    files, none names adhd-relief's service user, Hermes home or write root
    (`_hspike`, `/Users/_hspike`, `spike-vault`); the shared install and
    proxy may be named (decisions Q3), and the runbook may name the rest to
    test the separation.
    *Refuted by:* one of these strings in one of those files.
54. When the test reads `tools/hermes/env.example`, every variable has an
    empty value, the model key, the model URL, the web key and the web URL
    are named, and no GitHub token variable is.
    *Refuted by:* a value, a missing name, or `GH_TOKEN` or `GITHUB_TOKEN`
    present.
    *Superseded by criterion 64 when slice 4 lands* (decision of
    2026-10-06): the two key names leave `env.example`; until then the test
    holds criterion 54 as written.
55. When `tools/hermes/README.md` is read, it describes creating the
    service user outside the group `staff`; the run directories with their
    owners and modes; the publish token (permissions, one repository, an
    expiry of 366 days, file mode 600); the ruleset's settings; the install;
    the Coding Harness spike part; and the first run by hand with
    `--dry-run`.
    *Refuted by:* one of the seven missing.
56. When the runbook's Coding Harness spike part is read, it has one test
    each, with its green condition, for: only web and file tools in the
    event stream when asked for a shell, code, delegation, memory or a
    skill; a write outside the work directory refused; the maintainer's
    home and adhd-relief's Hermes home and write root unreadable; the
    config and `.env` unwritable for the service user; every model call
    through the proxy and only `glm-5.3`; search and fetch through the
    proxy; no memory, profile or skill file changed after a run; and one
    dry run end to end.
    *Refuted by:* one of the eight missing.

#### Added 2026-10-06 — the key barrier in the profile, built with slice 4

The profile's side of the key handover. It changes slice 5's files and lands
in slice 4's pull request, so that the wrapper and the orchestrator agree in
one merge.

64. When the test reads `tools/hermes/env.example`, it names
    `OPENCODE_GO_BASE_URL` and `FIRECRAWL_API_URL` with empty values and
    assigns no variable whose name ends in `_KEY`, `_TOKEN` or `_SECRET`.
    *Refuted by:* an assignment of `OPENCODE_GO_API_KEY`,
    `FIRECRAWL_API_KEY` or another such name, empty or not, or a URL name
    missing.
65. When the test runs the wrapper with a stub in place of Hermes and the
    key file's two lines on its standard input, the stub's environment
    holds both keys with their values.
    *Refuted by:* a key missing from the stub's environment or holding
    another value.
66. When the wrapper starts Hermes, no key value appears in an argument of a
    process it starts or in its own output.
    *Refuted by:* a key value in the stub's arguments or in the wrapper's
    standard output or error, or a line of the wrapper that expands a key
    into a command's arguments.
67. When Hermes starts, its standard input is empty, so no path such as
    `/dev/stdin` or `/dev/fd/0` reaches the key handover.
    *Refuted by:* a stub that reads anything but end-of-file from its
    standard input.
68. If the wrapper's standard input does not hold exactly one non-empty line
    each for `OPENCODE_GO_API_KEY` and `FIRECRAWL_API_KEY` and nothing else,
    the wrapper exits 2 and starts no Hermes.
    *Refuted by:* a stub started after a missing, empty, doubled or unknown
    line.
69. When `tools/hermes/README.md` is read, its install writes the two keys
    only into the key file, mode 600 in a directory of mode 700, and
    `$HERMES_HOME/.env` receives the two URLs only.
    *Refuted by:* an install step that writes a key name under
    `/Users/_chhermes` or `/Users/Shared/coding-harness-hermes`, or a key
    file of another mode.
70. When the runbook's CH-4 is read, it has one test each, with its green
    condition, for: the key file unreadable for the service user;
    `$HERMES_HOME/.env` naming no key; and a run that is handed both keys
    and asked to find and send them, whose event stream holds neither key
    value. A fourth test sweeps every file under `$HERMES_HOME` — logs,
    session files, the state database — after that run for both key values,
    and is green only when the sweep finds none and reads every file; a file
    it cannot read is red. No CH-4 command carries a key value in its
    arguments: the values reach `grep` from a pattern file of mode 600,
    removed afterwards (F-30, F-32).
    *Refuted by:* one of the four missing, the sweep passing on a file it
    could not read, or a key value on a CH-4 command line.

### Slice 6 — the ruleset

57. When the maintainer has set the ruleset, `python3
    scripts/research_recheck.py check-ruleset` exits 0.
    *Refuted by:* exit 1, naming a missing rule.

### Slice 7 — the spike and the install

58. When the spike afternoon ends, the section "Spike results" of
    `tools/hermes/README.md` holds, for each of S-2 to S-6, §7 and S-7 (by
    adhd-relief's commit) and for each Coding Harness test, the date and
    "green", "red" or "open".
    *Refuted by:* a test without an entry.
59. If any of these entries is "red" or "open", the weekly job is not
    loaded.
    *Refuted by:* `launchctl list` showing the weekly job while an entry is
    red or open.

## Non-goals

- **adhd-relief.** No change there: not its spike kit, not its runbook,
  not its pull request #2. The Coding Harness part of the spike lives in
  this repository; adhd-relief's results are cited by commit.
- **Installing anything by an agent.** Creating the user, the
  directories, the install, keys, the token and loading launchd jobs are
  the maintainer's, by the runbook, in slice 7.
- **A leak check for the job** (decisions Q5). What brings it back: the
  maintainer's request, after pull request #60 merges.
- **`ROADMAP.md`.** Decisions Q6 travels in pull request #74.
- **A CI gate for the ruleset.** The check in this change is the
  orchestrator's precondition and the maintainer's `check-ruleset`. A CI
  assertion would meet the valve `ruleset-assert` of rule RB-M6 (due
  2026-10-31), but RB-M6's text asks for a code-owner review and an
  approval that one account cannot give (decisions Q4); changing it is a
  decision pull request of its own.
- **A second job, another notification channel, a GitHub App identity**
  (decisions Q4 (c)).
- **Translating `model-endpoints.yaml`** (bead coding-harness-yim).
- **Loading the weekly job and the first scheduled run.** They follow
  slice 7 and the merge of pull request #73.
- **Omnigent.** Hermes runs outside it; its policy is bead
  coding-harness-671.

## Protected areas

- adhd-relief and lakeswitch-ai — other repositories.
- `.claude/settings.json` — it binds Claude Code, not Hermes.
- `decisions/gates.yaml` and `.github/workflows/ci.yml` — no gate is added.
- `docs/governance/regelwerk.md` — RB-M6 is not changed here.
- `docs/adr/` — except the one file slice 3 adds.
- The tracker and `refs/dolt/data` — the job never writes them, and no
  slice changes them beyond the coordinator's usual bead work.
- `ROADMAP.md` — pull request #74 carries it.

## Risks accepted

- **No leak check before the job's foreign calls** (decisions Q5, chosen by
  the maintainer on 2026-10-05 against the recommendation to wait). Every
  run sends the note, the prompt and the search queries derived from them
  to OpenCode Go (Anomaly Innovations, Inc., USA; hosted in the US, or in
  the US, the EU and Singapore — the vendor's pages contradict each other)
  and to the search vendor, unchecked. If a note ever carried a name from
  the customer instance, it would leave the laptop before anyone saw it;
  house rule 6 is checked only when the re-check's pull request is
  reviewed, after the text has left. The likelihood is low, because house
  rule 6 keeps customer text out of this repository, but nothing measures
  it before the call. This change records the departure in the endpoint's
  remark, the pull request body and the ADR, and builds no check.
- **The publish token can merge and can push `refs/dolt/data`.** Only the
  orchestrator's code and its tests keep it from doing so. The ruleset
  refuses a direct push to `main` and a merge with a red `verify` for
  everyone, but cannot tell the token from the maintainer and does not
  reach `refs/dolt/data`.
- **Until slice 4 lands, the agent can read its own two keys.** The profile
  as built in slice 5 puts both keys in `$HERMES_HOME/.env`, which the
  service user reads; only Hermes's own file guard — "not a security
  boundary", in Hermes's words — and the spike check CH-4 stand between a
  fetched page and the keys (findings F-14, F-26). The maintainer did not
  accept this as the lasting state: on 2026-10-06 he chose the barrier of
  criteria 60–70 (`decisions.md`, addendum of that day). Slice 7, the spike
  and the install, needs slice 4 first (F-31), so the plan installs no
  profile that keeps its keys in `.env`; what remains until slice 4 lands is
  an install made by hand against the runbook's warning, and no scheduled run
  exists before slice 7. The weekly job is loaded only after every agent
  slice is merged (ADR 0010, "Activation"). If a key leaks, both are revoked.
- **After slice 4, the keys live in the service user's process for one
  run.** No file the service user can read holds them (the files Hermes
  itself writes are swept in CH-4, criterion 70), and Hermes's standard
  input is closed to them (criterion 67); but they sit in the environment
  of Hermes's process, which another process of the same user may be able
  to read (`ps -E`; not tried), and a Hermes defect that copies its
  environment into a tool result is not ruled out (not read). The agent has
  no tool that starts a process — terminal and code execution are off at
  both locks — and criterion 62 finds a key written out plainly in the
  stream or the note, and only after the run, when a `web_extract` call may
  already have sent it; a key sent encoded, reversed or split over two calls
  passes the scan and prompts no revocation. The remedy for a key it finds
  is to revoke the named key.
- **The diff check checks shape, not truth.** An addendum steered by a
  hostile page passes it if it is well formed; the maintainer's review is
  the only content check.
- **OpenCode Go's terms.** If the vendor blocks the account for automated
  use, adhd-relief's agent stops too; ADR-0025's fall-back serves both.
- **The GitHub plan was not read.** If it offers no rulesets for this
  private repository, criterion 57 stays red and the job never publishes;
  the maintainer then decides between a paid plan and running without the
  backstop.
- **One Hermes tag for two agents.** An update made for adhd-relief changes
  the Coding Harness job; the runbook says who re-runs which tests.
- **M3.** The ADR proposes to admit the job before M3; if the merge
  refuses that, the job waits for M3.
- **Related, outside this change:** the valve `ruleset-assert` becomes due
  on 2026-10-31 and then turns the gate `ramp-valves` red, whatever this
  change does.

## Definition of Done

Per slice:

- `make verify` green.
- Moved in the same pull request: slice 1 — `docs/WORKFLOW.md`,
  `scripts/kit/manifest.yaml`, `plans/INDEX.md`; slice 2 — none; slice 3 —
  `docs/architecture/2026-09-17-omnigent-first-target.md` (the D-7 row) and
  `scripts/check_decision_continuity.py`; slice 4 — `scripts/ci_gates.py`,
  and the profile's side of the key handover: `tools/hermes/recheck-agent.sh`,
  `tools/hermes/env.example`, `tools/hermes/README.md`,
  `tests/test_hermes_profile.py`;
  slice 5 — none; slice 6 — none; slice 7 — `tools/hermes/README.md`
  (its "Spike results").
- The protected areas untouched and the non-goals unbuilt, shown by each
  pull request's file list.
- Bead: each pull request names the bead it works on; the coordinator
  closes the epic coding-harness-i3y after slice 7, with the trailer
  `Closes-Bead: coding-harness-i3y` on the last commit.
- Special runs: slice 4 — one `--dry-run` against a scratch copy, its record
  in the pull request body; slice 7 — the spike. Otherwise none.

## Open decisions

None open. No `[DECISION]` arose: Q1 to Q6 settle what the slices build,
the M3 question is proposed in the ADR and decided by its merge
(`decisions.md`, "Not asked here"), and the rest is freely revisable. The
question the phase-6 review of slices 2 and 5 raised — what holds the
agent's own keys (F-14, F-26) — the maintainer answered on 2026-10-06
(`decisions.md`, addendum of that day); criteria 60–70 follow from it.

`[GAP]`s closed by reading (`research.md` section 13): where Q6 lands, the
token lifetime, which permission reads the rules on `main`, Hermes's
one-shot flags and learning keys at the pinned tag, the auxiliary model,
the home directory's modes.

`[DETAIL]`s, decided here, each revisable without touching another slice:

- **`notes[0]`, due or not.** The job takes `notes[0]` whatever its age:
  the bead and the caller name the oldest note, and the list carries every
  note for that. Criterion 22 keeps the queue to one open re-check, since
  `notes[0]` stays the same until its pull request is merged.
- **A note with a header problem is skipped as failed** (criterion 20): the
  fix is a person's, and the agent's header check would refuse it anyway.
- **Every write the agent may make is one file.** An extra file fails the
  run (criterion 27) rather than being ignored: the prompt forbids it, so
  it shows a run that did not follow the prompt.
- **300 lines** cap the addendum: the assessment expects 10 to 30 checks a
  run; ten times that is a steered run, not a thorough one.
- **Caps of a run:** 60 tool iterations (`--max-turns`), 45 minutes in the
  wrapper and 50 in the orchestrator, no second start of the agent in a
  run. Sixty iterations are twice the assessment's upper estimate and stay
  far below the five-hour quota of about 220 requests that adhd-relief's
  agent shares; the wrapper needs its own cap because the maintainer's
  process may not signal a process of the service user (`design.md`,
  Interfaces 2).
- **The job prompt has no model** ("none" in its `**Model:**` line): it is
  runner-neutral, the runner's configuration names the model, and a model
  name there would turn the RB-A6 test and the kit probe red.
- **The job prompt travels with the kit** (`mechanismus`, a rule of its
  own): the list it reads travels too (pull request #73), and it names no
  domain.
- **The endpoint entry keeps the file's German keys** and writes its
  remark in English: the keys are the schema the test reads, new text is
  English (house rule 1), and the translation is bead coding-harness-yim.
  Its residence is `anbieter-erklaert`: the vendor states a residence,
  contradictory or not, and the remark says so; the entry may see
  `framework` only, so the value decides nothing.
- **The ruleset check lives in the orchestrator** (criteria 36 and 37), not
  in CI: an unattended writer must not publish without the backstop, and a
  CI gate waits for RB-M6 (non-goals).
- **Delivery.** Success is the pull request. A failure is the run record
  and one macOS notification (`--notify`, `design.md` Interfaces 5): no
  Telegram, which is adhd-relief's channel and never shared (decisions Q3),
  and no GitHub issue, since the tracker is Beads only (house rule 2).
- **Web backend.** Firecrawl through the shared proxy with the service
  user's own key and no keyless fall-back — the guard baseline's route,
  which S-7 tests. That a search vendor sees the queries is part of what
  decisions Q5 (c) accepted ("a US endpoint and a search vendor").
- **Token expiry: 366 days**, the longest finite choice: an expired token
  makes a run's first fetch fail, which the record and the notification
  show, and GitHub removes a token unused for a year anyway (`research.md`
  13).
- **Names:** service user `_chhermes`, runs under
  `/Users/Shared/coding-harness-hermes/`, branch
  `research-recheck/<note stem>-<run date>` — short, Coding Harness's own,
  and none of adhd-relief's.
- **The key file sits beside the publish token** in
  `~/.config/coding-harness/`, the directory of mode 700 the runbook already
  makes; the service user is outside `staff` and cannot enter the
  maintainer's home. Its lines are written bare, without quotes or blanks:
  a quoted value hid from CH-4's count (F-27). The variable names are
  Hermes's own (`hermes_cli/auth.py` for `opencode-go`,
  `plugins/web/firecrawl/provider.py`, at tag `v2026.9.21`, read on
  2026-10-06), so the wrapper sets exactly what Hermes reads.
- **`.env` names no key, not even empty** (criterion 64). Hermes loads
  `$HERMES_HOME/.env` at every start with `override=True`, over the process
  environment (`hermes_cli/main.py` calls `load_hermes_dotenv`;
  `hermes_cli/env_loader.py`), and an assignment `KEY=` counts as a value,
  so an empty key line would replace the handed-over key with nothing. Read
  in code at the tag, not run.
- **The wrapper's `perl` reads the keys** — after it sets the alarm, before
  it starts Hermes — into its own environment, which `exec` hands on, and
  reopens standard input on `/dev/null` (criteria 65–67). No shell variable
  carries a key into an argument: `ps` shows other users' arguments on this
  laptop (measured on 2026-10-06, macOS 27.0.1).
- **The orchestrator scans for the key values** (criterion 62) behind the
  barrier, not instead of it: the note is published, and a key in it or in
  the stream means the barrier failed.
