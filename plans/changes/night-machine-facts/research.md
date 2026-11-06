---
title: "Research — night-machine-facts"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-yql7
owner: Data Architect
provenance: human-written
tags: [research]
---

# night machine facts — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3354 commits, 12 rules.

## Runner exploration — 2026-11-06

Research complete. Here is the phase-1 result for `night-machine-facts`, ready to append to `plans/changes/night-machine-facts/research.md`.

---

## What exists today

**The bead and its class.** The change is bead `coding-harness-yql7`, "Machine facts at night-run start". It was filed on 2026-11-02 from the evaluation of outside practice — `docs/research/2026-11-02-model-wiki-and-egm.md`, section "Beads filed from this evaluation" — the same evaluation whose row 6 records that on 2026-11-02 "the disk and swap starved the maintainer's own session". The night-run plan of 2026-11-03 (`docs/research/2026-11-03-night-run-plan.md`, lane D backlog 3) schedules it and declares in the backlog preamble that every backlog item is a `bounded` change that "explores through GLM 5.3 Flash and stops at the interview (an explore writes only under `plans/changes/`)". That matches the routing of ADR 0020 for a `bounded` change: single-explorer explore, which is this run. The change folder holds only the skeleton `research.md` (opened by commit 31b244ff, "open the change folder").

**The incident the bead answers.** The five-lane night of 2026-11-01/02 ended on a full disk, recorded in `docs/journal/handover/2026-11-02-five-lane-night.md` (section "Incidents" and its two addenda): disk full twice (849 MB free, then 131 MB free at about 06:40 UTC on 2026-11-02); the macOS file-event daemon `fseventsd` held 18 GB of memory, 17 GB of it compressed or swapped; swap used 17.9 GB of 18.9 GB, and swap files live on the system disk; three runner jobs (lanes B, C, D) ended with exit 1 and their attempts went to side refs under `refs/stage2/attempts/…enospc-20261102`; in the three stopped worktrees `plan.md` was deleted, "presumably by the runner's plan-held-paths step failing to write it back on a full disk". A full `make verify` was "stopped at 38 % by the orchestrator's disk guard at 381 MB free" (addendum, lane D). The afternoon handover of the same day (`docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md`, "Where we are") adds that the machine recovered at 14:27 UTC only after `fseventsd` was restarted, swap fell from about 20 GB to 2.5 GB and 30 GB of disk were freed, and records the working practice: "a paused process keeps its memory, so the disk guard terminates instead of pausing". The phrase "the orchestrator's disk guard" appears only in these two handovers; a repository-wide search for `disk guard`, `df -h`, `df -k` and `statvfs` finds no script behind it — the guard was the orchestrating session's own practice, not code.

**What "night-run start" is today.** Doctrine has no machine check at start: `docs/WORKFLOW.md` section "Night runs" states two standing rules (Codex at capacity; a further case of the same mechanism) and names no machine-state reading. Each night plan carries a hand-written "State at the start" section, and the practice is inconsistent: the plan of 2026-11-02 (`docs/research/2026-11-02-night-run-plan.md`) writes one prose line — "The machine: 45 GB free, load low, the SSH signing key reloads at login" — while the plans of 2026-11-01 and 2026-11-03 record only git, pull-request and queue state with no machine line. The machine staying awake is arranged by hand per night: the 2026-11-02 plan's answer 9 ("`caffeinate` until 11:00 UTC") and the handover of 2026-11-03 ("`caffeinate` runs until about 11:00 UTC"). `AGENTS.md`'s session-start rule says: read the latest relevant handover and its addenda, check the working tree and current PR state — machine state is not named. Known standing machine facts from records: 8 GB of memory (`docs/orchestration.md`, "The resource rule"), 18.9 GB swap on the system disk (incident handover), macOS as the host platform (`scripts/verify_lock.py`, `read_available_memory`).

**Machine-reading code that exists.** Three readers and one admission exist, all memory-only:

