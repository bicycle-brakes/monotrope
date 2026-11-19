---
title: "A leak-check block stopped the research swarm"
category: research
created: 2026-11-18
updated: 2026-11-19
last_reviewed: 2026-11-18
status: draft
implementation_status: none
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: OpenCode, version: "deepseek-v4.1-flash via opencode-go, 2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [incident, leak-check, research-swarm, security]
---

# A leak-check block stopped the research swarm

On 2026-11-18 the research swarm for `trust-pyramid-swarm` could not start.
The cause was not the swarm: the leak check refused, and it refuses before
every foreign call.

## What happened

1. `prepare-explore trust-pyramid-swarm --class feature` selected three Go
   seats — `deepseek-v4.1-flash`, `glm-5.3-flash`, `mimo-v2.6-flash` — plus
   `hy4-flash-free`. The intelligence index was not read
   (`ARTIFICIAL_ANALYSIS_API_KEY` unset), so cost alone decided.
2. The first run ended incomplete: `finders-0-2 (timed-out)` after twenty
   minutes, and no later stage starts.
3. `research-swarm-limits.yaml` raised `finders` from 20 to 40 minutes; this
   repository has 1,117 files and about 4,670 commits.
4. The second run stopped at the leak check with **BLOCK**.

## The block

- Commit `a890e90d`, "docs(research): ontology as enforcement", 18:15 on
  2026-11-18, branch `ontology-relation-layer`, pushed to origin.
- File: `plans/changes/ontology-relation-layer/research.md`, 32,122 lines.
- Rule: `secret:connection-string-with-credentials`, match length 45, at two
  places (commit lines 27861 and 27922).
- **The matched text is not in this note.** The check never shows it, and
  printing it here would spread exactly what the check exists to contain.

## Why it blocks more than one run

The leak check runs immediately before every foreign call, and a BLOCK stops
without a fallback (`docs/WORKFLOW.md` §4). Blocked are `explore`,
`review-loop`, `review` and `repair`. Local work — gates, documents, pull
requests — is not affected.

## What is not known

Whether the match is a real credential or an example. The rule's exact shape
lives in the machine's denylist outside the repository, so only the maintainer
can put rule and place together. Searches for URLs with userinfo and for
`Key=Value` connection strings did not reproduce it; that says something about
the search patterns, not about the value.

## The options

1. **False positive.** The place is a placeholder; refine the denylist rule on
   that machine. No repository change.
2. **Real credential.** Rotate first, then decide about the history: the branch
   is pushed, so a rewrite means a force-push and a garbage collection — and
   the check itself notes that the reflog and the stash keep the value until
   then.
3. **Nothing.** Stage 2 stays blocked on every machine that runs this
   denylist.

## What was not done

No branch was rewritten, no value was shown, and the temporary copy made to
locate the place was deleted. The commit belongs to a parallel session.

## State at the time of writing

- PR #409, the research note on the trust pyramid, is **merged** (`f31d216e`).
- PR #410, RB-A1 to level 4, is **queued** in the merge queue.
- Bead `coding-harness-5kvq` and the change folder `trust-pyramid-swarm` carry
  the swarm. The two finished finders sit in the research store and are reused
  on resume.

## The limits change in the same pull request

`research-swarm-limits.yaml`: `finders` 20 → 40 minutes. It is the second
raise of the same limit — bead `coding-harness-ht1b` raised it from 600
seconds. Two raises for one repository size say the limit is not a constant: it
should follow the measured size, or the finder should report progress instead
of timing out silently. That is a question for its own change.

## Addendum — 2026-11-19, the outcome

- **Option 1 was taken.** On 2026-11-18 the maintainer had the place
  checked: a false positive, JSON-LD text in the research artefact of
  `ontology-relation-layer` (commit 6df696e5) whose shape resembles a
  connection string with credentials. No credential was exposed, and no
  branch was rewritten.
- The rule `secret:connection-string-with-credentials` in the machine's
  denylist was refined so that a "password" starting with `[`, `{` or a
  backslash no longer matches; the previous rule is kept as a dated backup
  beside it. The next leak check ran clean.
- The finder limit raise left this pull request. It contradicted the
  interview's decided value (20 minutes) without a decision; it now goes as
  its own decision pull request (#414), which the maintainer chose on
  2026-11-19.
- Open beads for the mechanisms named above: one blocked commit stops every
  lane (coding-harness-159n); the finder limit should follow the measured
  repository size (coding-harness-n76m); a timed-out seat voids a whole run
  (coding-harness-glqo).
