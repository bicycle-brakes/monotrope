---
title: "Session handover — package 2 (harness decide adr) researched, interview next, 2026-09-30"
category: handover
created: 2026-09-30
updated: 2026-09-30
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-30"
tags: [handover, harness-decide-adr, adr-answer, signing, lakeswitch]
target_ref: "fd6153e"
bead: coding-harness-3ar
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

**Next action:** run the phase 1a interview for package 2 with the maintainer.
Ask the four questions in section "Interview" one at a time, Q1 first, each
with its recommendation. Write the answers to
`plans/changes/harness-decide-adr/decisions.md` on branch
`feat/harness-decide-adr`. Then phase 2 (spec) on Opus 5.5 at effort xhigh.

Package 2 is bead `coding-harness-3ar`: move LakeSwitch's signed ADR answer
(command `lakeswitch decide adr`, gate M-31) into Coding Harness as
`harness decide adr`. It also covers bead `coding-harness-in1`, the key-list
weakness of LakeSwitch gate M-30 (signed commits): a new key can approve
itself, and a retired key turns its old commits red.

**Deadline: 2026-10-15.** From that day LakeSwitch's pilot record
`decisions/answers/pilot.yaml` expires, gate M-31 reports a finding and every
LakeSwitch pull request turns red. There are two ways out: LakeSwitch switches
to the Coding Harness version, or the maintainer signs a later `expires` date.
The research expects the second (Q1 below). Signing needs the maintainer's
Secure Enclave key, so it needs the laptop. The maintainer travels from
2026-09-30, and remote signing was deferred on 2026-09-29.

## Where we are (2026-09-30)

- Coding Harness `main` is at `39d2e12` (merge of #52) and green in CI.
  PRs #49 to #52 are merged:
  - #49: English workflow and worktree rules;
  - #50: Omnigent deny layers;
  - #51: the `frontmatter-current` gate;
  - #52: one Fable reviewer for the spec review (phase 2a) and the review
    (phase 6), where the spec review improves the spec first.
- Branch `feat/harness-decide-adr` is at `fd6153e` and pushed, with no pull
  request yet. It has one commit: the change folder
  `plans/changes/harness-decide-adr/` with `research.md` (phase 1). The
  research is unreviewed: `review.status` is `pending`.
- Worktrees:
  - `.claude/worktrees/harness-decide-adr` holds the package. Keep it.
  - `.claude/worktrees/handover-2026-09-30` holds this handover. Remove it
    after the merge.
- lakeswitch-ai `main` is at `9b9d5c8`, the merge of #62. Two PRs are open,
  and the maintainer said on 2026-09-30 that they merge them:
  - #66: one worktree per change, rule D-60 (only the first session writes the
    tracker) and the ADR answer in AGENTS.md;
  - #67: the handover of 2026-09-28.

  lakeswitch `main` refuses a PR that is behind. If one of them falls behind,
  merge `origin/main` into it, push, and wait for CI.

## What the research found

Read on 2026-09-30, against lakeswitch-ai `9b9d5c8` and Coding Harness
`39d2e12`. It ran on Opus at the maintainer's request; the default model for
phase 1 is Haiku 4.5. The full text is in `research.md`. I spot-checked one
claim in lakeswitch-ai: `signatures._load` reads `decisions/signers.yaml` from
the working tree, and `_examine` builds one key list from it. The rest has not
been checked by a second reader.

1. **LakeSwitch cannot consume Coding Harness yet.** It has no pinned copy, no
   `harness.lock.yaml` and no dependency. The gate shapes also differ: in
   LakeSwitch a gate is a Python `module:function` returning a `Result`, in
   Coding Harness it is a shell command with an exit code. So a real switch
   before 2026-10-15 is unlikely. PR #62 already predicted "a signed later date
   is likely".
2. **Coding Harness lacks most of the building blocks.** It has no `harness`
   CLI (no `pyproject.toml`, no entry point), no change class, no
   `adr_question`, no signers file and no signature gate. Whether Coding
   Harness holds its own history to signed decisions is still open: see
   `docs/how-to/signed-decisions.md` and
   `plans/changes/frontmatter-current/decisions.md` item 5.
