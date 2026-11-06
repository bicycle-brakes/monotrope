---
title: "Research — night-heartbeat"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-7x3c
owner: Data Architect
provenance: human-written
tags: [research]
---

# night heartbeat — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3391 commits, 12 rules.

## Runner exploration — 2026-11-06

Research complete. Here is the phase-1 prose for `plans/changes/night-heartbeat/research.md`, every statement with its source, ready to append.

---

## What exists today

**The change folder.** `plans/changes/night-heartbeat/` holds only `research.md` (confirmed by Glob); its skeleton frontmatter carries bead `coding-harness-7x3c`, `provenance: human-written`, and no `class:` field. `plans/INDEX.md` row at line 267 lists it as draft / implementation none / 2026-11-06. The branch is `feat/night-heartbeat`. The bead's own description was **not read**: the tracker is the Dolt database under `.beads/`, the worktree's `.beads/` holds only `config.yaml`, `metadata.json` and a two-line `interactions.jsonl` (last entry 2026-09-16), no rendered export, and reads outside the worktree are refused (`.git/logs/...` read attempt blocked). What exactly the change owes is therefore an open question, recorded below.

**"Heartbeat" exists in this repository as three separate, unrelated threads.**

1. **The recap-lock heartbeat, proposed and not applied.** `tools/claude-code/hooks/recap.sh` mode `stop` takes a per-session `mkdir` lock, waits up to `RECAP_LOCK_SEKUNDEN` (productive value 90) seconds, and removes any lock whose mtime is older than 300 seconds (line 60: `[ $(( $(date +%s) - $(mtime "$lock") )) -gt 300 ] && rmdir`); the EXIT trap runs `rmdir` without an ownership check (line 65). Finding A.3 in `docs/research/2026-09-26-agent-sdk-and-formal-models.md` ("Seam 4 — the recap lock", lines 201–243; TLA+ module `RecapLock`, lines 608–666) shows the design assumption "a lock only grows old once its holder is dead" fails when a child call runs longer than five minutes (hung network call, laptop asleep): a waiter then steals a live lock and two writers run — severity MINOR. The note's fix options are recorded "for a bead, not applied" (line 239): *a heartbeat that touches the lock while the child runs, so that "old" means "no sign of life"*, an owner token the trap checks, and a bound on the child call. `tests/test_recap_lock.py` (docstring) covers the 2026-09-22 possession fix (bead `hit`, part 3), not the A.3 live-holder-with-backdated-lock case the note proposes at its lines 420–423.

2. **The lane-watch heartbeat, planned and not built.** `docs/journal/handover/2026-11-01-five-lane-night.md` records: the maintainer's rule "every lane is always served" with "a lane watch mechanism is bead coding-harness-5q2p" (lines 62–63); five interview answers prepared for the 15:00 block (lines 117–119: where the lane record lives, who writes it, when it is checked, report or serve an idle lane, order with 4emv); and the folded design (lines 271–278): lane watch (5q2p) built together with lane planning (4emv) — "the runner writes a lane diary per lane into a state file at every verb's start and end; it is checked at every runner end, in the status line and **by a 20-minute heartbeat**; an idle lane always starts its next backlog bead itself". The same handover holds the evidence of the gap: "between about 11:00 and 12:38 UTC all lanes sat idle because the combined waiter fired once only. This is the case bead coding-harness-5q2p (lane watch) exists for" (lines 183–186), and the addendum of 18:15 UTC states "the lane heartbeat (a session-only timer) and the waiters were stopped" (lines 233–235) — a heartbeat that lived in one session and died with it, never in the repository. Grep for `lane` in `scripts/stage2.py` finds nothing: the lane diary is not in the runner.

3. **The bd lease heartbeat, internal to the tracker.** bd 1.3.0 writes `heartbeat_at` and `lease_expires_at` on claimed items; `scripts/render_beads_export.py` strips them as machine-local (`MASCHINENLOKAL` tuple, lines 38–45, with the measured reproduction of 2026-09-21 in the comment), and `tests/test_gate_machinery.py` (`_ZEILE_MIT_LEASE`, lines 446–449; `NichtReproduzierbar` on unknown fields, lines 478–484) pins that spelling. `docs/research/Lake-Switch-Architektur-arc42.md` line 327 describes the leases ("Leases mit Heartbeat und Compare-and-Set-Guards"). Grep over `scripts/` finds no harness code that reads or renews `heartbeat_at` — the heartbeat is bd-internal, the harness only strips it for reproducibility.

