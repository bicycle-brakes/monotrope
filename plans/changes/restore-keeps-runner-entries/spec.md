---
title: "Spec — restore-keeps-runner-entries"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-7awf
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, runner]
class: bounded
appetite: 2
adr_files: []
---

# Spec — restore-keeps-runner-entries

Runner-authored findings survive restoration while attempt-authored edits do not (bead `coding-harness-7awf`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `5e5313ce`, the research traces a credential scan writing a skipped-scan record after an attempt and before restoration of the attempt's findings edit; restoring the pre-call snapshot can erase that record. A later scan currently masks one observed case, while the research does not establish whether an audit line is lost.

## Acceptance criteria

1. When an attempt edits findings and the runner writes a record before restoring that edit, the runner-written record survives restoration.
   *Refuted by:* a genuine scan or audit record written in that interval is absent after restoration.
2. When an attempt edits findings, restoration removes the attempt's edits.
   *Refuted by:* an attempt-authored line, including one imitating a runner record, survives.
3. When the runner alone writes a findings record after an attempt, that record is not attributed to the attempt as an edit.
   *Refuted by:* a runner-only scan record triggers the attempt-edit notice.
4. When recovery refuses restoration for safety, the runner does not bypass that refusal to preserve a record.
   *Refuted by:* the refusal results in an additional findings write.
5. When implement or repair restores findings, the same preservation and attribution rules apply.
   *Refuted by:* either verb loses a genuine record or retains an attempt-authored edit in the same circumstances.

## Non-goals

Changing credential scanning policy, attempt acceptance, or the format of audit and scan records is outside this change.

## Protected areas

The runner's recovery preflight and safety refusals retain their protective behavior; protected paths remain under the existing ownership rules.

## Definition of Done

- `make verify` green.
- No associated documents, models or ADRs beyond this change's artifacts.
- The protected areas retain their behavior and the non-goals remain unbuilt, shown by tests and the pull request's file list.
- The pull request closes bead `coding-harness-7awf` and its last commit carries `Closes-Bead: coding-harness-7awf`.
- Special runs: none.

## Open decisions

[DETAIL] Preserve trusted runner writes separately from attempt output and restore them through the shared recovery path; this reversible choice avoids trusting lines merely because they resemble a runner record. No maintainer decision is open.
