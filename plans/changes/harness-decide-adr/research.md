---
title: "Research — harness-decide-adr"
status: draft
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-3ar
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# harness decide adr — Research

Phase 1 after [`prompts/01-explore.md`](../../../prompts/01-explore.md). Facts
as read on 2026-09-30: lakeswitch-ai `main` at `9b9d5c8` (merge of PR #62),
this worktree at `39d2e12`. Everything here was read in this session unless it
says "not read". Section 7 (open points) and section 8 (size and smallest
version) were asked for by the caller of this phase; they are candidates for
the phase 1a interview, not decisions.

The change covers two beads:

- Bead `coding-harness-3ar` — found the principle "research → interview →
  signed decision → ADR or Feature" in Coding Harness; the LakeSwitch pilot is
  lakeswitch-ai PR #62. Due 2026-10-15. Done when "LakeSwitch has deleted its
  own M-31 and the adr-answer command and reads the pinned Coding Harness
  version; no second copy of the format exists" (bead acceptance criteria).
- Bead `coding-harness-in1` — signed decisions: a new key cannot approve itself,
  and a retired key keeps what it signed (a bug in LakeSwitch gate M-30).

Related: bead `coding-harness-xv3` (`harness decide`: digest, ratification
generator, guided flow, reminder). Its ratification-generator part is obsolete
since ratification entry by entry ended (lakeswitch-ai PR #65, commit
`120bf2b`). Bead `coding-harness-4me` (findings as checked data) depends on
`3ar` and is queued behind it.

## 1 · What the LakeSwitch pilot does

### 1.1 The command `lakeswitch decide adr`

Wiring: `src/lakeswitch/cli.py`, `cmd_decide_adr` (subparser `decide` →
`adr`), calling `adranswer.decide_adr(repo.root())`. Logic:
`src/lakeswitch/adranswer.py`, function `decide_adr` and helpers.

- **Input.** Every change anchor `plans/changes/*/spec.md` and
  `plans/changes/archive/*/spec.md` (`adranswer.anchors`). The class is read
  from its frontmatter line first (`declared/change_anchor.py`,
  `anchor_class`); only `class: feature` anchors are parsed further, into
  `ChangeAnchorDocument` (title, `change`, `adr_question.proposed`,
  `adr_question.reason`, `intent.outcome`, plus fields admitted but unexamined).
- **Open questions** (`open_questions`): each Feature without
  `decisions/answers/<change>/adr.yaml`. An existing answer file the gate would
  refuse, or an anchor whose class cannot be read, stops the command with exit
  2 before anything is asked.
- **Dialogue.** Refuses without a terminal (exit 2). Per change it shows title,
  outcome, the proposal and its reason; takes only `y`/`n` (`_yes_no`); asks for
  a one-sentence reason, re-asking when it does not start with a capital letter
  or a backtick (`declared/adr_answer.reason_problem`) or when LakeSwitch gate
  M-6 (the denylist over commit messages, pattern DL-5 = German prose) would
  refuse it (`_message_problem`, which reads `floor.denylist._patterns`). Then
  three explain-back lines, the whole message re-checked against M-6. Ctrl-C /
  EOF writes nothing (exit 1).
- **Output.** One `adr.yaml` per answered change and a commit message file at
  `git rev-parse --git-path ADR_ANSWER_MSG` (`_message_file`). It never commits
  and never signs; it prints `git add decisions/answers` and
  `git confirm -F <file>` (`git confirm` is the maintainer's global git alias
  that signs with the Secure Enclave key — `docs/how-to/signed-decisions.md`
  in this repository).

### 1.2 The record format

`decisions/answers/<change>/adr.yaml`, model `AdrAnswerDocument`
(`src/lakeswitch/declared/adr_answer.py`), `schema_version: 1`:

| Field | Content |
|---|---|
| `change` | the change name, `^[a-z0-9][a-z0-9-]*$`, must equal the folder |
| `question` | literal `adr` |
| `answer` | `yes` / `no` |
| `reason` | non-empty, starts with a capital letter or a backtick |
| `shown` | `{proposed, proposal_reason}` — what the command displayed |
| `answered_by` | a roster role (`adranswer.ROLE = "architect"`), not a person |
| `answered_at` | date |

Five answer files exist (read): `agent-instructions-ask`,
`agent-merge-and-delete-ask`, `m30-merge-own-content`,
`m30-signed-decision-paths`, `signed-adr-answer` — all `answer: 'no'`, all
written by the maintainer's signed commit `9d34f91` (2026-09-28). Plus
`decisions/answers/pilot.yaml` (`AnswerPilotDocument`: `expires: 2026-10-15`,
`why`).

### 1.3 What gate M-31 checks

`adranswer.examine` (entry `lakeswitch.adranswer:check` in
`decisions/gates.yaml`, kind `existence`, `floor: false`; spec
`spec/gates.md` G-17 and acceptance criterion 24):

- the pilot file exists, parses, and `today < expires` — from the date on, a
  finding naming both ways out (move to Coding Harness, or sign a later date);
- every Feature anchor (active and archived) has an answer file that parses
  and names its own change;
- an anchor whose class cannot be read, or that is not UTF-8, is a finding;
- no Feature at all → nothing examined, never a pass (G-2).

M-31 does **not** check the signature. That is gate M-30's job, because the
file lies under `decisions/`, a signed-decision path.

### 1.4 How signing is verified (gate M-30)

`src/lakeswitch/signatures.py` (entry `lakeswitch.signatures:check`, kind
`signature`), declaration `decisions/signers.yaml` read through
`declared/signers.py` `SignersDocument`; spec `spec/gates.md` G-16, criterion
23.

- The declaration names an anchor commit (`c02f11d`, 2026-09-23), the
  signed-decision paths (`decisions/`, `docs/adr/`, `harness.lock.yaml`;
  `decisions/` and `docs/adr/` are mandatory, `REQUIRED_PATHS`) and the signers
  (principal = roster role, key body, fingerprint checked against the key,
  `held_in`). One signer today: `architect`, ECDSA nistp256 in the Secure
  Enclave, `SHA256:LMqO…QM7c`.
- `_examine`: builds **one** allowed-signers file from the declaration
  (`SignersDocument.allowed_signers`, `namespaces="git"`, no validity options),
  runs `git -c gpg.ssh.allowedSignersFile=… log --format=%H%x00%P%x00%G?%x00%GK
  HEAD --not <anchor parents>` and accepts a commit touching a declared path
  only with status `G` and a declared fingerprint (`_judge`).
- Merges are judged by their compact combined diff only (`_merge_writes`);
  symlinks/submodules at or above a declared path are findings (`_redirected`);
  a shallow clone, missing `ssh-keygen`, or missing anchor is "unreachable",
  never a pass.

### 1.5 Generic versus LakeSwitch-specific

| Part | Generic (portable as is) | LakeSwitch-specific |
|---|---|---|
| Answer format | all seven fields; the reason rule | `answered_by` value `architect` (from LakeSwitch's roster / provenance map) |
| Anchor | `class`, `adr_question.{proposed,reason}`, title, outcome | the full LakeSwitch anchor schema (`intent.*`, `class_history`, `appetite`, `review`) from decision D-24/D-25/D-28 of its decision interview |
| Gate M-31 | Features need an answer; archive counts; empty ≠ pass | `pilot.yaml` expiry (pilot only); result type `lakeswitch.verdict.Result`; entry form `module:function` |
| Command | terminal-only, y/n, reason, 3 explain-back lines, writes files + message, never signs | the M-6 / DL-5 denylist check; the `git confirm` alias; message text citing D-12, D-27, D-61 |
| Gate M-30 | the whole algorithm (anchor, paths, merge by `--cc`, reach) | the pydantic declared-document layer (`admit`, `BoundaryError`, `StrictModel`); `harness.lock.yaml` as a default path |

Infrastructure the pilot uses and Coding Harness does not have: the pydantic
declared-document layer (`src/lakeswitch/declared/`), `lakeswitch.repo`,
`lakeswitch.verdict`, `lakeswitch.floor.denylist`.

## 2 · What Coding Harness has today, and what is missing

### 2.1 Exists (read in this worktree)

- **The principle's front half.** `docs/WORKFLOW.md` §2: phase 1a interview
  (optional, called by a person) writing `decisions.md` as Y-statements; the
  question protocol `[DECISION]`/`[GAP]`/`[DETAIL]`; "Artefact lifecycle":
  ADRs at `docs/adr/NNNN-title.md`, permanent, append-only; on close
  "permanent architectural decisions as an ADR". `prompts/01a-interview.md`:
  "What holds beyond this change later moves unchanged into an ADR".
- **Six ADRs** under `docs/adr/` (0001–0006); `provenance.yaml` maps
  `docs/adr/` to `allowed: [human-decided]`.
- **Gate framework.** `decisions/gates.yaml` (schema v2: `command`, `job`,
  `enforcement`, `floor`, `placement`, `needs_history`, …), run by
  `scripts/ci_gates.py` / `scripts/verify_all.sh`; `.github/workflows/ci.yml`
  generated from it (gate `ci-drift`). Exit vocabulary in `scripts/_verdict.py`
  (0 / 1 / 2, and 3 = not measured). Gates are **shell commands with exit
  codes**, not Python entries.
- **A dated-transition mechanism.** `scripts/ramp_valves.py` (gate
  `ramp-valves`): dated transitions turn red on their date — the same idea as
  the pilot's expiry.
- **Human-gate records.** `scripts/gate_record.py`,
  `templates/gate-record.yaml`, `docs/governance/quality-gates.md`: records
  with `signers[]` as platform approvals (handles, review URLs), not SSH
  signatures.
- **Change scaffold.** `scripts/new_change.py` creates `plans/changes/<name>/`
  with `research.md` etc.
- **Kit / export.** `scripts/kit/manifest.yaml` classifies every tracked file
  as `mechanismus` (travels) or `bestand` (stays); `scripts/kit/probe.py`
  (gate `leerprobe`) runs the mechanism in a throwaway repository.
  `scripts/export/manifest.yaml` decides per prefix what goes to lakeswitch-ai
  (`carry`/`geruest`/`drop`). Note: the kit manifest classifies `decisions/`
  as `mechanismus`, the export manifest drops it; the difference is intended
  (header of `scripts/export/manifest.yaml`).
- **The signing practice, as prose.** `docs/how-to/signed-decisions.md`
  (status `proposed`): the key, `git confirm`, assistant prepares / maintainer
  signs, how LakeSwitch enforces it; step 3 for further repositories says
  "take over the code of `lakeswitch.signatures` or — once it exists — obtain
  it from the coding-harness kit (a pinned copy, no dependency)".

### 2.2 Missing (searched, not found)

- **No `harness` CLI.** No `pyproject.toml`, no entry point; scripts run as
  `python3 scripts/<name>.py` (Makefile, `decisions/gates.yaml`). A grep for
  `harness decide`, `harness verify`, `console_scripts`, `project.scripts`
  over `docs/`, `scripts/`, `tests/`, `AGENTS.md`, `README.md` found nothing
  outside this change package.
- **No change class and no ADR question.** Coding Harness spec frontmatter
  (e.g. `plans/changes/frontmatter-current/spec.md`) carries `title`, `status`,
  `implementation_status`, `bead`, `provenance`, … — no `class`, no `change`,
  no `adr_question`, no `intent`. A grep for `^class:` / `adr_question` in
  `scripts/new_change.py`, `plans/`, `prompts/` found nothing.
- **No signed-decision rule for Coding Harness itself.** No
  `decisions/signers.yaml`, no signature gate. `decisions/` holds only
  `gates.yaml`; `provenance.yaml` has no `decisions/` entry (only
  `docs/decisions/`). Whether Coding Harness adopts the rule is explicitly
  open: `docs/how-to/signed-decisions.md` §Open, and
  `plans/changes/frontmatter-current/decisions.md` item 5 ("that question stays
  open").
- **No pin / release mechanism.** No `harness.lock.yaml`, no
  `harness verify-pin`, no release bundle (planned in lakeswitch-ai's decision
  interview under D-21 and the kit-release entry around D-42; not built on
  either side).
- **No declared-document foundation.** lakeswitch-ai's decision interview
  plans Coding Harness as "the single source of a process-generic
  declared-document foundation" (strict model base, adapter, gate-result
  schema). No script under `scripts/` imports pydantic; no requirements file is
  tracked in this worktree (`git ls-files`).

## 3 · Bead `in1` in detail — where the key list is read

### 3.1 Where

`signatures.examine` → `_load(root, declaration)` reads
`root / "decisions/signers.yaml"` **from the working tree** with
`Path.read_text` — in a clean checkout, the version at HEAD. `_examine` then
builds one `keys` set and one allowed-signers file from that single document
and applies both to every commit since the anchor (`_commits`, `_judge`). The
module docstring and G-16 ("The declaration as it stands") state this on
purpose for the **paths**; for the **keys** nothing states it, and
`plans/changes/unified-research-and-work-management/decision-interview.md`
(amendment of 2026-09-23 to the attestation entry) says the opposite is owed:
"a commit is verified against the declaration as it stood at that commit … today
M-30 builds one allowed-signers list from the current declaration. That change
is in the owed list."

### 3.2 The two failure cases

1. **A new key approves itself.** Commit C adds key K2 to `signers.yaml` and is
   signed by K2. At HEAD the declaration contains K2, so git reports `G` with
   K2's fingerprint and `_judge` passes. Only review stops it. (Bead text says
   it was reproduced in a throwaway repository on 2026-09-29; not re-run here.)
2. **A retired key voids its history.** Removing K1 from the declaration
   leaves K1 out of the allowed-signers file; every earlier commit K1 signed now
   gets `U` → finding "is signed by …, a key the declaration does not name".
   A key can therefore never be removed, only kept.

Neither case has a test: `tests/signatures/test_the_signatures.py` builds a
repository with two keys (`good`, `other`) and passes the declaration from
**outside** the repository (`Estate.declaration = base / "signers.yaml"`), so no
test can see a declaration that changes along the history.

### 3.3 Facts that constrain any fix (read in lakeswitch-ai)

- **The first declaration approved itself.** `signers.yaml` was introduced by
  `03508a5` (2026-09-23 12:39), signed by the key it declares. The anchor
  `c02f11d` (11:04 the same day) is an ancestor of it. The anchor and the 3
  commits of `c02f11d..03508a5` (`git rev-list --count`) therefore have no
  declaration at their parent. Any "judge against the parent's declaration"
  rule needs a bootstrap rule for them.
- **Old declarations do not satisfy today's schema.** `03508a5`'s
  `signers.yaml` has only `schema_version`, `anchor`, `signers` — no `paths`
  (added by `a046b34`, 2026-09-27). `SignersDocument` requires `paths`
  (`min_length=1`, plus `decisions/` and `docs/adr/`). Reading a historical
  declaration with today's validator would refuse it; a historical reader must
  take only the key list.
- `signers.yaml` has been changed by 2 commits so far (`03508a5`, `a046b34`);
  the key list itself has never changed.
- Local tools: git 2.55.0, OpenSSH 10.3p1. CI runs on `ubuntu-latest`
  (`docs/how-to/signed-decisions.md`); its OpenSSH version was not read.

### 3.4 Known technical options, each with its cost

| # | Option | Fixes case 1? | Fixes case 2? | Cost |
|---|---|---|---|---|
| A | **Keys from the parent's declaration.** For each examined commit, read `git show <first parent>:decisions/signers.yaml`, take its key list, verify against it. Group commits by the declaration blob so there is one `git log` / allowed-signers file per version. | yes — adding a key needs a key already declared | yes — older commits are judged against older lists | a bootstrap rule (3.3); a tolerant reader of old declarations (3.3); a rule for merges (first parent, or every parent); a lost sole key can no longer be replaced without a re-anchor (7, Q4). Paths stay from HEAD per G-16 — keys and paths would then come from two different versions, which G-16's text must say. Runtime: one `git show` per commit, cacheable per blob. |
| B | **Validity periods** in the declaration, written as `valid-after="…"` / `valid-before="…"` into the allowed-signers file; declaration still from HEAD. `man git-config`, `gpg.ssh.allowedSignersFile`: "Since OpenSSH 8.8 this file allows specifying a key lifetime using valid-after & valid-before options. Git will mark signatures as valid if the signing key was valid at the time of the signature's creation." `ssh-keygen(1)` documents both options and `-O verify-time=`. | **no** — a key added at HEAD with `valid-after` = today still validates the commit that adds it | yes — retire by setting `valid-before` instead of deleting | the time comes from the commit itself, which the signer writes; a retired or stolen key can backdate into its window (git's exact time source — committer date — was not read in git's source this session). Needs OpenSSH ≥ 8.8 on every verifier. Keeps a growing list of dead keys. |
| C | **Revocation list** — `gpg.ssh.revocationFile` (`man git-config`: a listed key "will always be treated as having trust level never"). | no | no — it refuses the key's past signatures too | the right tool only for a *compromised* key, the opposite of retirement. The decision interview names compromise as "a different event … stated with the date from which its signatures are refused" — that is B's `valid-before`, not C. |
| D | **A + B together.** A decides who may add a key; an optional `valid-before` (or `retired:`) marks a compromised key from a date. | yes | yes | A's cost plus B's field; B's backdating weakness only matters for the compromise case. |
| E | **Signed-key ceremony outside git** (SSH CA with `cert-authority`, sigstore/gitsign). | depends | depends | a second trust root and infrastructure; mentioned in `man git-config` (`cert-authority`); not examined further. |

Option A is what the bead states as "Expected" and what the decision
interview's amendment asks for; it is the only one of A–C that closes case 1.

## 4 · How LakeSwitch would switch, and what 2026-10-15 means

### 4.1 What happens on 2026-10-15

`adranswer._pilot`: from `today >= expires` M-31 reports a finding →
`lakeswitch verify` red → every LakeSwitch PR red (PR #62 description and
`decisions/answers/pilot.yaml`). Two ways out, both named by the gate:

1. switch to the Coding Harness version and delete the pilot, or
2. a signed commit (M-30 holds it) to `pilot.yaml` with a later `expires` and
   its reason in `why`.

PR #62 itself predicted: "The move needs the pin mechanism, which does not
exist yet, so a signed later date is likely." Today is 2026-09-30: 15 days
remain.

### 4.2 What a switch needs that does not exist

- **A way for LakeSwitch to hold Coding Harness code.** lakeswitch-ai has no
  `harness/` copy, no `harness.lock.yaml` (file absent), and no dependency on
  coding-harness in `pyproject.toml` / `requirements-ci.txt` (grep found none).
  `docs/workflow.md` §9 (lakeswitch-ai) says the pinned copy "replaces this
  adaptation" once D-21's pin exists. The planned route (kit release bundle,
  `harness.lock.yaml`, `harness verify-pin`, upgrade PR as a signed Feature
  change — D-21 and the kit-release entry of the decision interview) is not
  built on either side.