3. **Bead in1 is confirmed in code.** One key list, taken from HEAD, judges
   every commit. Only option A fixes both failure cases: read each commit's
   keys from its parent's declaration. Validity periods (`valid-after` and
   `valid-before`) fix only the retirement case, and they trust a date the
   signer writes. Two constraints apply to any fix:
   - The first declaration (`03508a5`) approved itself, so the anchor and the
     three commits after it need a bootstrap rule.
   - That first declaration has no `paths`, so historical declarations need a
     tolerant reader.

Sizes, as estimated by the research:
- The smallest version is about 4.5 to 5 hours in one PR. It is the ADR answer
  in Coding Harness (gate, command, gate list, manifests), with the format
  unchanged from the pilot.
- The signature check with the in1 fix is 3 to 4 hours, as its own change.
- The LakeSwitch switch is 2 to 3 hours, but only after a pin mechanism
  exists. That mechanism has not been sized; it takes several sessions.

## Interview (phase 1a), in this order

Each question below comes with the research's recommendation. None has been
asked yet.

- **Q1: What must be true on 2026-10-15?** Recommendation (b):
  - the mechanism is merged in Coding Harness;
  - the maintainer signs a later pilot date in LakeSwitch, tied to the pin
    mechanism;
  - LakeSwitch switches later, in its own change.

  The alternatives are (a), switch fully by then, which carries a high risk,
  and (c), only sign a later date.
- **Q2: Is the signature check with the in1 fix part of this change? Does
  Coding Harness adopt signed decisions for itself?** Recommendation (a): port
  only the ADR answer now, and make the signature check with the in1 fix the
  very next change. Coding Harness adopting signed decisions for itself goes to
  the not-now list.
- **Q3: Which Coding Harness changes owe an ADR answer?** Recommendation (a):
  take over LakeSwitch's four classes plus `adr_question`, where only
  `feature` owes an answer. The format stays identical, so LakeSwitch migrates
  nothing.
- **Q4: If the only key is lost, how does a repository recover?** Ask this only
  if the signature check is in scope. Recommendation (c): a second
  presence-bound key as practice, and a re-anchor that the report shows loudly
  as the last resort.

## Decisions and preferences of this session

- 2026-09-29: the maintainer asked for package 2 with the research on Opus
  instead of Haiku. The workflow itself was not changed.
- 2026-09-30: the **first LakeSwitch run** uses Northwind:
  - the legacy source is <https://github.com/harryho/db-samples> (Northwind
    for MySQL, PostgreSQL and others; GitHub declares no licence, read
    2026-09-30);
  - LakeSwitch builds a Data Vault from that source;
  - the reference, the target picture the result is measured against, is
    <https://github.com/CarlTimms/Data-Vault-Example-Northwind> (Data Vault
    2.0, MIT licence).

  The missing licence on db-samples must be settled before anything from it
  lands under lakeswitch-ai `examples/`. This is not yet in the tracker (see
  the next section).

## Open, and ownership

- **Tracker not written this session after 2026-09-30.** When the handover was
  written, two other interactive Claude sessions were running on this machine,
  and it was not read which repository they were in. By house rule 4 (only
  the first session writes the tracker), nothing was written. Owed once only
  one session writes:
  - a note on bead `coding-harness-3ar` pointing to `research.md` at
    `fd6153e`;
  - a new bead for the first LakeSwitch run on Northwind, with the roles above
    and the licence question.
- The research lists four things it did not read:
  - which timestamp git hands to `ssh-keygen -O verify-time`;
  - the OpenSSH version on the CI runner;
  - whether Coding Harness has an equivalent of LakeSwitch gate M-6 (no German
    prose in commit messages);
  - it did not re-run the in1 reproduction.
- Still open from earlier sessions and unchanged here:
  - the live probe of the Omnigent deny layer 1, run by the maintainer (about
    5 minutes);
  - bead `coding-harness-671` (install deny layer 2, after the trip);
  - bead `coding-harness-4me` (findings as checked data, queued behind 3ar);
  - bead `coding-harness-yim` (the remaining German, starting with
    `prompts/07-commit.md`).
