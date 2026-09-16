---
title: "Review: the research corpus against the running workflow — what to adopt, what to keep, what to decide"
category: research
status: current
created: 2026-09-16
last_reviewed: 2026-09-16
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-16"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, review, adw, lakeswitch, omnigent, workflow, harness]
---

# Review: the research corpus against the running workflow

**Read at:** coding-harness `5a950c2` (main, 2026-09-16) — the three documents
under `docs/research/`, `docs/WORKFLOW.md`, `docs/governance/regelwerk.md`,
`prompts/`, `templates/`, `scripts/kit/manifest.yaml`. Cross-checked against
portfolio-agentic-engineering master `4ce8240` and the lakeswitch-ai clone.
**Measured:** nothing in this review is a benchmark; where a claim was
verifiable by reading the repository, the location is named. Where it was not,
it says `unverified`.

**Who this is for.** The maintainer, before the doctrine is rewritten. This
document decides nothing. It sorts the corpus into three piles — adopt, keep
ours, decide — and puts every open decision into §7 in the form the workflow
prescribes for questions to a human (goal, options as consequences,
recommendation with reason).

## 1 · The verdict in one screen

The corpus and the running workflow agree on the foundation and disagree on the
machinery around it.

**They agree on:** files not chat as the handover between steps; humans decide
intent, agents decide mechanics; independent review in a fresh context, ideally
across model families; Beads as the only operational task store; no agent merge
to the main branch; CI as the real enforcement, local hooks as comfort; a
living spec plus change deltas plus a dated archive; context is the scarce
resource.

**They disagree on:** *when* a meta-harness (Omnigent) enters; *where* the
contract of a change lives (ticket body vs spec file); *whether* a plan is
transcribed into task beads or stays one bead per change; *how many* human
gates a change passes; *how* a rule becomes enforced over time.

**The corpus's structural weakness:** it is normative prose. The reference
architecture grades 20 requirements MUSS itself (KB-1–6 and KB-10, IS-1–6,
AG-1–7) and consolidates about forty more by reference (I1–I6, SM-1–31,
P-rules) — and no rule names the test or gate that holds it. C5 names branch
protection as the place, KB-1 names CI as the place, §8.7 demands that every
enforcement mechanism ships a test suite; none of the sixty says *which*. The
running workflow's rule set (`regelwerk.md`) refuses exactly that: a rule
without a named test or gate stands at level 2 at most and must name a ramp
valve with a due date. Applied to the corpus, most of its MUSS lines are
"requests dressed as rules" (regelwerk §2). That is not a reason to discard
them. It is the intake procedure: **every idea adopted from the corpus enters
as a rule with an enforcer or a valve, never as prose.**

**The running workflow's blind spots the corpus fills:** no proportionality
beyond "do not plan what fits in one sentence" (the corpus has four task
classes and a one-way ratchet); no planning layer above beads (the toolchain
document has a one-page `ROADMAP.md`); no stop conditions for unattended
runs; no traceability from requirement to test; no search-first duty before
adding a dependency; no explicit approval-boundary list beyond
`permissions.deny`.

**What coding-harness should become:** one doctrine (`WORKFLOW.md`), one rule
set with the enforcement ladder, one kit manifest measured by the Leerprobe —
and the corpus as *sources* behind them, dated and cited, never normative on
its own. The instance repositories (portfolio, lakeswitch) copy the kit;
everything the toolchain document describes below the kit (Obsidian inbox,
LikeC4, Argdown, static site, Databricks domain content) is an instance
decision and stays out of the harness.

## 2 · Findings on the corpus as documents

These are defects of the files, independent of their content.