- **A gate seam.** LakeSwitch's one list resolves `entry: module:function`
  returning `lakeswitch.verdict.Result` (`onelist.py`, `GateEntry.resolve`);
  Coding Harness gates are commands with exit codes. A switch needs either an
  adapter entry in LakeSwitch that runs the Coding Harness command and maps
  its exit code to a `Result`, or a Coding Harness module LakeSwitch can
  import from its copy.
- **The same format.** The switch is migration-free only if the answer file
  and the anchor fields (`class`, `adr_question`, title, `intent.outcome`)
  stay as in schema_version 1; the five signed answer files and the five
  LakeSwitch Feature anchors (`grep -l "^class: feature"` over
  `plans/changes/*/spec.md`) would then be read unchanged.

### 4.3 Files LakeSwitch touches on the switch (its own PR, its own session)

`src/lakeswitch/adranswer.py`, `declared/adr_answer.py`,
`declared/answer_pilot.py` and `tests/adranswer/` (deleted);
`src/lakeswitch/cli.py` (`decide` subparser), `src/lakeswitch/specmap.py`
(`INFRASTRUCTURE`); `decisions/gates.yaml` M-31 entry and
`decisions/answers/pilot.yaml` (signed commit by the maintainer);
`spec/gates.md` G-17, §5.1 row "decide adr", criterion 24; `docs/workflow.md`
§9 rows 4–5; `rendered/registries/` (regenerated). If M-30 moves too:
`signatures.py`, `declared/signers.py`, `tests/signatures/`, G-16, criterion 23.
Bead `in1` says: fix M-30 "there and in the lakeswitch-ai pilot, or in the
harness only if the pilot has moved by then".

