---
title: "Research — pi-pin"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-agx
class: feature
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, pi]
---

# The runner's own pinned Pi — Research

Phase 1 for bead coding-harness-agx, seeded by the orchestrating session on
2026-10-15 against `origin/main`.

## The question

On 2026-10-15 at 13:14 the globally installed Pi moved from 1.1.0 to 1.2.0
(the mtime of its `package.json`). `scripts/stage2.py` pins
`PI_VERSION = "1.1.0"` and refuses every Pi call on any other version, so
the review loop (4b) cannot run on any change. The maintainer chose
(2026-10-15):

1. The runner uses its own Pi install in a repository tools folder, with
   the version and a lock file in one place (as `tools/bd` does for beads),
   so a global Pi update no longer stops it.
2. Offline contract tests for what the runner relies on gate a version
   move: the extension tool contract, the `--list-models` table, and the
   session policy extension that blocks foreign reads.
3. Requirement, in the maintainer's words: "das eigene pi muss mit opencode
   go und zen funktioneren" — the runner's Pi reaches both providers,
   `opencode-go` (OpenCode Go) and `opencode` (OpenCode Zen).

A weekly update check that opens a pull request is a later bead.

## Known so far (read, not run)

- Pi 1.2.0 documentation (`docs/providers.md`, `docs/models.md` of the
  installed package): OpenCode Zen and Go both take `OPENCODE_API_KEY`;
  credential order is `--api-key`, stored `auth.json`, `models.json`
  `apiKey`, then the environment variable; Pi can overlay newer catalog data
  from pi.dev (`pi update --models`) and `models.json` can add model ids.
- Pi's bundled catalog: provider `opencode` → `https://opencode.ai/zen/v1`,
  `opencode-go` → `https://opencode.ai/zen/go/v1`.
- `pi --list-models` on 2026-10-15 listed 33 `opencode-go` models and no
  `opencode` model: the global Pi has no usable Zen credential. `auth.json`
  was not read.
- Places that name the pinned version: `scripts/stage2.py` (`PI_VERSION`,
  the version check), `model-endpoints.yaml`, `scripts/stage2_session_policy.mjs`.

## To explore

Where Pi is installed and called from today; what the runner's version check
and policy extension rely on; what changed between Pi 1.1.0 and 1.2.0 in
those places; how a repository-local install (npm with a lock file, a
wrapper like `tools/bd`) is built, updated and verified in CI and on a fresh
clone; how the runner's Pi gets a credential for both providers without the
runner reading or printing it.

Stage-2 call, 2026-10-15: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 435 files, 1236 commits, 12 rules.

## Runner exploration — 2026-10-15

Exploration complete. Here is the research as prose ready to append to `plans/changes/pi-pin/research.md`. Facts only, each with its source; open questions marked; nothing designed or recommended.

---

## Explored 2026-10-15 — where Pi stands today (read in this worktree, nothing run)

### How Pi is installed and reached today

- The runner starts Pi by bare name: `require_pi()` runs `["pi", "--version"]` and `run_reviewer()` runs `["pi", "--print", …]` (`scripts/stage2.py`, functions `require_pi` and `run_reviewer`). Which Pi runs is decided by `PATH`; the runner's environment allow-list `ENV_ALLOW` carries the caller's `PATH` and `HOME` through (`scripts/stage2.py`, tuple `ENV_ALLOW`). The session verb resolves the CLI with `shutil.which("pi")` and refuses a miss (`scripts/stage2_session.py`, function `executables`).
- Nothing in the repository installs, pins or updates Pi. The tree holds no npm manifest at all: no `package.json`, no lock file, no `.npmrc` (glob over the whole worktree; only `.github/workflows/ci.yml` and `Makefile` match the tooling globs). The Makefile has no Node target — its targets are `verify`, `test`, `staleness`, `gates`, `leakcheck`, `venv`, `lock`.
- The Pi on this machine is a global install under Homebrew's node: `pi` at `/opt/homebrew/bin/pi`, package at `/opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent` (measured and read 2026-10-08, `plans/changes/archive/2026-10-07-stage2-mimo/research.md`, addendum "How it was measured" and §L; same path in `docs/research/2026-10-11-glm-through-pi.md`, "What Pi 1.1.0 allows"). Z.ai's Pi guide installs the same package with `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` (`docs/research/2026-10-11-glm-through-pi.md`, Hurdle 1).

### The pin and its enforcement