| # | Finding | Where | Why it matters |
|---|---|---|---|
| D1 | **Dated in the future.** The reference architecture says "Stand: 17. September 2026"; the toolchain document carries "Datum 2026-09-17" and four history rows (2.1, 3.0, 3.1, 4.0) dated 2026-09-17. Both were committed 2026-09-16. | ADW header; toolchain metadata block and Anhang C | "Every number carries its cut-off" (WORKFLOW §2). A future date reads as a measurement that has not happened. |
| D2 | **Two images do not exist.** `assets/arc42_bausteinsicht.png` and `assets/kontextbudget_allokation.png` are referenced; `docs/research/assets/` is absent. | ADW §3.2, §8.9 | The block view (§5.1 refers to "blau im Diagramm §3.2") and the budget calculation are argued from pictures the reader cannot see. |
| D3 | **Three ADR namespaces collide.** ADW uses ADR-01…17, the toolchain document ADR-0001…0012, portfolio ADR-009…031 (032 is proposed in portfolio PR #162, not merged). "ADR-11" in ADW (protect the enforcement layer) is not portfolio's ADR-011 (Git-first). | ADW §9; toolchain §9; portfolio `docs/adr/` | A reader inside coding-harness sees three decision series with overlapping numbers and no prefix. |
| D4 | **Five meanings of "Stufe".** WORKFLOW.md: model-routing stages 1–3. Migrationsplan: Omnigent stages 0–4. Toolchain Anhang A: build-up stages 0–7. Toolchain §8.8: solo-to-team stages 0–4. ADW: MUSS/SOLL/KANN. | all four documents | The same word cannot carry five scales in one repository (regelwerk §1: "a rule that stands everywhere is not followed either"). |
| D5 | **Unsourced numbers.** "Kosten ×2–15, Identity Drift" for orchestration (ADW §4); "~5–10k Token (~7 % eines 200k-Fensters)" (ADW §8.9); "Leerprobe 173 von 235" is sourced in portfolio evidence, the others are not. | ADW §4, §8.9 | Portfolio's rule RB-P3: a hand-typed count outside a facts block is a finding. In research it is tolerable only with a source. |
| D6 | **Unverifiable security claim.** "CVE-2026-62674, CVSS 9.0 … gefixt in 0.3.0" (ADW §11). `unverified` — not checked against a CVE database in this review. | ADW §11 | If it is wrong, the risk row that carries the Omnigent pinning argument is wrong. |
| D7 | **The toolchain document is about a different system.** Its scope is the Lake Switch development environment: Obsidian, LikeC4, Argdown, static site, PyPI release, employer IP separation. Roughly half of it is not harness material. | toolchain §5.2.1–5.2.2, §5.2.8, §8.6, Anhang B.2 | Fine as a source. As a member of "the research corpus behind the coding workflow" (`_INDEX.md`) it invites copying instance layers into the kit. |
| D8 | **Two answers to when a bead closes.** ADW §6.1 steps 8–9 and AG-4 agree with each other: close after the G4 verdict. Portfolio closes only after merge (`Closes-Bead:` trailer + `close-merged` on the integration branch). | ADW §6.1, §8.11; portfolio AGENTS.md | A difference, not a contradiction — but portfolio's rule is the stricter one and the only one with an enforcer (`ci.yml#merged-beads`, which reports a declared close nobody carried out). |
| D9 | **Language of the toolchain document contradicts the decided direction.** §2.3: "Deutsch für Wissen und Entscheidungen". lakeswitch-ai commits are English by ruleset; portfolio's AGENTS.md records English as the decided direction for content artefacts. | toolchain §2.3 | A convention line that the two instances already violate is not a convention. |
| D10 | **coding-harness's own `CLAUDE.md` does not import `AGENTS.md`.** It opens with a hand-written pointer ("instructions live in `AGENTS.md` — read them first"), then the managed Beads block, then three empty `bd init` placeholder sections ("_Add your build and test commands here_"). A pointer is not an import. | `CLAUDE.md` | RB-S1 (one instruction file, one import) travelled here as a mechanism entry and is broken in the host that owns it. Not corpus, but found while reading. |

## 3 · Comparison: topic by topic

Legend for the verdict column — **adopt** (the corpus is better, take it),
**keep** (the running workflow is better or already has it), **decide** (a
human choice, listed in §7), **out** (not harness material).

| Topic | Reference architecture (ADW) | Toolchain document (Lake Switch) | Running workflow (WORKFLOW.md, regelwerk, prompts) | Verdict |
|---|---|---|---|---|
| Handover between steps | Artefact per phase, next step reads only artefacts (S1, I1) | Ticket body + PR; handoff context at `/land-the-plane` | Artefact per phase; handover file with schema (`handover_schema.py`) at session end | **keep** — same principle, ours has the schema and a test |
| Phases | P0–P6 (idea, spec, design, plan, implement, verify, integrate) | `/decompose` → worker loop → PR | 1 Explore · 1a Interview · 2 Spec · 2a Spec-Review · 3 Plan · 4 Implement · 5 Verify · 6 Review · 7 Commit | **keep** — P2 "design with ADRs" is folded into Spec/Plan here; nothing is missing, only named differently |
| Human gates | G0–G3 and G5 human, G4 automated; bounded work passes G1 short + G5 (§8.2) | No G-gates: the human confirms the ticket list at `/decompose` and merges | Human owns *intent* only; phase gates are machine presence checks; a human sees only open `[DECISION]` marks; veto is one word | **keep** — the corpus's own constraint C7 (minutes per day) is met by the running design, not by three human gates per feature |
| Proportionality | Four task classes (Spike/Bounded/Feature/Architectural), one-way ratchet, bounded test (I5, I6) | Ticket size by context budget (< 30k tokens) | One rule: "never plan what fits in one sentence" | **adopt** — task classes with the ratchet; map each class to the phases it must pass (§8) |
| Contract of a change | Spec in `changes/<name>/` (proposal, delta specs, design, tasks) | The bead body is the contract (ticket schema 8.1.1: provenance, scope, out-of-scope, GIVEN/WHEN/THEN, DoD) | `spec.md` in the change folder is the contract; the bead tracks status ("artefacts say what, the tracker says where it stands") | **decide** (§7 D-2) — recommendation: the file; take the ticket schema's *fields* into `spec.md` |
| Task tracking granularity | Plan approved first, then transcribed into epic + task beads with dependencies (AG-2) | `/decompose` creates epic + task beads before work; workers claim | One bead per change, created before the change folder (`make change … BEAD=`); plan steps are not beads | **decide** (§7 D-3) — recommendation: one bead per change by default; task beads only where parallel workers claim |
| Bead closing | After the G4 verdict (§6.1 steps 8–9, AG-4) | At `/land-the-plane` after merge | Declared by `Closes-Bead:` trailer, executed on the integration branch; the `merged-beads` gate reports a declaration nobody carried out | **keep** — strictest, and enforced |
| Discovered work | New bead with `discovered-from` edge, never in the running task (AG-3) | Same, sighted in the weekly review | "File issues for follow-up" (AGENTS.md); no edge type named | **adopt** — the edge is one `bd` flag and makes scope creep visible |
| Test-first | "Iron law": failing test before code (ADR-05) | Tests first in the worker protocol | Test *with* the change, and for every test its counterpart that plants the fault and goes red (RB-G4 ratchet) | **keep + adopt** — keep the counterpart rule (the corpus lacks it), add the ordering as a SOLL |
| Review | G4: reviewer subagent, SHA-range diff + spec slice, Critical/Important/Minor, escalate on repeat FAIL | Cross-vendor reviewer via Omnigent | Phase 6: fresh Opus, diff + spec only, findings table with dimension (SPEC/MAINT), origin (`base`/`fix-r<N>`), `[AMBIGUITY]`, `[DIVERGENT]`; two fix-origin rounds = escalation | **keep** — richer and implemented; vocabulary stays BLOCKER/MAJOR/MINOR |
| Cross-vendor review | Target instantiation of I4 (Polly) | Reviewer with `executor.harness: kimi` | Stage 2: review on Kimi, implement on GLM, with the leak-check barrier before any foreign endpoint | **keep** — same idea; ours adds the barrier the corpus lacks (see §5.4) |
| Model endpoints and residency | Not addressed; "LLM-Provider … austauschbar" | `deny_pii_in_llm_request` policy; keys in `.env` | `model-endpoints.yaml`: every named model resolves to a declared endpoint with operator, residency, billing; customer code only to declared residency; unlisted is BLOCK (RB-A6, tested) | **keep and feed back** — a hard gap in the corpus for any customer-facing instance |
| Rule enforcement over time | MUSS/SOLL/KANN; Migrationsplan has exit criteria per stage | Policies as gates; verification list B.1 | Enforcement ladder 1–5; each rule names its test; ramp valves with due dates (`ramp_valves.py`); mutation test per gate (RB-G4); non-vacuity (RB-G7) | **keep and feed back** — the corpus has no mechanism for a rule that is not yet enforced |
| Portability | Harness neutrality via MCP/ACP/AGENTS.md (C2, ADR-07) — asserted | Portability via `AGENTS.md` + Omnigent YAML (Q2, S4) — asserted | Kit manifest with the roles `mechanismus`/`geruest`/`bestand`, Leerprobe copies the mechanism into an empty repo and measures (173 of 235 green, 2026-09-16) | **keep** — the Leerprobe is the only *measurement* of C2 in the whole corpus |
| Learning loop | Confidence lifecycle for learned rules: score 0.3–0.9, project scope, promote after 2+ projects, injection budget of 6 rules (ADR-13, KB-3) | Lessons in `brain/`, weekly curation | Lessons (level 7) are experience, not rule; binding only through governance + a gate; human PR | **keep** — see §5.6; the confidence score has no measurement behind it |
| Context budget | KB-1–10: verdict-not-log, delta loading, ≤ 15 % fixed cost, telemetry in every gate report | Sessions end at about half the window; tickets cut by budget | `/clear` between plan and implement; new session at ~60 %; instruction files ≤ 200 lines (RB-S1, tested); subagents for exploration and review | **adopt in part** — KB-1/2/6/8 are already practice; KB-10 (telemetry) has no enforcer in Claude Code today → level 2 with a valve |
| Unattended runs | Night mode with stop conditions, heartbeat, spend cap, checkpoint commits (P6-5, §6.4, §8.4) | Omnigent automations with `max_cost_usd` and explicit permission mode | Stage 2 `run_change.sh`: segments a marked plan into sessions with a verify gate after each, pauses with exit 2 on an open `[AMBIGUITY]`, BLOCKER or MAJOR; no stop conditions | **adopt** — stop conditions (max iterations, time, idle) belong into the Stage-2 runner spec; the Omnigent parts wait |
| Approval boundaries | Model is never final authority for unsandboxed shell, network egress, secret paths, writes outside the repo, workflow dispatch (§8.4) | `write_paths`, `github_policy`, `ask_on_os_tools` | `permissions.deny` ≥ prod deploy, `bundle destroy`, force-push, `rm -rf` (RB-A2, tested); read-only agents have no shell | **adopt** — complete RB-A2's list with the five boundaries; note that path rules do not catch `Bash` writes (WORKFLOW §3) |
| Planning above beads | Vision + spec register | `ROADMAP.md` Now/Next/Later, Shape-Up appetite, one page; milestones as derived view | None — `journal/planning/` ages by design; beads carry epics | **adopt** — one `ROADMAP.md` per instance, in the kit as a template |
| Meta-harness / Omnigent | Target runtime from stage 0 (C11, ADR-17); Migrationsplan stages 0–4 | From build-up stage 5 only, purely additive; git-native gates must work alone (ADR-0007, P6) | Stage 3, "evaluative, not productive"; order: process, then model diversity, then orchestration (§6) | **keep** — the toolchain document and the running workflow agree; ADW's C11 is the outlier (§5.1) |
| Session substrate (tmux/Herdr) | IS-1–6 | Omnigent terminals | Stage 2 `--mode herdr` as a *human's* visibility tool, not a dependency; "no multiplexer isolates anything" | **keep** — IS-5 in ADW says the same; the rest is Omnigent-specific |
| Worktrees | Worktree per task (P4) | Inside the repo under `.claude/worktrees/<ticket-id>/` so `bd` finds `.beads/` walking up | One worktree per change, condition: every tree sees the same tracker state and the export moves only by what a session did — "half two holds nothing today" (§3) | **decide** (§7 D-5) — the prefix defect reproduced today (portfolio wp-p0.1) is exactly this seam |
| JSONL export | Committed alongside as audit view (AG-6) | Written **only** at `/land-the-plane` on main, never from a worktree; `bd` auto-commit and auto-hooks off (R15) | Rendered by script; coding-harness set `export.auto true` at bootstrap | **decide** (§7 D-4) — portfolio broke the export three times in four days; the toolchain document's rule is the measured lesson |
| Local gates | CI + hooks | `.pre-commit-config.yaml` (ruff, mypy, gitleaks, commit format) **and** CI "wie Stufe 2, serverseitig" | Exactly one gate list in `ci.yml`; `make verify` reads it; no pre-commit by decision (WORKFLOW §8, RB-G1 tested) | **keep** — two lists drift; the toolchain document reintroduces the second list the running workflow measured and removed |
| Static analysis | — | `mypy` | `ruff` + `pytest` only, pinned in `requirements-ci.txt` | **decide** (§7 D-6) — for lakeswitch (a Python product) `mypy` is reasonable; for the kit it is a new gate needing a mutation test |
| Instruction file | `AGENTS.md` (C6) | `CLAUDE.md` = `@AGENTS.md` only (ADR-0012) | `CLAUDE.md` = `@AGENTS.md` + short addendum (conversation language, slash commands) ≤ 200 lines | **keep** — the addendum is the one thing a bare import cannot carry; coding-harness itself violates both today (D10) |
| Traceability | FR-ID → scenario → test → commit → PR → change → archive; generated matrix; gaps are blocking (SM-28, §8.5) | Provenance field in ticket; ADR links | Acceptance criteria in `spec.md`; review checks each; no IDs, no matrix | **adopt in part** — IDs in `spec.md` and in test names at level 2 first; the generated matrix is a gate that needs a mutation test before it blocks |
| Search-first for dependencies | Adopt/Extend/Build with ≥ 2 candidates; skipped channels declared (§6.1 step 4) | — | Practice ("established best practice, name the source"), not a rule | **adopt** — as a Plan-phase line with a `[DETAIL]` reason in the artefact |
| Verification report | Normalised `verification-report.md`: Build/Types/Lint/Tests/Security/Diff × PASS/FAIL, READY/NOT READY | CI status | `make verify` output as evidence; `_verdict.py` shared exit vocabulary; gate record for *human* gates only | **adopt** — as a machine-rendered file from `verify_all.sh`, not hand-written; pairs with RB-P3 |
| Living spec model | Two levels: living specs per domain + change deltas (ADDED/MODIFIED/REMOVED/RENAMED), sync at archive, drift audits (SM-*) | Optional `openspec/` | `plans/specs/<capability>/spec.md` living, `plans/changes/` active, dated archive; two status fields; delta into the living spec at close | **keep + adopt in part** — the model is the same; the delta section vocabulary and "MODIFIED carries the full new text" (SM-3) are worth taking; drift audits wait for traceability IDs |
| Knowledge layers (Obsidian, LikeC4, Argdown, site) | — | L0 and L6 in detail | Portfolio: ADR-026 eight knowledge levels; lakeswitch: its own | **out** — instance layer |
| Employer/IP separation, PyPI, SBOM | — | Anhang B.2, §8.6 | — | **out** — lakeswitch decision |

## 4 · Where the three research documents contradict each other

Contradictions between sources are findings, not preferences. Each needs one
answer.

1. **When Omnigent.** ADW C11/ADR-17: target runtime, POC in stage 0 of the
   Migrationsplan. Toolchain ADR-0007: from build-up stage 5, additive only,
   "the preventive layer may never be a precondition for the reactive one"
   (P6). WORKFLOW §5–6: stage 3, evaluative, after process and model
   diversity. **Two of three say late and additive.** ADW's argument
   ("Einzige verfügbare Instanz, die mehrere Bausteine produktfertig liefert")
   is a market claim without a measurement; its own §11 lists alpha maturity
   with fast breaking changes, telemetry default and a critical CVE, and the
   toolchain document puts the breaking changes at weekly cadence (§2.1).
2. **Where the contract lives.** ADW: change folder with delta specs.
   Toolchain: the ticket body, with `Size` and `Out of scope` as normative
   fields. WORKFLOW: `spec.md`. A bead body cannot be reviewed in a pull
   request, is not covered by `validate_change_artefacts.py`, and the tracker
   export has broken repeatedly; the file can be gated and diffed.
3. **Worktree placement.** ADW: silent. Toolchain: inside the repo under
   `.claude/worktrees/<ticket-id>/`, reasoned from `bd`'s upward search and
   Omnigent's sandbox. Portfolio practice and its memory: sibling directory
   (`../portfolio-wt-<name>`) off `origin/master`. Today's live reproduction
   (portfolio PR #162): `bd create` in a worktree whose directory name differs
   from the repository name produced a wrong id prefix. The toolchain's
   placement rule may or may not avoid this — `unverified`; it is a
   verification item, not a decision yet.
4. **Export writing.** ADW AG-6: export committed as audit view (no rule on
   *who* writes it). Toolchain: only `/land-the-plane` on main writes it;
   never from a worktree. coding-harness bootstrap: `export.auto true`.
   Portfolio: `render_beads_export.py`, plus the gate that the export is
   byte-identical to what the store renders. The toolchain rule is the
   lesson portfolio learned the hard way (WORKFLOW §3: broken three times in
   four days).
5. **Number of human gates per change.** ADW: G1, G2, G3, G5 for a Feature.
   Toolchain: confirmation at `/decompose` and merge. WORKFLOW: none as
   approval steps; a human answers open `[DECISION]` marks and merges. ADW's
   own C7 and Q5 (≤ 10 minutes of human time for bounded work) are met by the
   WORKFLOW design; three approval gates per feature are met only by task
   classes — which is why ADW needs them and WORKFLOW does not.
6. **Stage vocabulary.** See D4. The Migrationsplan's stage 0 (Omnigent POC)
   and the toolchain's stage 0 (repo skeleton, no agents) are unrelated
   events with the same name.

## 5 · The challenges

### 5.1 Omnigent as target runtime is a commitment the evidence does not carry

ADW makes Omnigent a *constraint* (C11) and a *decision* (ADR-17). Its
evidence is a feature list. Its own risk table says: alpha with fast breaking
changes, telemetry opt-out required, one critical CVE in history, sandbox
asymmetric across platforms; the toolchain document adds "breaking changes
weekly" (§2.1, ADR-0007). The Migrationsplan then spends stages 0–4 on
instantiating it. Nothing in the running workflow depends on any of this, and
the toolchain document's ADR-0007 shows the sounder shape: git-native gates
first, they must work alone, the policy layer is added later and only adds.

**Consequence for coding-harness:** Omnigent stays where WORKFLOW §5 put it —
stage 3, evaluative — and the Migrationsplan is parked as a source until the
stage-2 signal exists (WORKFLOW §6: "the phase gates bite without thinking, and
Sonnet implementation is the visible cost block" — unmeasured today; portfolio
bead `uqvm` is paused for that reason). The Migrationsplan's *form* is worth
keeping where it holds to its own principle 2 ("exit criteria, not
durations"): stages 0–2 carry exit and abort criteria, one active topology
per class, a retrospective in the repo. It does not hold everywhere — every
stage heading still carries a duration, stages 3 and 4 have no abort
criteria, stage 4 no exit criteria. Where it holds, that form is what a ramp
valve is for a whole stage.

### 5.2 Sixty rules, none names its enforcer

Take KB-10: every gate report contains the current context occupancy, and a
fixed-cost share (system, rules, spec, evidence) above 15 % of the window is
a review finding. Claude Code exposes context occupancy to the status line,
not to hooks or subagents, and nothing separates the fixed-cost share from
the rest. There is no way for a gate report to contain it today. As written,
KB-10 is a MUSS that cannot be red. The
regelwerk's answer is exact: a rule without an enforcer stands at level 2 and
names a valve with a due date, or it is not written. The same test applies to
SM-25 (periodic drift audit), SM-28 (generated traceability matrix), AG-4
(evidence-bound closing), IS-3 (observability of every session), §8.7
(runtime non-vacuity). Each is a good idea; each needs the ladder.

**Consequence:** intake of the corpus into the doctrine goes through
`regelwerk.md`. For every adopted line: rule sentence, level, enforcer or
valve, scope (P/L/I). What cannot be given a level is a lesson, not a rule —
and lessons are experience (portfolio level 7), binding only through a gate.

### 5.3 The corpus has no mechanism for "not enforced yet"

The Migrationsplan has exit criteria for stages 0–3. ADW has MUSS/SOLL/KANN. Neither
has the object the running workflow calls a ramp valve: a named, dated
statement that check X reports lower than it should, with the condition under
which it steps up — and a gate that goes red when the condition is met and
nobody stepped it up. Without it, "temporarily non-blocking" is permanent.
The corpus should adopt this from the running workflow, not the other way
round.

### 5.4 The corpus does not know about data residency

ADW treats LLM providers as interchangeable (§3.2) and cross-vendor review as
a pure quality measure. The toolchain document has one policy that scans
prompts for PII. Neither has the rule that portfolio enforces and that
travelled to coding-harness as a mechanism entry: every model name resolves to
a declared endpoint with operator, residency and billing; customer code goes
only to endpoints with declared residency; customer data goes to none;
unlisted is BLOCK (RB-A6, `tests/test_model_endpoints.py`). Stage 2 in
WORKFLOW §4 additionally requires `make leakcheck` before any artefact leaves
for a foreign endpoint. For any instance that touches a customer estate this
is the constraint that decides whether cross-vendor review is *allowed*, not
merely useful. It belongs in ADW §8.4 next to the approval boundaries.

### 5.5 Task classes are right; three human gates are not

ADW's four classes with the one-way ratchet and the bounded test are the best
proportionality rule in the corpus and the running workflow has nothing
comparable. But ADW pairs them with G1/G2/G3 as human approvals, which is the
load its own C7 forbids. The running workflow already resolved this
differently: the human owns intent, the machine checks presence, and a human
sees only what is genuinely open. Adopt the classes, keep the gate design.
What the classes then decide is *which phases are mandatory*:

| Class | Recognition | Mandatory phases | Human touch |
|---|---|---|---|
| Spike | a feasibility question; the output is a recommendation | 1 Explore, time-boxed; result in `research.md` | reads the recommendation |
| Bounded | change to an existing, readable flow (bounded test: no existing flow → not bounded) | 4 Implement · 5 Verify · 7 Commit; `spec.md` may be five lines | open `[DECISION]` marks, merge |
| Feature | self-contained deliverable | all seven; 1a and 2a optional by the author's stated reason | open `[DECISION]` marks, merge |
| Architectural | new subsystem or interface break | all seven, 1a and 2a mandatory, an ADR in the change | open `[DECISION]` marks, ADR sign-off, merge |

Ratchet: a class may go up mid-change, with a stop and a reason in the
artefact; never down. "Do not plan what fits in one sentence" survives as the
lower edge of Bounded.

### 5.6 The confidence lifecycle is pseudo-precision

ADW ADR-13 (from ECC) gives learned rules a confidence score 0.3–0.9, a
project scope, promotion after two projects, an injection budget of six rules
at ≤ 250 tokens. Nothing measures the score; it is set by the writer. The
running workflow's model is simpler and honest: a lesson is written as
experience; it becomes a rule only when someone writes the rule with its
enforcer and a human merges the PR; a rule that cannot be enforced names a
valve. The injection budget is real (RB-S1, ≤ 200 lines, tested) and is the
only part worth keeping. Recommendation: do not adopt the score; keep the
budget; record ECC as the source for the budget number.

### 5.7 Beads: one bead per change, not a transcribed plan

ADW AG-2 and the toolchain's `/decompose` both create an epic with task beads
before implementation, so parallel workers can claim. The running workflow
creates exactly one bead per change, before the change folder exists, and
keeps plan steps in `plan.md`. Two observations decide this: the tracker
export is the most fragile file in portfolio (three breaks in four days;
today's prefix defect), and parallel workers claiming tasks is a stage-2/3
scenario, not stage 1. Multiplying beads multiplies exposure to the fragile
seam for a benefit that does not exist yet. Recommendation: one bead per
change stays the default; task beads under an epic become the rule for
Feature and Architectural classes **once** a stage-2 run actually has two
workers claiming — and then with the `discovered-from` edge (AG-3) from day one.

### 5.8 The toolchain document reintroduces the second gate list

`.pre-commit-config.yaml` with ruff, mypy, gitleaks and commit format, and CI
"like stage 2, server-side". WORKFLOW §8 and RB-G1 forbid exactly this, from
measurement: two lists drift, and the divergence is noticed when someone
relied on the wrong one. The local gate is `make verify`, which reads
`ci.yml`. If a pre-commit hook is wanted for speed, it is *generated* from
the same list or it is not there. The toolchain document should say so.

### 5.9 What the corpus adds that the running workflow should take

In priority order, with the enforcement level each can have *today*:

1. **Task classes + ratchet** (§5.5) — level 2 now (the class is a field in
   `spec.md` frontmatter; `validate_change_artefacts.py` can check presence at
   level 4 with one test).
2. **`ROADMAP.md`** Now/Next/Later, one page, appetite per Now item, epic
   reference once cut — level 2 now; a template in the kit; `plans_registry`
   can check that every active change names a Now item (level 4 later).
3. **`discovered-from` edges** for work found mid-task — level 2 now; the
   `dangling-beads` gate can verify every new bead created during a change has
   the edge (level 4 later).
4. **Stop conditions for the stage-2 runner** — max segments, wall-clock
   limit, idle detection (no new commit in N segments) — level 4 as soon as
   `run_change.sh` has a test for each (its fake-session suite exists:
   `tests/test_orchestrator.py` in portfolio).
5. **Approval boundaries** completing `permissions.deny` — network egress
   tools, secret paths, writes outside the repository, workflow dispatch —
   level 4 (extend `test_settings_deny_the_irreversible_commands`).
6. **Search-first for dependencies** — a Plan-phase line: two candidates,
   skipped channels named — level 2 now; `[DETAIL]` reason goes in `plan.md`.
7. **Requirement IDs in `spec.md` and test names** — level 2 now; the
   generated matrix later, as a gate with a mutation test.
8. **Machine-rendered verification report** — `verify_all.sh` writes a
   READY/NOT READY file with per-gate verdicts; level 4 once it exists,
   because RB-P3 already forbids a hand-typed one.
9. **Delta section vocabulary** for the living spec (ADDED/MODIFIED/REMOVED/
   RENAMED; MODIFIED carries the full new text) — level 2 in `plans/_README.md`.
10. **Compaction protect list** (KB-7) — Claude Code has a `PreCompact` hook;
    a hook that re-injects the open `[DECISION]` marks and the current change
    name is small and testable — level 4 possible.

### 5.10 What the running workflow has that the corpus should take

Feed back into ADW when it is next revised (these are the parts that make
coding-harness *the* foundation rather than one more instantiation):

- the question protocol `[DECISION]` / `[GAP]` / `[DETAIL]` — sharper than
  the clarify loop; it forbids asking a human a mechanics question;
- the findings table with dimension, origin and the two overriding marks;
  and the rule that two consecutive fix-origin rounds are an escalation;
- the enforcement ladder, ramp valves, mutation test per gate, non-vacuity
  as a *tested* property;
- the kit manifest and the Leerprobe as the measurement of portability;
- endpoint residency and the leak-check barrier;
- provenance classes on every artefact and generated-not-typed numbers;
- the handover file with a schema, and "every number carries its cut-off".

## 6 · What coding-harness is, and is not

**Is:** the doctrine (`WORKFLOW.md`), the phase prompts, the templates, the
rule set with its ladder and valves, the kit manifest and the Leerprobe, the
model routing and the endpoint declaration, the session handover — and the
research corpus as dated sources behind them.

**Is not:** an instance's knowledge layers (Obsidian, LikeC4, Argdown, static
site), an instance's domain content (Databricks, migration patterns), an
instance's release pipeline, a meta-harness deployment.

**One vocabulary.** Proposal, to be decided (§7 D-1):

| Today | Proposed | Scope |
|---|---|---|
| WORKFLOW "Stufe 1–3" | **Stage 1–3** (model routing: single vendor → cross-vendor → meta-harness) | harness |
| Toolchain "Stufe 0–7" (Anhang A) | **Setup step S0–S7** | instance build-up |
| Toolchain "Stufe 0–4" (§8.8) | **Team level T0–T4** | instance |
| Migrationsplan "Stufe 0–4" | **Omnigent adoption M0–M4** | parked |
| ADW "MUSS/SOLL/KANN" | **Level 1–5** of the enforcement ladder | rule set |
| ADW "ADR-nn", toolchain "ADR-nnnn" | **ADW-Dnn**, **LS-ADR-nnnn** whenever a harness document cites them; the corpus keeps its own numbering; harness decisions get their own series when the first one is written | harness citations |

**Order of work** (unchanged from WORKFLOW §6, sharpened): process → model
diversity → orchestration. Concretely: (1) intake of §5.9 items 1–3 and 5–6
as rules; (2) the first full seven-phase run *in this repository* with
metrics (portfolio `uqvm`'s successor); (3) stage 2 with the runner's stop
conditions; (4) only then the Migrationsplan.

## 7 · Decisions for the maintainer

Each in the form `prompts/02-spec.md` prescribes: goal in one sentence, options
as consequences, recommendation with reason, and what happens on "ok".

### D-1 · One stage vocabulary

**Goal:** one word per scale, so "Stufe 2" has one meaning in this repository.
**Options:** (a) rename as in §6 — three documents change a handful of
headings; (b) keep the words and add a disambiguation table to the research
index — nothing changes, every reader carries the table; (c) rename only in
the harness documents and leave the corpus as is — the corpus becomes the
odd one out, which is acceptable for sources.
**Recommendation:** (c). The corpus is a source; sources keep their wording
with a note. The harness speaks one language, and cites the corpus with the
prefixes from §6.
**On "ok":** WORKFLOW.md keeps "Stage 1–3"; the research index gets the table
from §6; the corpus documents are not renamed (the two rename items in §8
apply only under option (a)).

### D-2 · Where the contract of a change lives

**Goal:** one place a reviewer and a gate read to know what was promised.
**Options:** (a) `spec.md` — reviewable in the PR, gated by the validator;
the bead carries status only; (b) the bead body per the toolchain's ticket
schema — visible to `bd ready`, not diffable in a PR, outside every gate;
(c) both — two truths.
**Recommendation:** (a), and take four fields from the ticket schema into the
spec template: *out of scope*, *protected areas*, *failure mode* (what wrong
output looks like), *size* as a context-budget class.
**On "ok":** `templates/` spec template gains the four fields; the toolchain
document's 8.1.1 is annotated as "instance choice, superseded by spec.md in
harness instances".

### D-3 · One bead per change, or task beads

**Goal:** a tracking granularity that the tracker seam can carry.
**Options:** (a) one bead per change (today) — no claims for parallel
workers, minimal exposure; (b) epic + task beads transcribed after the plan
gate (ADW AG-2) — enables parallel claiming, multiplies writes to the fragile
export; (c) (a) by default, (b) for Feature/Architectural once stage 2 has two
workers.
**Recommendation:** (c); see §5.7.
**On "ok":** WORKFLOW §2 gains the sentence; nothing else changes until stage 2.

### D-4 · Who writes the JSONL export

**Goal:** an export that never carries conflict markers.
**Options:** (a) `export.auto true` (coding-harness today) — every write
renders; worktrees collide; (b) only the session-end handover step on the
integration branch writes it (toolchain `/land-the-plane`) — one writer, one
moment; (c) portfolio's render script plus the byte-identity gate — one
writer, and a gate that catches a second.
**Recommendation:** (b)+(c): the render script is the only writer, the
session-end step is the only moment, the gate checks identity; `export.auto`
off. This also settles the "one writer per tracker" house rule with a
mechanism instead of a request.
**On "ok":** `bd config set export.auto false` in coding-harness; the
handover prompt names the render step; the identity gate enters `ci.yml`
with `bo0`.

### D-5 · Worktree placement

**Goal:** a worktree in which `bd` behaves exactly as in the main checkout.
**Options:** (a) sibling directory (today's practice) — known defect: wrong
id prefix when the directory name differs; (b) inside the repository under an
ignored path with the change name (toolchain rule) — `unverified` whether the
prefix defect depends on the directory name or on the worktree mechanism;
(c) no `bd` writes from worktrees at all — beads are created in the main
checkout before the worktree exists (today's `make change` order already
does this).
**Recommendation:** (c) now, because it is true today and needs no
verification; run the toolchain's four-point verification (5.2.6) once, in a
throwaway repository, before choosing (a) or (b) — with the prefix defect as
a fifth point.
**On "ok":** the house rule "no `bd create` outside the main checkout" is
written; the verification is a bead in coding-harness.

### D-6 · `mypy` and other instance gates in the kit

**Goal:** the kit carries only gates the Leerprobe can measure everywhere.
**Options:** (a) `ruff` + `pytest` only (today); (b) add `mypy` to the kit —
every instance inherits a type gate, including docs-only ones; (c) `mypy`
as an instance gate in lakeswitch's `ci.yml`, not in the kit.
**Recommendation:** (c).
**On "ok":** nothing changes in coding-harness; the toolchain document keeps
`mypy` in L5 as lakeswitch's own.

### D-7 · What happens to the Migrationsplan

**Goal:** a document that is either a plan somebody executes or a source
somebody cites.
**Options:** (a) keep as research, parked, with the precondition named
(stage-2 signal measured); (b) archive it; (c) start stage 0 (POC) now.
**Recommendation:** (a). The form of its stages 0–2 (exit and abort
criteria, no reliance on the duration in the heading) is the model for how
stage 2 should be written up.
**On "ok":** the research index marks it "parked until stage-2 signal
(WORKFLOW §6)".

### D-8 · Corrections to the corpus documents

**Goal:** sources that do not mislead.
**Options:** (a) apply the corrections in §8 as one PR after these decisions;
(b) leave the documents untouched and let this review stand beside them;
(c) delete the toolchain document from coding-harness and keep it in
lakeswitch only.
**Recommendation:** (a) for D1–D3, D8–D9 (mechanical, no judgement); (b) for
everything else — a reviewed source with a review beside it is more honest
than a silently corrected one.
**On "ok":** one PR with the §8 list.

## 8 · Proposed corrections to the three documents

Concrete, so they can be applied without re-reading this review. None is
applied here: the documents are unreviewed drafts, and a parallel session may
hold them open.

**Reference architecture (ADW)**

1. Header: "Stand: 17. September 2026" → "Stand: 16. September 2026 (übernommen), Fassung 1.2".
2. §3.2 and §8.9: remove the two image references or add the files under
   `docs/research/assets/`; the block view text in §5.1 must stand without
   the picture ("blau im Diagramm" → name the four main blocks in words).
3. §4 "Kosten ×2–15": add the source or mark `unbelegt`.
4. §6.1 step 9 vs AG-4: align to AG-4 wording, then to the stricter portfolio
   rule if D-3/D-4 are decided ("a bead closes when the declaring PR is on
   the integration branch").
5. §8.4: add the endpoint-residency boundary (§5.4 above) as a sixth approval
   boundary.
6. §9: prefix the internal series `ADW-D01…D17` and say so in a note.
7. §11 CVE row: mark `unverified` until checked, with the check date.
8. New §8.12 (or a note in §8.7): "a rule without an enforcer names a valve
   with a due date" — cite `regelwerk.md` §2–3 as the source.

**Toolchain document (Lake Switch)**

1. Metadata "Datum 2026-09-17" → 2026-09-16; Anhang C rows dated 2026-09-17
   → 2026-09-16 (or the true dates if the versions were written earlier).
2. §2.3 language line → "English for content artefacts, commit messages and
   PR bodies (decided direction; German transitional in existing
   documents)".
3. §5.2.7 stage 2 (pre-commit) → "generated from the one gate list, or
   absent"; cite WORKFLOW §8.
4. §5.2.6 worktree rule: add the prefix defect (portfolio wp-p0.1,
   reproduced 2026-09-16) as the fifth verification point.
5. §8.1.1 ticket schema: add a note "in harness instances the contract is
   `spec.md`; these fields migrate there (D-2)".
6. Anhang A: rename "Stufe" → "Setup step" only if D-1 (a) is chosen; under
   (c) add the disambiguation note instead.

**Migrationsplan**

1. Header: add "parked until the stage-2 signal (WORKFLOW §6) is measured".
2. "Stufe 0–4" → "M0–M4" only if D-1 (a); under (c) the note suffices. The
   exit/abort form of stages 0–2 stays as the model for stage write-ups;
   stages 3–4 lack abort criteria and stage 4 lacks exit criteria — add them
   or say why not.

**coding-harness itself (found while reading, D10)**

1. `CLAUDE.md`: replace the three placeholder sections with nothing; keep the
   managed Beads block; add `@AGENTS.md` as the first line so RB-S1 holds in
   the repository that owns the rule.

## 9 · What this review did not do

- Did not run the Leerprobe. The test suite was run once in this review's
  worktree at `5a950c2` (`pytest tests/ -q`): 64 failed, 182 passed,
  4 skipped — unchanged by this document. The bootstrap handover's
  167/60/4 is the same run with `test_kit.py` excluded (see the review on
  coding-harness PR #1).
- Did not verify the Omnigent version claims (v0.7.0 … v0.13.0 feature
  attributions) or the CVE.
- Did not read the lakeswitch-ai instance's `docs/workflow.md` beyond
  confirming it exists; whether the instance diverged from the kit is the
  Leerprobe's question, not this review's.
- Did not create a bead: one writer per tracker, and a parallel session
  could not be excluded. The maintainer creates the intake bead when picking
  up §7.