## 5 · Which files a change in Coding Harness would touch

Names are provisional; the spec phase settles them.

- New: a command (e.g. `scripts/decide_adr.py`), an answer gate
  (e.g. `scripts/check_adr_answers.py`), and — if in scope — a signature gate
  (e.g. `scripts/check_signed_decisions.py`); their tests under `tests/`.
- `decisions/gates.yaml` (new gate entries; the signature gate needs
  `needs_history: true`) and `.github/workflows/ci.yml` (regenerated by
  `python3 scripts/ci_gates.py --generate-ci`, never edited).
- `scripts/kit/manifest.yaml` (new scripts and tests as `mechanismus`; today
  the catch-all `scripts/` / `tests/` rules make a new file `bestand`) and
  `scripts/export/manifest.yaml` (`carry`).
- `scripts/new_change.py` and its tests, if the spec scaffold gains `class` and
  `adr_question`.
- `docs/WORKFLOW.md` (the ADR question at close), `prompts/01a-interview.md`
  and/or `prompts/02-spec.md`, `docs/how-to/signed-decisions.md` (status and
  "what a further repository has to do"), `provenance.yaml` (an entry for the
  answer location), possibly `AGENTS.md`.
- A template for the answer file under `templates/`, if the pattern of
  `templates/handover.md` + `scripts/handover_schema.py` is followed.

