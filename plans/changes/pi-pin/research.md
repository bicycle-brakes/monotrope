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
