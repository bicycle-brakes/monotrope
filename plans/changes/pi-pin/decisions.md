---
title: "Decisions — pi-pin"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-agx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, pi]
---

# The runner's own pinned Pi — Decisions

Phase 1a for bead coding-harness-agx. Before the interview the maintainer
had settled the scope in the conversation on 2026-10-15 (recorded on the
bead): the runner uses its own Pi install in a repository tools folder with
the version and a lock file in one place; offline contract tests gate a
version move; and "das eigene pi muss mit opencode go und zen funktioneren".

## Q-1 · How a new Pi version proves the isolation

asked: 2026-10-15
answer: "a" — the isolation measurement becomes a contract test suite against the real pinned Pi, with a local stand-in server and no key, run locally and in CI.
answered_by: maintainer
status: answered
context: |
  Topic: how we prove that a new Pi isolates foreign models as well as the old one.
  Intention: ADR 0011 decision 6 says the isolation was measured on Pi 1.1.0 and another version means measuring again; that measurement ran once by hand on 2026-10-08 (local stand-in server, no real key), and Pi keeps releasing.
  Today: the suite never starts a real Pi, only a stand-in script; no test checks whether a real Pi reads outside the worktree or admits foreign tools.
  Repository change: A — a contract suite against the real pinned Pi, locally and in CI (CI needs node and downloads Pi, about 1-2 minutes more); B — the same suite, local only; C — keep the hand measurement in a research note.
  Architecture change: A and B replace "measured on version X" with "measured by the suite" — a new ADR amending ADR 0011 decision 6.

In the context of a Pi that keeps releasing and an isolation measured once
by hand on 1.1.0, facing the choice between a hand measurement, a local
suite and a suite that also runs in CI, we decided on a contract suite
against the real pinned Pi run locally and in CI, to achieve that every
version move is measured automatically, accepting node and a Pi download in
CI. — 2026-10-15

## Q-2 · How the runner's Pi is installed

asked: 2026-10-15
answer: "A" — `tools/pi/` with `package.json` and `package-lock.json`, an install script running `npm ci --ignore-scripts`, and a wrapper `tools/pi/pi` that runs exactly this Pi and checks its version; the runner calls only the wrapper.
answered_by: maintainer
status: answered
context: |
  Topic: how the runner's own Pi is installed.
  Intention: the runner must stop using the global Pi, which updates itself; such an update stopped the runner on 2026-10-15 at 13:14.
  Today: the runner calls `pi` through PATH and finds the global `/opt/homebrew/bin/pi`; nothing in the repository pins Pi; no Node precedent exists, only `tools/bd` (a checksummed binary) and the hash-locked Python requirements.
  Repository change: A — `tools/pi/` with a lock file holding a checksum per package, an install script (`npm ci --ignore-scripts`), a wrapper that checks the version; an update is a pull request changing one line and the lock file, and CI installs with the same script; B — a versioned global install such as `~/.local/bin/pi-1.2.0`, without a lock file for Pi's own dependencies.
  Architecture change: the wrapper becomes the only path to Pi; `stage2.py` and `stage2_session.py` no longer call `pi` through PATH.

In the context of a global Pi that updates itself, facing the choice
between a repository install with a lock file and a versioned global
install, we decided on `tools/pi/` with lock file, install script and
wrapper, to achieve the same pin pattern as `tools/bd` with every
dependency locked, accepting a `node_modules` folder under `tools/pi/`. — 2026-10-15

## Q-3 · What "works with Zen" means after the free-tier refusal