## 6 · What is unclear (gaps, not decisions)

- `[GAP]` Which timestamp git hands to `ssh-keygen -O verify-time` for a
  commit (committer date is expected; git's source was not read). Matters only
  for option B.
- `[GAP]` The OpenSSH version on the CI runner (≥ 8.8 needed for option B).
  Not read.
- `[GAP]` Whether Coding Harness has an equivalent of LakeSwitch's M-6 /
  DL-5 check (German prose in commit messages). Not searched; the command's
  message check depends on it.
- `[GAP]` The reproduction of `in1` in a throwaway repository (bead text,
  2026-09-29) was not re-run here.

## 7 · Open points for the phase 1a interview

Sorted by the question protocol of `docs/WORKFLOW.md`. Scope-changing ones
first. Each `[DECISION]` carries a recommendation.

**Q1 `[DECISION]` — What must be true on 2026-10-15?**
Goal: LakeSwitch's PRs do not turn red, and the principle gets its home.

- (a) The mechanism is in Coding Harness **and** LakeSwitch has switched
  (pilot deleted). Consequence: a consumption path must be built first — at
  minimum a hand-made pinned copy plus a gate adapter in LakeSwitch; the
  planned release/lock mechanism is several sessions more. Highest risk of
  missing the date.
- (b) The mechanism is in Coding Harness with its tests; the maintainer signs a
  later `expires` in LakeSwitch's `pilot.yaml`, tied to the pin mechanism;
  LakeSwitch switches in its own later change. Consequence: two copies exist
  for a while, dated and visible.
- (c) Only sign a later date now; build nothing yet. Consequence: nothing
  moves; the bead's due date passes.

Recommendation: **(b)**. It gives the principle its home within the date and
keeps the switch where it belongs — with the pin mechanism, which is its own
plan. If "ok": this change ends with the Coding Harness mechanism merged, and
the maintainer signs one pilot-date commit in LakeSwitch before 2026-10-15.

**Q2 `[DECISION]` — Does the signature check (with the `in1` fix) belong to
this change, and does Coding Harness adopt signed decisions for itself?**

- (a) This change ports only the ADR answer (gate + command); the signature
  check with the `in1` fix is the next change.
- (b) This change ports both; Coding Harness ships them as mechanism for
  instances and tests them in throwaway repositories, but does not hold its own
  history to the rule.
- (c) Like (b), and Coding Harness also declares its own signers and turns its
  own gate on.

Consequence: the ADR answer is only worth something together with a signature
check — without one, an agent could write the answer file. LakeSwitch has that
check (M-30); Coding Harness has none. (c) needs an anchor, a key declaration
and a signed commit here, and answers the question left open in
`plans/changes/frontmatter-current/decisions.md` item 5.

Recommendation: **(a)**, smallest version first — with `in1` fixed in the
signature change immediately after, since LakeSwitch keeps M-30 until it
switches anyway. (c) stays on the not-now list.

**Q3 `[DECISION]` — Which Coding Harness changes owe an answer to the ADR
question?**

- (a) Take over LakeSwitch's four classes (spike, bounded, feature,
  architectural) as a closed set in the spec frontmatter, plus
  `adr_question`; only `feature` owes an answer. No class duties beyond that.
