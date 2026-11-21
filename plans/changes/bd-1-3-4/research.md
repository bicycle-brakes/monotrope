---
title: "Research — bd-1-3-4"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-15
supersedes: null
superseded_by: null
bead: coding-harness-tr84
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-14", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# bd 1 3 4 — Research

Stage-2 call, 2026-11-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1072 files, 4219 commits, 12 rules.

## Runner exploration — 2026-11-14

The phase-1 explorer's answer (route `flash`, model `glm-5.3-flash`, the
stage-2 call above), translated into English by the orchestrator on
2026-11-15 and stripped of the explorer's handover scaffolding — its
"append this prose" preamble, a rule, a pending-section heading and a closing
note to the runner whose frontmatter change was already made (loop rows L1-5
and L1-8). The findings and their line references are unchanged; the German
original is in commit `5572158a`.

### Neighbouring changes

`plans/changes/archive/2026-11-06-pi-pin/spec.md` (the precedent for a pin
bump), `plans/changes/archive/2026-09-21-reproducible-bead-export/research.md`
(render identity and machine-local fields), `plans/changes/ci-bead-summary/research.md`
(tracker reads through `tools/bd`).

### What exists today

The repository pins the Beads CLI (`bd`) to an exact version and routes every call through a wrapper. The pin itself is the file `tools/beads/VERSION`, which currently holds `1.3.0`. The change name `bd-1-3-4` reads as version 1.3.4: that is the reading the repository evidence supports — the pin is a three-part version string of the same scheme, the last pin step (1.1.2 → 1.3.0) is documented as "tracker pin to bd 1.3.0" (`docs/journal/handover/2026-09-17-tracker-pin-and-session-end-interview.md`, title and section "What changed in this repository"), and no other numbered scheme applies (1.3.4 appears in no tracked document — `plans/INDEX.md` lists only the change folder). The bead's own title and description could not be read for this research: the tracker is the Dolt database on `refs/dolt/data` on origin (`AGENTS.md`, house rule 2), and no tracked file nor the local `.beads/` directory (`metadata.json`, `config.yaml`, `interactions.jsonl`) contains `tr84`. That is "could not read", not "not there".

The wrapper `tools/bd` reads the pin (`PINNED`, line 23), resolves the versioned binary `~/.local/bin/bd-<pinned version>` first (`BD_BIN`, line 33), falls back to the `bd` on PATH, refuses on a mismatch (`INSTALLED != PINNED`, lines 49–54), refuses the three verbs `init`, `migrate`, `upgrade` unless `BD_PIN_BYPASS=1` is set (lines 56–62), and exits with code 127 when no binary is found — an exit code that `scripts/render_beads_export.py` (`BD_FEHLT`, line 35) explicitly consumes as "the tracker does not live on this machine". The wrapper's header comment explains the side-by-side versions: "a newer bd migrates a store's schema on open — a one-way step" (`tools/bd`, lines 27–28), and gives the reason for the escape hatch: "a future schema upgrade has to run `bd migrate` once, on one machine" (lines 16–19).

The installer `tools/beads/install.sh` derives the version from the same pin (`VERSION` from `tools/beads/VERSION`, line 18), builds the tarball name `beads_<version>_<os>_<arch>.tar.gz` (line 31), requires the checksum file `tools/beads/checksums/<tarball>.sha256` and refuses the installation, fail closed, when it is missing (lines 32–36; the mismatch message is German, lines 57–60), downloads from `https://github.com/steveyegge/beads/releases/download/v<version>/…` (line 44), installs to `~/.local/bin/bd-<version>` (line 69), and skips the download when that destination already exists and reports the version (lines 38–42). Checksums exist today for exactly two platforms: `tools/beads/checksums/beads_1.3.0_darwin_arm64.tar.gz.sha256` and `beads_1.3.0_linux_amd64.tar.gz.sha256`; the Linux file holds `2f92b904…cdcf3b` — the same hash that is duplicated in `tools/cloud-env/setup.sh` (`BD_SHA256`, line 10).

A second, independent installation site exists: `tools/cloud-env/setup.sh` hardcodes `BD_VERSION=1.3.0` and the Linux hash (lines 9–10) — it does not read `tools/beads/VERSION`, because it runs "outside any checkout" (header comment, lines 2–5). The README's own "Known limits" names the coupling gap explicitly: "A bd version bump has to change both; no check holds them together yet" (`tools/cloud-env/README.md`, lines 38–41). The README also names the installed version in prose ("**bd 1.3.0** to `~/.local/bin/bd-1.3.0`", lines 20–21).