asked: 2026-10-15
answer: "A" — Go only now; the contract suite still checks the `opencode` (Zen) provider offline (address, key variable), so paid Zen can be enabled later by one declaration.
answered_by: maintainer
status: answered
context: |
  Topic: whether the runner's Pi must reach OpenCode Zen, now that Zen's free tier refuses every client but OpenCode.
  Intention: the maintainer required that the runner's own Pi works with OpenCode Go and Zen; on 2026-10-15 a free Zen call from Pi answered 403 FreeTierError, and the research swarm moved its online topics to Go models (research-swarm Q-8).
  Today: the runner calls only `opencode-go`; the global Pi has no usable Zen credential; paid Zen models through Pi were not tried.
  Repository change: A (recommended) — Go only now; the contract suite still covers the `opencode` provider offline (address, key variable) so that paid Zen can be added by one declaration later; B — declare paid Zen now, with its own endpoint entry and quota note.
  Architecture change: none for A; B adds a second declared paid endpoint.

In the context of a Zen free tier that refuses Pi, facing the choice
between Go only and a paid Zen endpoint now, we decided on Go only with the
Zen provider checked offline, to achieve one declared endpoint and a ready
path to paid Zen, accepting that no Zen model is callable until declared. — 2026-10-15

## Q-4 · Does the interactive session use the same Pi

asked: 2026-10-15
answer: "A" — the interactive session also starts Pi through the wrapper `tools/pi/pi`; its sign-in stays the maintainer's `~/.pi/agent`.
answered_by: maintainer
status: answered
context: |
  Topic: whether `stage2.py session` also starts Pi through `tools/pi/pi`.
  Intention: Q-2 makes the wrapper the runner's only path to Pi; the session verb resolves `pi` through PATH today and signs in from the maintainer's own `~/.pi/agent`.
  Today: the session runs whatever global Pi is installed; from 1.2.0 it may load `AGENTS.md` in nested worktrees where 1.1.0 did not.
  Repository change: A (recommended) — the session uses the wrapper too, so every Pi the runner starts is the measured one; B — the session keeps the global Pi.
  Architecture change: A gives one Pi for every runner path; B keeps a second, unmeasured one for the interactive path.

In the context of a wrapper that is the runner's only path to Pi, facing
the choice between the session on the wrapper and the session on the global
Pi, we decided on the wrapper, to achieve that every Pi the runner starts is
the measured one, accepting that a session waits for the pinned install. — 2026-10-15

## Q-5 · Is Node pinned too

asked: 2026-10-15
answer: "A" — CI installs one exact Node version, and the wrapper refuses a Node major version other than the one the contract suite measured; minor Node updates stay allowed.
answered_by: maintainer
status: answered
context: |
  Topic: which Node runs the runner's Pi.
  Intention: Pi is a Node program; its behaviour can depend on the Node version, and a lock file pins only the packages.
  Today: Node comes from Homebrew on the maintainer's machine; CI has whatever its image provides; the policy tests skip without Node.
  Repository change: A (recommended) — CI installs one exact Node version, and the wrapper refuses a Node major other than the one the suite measured; B — Node unpinned, only Pi pinned.
  Architecture change: A adds Node to the measured toolchain; B leaves it outside.

In the context of a lock file that pins packages but not their runtime,
facing the choice between pinning Node's major version and leaving Node
free, we decided on the major version, checked by the wrapper and exact in
CI, to achieve that Node belongs to the measured toolchain, accepting a pull
request for every Node major move. — 2026-10-15

## Q-6 · The rule as an ADR

asked: (prepared 2026-10-15, not yet asked)
answer: —
answered_by: —
status: open
context: |
  Topic: recording "Pi is pinned in the repository and a version move is measured by the contract suite" as an ADR.
  Intention: ADR 0011 decision 6 says the isolation was measured on Pi 1.1.0 and raising the pin means measuring again; ADR files are decided by the maintainer.
  Today: ADR 0011 ties the measurement to one version by hand.
  Repository change: a new ADR that amends ADR 0011 decision 6 (and ADR 0012's Pi 1.1.0 statements), its answer recorded with `harness.py decide adr` as the maintainer states it; the change becomes a decision pull request.
  Architecture change: the isolation guarantee is held by a repeatable suite instead of a one-off measurement.