- The pin lives in one constant: `PI_VERSION = "1.1.0"` (`scripts/stage2.py`, with the comment "The one Pi the loop's isolation was measured on (research §L); any other prints a refusal"). Beside it: `PI_TOOLS = "read,grep,find,ls"`, `REVIEWER_MINUTES = 30`, `PI_VERSION_SECONDS = 30`.
- `require_pi()` runs `pi --version` in a scratch directory under `foreign_env({"HOME": tmp, "PI_CODING_AGENT_DIR": tmp})` — no key — and refuses with exit 2 when the process fails, outlasts 30 seconds, or prints anything but the pin exactly. Refusal happens before the leak check and the audit line (`scripts/stage2.py`, `require_pi`; stated in the module docstring and `docs/WORKFLOW.md` §4 runner paragraph).
- Call sites: `review_loop()` calls it after `reviewer_key()`, before building the diff; `probe()` calls it once before the first rung (both `scripts/stage2.py`); the session verb calls it for the pi transport only (`scripts/stage2_session.py`, `run()`).
- The reviewer launch is the measured set: `--print --no-session --no-approve --no-extensions --no-mcp --no-skills --no-context-files --no-prompt-templates --no-themes --offline --tools read,grep,find,ls --thinking max --model opencode-go/<rung> --append-system-prompt <scratch file>`, with a scratch home, a scratch agent directory whose only file is `settings.json` = `{"retry": {"enabled": false}}`, and the key as `OPENCODE_API_KEY` only (`scripts/stage2.py`, `run_reviewer`; key from `reviewer_key()` reading `OPENCODE_GO_KEY` out of the secrets file, `secrets_path()`). The suite starts no real Pi: tests drive a stand-in script written into a fake bin dir, parameterized on `stage2.PI_VERSION` (`tests/test_stage2.py`, `STAND_IN` replacements; `tests/test_stage2_session.py`, `PI_VERSION_STEP`/`pi_steps`).
- Which model a round calls is data, not code: `ladder()` reads the ordered `modelle` of the `opencode-go` entry in `model-endpoints.yaml` (`scripts/stage2.py`, `ladder`; ADR 0011 decision 3). The declaration gate (`declaration_problem`) checks endpoint, model, `framework` in `darf_sehen`, residency.

### What the measurement tie means (why the pin exists)

- ADR 0011 decision 6: the isolation was measured on Pi 1.1.0, the runner refuses any other version, and "raising the pin means measuring it again". The measurement record is the stage2-mimo research addendum §L–§O (stand-in HTTP server on 127.0.0.1, scratch `models.json` with `providers.opencode-go.baseUrl` as the test seam, no real key): `--tools` replaces the declared set and an undeclared tool is refused by Pi; a `read` outside the working directory is executed; extensions can shadow a built-in tool name and load whatever `--tools` says; the agent directory still loads under the full flag set, and its `models.json` `apiKey`/header values may be `!command` run at request time; a fresh empty `PI_CODING_AGENT_DIR` plus the flag set is what isolates a call; the `opencode-go` provider is defined in `<pkg>/node_modules/@earendil-works/pi-ai/dist/providers/opencode-go.js`, reads `OPENCODE_API_KEY` only, and sends `https://opencode.ai/zen/go/v1/chat/completions` with the `x-opencode-session` and `x-opencode-client: pi` headers; `--print` exits 1 on provider errors while JSON mode exits 0; an unknown id under a known provider is sent, not refused — which is why the ladder membership is checked in code; stdin is prepended to the prompt without a separator (the runner uses `stdin=DEVNULL`).
- `--list-models` was read in Pi's `docs/cli.md` as "Lists available models, optionally filtered by a fuzzy search, then exits", with "Not measured: what `--list-models` prints, and whether it needs the key" (stage2-mimo research §S). A later observation on the real Pi: "`--list-models` prints a table, not JSON" (handover `docs/journal/handover/2026-10-15-night-run-fourth.md`, §1 item 2, quoting the research-swarm findings rows). The seed's 2026-10-15 count (33 `opencode-go` models, no `opencode` model) came from the orchestrating session's run.

### The session verb's Pi surface