- (b) Every change package owes an answer; no class field.
- (c) The full class model of LakeSwitch's decision interview (D-24 and its
  duties).

Consequence: (a) keeps the format identical to the pilot, so LakeSwitch
switches without migrating its five signed answers or its five Feature anchors; (b) asks
more often and diverges from LakeSwitch; (c) is a much larger change.

Recommendation: **(a)**.

**Q4 `[DECISION]` — (only if the signature check is in scope) If the only
declared key is lost, how does a repository recover?**
With the `in1` fix, a new key must be signed in by a key already declared. If
the only key is gone, no new key can ever be added validly.

- (a) Declare a second presence-bound key (a backup device) from the start.
- (b) Allow a re-anchor: a commit that moves the anchor starts a new trust
  root, and the report says so loudly; guarded only by pull-request review.
- (c) Both: (a) as practice, (b) as the documented last resort.

Recommendation: **(c)**. If "ok": the spec names both, and the report shows
every re-anchor.

Details the agent decides (`[DETAIL]`, with reason in the artefact):

- **Command name.** `harness decide adr` as a real CLI would need packaging
  that does not exist (2.2). Proposed: a script now, with the same verb shape,
  so a later `harness` wrapper is a rename. Reversible.
- **Format.** Keep `schema_version: 1` and every field as in the pilot (1.2);
  `answered_by`'s role name becomes configuration, not the constant
  `architect`.