CI installs `bd` through the installer without any version literal: the step "Hydrate the tracker (pinned bd, checksum-verified)" (id `setup-tracker`) runs `bash tools/beads/install.sh`, then `bash tools/bd bootstrap --yes`, in both jobs (`.github/workflows/ci.yml`, lines 48–61 and 186–199). `tests/test_ci.py` (assertion at line 313) checks only that the installer line is present. Five git hooks run the bare `bd` through the PATH shim `tools/beads/bin/bd`, which forwards to the wrapper (`exec "$here/../../bd"`) — independent of the version. Each of the five hook files still carries a managed section installed by an older bd: `--- BEGIN BEADS INTEGRATION v1.1.2 ---` in all five under `.beads/hooks/` (pre-commit, pre-push, post-merge, post-checkout, prepare-commit-msg). The pin step of 2026-09-17 did NOT update them — the markers still say v1.1.2 while the pin is 1.3.0. That is the repository precedent for what the last step did not do to the hooks.

The renderer's behaviour is version-sensitive in one place: `scripts/render_beads_export.py` documents that "bd 1.3.0 writes `heartbeat_at` and `lease_expires_at` into the writer's export" and lists these two machine-local fields once in `MASCHINENLOKAL` (lines 38–45); if the tracker's notation changes, the script refuses to rewrite silently (`NichtReproduzierbar`, line 52; the byte-for-byte reproduction guard, `_ohne_maschinenlokales`, lines 63 onward). The research note of the archived change `2026-09-21-reproducible-bead-export` added that "not found is not 'not there'" — whether bd keeps further machine-local fields in other situations was open when that note was written (its "What is unclear", lines 59–64). Tracker access for gates runs through `scripts/bead_render.py` (a fresh render through `tools/bd` or the preset `BEAD_RENDER`, `render_pfad`, lines 81–106; exit 3 "not measured", `nicht_gemessen`, lines 109–117) — every gate that reads the tracker runs, indirectly, on the version the wrapper provides.

Pin history and the schema lesson: the wrapper arrived on day 1 with pin 1.1.2 (`docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`, lines 62–64). The step to 1.3.0 was reactive and carries the change's core lesson: "The tracker store had been migrated to schema v66 overnight, and bd 1.1.2 refuses that store" and "bd 1.3.0 migrates a store when it opens it — a one-way write" (handover 2026-09-17, lines 37–38 and 83). The same handover also documents the machine-side consequence that stays outside this repository: the maintainer's global `bd` guard at `~/.local/bin/bd` (exit 64), which protects the customer instance's store on the 1.1.2 schema from any newer bd (lines 80–88).

Nothing tests the wrapper logic itself: `BD_PIN_BYPASS` occurs only in the wrapper and two historical documents; the tests that reference `tools/bd` (`tests/test_beads_start.py`, `tests/test_close_merged_beads.py`, `tests/test_gate_machinery.py`, `tests/test_omnigent_deny_layers.py`, `tests/test_archive_closed_changes.py`) all replace it with stand-in fakes for the tracker and do not exercise the wrapper's version check, bypass or 127 semantics — "not found" by a targeted search for `BD_PIN_BYPASS`, `beads/VERSION` and `checksum` under `tests/`. No test holds `tools/cloud-env/setup.sh`'s `BD_VERSION` to the pin or to the checksum directory — "not found", by the same search; the README confirms it in prose (see above).

### Where it lives

- Pin: `tools/beads/VERSION` (one line, `1.3.0`).
- Wrapper: `tools/bd` (version check, versioned-binary lookup, verb refusal, escape hatch, exit 127).
- Installer: `tools/beads/install.sh` (version derived from the pin, platform detection, fail-closed checksum, versioned destination); hook shim: `tools/beads/bin/bd`.
- Checksums: `tools/beads/checksums/beads_1.3.0_{darwin_arm64,linux_amd64}.tar.gz.sha256` — only these two.
- Second installation site: `tools/cloud-env/setup.sh` (`BD_VERSION`, `BD_SHA256`, Linux amd64 only) plus the version named in prose in `tools/cloud-env/README.md`.
- CI: `.github/workflows/ci.yml`, "Hydrate the tracker" (`setup-tracker`) in both jobs — no literal; assertion in `tests/test_ci.py` (the installer line).
- Hooks: `.beads/hooks/*` — shims independent of the version, managed sections still labelled `v1.1.2`.
- Version-sensitive behaviour: `scripts/render_beads_export.py` (`MASCHINENLOKAL`, reproduction guard); tracker rendering for gates: `scripts/bead_render.py`.
- Historical precedent: `docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`, `docs/journal/handover/2026-09-17-tracker-pin-and-session-end-interview.md`; change precedent for pin work: `plans/changes/archive/2026-11-06-pi-pin/` (spec, design, plan, research, decisions, findings — class `feature` with ADR 0019); render-contract context: `docs/adr/0004-tracker-render-is-the-contract.md`, `docs/adr/0002-exclusive-coordinator-writer.md` (renderer holder), `docs/adr/0005-workers-claim-their-own-bead.md` (claim measurement on bd 1.3.0, line 43).

