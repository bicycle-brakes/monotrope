---
title: "GLM through Pi — subscription coverage, confinement, decision path"
category: research
status: proposed
created: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-11
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-11"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, stage-2, glm, pi, sandbox, decision]
---

# GLM through Pi

Research for bead coding-harness-rwa ("Stage 2: start GLM 5.3 / 5.3 Flash for
explore, implement and the loop through Pi instead of Claude Code"). Repository
facts read on 2026-10-11 at `origin/main` `0c71403`; web pages read on
2026-10-11. No model was called and no key was read. The choice among the
options is the maintainer's.

Evidence classes: **measured here** (run in this session), **documented**
(the vendor's own text, quoted), **read** (this repository), **inferred**.

## Question and status

Can explore (phase 1), implement (phase 4) and the review loop (4b) start GLM
5.3 / 5.3 Flash through Pi 1.1.0 (`@earendil-works/pi-coding-agent`, pinned)
instead of Claude Code, and what stands in the way? The bead names three
hurdles: subscription coverage, confinement of a write-capable run, and
ADR 0007 binding GLM to Claude Code.

**Status:** hurdle 1 is cleared by Z.ai's own pages; hurdle 2 is smaller
than the bead assumed; hurdle 3 needs one decision pull request. Nothing is
built.

## Hurdle 1 — does the GLM Coding Plan cover Pi?

**Yes, as far as read: Z.ai lists Pi as a supported tool and publishes a Pi setup guide** (quotes came through a summarising fetch; check the live wording before an ADR cites it)
(documented, 2026-10-11).

- `https://docs.z.ai/devpack/tool/others`, "Supported tools", step 1
  "Coding Agent Tool": ZCode, Claude Code, Claude for IDE, Codex, OpenCode,
  **Pi**, Cursor, Cline, TRAE, Qoder, Droid, Kilo Code, Roo Code, Crush,
  Goose, Eigent. The tip above the list closes: "users may not use their
  subscription benefits for tools or scenarios outside of this scope."
- `https://docs.z.ai/devpack/tool/pi` — heading "Methods for Using the GLM
  Coding Plan in Pi Coding Agent". It installs the same package this
  repository pins (`npm install -g --ignore-scripts
  @earendil-works/pi-coding-agent`), signs in with `/login zai` (stored in
  `~/.pi/agent/auth.json`) or with the variable `ZAI_API_KEY`.
- `https://docs.z.ai/devpack/faq`: "The GLM Coding Plan is strictly limited
  to use within officially supported tools and products." · "The subscriber
  shall not use the subscription benefits in any unsupported tools or
  scenarios." · "API calls outside the plan are not available." · "Only the
  following two models can be called: GLM-5.3, GLM-5.3-Flash."
- `https://docs.z.ai/devpack/usage-policy`: "GLM Coding Plan may only be used
  within officially supported tools and products." · "Accounts with more than
  three violations may be banned." The page has no sentence on automated,
  scripted or headless use (read; absence on this page, not a permission).
- `https://docs.z.ai/devpack/overview`: "Works with 20+ Agent Tools"; links
  the list above.

Not read: Z.ai's general terms of service for the subscription (not fetched
in this session). The quotes come through a summarising fetch tool, so
wording should be checked against the live page before an ADR cites it.

**The address differs from the declared one** (read, Pi package, 2026-10-11):
Pi's built-in `zai` provider sends to `https://api.z.ai/api/coding/paas/v4`
(OpenAI-compatible, `ZAI_API_KEY`; file
`node_modules/@earendil-works/pi-ai/dist/providers/zai.js` under the package)
and lists `glm-5.3` and `glm-5.3-flash`. The `glm-coding-plan` entry of
`model-endpoints.yaml` and `GLM_BASE_URL` in `scripts/stage2.py` name the
Anthropic-compatible `https://api.z.ai/api/anthropic`. The entry's remark
"**Only through Claude Code** … an own integration would not be covered" is
outdated by the list above.

## Hurdle 2 — confining a write-capable Pi run

### The premise is narrower than the bead says (read)

Implement through Claude Code today has **no shell**: `run_work_model` passes
`--tools Read,Grep,Glob,Edit,Write` with `--restricted`, and the runner itself
runs `make verify` (`scripts/stage2.py`, `WORK_WRITE_TOOLS`;
`docs/WORKFLOW.md` §4). The same shape on Pi is `--tools
read,grep,find,ls,edit,write` — no `bash`. A shell is only needed if the
maintainer wants Flash to run tests itself, which it does not do today.

### What exists in the repository (read)

| Piece | What it holds | Evidence |
|---|---|---|
| Pi isolation flags for the loop (ADR 0011 decision 6) | fresh agent dir and home, `--no-extensions --no-mcp --no-skills --no-context-files --no-prompt-templates --no-themes --no-approve --offline --no-session` | measured once by hand on Pi 1.1.0 (`plans/changes/archive/2026-10-07-stage2-mimo/research.md` §L, §P) |
| Undeclared tool refused | a `bash`/`write` call outside `--tools` → "Tool … not found", nothing run | measured, same §L |
| Reads not confined | the loop's `read` returned a file outside the working directory | measured, same §L; WORKFLOW §4 "Reads" |
| Policy extension `scripts/stage2_session_policy.mjs` (ADR 0012) | keeps `read grep find ls edit write` inside the worktree as Pi resolves a path (`@`, `~`, `file://`, symlinks), protects `.stage2-sessions/` and `.pi/`, asks or blocks dangerous `bash` patterns, blocks on handler failure | 21 test functions (about 200 cases per the ADR 0012 handover) in `tests/test_stage2_session_policy.py` at `origin/main` `0c71403`, 2026-10-11, run **without Pi** |
| The suite on this Mac | one case red at `0c71403` on a clean tree: `test_case_folding_is_a_host_setting_…` expects `.PI/settings.json` allowed with `caseInsensitive: false`, but `realpathSync.native` on case-insensitive APFS resolves it to `.pi` and the policy blocks — the safe side; the test assumes a case-sensitive disk (CI on Linux is green) | measured here, 2026-10-11 |
| The extension in a live Pi | not run — the Mac smoke test (handover 2026-10-10, package 7) is still open | not measured |
| Claude Code `--restricted` for today's GLM calls | "confines the file tools to the working directories" | documented by `claude --help`, not measured (WORKFLOW §4) |

### What Pi 1.1.0 allows (documented, package under `/opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent`)

- `docs/security.md`: Pi "does not ask for approval before every tool call";
  "The working folder … does not prevent commands from accessing other
  paths"; running "Entirely inside a container, virtual machine, or sandbox"
  is "usually the strongest practical option".
- `docs/extensions.md`: "`tool_call` can mutate input or block execution";
  "A `tool_call` handler failure blocks the tool as a fail-safe". That is the
  hook the policy extension uses; nested calls (`ctx.executeTool`, e.g.
  `codemode`) pass the same handlers.
- `docs/containerization.md`: plain Docker, Docker Sandboxes (`sbx`, proxy
  substitutes the key), NVIDIA OpenShell, and the Gondolin micro-VM extension
  (QEMU; commands "inherit the host process environment").
- `examples/extensions/sandbox/`: wraps **only `bash`** in
  `@anthropic-ai/sandbox-runtime` 0.0.26 (`sandbox-exec` on macOS); the file
  tools stay in-process and unwrapped. It would add an npm dependency.

### OS-level options on this Mac (measured here, 2026-10-11)

- `which`: `/usr/bin/sandbox-exec` present; `docker`, `container`, `podman`,
  `colima`, `orb`, `lima`, `limactl` not found. macOS 27.0.1.
- `man sandbox-exec`: "The sandbox-exec command is DEPRECATED" (still ships).
- A profile `(allow default)` + `(deny file-write* (require-not …worktree,
  scratch home, agent dir, /private/var/folders, /dev/null…))` +
  `(deny file-read* (subpath <scratch secret dir>))`, run on scratch
  directories: a write inside the allowed dir succeeded; a write outside and
  a read of the denied dir failed with "Operation not permitted"; `pi
  --version` under the same profile printed `1.1.0`, exit 0. Caveat: this
  session itself may run inside Claude Code's sandbox, so the nesting was
  not isolated from it.
- Inferred, not measured: the kernel profile binds the whole Pi process, so
  it also binds Pi's in-process `read`/`write` tools, not only `bash`.
  `sandbox-exec` filters network by address and port, not host name, so
  "only `api.z.ai`" cannot be written directly; a deny-all-but-443 rule does
  not stop exfiltration over 443.
- A container (Docker or Apple's `container`) would need an install; not done.

## Options

| | What runs | Confinement | Cost | Consequence |
|---|---|---|---|---|
| **A — stay on Claude Code** | today's `run_work_model` with `glm_env` | file tools by `--restricted` (documented) | none | Works today; Claude Code against a non-Anthropic address is a supported Z.ai tool; Pi gains nothing. Mixed launchers stay (Claude Code for Z.ai, Pi for OpenCode Go). |
| **B — Pi with the policy extension, no shell** | Pi `--print`, provider `zai`, `--tools read,grep,find,ls,edit,write`, ADR 0011 flags, `-e` policy copy, key as `ZAI_API_KEY` | file tools to the worktree by the extension (tested without Pi); no shell to confine | one runner change: a Pi variant of `run_work_model`, reuse of `require_pi` and the extension; a live smoke test first | Parity with A on paper, better on reads (A's confinement is documented, B's is tested code). One launcher for all foreign calls. Risk: the extension is unproven in a live Pi. |
| **C — Pi inside `sandbox-exec`** | B wrapped in a runner-written profile: writes only in the worktree, `.git`, scratch dirs; reads denied for `~/.config/cc-routing`, `~/.pi`, `~/.ssh`, the customer checkout | kernel-level, covers a shell too | profile + tests; deprecated tool; network not host-filtered | Allows `bash` for Flash if wanted. The profile is macOS-only and a deprecated interface may break on a macOS update. |
| **D1 — container** | Pi in Docker/Apple `container`, worktree mounted | strongest per Pi's docs | install + image + pin; Docker not installed | Too heavy for one Mac now; fits the later Kubernetes verifier pilot. |
| **D2 — loop on GLM through Pi** | `review-loop` rung `zai/glm-5.3` | read-only, as today's loop | data change only | Not asked by ADR 0011, which moved the loop to OpenCode Go; listed for completeness. |

## Recommendation

**B now, C as the step if a shell is ever granted.** Reasons:

1. Coverage is no longer a blocker: Pi is on Z.ai's supported list.
2. Implement needs no shell today; B keeps the runner's "edit but not run"
   rule and adds tested worktree confinement for reads, which the loop lacks.
3. Order: first the open Mac smoke test of the policy extension (handover
   2026-10-10, package 7) — B rests on it. Then a decision PR, then a probe
   call through the runner (one call, as ADR 0011 decision 7 did).

## Remote use until 2026-10-14

The maintainer is away from the Mac until Wednesday 2026-10-14 and steers
Claude Code remotely (read: bead comment, task brief).

- **Headless verbs** (subprocess, captured output, no window; read,
  `scripts/stage2.py`): `explore`, `implement`, `spec-review`, `review-loop`,
  `release-loop`, `review`, `probe`. They work from a remote-steered session
  that runs **on the Mac**, where Pi, Claude Code, Codex and the secrets file
  are.
- **`session`** opens a macOS Terminal window through `osascript`
  (`scripts/stage2_session.py`); nobody is at that window, so it is not
  usable remotely. The Mac smoke test of B therefore waits for 2026-10-14
  unless a headless check (Pi `--print` with the extension and a stand-in
  server, as research §L did) is accepted instead.
- If a remote session runs in a cloud container rather than on the Mac, no
  verb runs there (no secrets file, no pinned Pi; the 2026-10-10 handover
  records an egress proxy refusing `tools/bd dolt push`) — inferred.

## What a decision pull request would change (hurdle 3)

ADRs are `human-decided` (`provenance.yaml`, prefix `docs/adr/`), so the
amendment is a new ADR, as ADR 0011 and 0012 did — not an edit of 0007.

- **`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`, Decision 2:** "to
  `glm-coding-plan` through Claude Code" — the new ADR amends this to "through
  Claude Code or Pi" (or Pi only). Decision 4 (accepted unconfined reads) is
  the risk B narrows and C closes.
- **`docs/adr/0011-stage-2-reviews-through-opencode-go.md`:** Decision 2
  ("explore and implement stay on GLM 5.3 Flash") is fine; Consequences,
  "The runner's shape": "explore and implement stay Claude Code launches
  against Z.ai" — amended. Decision 6 (Pi isolation, pin) is extended to the
  `zai` provider; decision 5 (key only in the environment) gains `ZAI_API_KEY`.
- **`docs/adr/0012-interactive-stage-2-sessions-run-through-the-checked-runner.md`:**
  its header scopes the decision to the session verb only, and Decision 3 says
  what the extension does; the new ADR extends it to non-interactive implement (in
  print mode the "ask" patterns block, which suits a run without `bash`).
- **Not human-decided, changed in the same PR:** `model-endpoints.yaml`
  (`glm-coding-plan` remark: the Claude-Code-only sentence, and the coding
  address `https://api.z.ai/api/coding/paas/v4`); `docs/WORKFLOW.md` §4
  routing rows 1 and 4 ("through Claude Code against Z.ai"), the runner paragraph
  ("Explore and implement start Claude Code against Z.ai …"), "Reads: confined
  for the Claude Code calls …", and the caveat "Claude Code for Z.ai";
  `scripts/stage2.py` module docstring, `GLM_BASE_URL`, `glm_env`,
  `run_work_model`; `tests/test_stage2.py`.
- D-13 (decision continuity) is untouched: no new endpoint, same data class.

## Open decisions for the maintainer

1. Should GLM explore and implement through Pi (option B) instead of Claude
   Code — yes, or stay on A?
2. If B: does implement stay without a shell, as today?
3. May the extension's live check run headless with a stand-in server before
   2026-10-14, or wait for the Mac smoke test in a Terminal window?
4. Should the review loop ever use GLM again (D2), or stays it with OpenCode
   Go as ADR 0011 decided?