- **Pilot expiry.** Not ported; it is LakeSwitch's reminder, and
  `scripts/ramp_valves.py` already covers dated transitions here.
- **Merge rule under option A.** A merge that writes content of its own is
  judged against its first parent's key list; reason: the main line is where
  the decision lands.
- **Historical declarations.** Read only the `signers` part, tolerant of older
  schema versions (3.3).

## 8 · Size and the smallest version (requested by the caller)

Rough sizes, from the pilot's own plan (journal
`2026-09-28-signed-answers-and-scope-reset.md` in lakeswitch-ai: gate 2 h,
command 1.5 h) and the M-30 code (314 lines, 35 test functions):

| Package | Size |
|---|---|
| 0 · change package (spec, plan) | 0.5 h |
| 1 · answer gate + format in Coding Harness, stdlib + YAML, tests | 2 h |
| 2 · command (dialogue, files, message; never signs), tests | 1.5 h |
| 3 · gate list, generated CI, kit and export manifests, docs | 0.5–1 h |
| 4 · signature check ported with the `in1` fix (option A, bootstrap, tolerant reader, two new seeded faults) | 3–4 h |
| 5 · LakeSwitch switch (copy + adapter + deletions + signed commits) | 2–3 h, **after** a consumption path exists |
| — · the pin / release mechanism (D-21, kit release) | not sized; several sessions |

