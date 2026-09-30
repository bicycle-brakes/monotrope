<!--
Template for a spec. Copy it to `plans/changes/<change>/spec.md` and fill it in.
This comment is not copied.

1. The yaml block below is the header of the copy: put its lines between two
   `---` lines at the top of the file and replace every `<...>`. It carries no
   header of its own here (`provenance.yaml`, prefix `templates/`).
2. The header is a feature's, the form with the most keys. `change` and
   `adr_question` belong to a `feature` only: delete both for any other class.
   What the four classes mean: `docs/WORKFLOW.md`, "Change classes, the ADR
   question and decision pull requests".
3. The rules for each section are in `prompts/02-spec.md`. Replace the
   instruction paragraphs below with your own text; delete "Terms" if no word
   needs defining.
-->

```yaml
title: "Spec — <change>"
status: draft
implementation_status: none
date: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
supersedes: null
superseded_by: null
bead: <bead id>
owner: <role>
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: <agent>, version: "<YYYY-MM-DD>"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, <topic>]
class: feature  # spike | bounded | feature | architectural
appetite: <hours>  # hours of phase 4, repair rounds included — a stop, not an estimate
change: <change>  # a feature only
adr_question: {proposed: "<yes|no>", reason: "<one sentence>"}  # a feature only, the quotes kept
```

# Spec — <change>

The goal in one sentence: what holds after this change that does not hold
today (bead `<bead id>`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

What does not work today, with evidence from `research.md`: one point per
failure, each with where it was read and on which commit or date.

## Terms

Optional. One line per word this spec uses in a special sense: the word in
bold, then what it means here. Delete the section when no word needs one.

## Acceptance criteria

Each criterion is one checkable sentence with its *Refuted by:* line. The
failure mode is that line: what a wrong result looks like. There is no section
for it. A criterion that cannot go red is not one.

One condition per criterion. Beginning the sentence with When, While or If is
recommended, not required: it becomes the rule once pull request #60 merges,
and until then the rule is `prompts/02-spec.md`.

1. When <trigger>, <what holds>.
   *Refuted by:* <the result that shows it does not hold>.

## Non-goals

What explicitly does not belong to this change, so that the scope does not grow
during implementation. A part postponed rather than refused says what brings
it back.

## Protected areas

The paths or areas this change must not touch, each with its reason. If there
are none, write the single line: None beyond the non-goals.

## Definition of Done

- `verify` green.
- Moved in the same pull request: the documents, models and ADRs that change
  with the code, each by name — or "none".
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes `<bead id>`, and its last commit carries the
  trailer `Closes-Bead: <bead id>` (`prompts/07-commit.md`).
- Special runs, each with its commit in the pull request body — or "none".

## Open decisions

Classify first, then ask (`prompts/02-spec.md`): a `[DECISION]` in the form the
prompt gives, a `[DETAIL]` with its reason. If nothing is open, write: None
open.