**What supervises a run today.** The runner's per-call bounds are in `scripts/stage2.py`: `launch()` (line 946) takes `timeout`/`deadline`, leads a process group and kills the whole group on timeout (a hung `make verify` leaves nothing behind, "O188-4 of the #188 review" per its docstring), registers live groups so an interrupted runner kills them (`kill_live`), drains for `KILL_DRAIN_SECONDS = 5` (line 889); stage constants are `TOOL_SECONDS = 5*60`, `VERIFY_SECONDS = 30*60`, `GIT_SECONDS = 2*60` (lines 4072–4074). `tests/test_stage2.py` (lines ~20250–20292) proves an exception inside main-thread `communicate` kills leader and descendant — the test uses its own `heartbeat` file as a liveness probe of the descendant. This is per-call supervision; **there is no cross-call liveness signal**: not found, in the sense of "not there" — no `heartbeat`, `pulse`, `lifesign` symbol exists in `scripts/` (grep), and the only run-time bookkeeping is after the fact: the fixed time-record lines under `## Time used` written by `scripts/time_records.py` (`MARKER = "measured by the runner"`, explicit elapsed seconds, docstring lines 1–15; doctrine at `docs/WORKFLOW.md:518–525`), and the loop record at `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md` (`scripts/stage2.py:122–138`, `STATE_KEY = "Loop state: "` at line 407).

**How night runs keep time and notify today.** Doctrine: `docs/WORKFLOW.md` §4 "Night runs" (heading at line 1702) — the queue works alone and sequentially; night rule 1 (maintainer, 2026-10-26, bead coding-harness-yuw.4): Codex at capacity → wait four minutes, retry once, then Sonnet 5.5 takes the step, with the note "The runner automates this once bead coding-harness-m98e lands" (not landed in this text); night rule 2: a same-mechanism re-check finding is recorded, the pull request parked, the run continues. `prompts/04-implement.md:63–71` sets the night appetite rule: by day the session asks at twice the appetite, at night the night rules — cut, park or drop — decide. One 15:00 question block a day; at night a run keeps its own rule, record–park–continue (`docs/WORKFLOW.md:198–203`). The concrete practice lives in the night-run plans under `docs/research/` (bead coding-harness-4emv, lane orchestration): the 2026-11-02/03 plan runs five lanes from one orchestrating session, keeps the machine awake with `caffeinate` until 11:00 UTC (answer 9, line 63), reports status at 07:00 UTC (rule 9), and sends a push notification "only when all five lanes stop or something security-relevant happens" (answer 12, lines 69–71). That notification and the 07:00 status are the orchestrator's chat actions — **no notification mechanism exists in the repository** (grep for `ntfy|pushover|telegram|notify` over `scripts/` and `tools/claude-code/`: no files). The newest standing rule is `AGENTS.md:186` (maintainer, 2026-11-04): a long runner job starts in the harness's background mode, one job per call — never `&` or `nohup` inside a command, "which ends without a notice and leaves a lane idle unseen". That rule is not mirrored in `docs/WORKFLOW.md` (grep `nohup|background` there: no matches).

**The only scheduled night mechanism in the repo** is the CI `schedule` trigger, `cron "23 4 * * *"` in `.github/workflows/ci.yml` (lines 12–13), which runs the `drift` job (plans-registry `--strict`, research-currency; lines 165–208). `scripts/pr_sync.py`'s sync is, by contrast, explicitly on-request only — "Called explicitly by the day session or the night orchestrator — no scheduled job runs it" (module docstring lines 21–27; echoed in the `ci_gates.py` denylist entry for `pr_sync.py`, lines 113–117).

**Neighbouring machinery a heartbeat sits beside.** The verify admission lock lives in the shared machine state home `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` as `verify.lock` with an owner token published at admission (`HARNESS_VERIFY_LOCK_TOKEN`) and inherited by nested work (`plans/changes/verify-machine-lock/spec.md`, "Shared state" and criterion 5–6: a dead holder must not block progress); a full `make verify` takes 12–13 minutes under the one lock (`docs/WORKFLOW.md:1690–1692`, measured 2026-10-30). The research swarm carries checked-in time limits: `research-swarm-limits.yaml` at the worktree root (`run_minutes`, `role_minutes` for finders/merge/sentence/topics/judge), loaded once per invocation at `Run.open` by `scripts/stage2_research_limits.py` (module docstring; `LimitsError` names path and fault) — the swarm-time-limits change, bead coding-harness-ht1b (`plans/changes/swarm-time-limits/spec.md`, dated 2026-11-04). The corpus names the pattern explicitly: "Heartbeat-Modell — Überwachung unbeaufsichtigter Läufe: Task schreibt periodisches Lebenszeichen; Supervisor terminiert bei Ausbleiben die gesamte Prozessgruppe" (`docs/research/arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md:475`; "Heartbeat + Prozessgruppen-Kill" against unattended-run PR floods, line 434) and the migration plan's probe steps "Heartbeat-Überwachung" for the controlled night run and "Heartbeat-Prozessgruppen-Kill prüfen" (`docs/research/Migrationsplan_Omnigent_Referenzarchitektur.md:82,105`); the corpus comparison marks "stop conditions (max iterations, time, idle) belong into the Stage-2 runner spec" as **adopt** (`docs/research/2026-09-16-review-corpus-vs-running-workflow.md:124`). A vendored third-party implementation exists in the tree but is not referenced by harness code: `tools/pi/node_modules/@anthropic-ai/sdk/src/lib/environments/worker.ts` with `HEARTBEAT_DEFAULT_MS = 30_000` / `HEARTBEAT_TTL_DEFAULT_MS = 90_000` / `NO_HEARTBEAT_SENTINEL` (dependency of the pinned Pi client).