**Smallest version:** packages 0–3 — the ADR answer in Coding Harness, format
identical to the pilot, about 4.5–5 h, one PR. Then the signature check with
`in1` (package 4) as its own change. Before 2026-10-15 the maintainer signs a
later pilot date in LakeSwitch (Q1 b). The switch (package 5) follows the pin
mechanism.

Not now: Coding Harness adopting signed decisions for its own history (Q2 c);
bead `xv3`'s remaining parts (guided flow, reminder); a check that a "yes"
is followed by an ADR under `docs/adr/` (a non-goal of the pilot too); further
question kinds; the declared-document foundation.

## Corrections after verification

Added in phase 2 (spec), 2026-09-30, after reading the pilot again at
lakeswitch-ai `09c9d62` (the merge of its pull request 68) and this worktree
at `34e23d5`. Where these disagree with the text above, these hold.

1. **The anchor's `adr_question` has three keys, not two:** `proposed`,
   `answered_by` (null in all five LakeSwitch anchors) and `reason`
   (`declared/change_anchor.py`, `AdrQuestion`). Sections 1.1 and 1.5 name
   two.
2. **The pilot's feature anchor declaration requires more than 1.1 lists:**
   `title`, `artifact: change-spec`, `change`, `status`, `created`,
   `provenance`, `review`, `class`, `class_history`, `appetite`,
   `adr_question` and `intent` with `schema`, `scope`, `outcome`, `in_scope`,
   `non_goals`, `acceptance` (and optional `constraints`). The base model
   forbids unknown keys, refuses coercions (a boolean or float for an integer,
   a string for a date) and refuses duplicate keys (`declared/base.py`).
3. **The answer's `change` is compared with the anchor's `change:` field,
   not with a folder.** The pilot builds the answer path from the anchor's
   field and never compares either with the folder name. Section 1.2 says
   "must equal the folder". All five LakeSwitch anchors' `change` equals
   their folder name.
4. **"Examined nothing" is red in LakeSwitch**, not merely "not a pass":
   `verdict.Result.outcome` returns BLOCK for an empty key set (section 1.3).
5. **Coding Harness does know the four classes — in prose.** The reference
   architecture `docs/research/arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md`
   §8.2 defines Spike, Bounded, Feature and Architectural with a recognition
   rule each, LakeSwitch's decision D-24 names them "Coding Harness's four
   change classes", and the archived spec
   `2026-09-21-reproducible-bead-export` states "Class: Bounded." in its body.
   What does not exist is a header field and a check (section 2.2).
6. **There is no spec scaffold.** `scripts/new_change.py` writes
   `research.md` only (section 5, "if the spec scaffold gains …").
7. **The pilot's date moved.** lakeswitch-ai pull request 68 set
   `expires: 2026-12-15` (section 4.1 names 2026-10-15).
8. **Commit signing is out for Coding Harness altogether.** The maintainer's
   direction of 2026-09-30, relayed to phase 2: Coding Harness introduces no
   commit signing. Section 3 and the points on signing in sections 6–8 no
   longer describe work for this repository; bead coding-harness-in1 concerns
   LakeSwitch's gate M-30 only. The same day the maintainer decided what
   confirms a decision instead: its pull request, merged by the maintainer or
   on their explicit request (`spec.md`, criterion 11).