- `opencode-go/<model>` ids select Pi, never the OpenCode CLI (`scripts/stage2_session.py`, `TRANSPORTS`, `resolve_endpoint`; ADR 0012 decision 2). The interactive launch is `--no-extensions --no-mcp --no-skills --no-prompt-templates --no-themes -e <policy copy> --offline --no-approve --model <id> -- <prompt>`, context files on so `AGENTS.md` loads (`cli_argv`). It runs under `env -i` with no `OPENCODE_API_KEY` and no `PI_CODING_AGENT_DIR`: the session signs in from the maintainer's own `~/.pi/agent`, which may hold other providers' credentials — a recorded consequence, with `models.json` redirection there explicitly not measured (ADR 0012 decisions 2 and 5 and Consequences; `docs/WORKFLOW.md` §4 session paragraph).
- The policy extension `scripts/stage2_session_policy.mjs` is plain ESM with no imports beyond node's own, and states two version-bound dependencies in its own comments: Pi's no-approval/no-sandbox posture ("docs/security.md of the pinned Pi 1.1.0") and path resolution copied from Pi internals ("the way Pi's `resolvePath` reads it (dist/utils/paths.js, Pi 1.1.0)", function `resolveToolPath`). Against Pi's extension API it uses `pi.registerFlag`, `pi.on("tool_call", …)`, `ctx.cwd`, `ctx.hasUI`, `ctx.ui.select`; Pi's docs say a `tool_call` handler failure blocks the tool as a fail-safe (`docs/research/2026-10-11-glm-through-pi.md`, quoting Pi's `docs/extensions.md`).
- The runner confirms only that the extension loaded: `confirm_loaded()` runs `pi --no-extensions -e <copy> --offline --no-approve --help` under a scratch home and agent directory and refuses unless the output lists `--stage2-session-policy` (`scripts/stage2_session.py`, `confirm_loaded`, `POLICY_FLAG`; ADR 0012 decision 4: "confirms that the extension loaded, not how it behaves").
- The extension's behaviour is held offline today: `tests/test_stage2_session_policy.py` with `tests/stage2_session_policy_driver.mjs` run its handler without Pi and without a model — about 200 cases, 26 planted faults (ADR 0012 Validation) — and the suite skips when `node` is not installed (`pytestmark`). One recorded environment caveat: a case-folding test assumes a case-sensitive disk and runs red on this Mac's APFS, on the safe side (`docs/research/2026-10-11-glm-through-pi.md`, "What exists in the repository" table).

### Where the pin literal appears (files a version move touches today)

- `scripts/stage2.py` — `PI_VERSION`, the refusal messages that interpolate it, and the `pi` program name as a literal in `require_pi` and `run_reviewer`.
- `tests/test_stage2.py` — a test asserts `stage2.PI_VERSION == "1.1.0"` literally (criterion-27 test, function asserting the constant); fault fixtures carry `"1.1.1"`, `"1.1.0 (dev)"` literals; a docs-content test holds needles against `docs/WORKFLOW.md`, among them "outside the worktree (measured with Pi 1.1.0" and "and they are not confined" (parametrized docs test near the end of the file).
- `tests/test_stage2_session.py` — parameterized on `stage2.PI_VERSION`; asserts the scratch agent directory of confirm-load and the absence of `PI_CODING_AGENT_DIR` in the interactive launch env.
- `docs/WORKFLOW.md` §4 — "pinned at 1.1.0" (loop paragraph), "anything but the pinned `1.1.0`" (runner paragraph), "measured with Pi 1.1.0" (twice), and the session paragraph's `~/.pi/agent` rules.
- `docs/adr/0011-stage-2-reviews-through-opencode-go.md` (decision 6 and the Reads decision) and `docs/adr/0012-…` (Pi 1.1.0 statements) — ADR files are `provenance: human-decided`; a change amends by a new ADR, as `docs/research/2026-10-11-glm-through-pi.md` §"What a decision pull request would change" already maps for a neighbouring amendment.
- `model-endpoints.yaml` — the `opencode-go` `bemerkung` says "Pi at the version the runner pins (1.1.0)"; the gate `tests/test_model_endpoints.py` checks the entry's structure (operator, residency, billing, `darf_sehen`, `modelle`) and that every agent-pinned model resolves to a declared endpoint, but pins no Pi version.
- `scripts/stage2_session_policy.mjs` — the two 1.1.0 comments named above. `decisions/answers/stage2-mimo/adr.yaml` and the archived stage2-mimo artefacts record the 2026-10-08 pin decision as history, not live configuration.

### Pinning precedents already in the repository

- `tools/bd` + `tools/beads/`: the pin sits in one file (`tools/beads/VERSION`, currently `1.3.0`), the wrapper looks up the versioned binary `~/.local/bin/bd-<pin>` first and falls back to PATH only to re-check the version, refuses mismatches, refuses `init|migrate|upgrade` behind `BD_PIN_BYPASS`, and exits 127 when nothing is found (`tools/bd`). `tools/beads/install.sh` downloads the pinned release tarball, verifies sha256 against `tools/beads/checksums/<tarball>.sha256` — fail closed when the checksum file is missing — installs to `~/.local/bin/bd-<version>`, and skips when that exact version is already there.
- CI provisions through that same script: `.github/workflows/ci.yml` runs `bash tools/beads/install.sh` in both jobs ("pinned bd, checksum-verified"). ci.yml is generated from `decisions/gates.yaml` by `scripts/ci_gates.py --generate-ci`; hand edits fail the `ci-drift` gate (header comment of ci.yml).
- The Python toolchain is pinned the second way: `make lock` writes `requirements-ci.txt` from `pyproject.toml` under a `--exclude-newer` cutoff, `make venv` and CI install with `pip --require-hashes` (`Makefile`, targets `lock`/`venv`; CI step "Install the pinned toolchain").
- A Node-side equivalent exists nowhere in the tree; the only Node dependency today is `node` being on PATH for the policy tests, which skip otherwise.

### The credential surface for both providers (the requirement's third clause)

- Loop and probe: `OPENCODE_GO_KEY` from the secrets file reaches the child as `OPENCODE_API_KEY` only, never an argument, scrubbed from everything printed or written (`scripts/stage2.py`, `reviewer_key`, `run_reviewer`, `scrub`; ADR 0011 decision 5; `docs/WORKFLOW.md` §4 credential paragraph).
- Session: no key handed over; sign-in from `~/.pi/agent` (ADR 0012).
- Provider facts in the repository's records: Pi's `opencode-go` provider reads `OPENCODE_API_KEY` only (stage2-mimo research §M, package file); Pi's built-in `zai` provider sends to `https://api.z.ai/api/coding/paas/v4` with `ZAI_API_KEY`, or signs in with `/login zai` into `~/.pi/agent/auth.json` (`docs/research/2026-10-11-glm-through-pi.md`, Hurdle 1 and the address note). The same note records that the declared `glm-coding-plan` endpoint names the Anthropic-compatible `https://api.z.ai/api/anthropic`, which Claude Code uses — no runner verb calls Pi against `glm-coding-plan` today, so the two addresses never meet in one call path. The seed's 1.2.0-docs statements (both OpenCode endpoints take `OPENCODE_API_KEY`; credential order `--api-key` → `auth.json` → `models.json` → environment; `pi update --models` catalog overlay) come from the orchestrating session's read of the installed package.

### What is unclear (open questions, not guesses)

- The 1.1.0 → 1.2.0 delta in everything the runner relies on — `--version` output shape, the tool contract behind `--tools`, the `--help` flag listing that `confirm_loaded` greps, `resolvePath` behaviour that the policy re-implements, provider catalog shape, exit codes — is recorded nowhere in this worktree. The installed package lies outside it and was not read in this session; only the seed's `providers.md`/`models.md` quotes describe 1.2.0.
- Whether the research-swarm findings rows about real-Pi behaviour ("wrong tool signature", table-not-JSON `--list-models`) bear on the contract tests the maintainer named: known here only through the handover's quotation; the rows themselves live on the `explore/research-swarm` branch, not in this worktree.
- Bead coding-harness-agx's full text: the tracker is the Dolt database under `.beads/`, the rendered export is not committed, and the render needs the hydrated store — the bead body beyond the seed's summary was not read.
- How a Node CLI would be provisioned on a fresh clone and in CI (node itself, an npm cache, an offline-installable artifact) has no precedent in the tree — the two existing patterns are a checksummed binary download (`tools/beads/install.sh`) and a hash-locked Python requirements file.
- Still open from the records, unchanged by this change's question: whether `~/.pi/agent`'s `models.json` can redirect an address (ADR 0012 Consequences, "not measured"), and the live-Mac smoke test of the policy extension in a real Terminal session (ADR 0012 Validation, "Not validated: any live Pi"; still listed as open in `docs/research/2026-10-11-glm-through-pi.md`).

## Observed by the maintainer — 2026-10-15

A call to a free OpenCode Zen model from the maintainer's own Pi answered:
`Error: 403: {"type":"FreeTierError","message":"OpenCode's free tier can only
be used from within OpenCode. Download it at https://opencode.ai and keep
building."}` (reported in the conversation on 2026-10-15; the model id and
the Pi version of that call were not recorded). So the free tier of Zen is
not reachable through Pi at all; what Pi can reach on the `opencode`
provider is at most the paid Zen models. The requirement "das eigene pi muss
mit opencode go und zen funktioneren" needs restating for Zen.