## Where it lives

Files and symbols named inline above; the concentrated map: `scripts/stage2.py` (`launch` line 946, `KILL_DRAIN_SECONDS` line 889, `TOOL_SECONDS`/`VERIFY_SECONDS`/`GIT_SECONDS` lines 4072–4074, loop-record block lines 122–138), `scripts/time_records.py` (module docstring), `scripts/stage2_research_limits.py` plus `research-swarm-limits.yaml`, `tools/claude-code/hooks/recap.sh` (lock loop lines 56–65), `tools/claude-code/statusline.sh` (two-line display, cache under `${TMPDIR:-/tmp}/claude-statusline`), `tests/test_stage2.py` (descendant-kill proof), `tests/test_recap_lock.py`, `docs/WORKFLOW.md` §4 "Night runs" (line 1702) and the hand-repair timing facts (lines 1690–1700), `prompts/04-implement.md` (night appetite rule), `AGENTS.md:186`, the night-run plans and handovers under `docs/research/` and `docs/journal/handover/` (beads 4emv and 5q2p), `.github/workflows/ci.yml` (schedule lines 12–13, drift job lines 165–208), `scripts/render_beads_export.py` (`MASCHINENLOKAL`).

## What is unclear about it

- `[DECISION-shaped, for the interview]` The bead `coding-harness-7x3c`'s description was not readable with this phase's tools (tracker is a Dolt database; no rendered export in the worktree). Which liveness signal the change owes — runner-level, lane-level, or lock-level — is not stated anywhere in the tree; three candidate "heartbeat" threads exist (recap lock A.3, lane watch 5q2p, unattended-run supervision) and the change folder names none.
- The lane-watch interview (bead 5q2p, five answers) stood before the maintainer's 15:00 block per the 2026-11-01 handover; the latest handover (2026-11-03) lists four explores waiting for interviews and 5q2p is not among them — its current state after 2026-11-01 is unknown to this phase.
- Whether the recap-lock fix options (heartbeat touch, owner token) ever got their bead opened and what its id is — the A.3 note says "for a bead, not applied" without an id.
- The registry rows for swarm-time-limits, time-records-data and verify-machine-lock all still read `none` in `plans/INDEX.md` while parts of each exist in the tree (`scripts/stage2_research_limits.py`, `scripts/time_records.py`, the verify-lock spec's token mechanism); this phase records both facts without reconciling them.
- Not read (not "none"): `scripts/stage2.py` in full (~9000 lines; only the sections cited), `tools/claude-code/statusline.sh` beyond its first 60 lines, any machine-local state under `~/.local/state/coding-harness/`.

## Which files a change would have to touch

Depends on which thread the bead names, but the surfaces are: `scripts/stage2.py` and `tests/test_stage2.py` for runner-level signalling (declared hot file: at most three open changes at once, night-run plan 2026-11-02/03 rule 3); `tools/claude-code/hooks/recap.sh` and `tests/test_recap_lock.py` for the lock heartbeat (changes belong in `tools/claude-code/` with a reinstall via `install.sh`, never only in `~/.claude`, per AGENTS.md); a state file beside `verify.lock` under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` for machine-scoped liveness (the shared home the verify-machine-lock spec names); `docs/WORKFLOW.md` §4 "Night runs" and `prompts/04-implement.md` wherever the night rules gain a mechanism; `tools/claude-code/statusline.sh` if the signal reaches the maintainer's display; `plans/INDEX.md` regenerated via `scripts/plans_registry.py --index` after any frontmatter edit.

**Candidate neighbours for the header:** `plans/changes/verify-machine-lock/spec.md`, `plans/changes/swarm-time-limits/spec.md`, `plans/changes/time-records-data/spec.md`, `plans/changes/run-report/spec.md`, `plans/changes/attempt-diagnostics/spec.md`, `plans/specs/implementation-verification/spec.md` (the one living spec), and the archived `plans/changes/archive/2026-09-21-reproducible-bead-export/spec.md` (the lease-field stripping).

---

Not done here, by design: no design, no recommendation, no judgment — the three heartbeat threads are reported as they stand.