## Addendum — gaps closed in phase 2

1. **No commit-message language check exists here** (section 6, third gap).
   No script, test, workflow or tool under `scripts/`, `tests/`, `.github/`
   or `tools/` checks commit messages for German; the only tracked commit hook
   is the tracker's `.beads/hooks/prepare-commit-msg`.
2. **The phase gate validator is absent.**
   `scripts/validate_change_artefacts.py`, named by `prompts/02-spec.md` and
   `prompts/03-plan.md`, does not exist; `python3 scripts/plans_registry.py
   --check` is the validator that runs (the same finding as
   `plans/changes/frontmatter-current/research.md`, item 14).
3. **The pilot's rollout.** The maintainer's answers for the pilot itself and
   four earlier features landed inside the pilot's pull request, before its
   merge: commit `9d34f91` (2026-09-28) is an ancestor of the merge `9b9d5c8`
   of pull request 62, and the same commit added the gate entry.
4. **Existing anchors in Coding Harness:** three, none with a `class:` line —
   `plans/changes/frontmatter-current/spec.md`,
   `plans/changes/omnigent-deny-layers/spec.md` and
   `plans/changes/archive/2026-09-21-reproducible-bead-export/spec.md`.
   Archived headers have been edited before: commit `e553bc8` stamped
   `updated:` into them.
5. **`provenance.yaml` path entries have no key validation.**
   `tests/test_provenance.py` holds two tests about journal dates;
   `scripts/validate_provenance.py`, named in the file's header, does not
   exist. `scripts/check_frontmatter_current.py` reads `prefix` and
   `frontmatter`, `scripts/ramp_valves.py` reads `roles:`. LakeSwitch keeps
   the answering role as `owner_role` per path in `decisions/provenance.yaml`.
6. **What a new gate and a new script must meet** (`tests/test_ci.py`): a
   test named like a mutation test (`MUTATIONS_NAMEN`; the exemption list
   may only shrink), a test that imports or runs every script, and a CI
   caller or a reason in `ci_gates.OHNE_AUFRUFER`.
7. **The CI installs `pytest`, `PyYAML` and `ruff` only**
   (`.github/workflows/ci.yml`); no pydantic.
8. **The kit probe runs `pytest` in a throwaway copy** of every
   `mechanismus` file (`scripts/kit/probe.py`), not the gates; the kit
   manifest classifies `decisions/` as `mechanismus`, so without a longer
   prefix every answer file would travel.
9. The gaps on `ssh-keygen -O verify-time`, the CI runner's OpenSSH version
   and the reproduction of bead coding-harness-in1 are moot for this
   repository (correction 8).
10. **What a Claude Code `ask` rule does** (for the merge guard the
    maintainer decided on 2026-09-30). Read on 2026-09-30 by a documentation
    sub-agent of the phase 2 session, which quoted the pages; this session did
    not re-read them. Sources: <https://code.claude.com/docs/en/permissions>,
    <https://code.claude.com/docs/en/permission-modes>,
    <https://code.claude.com/docs/en/headless>,
    <https://code.claude.com/docs/en/settings>.
    - An explicit ask rule prompts in every mode, `bypassPermissions` and
      auto mode included ("Actions no mode auto-approves").
    - Where nobody can answer — `dontAsk`, or a `-p` run without a
      permission-prompt host — the matching call is denied.
    - Rules are evaluated deny, then ask, then allow, lists from all scopes
      are combined, and an allow rule from a user file does not outrank a
      project ask rule.
    - `Bash(gh pr merge:*)` is a prefix rule; `*` may stand anywhere; ask
      rules match any subcommand of a compound command and past leading
      variable assignments. They match the command's text and "aren't a
      security boundary" — an absolute path, `sh -c` or another program
      passes them.
    - Ask rules accept tool-name globs (`mcp__*`), so an MCP server's merge
      tool can be named by a glob; the exact tool name of a GitHub MCP server
      was not read.
11. **One existing test pins the ask list.**
    `tests/test_omnigent_deny_layers.py::test_settings_ask_exactly_the_asked_tools`
    asserts that `permissions.ask` in `.claude/settings.json` equals the
    Omnigent asked tools; a merge rule beside them turns it red.
    `scripts/omnigent_policy.py --write` already keeps ask rules it does not
    own (the same file's test with `Bash(git push:*)`).