### What is unclear

- The title and description of bead `coding-harness-tr84` were not readable in this phase (Dolt tracker under `refs/dolt/data`; nothing tracked or local under `.beads/` names it). The reading "bump the bd pin 1.3.0 → 1.3.4" follows from the change name and the repository evidence; the bead's own wording is an open question.
- Whether upstream releases 1.3.1 to 1.3.4 exist, which hashes their tarballs carry, and whether any release between 1.3.0 and 1.3.4 changes the store schema or the export JSON notation cannot be decided from the repository — the release page of `steveyegge/beads` is outside it. Whether `bd migrate` is needed once (the escape-hatch situation that `tools/bd` lines 16–19 exist for) depends on exactly that. Earlier measurements here (the claim test, ADR 0005 line 43; the worktree five-check, `docs/research/2026-09-23-worktree-tracker-writes.md` lines 23, 36) are bound to 1.3.0 and go stale silently if the pin moves without a new measurement.
- Whether 1.3.4 wants to rewrite the managed hook sections when `bd hooks install` is run by the new version, and whether the sections should be updated at all, cannot be decided from the repository — they still say `v1.1.2` after the 1.3.0 step, so the precedent is "leave them", but the handover does not record that decision explicitly.
- Whether bd 1.3.4 introduces further machine-local export fields beyond `heartbeat_at`/`lease_expires_at` (`MASCHINENLOKAL` in `scripts/render_beads_export.py`) is unknown; the 2026-09-21 research note named the same uncertainty for 1.3.0 and did not resolve it.
- Whether `tools/bd bootstrap --yes` (CI and `tools/cloud-env/setup.sh` lines 55, 56; AGENTS.md house rule 2) behaves differently between versions is not documented here; the hydration side effects of the bootstrap (writing `.beads/.gitignore` and `.beads/config.yaml`, per ADR 0004 "Decision", lines 85–87, and the cloud-env restore in `setup.sh` line 56) are the known surface.

### Which files a change would have to touch

- `tools/beads/VERSION` — the pin itself.
- `tools/beads/checksums/` — checksum files for the new version, at least for the two platforms the installer and the cloud environment cover today (`darwin_arm64`, `linux_amd64`).
- `tools/cloud-env/setup.sh` — `BD_VERSION` and `BD_SHA256` (lines 9–10); `tools/cloud-env/README.md` — the version mentions (lines 20–21) and the checksum-copy remark (lines 38–41). In the README's own words, a bump has to hit both places and no check holds them together.
- `.github/workflows/ci.yml` — only if the hydration step itself has something new to say; today it carries no version literal (the change flows through VERSION and the checksums).
- `scripts/render_beads_export.py` — only if the export notation or the machine-local fields change under the new version (`MASCHINENLOKAL`; the reproduction guard then decides by itself).
- `.beads/hooks/*` — only if the managed sections are to be updated (precedent: not touched in the 1.3.0 step).
- Evidence updates: the measurement sentences bound to 1.3.0 in `docs/WORKFLOW.md` (line 776), `docs/adr/0005-workers-claim-their-own-bead.md` (line 43), `docs/research/2026-09-23-worktree-tracker-writes.md` — historical sentences; whether they are remeasured or only dated is a question for the spec phase.
- The German installer messages in `tools/beads/install.sh` (lines 34, 57–60) are in the tree, but `AGENTS.md` house rule 1 assigns in-tree translations to pull requests of their own (bead `coding-harness-yim`) — noted here as a neighbouring boundary, not as part of this change's path.

### Open questions for the human

None that block the exploration. The one question that reaches the spec is the one unanswerable above: whether 1.3.1–1.3.4 change the store schema (and so trigger the one-time `bd migrate` with `BD_PIN_BYPASS=1` whose existence `tools/bd` lines 16–19 anticipated) — that is answered by the upstream release notes plus a measurement on scratch copies before the shared store is opened, not by this phase.