- `scripts/verify_lock.py` (bead `coding-harness-p6mu`, merged as #284 — `docs/orchestration.md`, table "Stated, enforced, planned"): `read_available_memory()` reads macOS `memory_pressure`'s system-wide free percentage or Linux `MemAvailable`/`MemTotal`; `memory_floor()` defaults to 25 percent, overridable by `HARNESS_VERIFY_MEMORY_FLOOR`; below-floor readings wait and recheck every 30 seconds, refusing after 60 minutes. `scripts/verify_all.sh` hands every protected run to this admission before its gates, and its worker-sizing block reads `sysctl hw.logicalcpu`/`hw.memsize` (Darwin) and `nproc`/`MemTotal` (Linux) to cap pytest workers (bead `coding-harness-l7sc`). Documented in `docs/WORKFLOW.md`, "One admission per user and machine".
- `scripts/run_report.py` (`make report`, bead `coding-harness-o2yc`): a read-only live block with the process table (runner and verification invocations) and the platform memory snapshot — `macos_memory()` (`memory_pressure` free percentage, `vm_stat` compressor share over `hw.memsize`) and `linux_memory()` (`MemAvailable`/`MemTotal`, Zswap) — with a below-floor warning at its local constant `MEMORY_FLOOR = 25.0` and the `not read` discipline for every failed source. Its spec (`plans/changes/run-report/spec.md`, criteria 8–11) fixes this scope as a snapshot "to read before a verify-bearing step", explicitly not a gate.
- `scripts/verify_duration.py` (bead `coding-harness-1um6`, merged 2026-11-04; baseline note `docs/research/2026-11-04-verify-duration-baseline.md`): `cmd_start` writes a run-start event carrying `memory_pct` from `verify_lock.read_available_memory()`, the commit, the dirty flag, the worker setting and the admission id/wait — machine context is already stamped at the start of verification runs, in the runner's JSONL event format.
- `scripts/stage2.py` runs the same machine-wide admission (queue and memory wait) before its timed checks (comments citing bead `coding-harness-p6mu` at the verify, red-first proof and probe entries).

**The session-display seam.** `tools/claude-code/settings.json` wires two SessionStart hooks — `handover.sh start` and `parallel-sessions.sh start` — plus `recap.sh` on prompt submit and stop; the folder holds `hooks/` (beads-start, handover, parallel-sessions, recap, session-scan) and `statusline.sh`. A search of `tools/claude-code/` for disk, memory and load reading finds nothing but a comment in `recap.sh`: no hook or statusline element reports machine state today. The house rule in `AGENTS.md` puts this display in `tools/claude-code/`, installed through `tools/claude-code/install.sh`, never only in `~/.claude`.

**Statements of absence.** Not there: any disk-space reading in `scripts/` (`shutil.disk_usage`, `f_bavail`, `statvfs`, `df` — no matches) or in `tools/claude-code/`; any night-run-start checklist or template (`templates/` holds ADR, design, findings, handover, spec and others — no run-plan template; night plans are hand-written notes under `docs/research/`). Not read: the tracker entries themselves — `coding-harness-yql7`, `coding-harness-87b0` ("disk floor in the verify admission", named in the incident handover as covering prevention), `coding-harness-wpb0` ("machine-wide admission for runner jobs") and `coding-harness-ofmz` ("admission order and a stuck-wait alarm"), all filed from the same incident per the 2026-11-02 handover; a tracker read needs `tools/bd`, which this phase does not run. Not read also: whether any work on `-87b0` has started outside `plans/changes/` — no change folder for it exists.

## Where it lives

The incident record: `docs/journal/handover/2026-11-02-five-lane-night.md` ("Incidents", addenda) and `docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md`. The bead's origin and scheduling: `docs/research/2026-11-02-model-wiki-and-egm.md` and `docs/research/2026-11-03-night-run-plan.md` (lane D backlog). Night-run doctrine and practice: `docs/WORKFLOW.md` ("Night runs"), `docs/orchestration.md` (lanes and the resource rule), the night plans under `docs/research/2026-11-0*.md`. Machine-reading code: `scripts/verify_lock.py`, `scripts/verify_all.sh`, `scripts/run_report.py`, `scripts/verify_duration.py`, `scripts/stage2.py`. The session-start seam: `tools/claude-code/`.

## What is unclear

- What exactly the bead's description names as "machine facts" beyond what the handovers quote (title only) — the tracker entry is unread.
- The boundary to bead `coding-harness-87b0` (disk floor in the verify admission): -yql7 is facts *at night-run start*, -87b0 is a floor *in the admission*; whether this change reads disk at all, or only gathers what exists, is an interview question, not a settled fact.
- The boundary to the sibling backlog item "Session start checks the worktree environment" (bead `coding-harness-cjf9`, lane D backlog 2 of the same night plan): it has no change folder yet, and both concern start-time checks.
- Where a machine-facts reading would be recorded so a night orchestrator meets it — the existing carriers disagree in kind (run-plan prose, `make report` snapshot, `verify_duration` run-start event, SessionStart hook), and nothing in the repository states a choice.
- Whether `scripts/run_report.py` should read the admission's floor instead of its own `MEMORY_FLOOR` constant: the constant's comment says "Local until separate verification-resource work lands (bead coding-harness-p6mu)", and `-p6mu` has since merged.
- The load average the 2026-11-02 plan's prose line mentions is read by nothing in the repository today — where that figure came from is unrecorded.

## Which files a change would have to touch

By today's layout, the candidates are: the session-start seam `tools/claude-code/settings.json` plus a hook under `tools/claude-code/hooks/` (documented via `tools/claude-code/README.md` and installed by `tools/claude-code/install.sh`); `scripts/run_report.py` and its tests if machine facts extend the read-only live block; `scripts/verify_lock.py` and `scripts/verify_all.sh` only if the admission gains readings beyond memory (that area is bead `coding-harness-87b0`'s declared subject); `scripts/verify_duration.py` if facts ride the existing run-start event; doctrine text in `docs/WORKFLOW.md` ("Night runs") and `docs/orchestration.md`; `AGENTS.md` only as a maintainer proposal — night-run rule 4 and rule 6 forbid agents writing it. A start-checklist template would be new under `templates/`.

## Neighbours (for the `neighbours:` header)

`plans/changes/verify-machine-lock/spec.md` (the memory-floor admission, bead `coding-harness-p6mu`) · `plans/changes/run-report/spec.md` (the read-only live figures, bead `coding-harness-o2yc`) · `plans/changes/verify-worker-cap/spec.md` (machine-sized pytest workers, bead `coding-harness-l7sc`) · `plans/changes/verify-duration/spec.md` (machine context in run-start events, bead `coding-harness-1um6`) · `plans/changes/docs-job-report-header/spec.md` (the `--job docs` header, bead `coding-harness-ooj5`) · `plans/changes/guard-test/spec.md` (environment-gate checks, bead `coding-harness-0ho`) · `plans/changes/time-records-data/spec.md` (the record grammar the report consumes, bead `coding-harness-v6vk`) · the living page `docs/orchestration.md` as the lanes/resource-rule spec.
