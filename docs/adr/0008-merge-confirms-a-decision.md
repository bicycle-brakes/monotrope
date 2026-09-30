---
title: "ADR 0008 — A decision takes effect when the maintainer merges the pull request carrying it — no commit signing in Coding Harness"
category: adr
status: accepted
created: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr]
---

# ADR 0008 — A decision takes effect when the maintainer merges the pull request carrying it — no commit signing in Coding Harness

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends no decision of the 2026-09-16
  interview and supersedes no ADR.
* Review: direction chosen by the maintainer, 2026-09-30 (option "the merge
  confirms" of three offered after the interview, with signed commits
  already set aside); the ADR question of the change answered "yes" by the
  maintainer, 2026-09-30 (`decisions/answers/harness-decide-adr/adr.yaml`) ·
  the acceptance is the merge commit and is written nowhere else, so the
  header's `review` stays empty: no agent writes an approval for a merge
  that has not happened · Decider: maintainer · prepared by a Claude Code
  session
* Date: 2026-09-30 · takes effect on merge

## Context

The acceptances of ADR 0004, ADR 0005 and ADR 0006 were recorded in commits
signed with the maintainer's Touch-ID key, the practice lakeswitch-ai
enforces with a signature gate (gate M-30; lakeswitch-ai decision D-55, not
ratified). In Coding Harness nothing checked those signatures; the practice
was a habit here, described in `docs/how-to/signed-decisions.md`.

The change that brought the ADR question into Coding Harness
(`plans/changes/harness-decide-adr/`, bead coding-harness-3ar) made the gap
concrete. Every feature now owes the maintainer's answer to the question
"does this need an ADR?", stored in `decisions/answers/<change>/adr.yaml`
and held by the gate `adr-answers`. That gate can see that an answer exists
and has the right format. It cannot see whether the maintainer gave it or an
agent wrote it. The interview of 2026-09-30 first planned a signature check
as the very next change: a port of the LakeSwitch gate with the fix of its
key-list weakness (bead coding-harness-in1) and a recovery for the loss of
the only key.

Later the same day the maintainer decided against signing in Coding Harness
altogether. The signing key lives in the laptop's Secure Enclave, and much
of the maintainer's work happens from a phone; a decision that can only be
confirmed at the laptop waits for the laptop.

Two facts bound every option:

* Agents act under the maintainer's GitHub account. GitHub shows the
  maintainer as the one who merged, whoever pressed the button.
* GitHub lets no author approve their own pull request. Under one account,
  the approval rule of the rule set — whoever approves is neither the author
  nor the last pusher (rule RB-M2 of `docs/governance/regelwerk.md`) —
  cannot be met.

## Decision Drivers

* The maintainer can confirm a decision from a phone.
* An agent may prepare a decision; it never makes one.
* The confirmation happens where the maintainer already looks: the pull
  request.
* One mechanism for every decision file — the paths `provenance.yaml`
  reserves for `human-decided`: ADRs, ADR answers, the rule set.
* LakeSwitch can read Coding Harness's answer format unchanged
  (`schema_version: 1`), whatever it decides about its own signing.

## Considered Options

* (a) **Signed commits, as in LakeSwitch.** A decision takes effect only
  through a commit the maintainer signs with the Touch-ID key, checked by a
  port of the LakeSwitch signature gate with a signers file and an anchor
  commit. It proves the person. It needs the laptop for every decision, a
  recovery for a lost key, and the key-list fix first. Set aside by the
  maintainer on 2026-09-30: impractical from a phone.
* (b) **The maintainer's merge confirms, with an ask rule.** A decision
  takes effect when the maintainer merges its pull request, or asks an agent
  in the conversation to merge it. Decision pull requests are marked, and
  Claude Code asks before every merge command it recognises. Works from a
  phone; it is a rule, not proof.
* (c) **A bot identity for agents.** Agents push and open pull requests
  under a GitHub identity of their own, and branch protection requires an
  approval by someone other than the pusher. The server would tell agent
  from maintainer. It costs a second identity with its own tokens, and
  whether branch protection is available for this private repository owned
  by a user account is not verified.
* (d) **Documentation only.** State the rule and add nothing. Nothing marks a
  decision pull request, and nothing slows an accidental merge.

## Decision

**(b)**, with these contracts:

* **The merge is the confirmation.** A decision takes effect when the pull
  request carrying it is merged by the maintainer, or by an agent on the
  maintainer's explicit request in the conversation. A decision is any file
  `provenance.yaml` reserves for `human-decided`: an ADR under `docs/adr/`,
  an ADR answer under `decisions/answers/`, the rule set
  (`docs/governance/regelwerk.md`, `docs/governance/quality-gates.md`) and
  `.claude/rules/`.
* **No commit signing in Coding Harness, now or later.** No signers file, no
  anchor commit, no key-loss recovery, no signature gate. The follow-up
  signature change the interview planned is void.
* **An agent records; it does not decide.** An agent may write a decision
  file, recording only what the maintainer stated
  (`python3 scripts/harness.py decide adr … --stated-in …`), and never writes
  an answer of its own as the maintainer's.
* **A decision pull request says that it decides.** Its title is
  `decide(<scope>): <the decision as a statement>`, it carries the label
  `decision`, and its body starts with the block from
  `.github/PULL_REQUEST_TEMPLATE/decision.md`: what the merge decides, what
  it confirms, the options and what follows. One decision per pull request;
  up to three only when none can be accepted without the others. Every other
  pull request takes `.github/pull_request_template.md`, which says on its
  first lines that nothing is decided.
* **An agent merges only on request, with the decision in view.** It
  restates the decision block in the conversation and as a pull request
  comment, stops if CI is red, never uses `--admin`, and merges with
  `--match-head-commit`, so a branch that moved after the restatement is not
  merged (`prompts/07-commit.md`, "The merge").
* **Claude Code asks before every merge command it recognises.** The ask
  rules in `.claude/settings.json` come from one list
  (`scripts/merge_guard.py`); the permission prompt appears right below the
  restatement.
* **The acceptance is recorded in the merge and nowhere else.** No agent
  writes an approver's name or date for a merge that has not happened —
  accepted is derived, not set (the idea of rule RB-M1). The gate
  `adr-answers` holds existence and format only.

## Consequences

* **A rule, not proof.** Neither GitHub nor a gate can tell who pressed
  merge. The agent's restatement comment on the pull request is the only
  record that an agent merged. The ask rules are a brake against an
  accidental merge, not a lock: another spelling passes them, and
  `docs/WORKFLOW.md` ("What this does not do") names the known ones.
* **The upgrade path is (c), not now.** If an agent is ever found deciding
  on the maintainer's behalf, agents move to a bot identity of their own and
  branch protection requires an approval by someone other than the pusher.
  A wording of rule RB-M2 for the one-account case is proposed in the plan
  of the change and waits for the maintainer's own decision pull request.
* **LakeSwitch keeps its own signing** (gate M-30) until it switches to the
  Coding Harness mechanism in a change of its own; whether it keeps signing
  after that is its own question. The key-list weakness of that gate now
  concerns LakeSwitch only (bead coding-harness-in1). The Coding Harness
  kit carries no signature check;
  `docs/how-to/signed-decisions.md` stays the description of LakeSwitch's
  practice.
* **Earlier signatures stay history.** The Touch-ID-signed acceptances of
  ADR 0004, ADR 0005 and ADR 0006 are not re-checked, and no gate reads
  them.
* **Every pull request says whether it decides.** A decision pull request
  names the decision on its first line; an ordinary one says it decides
  nothing. Nothing checks the label or the block on the server — the
  maintainer's reading before the merge holds them. A hosted check and a
  hook that shows the decision line in the permission prompt are optional
  follow-ups.
* **ADR headers after this one.** An ADR that takes effect by merge carries
  `status: accepted` — the state it has once it is on `main`, the only place
  its header is authoritative — and an empty `review`, because the merge
  commit is the record. This ADR is the first of that kind.
* **No interview decision is amended.** The target document's "the human
  holds the merge" stands; this ADR says how the maintainer holds it when
  an agent does the typing.

## Validation

* `python3 scripts/check_adr_answers.py` is green on `main`, with every
  feature answered.
* `tests/test_merge_guard.py` and `tests/test_pr_templates.py` are green:
  every recognised merge command asks, and each part of the decision block
  is in the template.
* Every decision pull request after this one carries the label and the block
  (`gh pr list --label decision --state all`, read by the maintainer).
* No sentence in `AGENTS.md`, `docs/WORKFLOW.md` or
  `docs/how-to/signed-decisions.md` names a signature, anchor or key as the
  confirmation in Coding Harness.
