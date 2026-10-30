---
title: "Decisions — kimi-admission"
status: draft
implementation_status: partial
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-bomd
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# kimi-admission — Decisions

Class: bounded, with an ADR edit (five counted interview records owed).
The answers were given in German in the conversation; each `answer` quotes
it and adds the English sense.

## Q-1 · Which of the Go models read on 2026-10-30 are admitted

context: |
  Topic: model admission for the review loop (phase 4b).
  Intention: the Go page listed models the declaration did not carry; some
  keep data 0 days, some 30 days.
  Today: only models with a reading in model-endpoints.yaml run.
  Repository change: readings for the new models in model-endpoints.yaml.
  Architecture change: none.
asked: 2026-10-30, conversation 2026-10-30 (interview)
answer: "Alle mit 0 Tagen, Auch die mit 30 Tagen" — every model read, with 0 days of retention and with 30 days alike
answered_by: maintainer
status: answered

In the context of the review loop's model admission, facing nine Go models read on 2026-10-30 with 0 or 30 days of retention, we decided to admit every reachable one through its reading, to achieve a wider and cheaper review ladder, accepting that some providers keep review text for 30 days. — 2026-10-30

## Q-2 · Whether the Kimi exclusion of 2026-09-30 stands

context: |
  Topic: the Kimi exclusion of ADR 0007, decision 3.
  Intention: two of the new Go models are Kimi models.
  Today: Kimi stands under `ausgeschlossen` and no Kimi model may run.
  Repository change: the exclusion entry goes; ADR 0007 gets a dated amendment.
  Architecture change: one decision of ADR 0007 is amended.
asked: 2026-10-30, conversation 2026-10-30 (interview)
answer: "Ausschluss aufheben" — lift the exclusion
answered_by: maintainer
status: answered

In the context of ADR 0007, decision 3, facing two reachable Kimi models on OpenCode Go, we decided to lift the Kimi exclusion of 2026-09-30, to achieve that Kimi is admitted like any other Go model, accepting that its terms are held only by its dated reading. — 2026-10-30

## Q-3 · What happens to the Go models that no longer answer

context: |
  Topic: models OpenCode Go no longer serves.
  Intention: prepare-loop on 2026-10-30 got 410 (deprecated) from mimo-v2.5
  and mimo-v2.5-pro and 403 (access disabled) from glm-5.2.
  Today: all three stand admitted; every run skips them with an error.
  Repository change: they are removed, or marked with date and status.
  Architecture change: none.
asked: 2026-10-30, conversation 2026-10-30 (interview)
answer: "Markieren, behalten" — keep them declared and mark them with the date and status code
answered_by: maintainer
status: answered

In the context of the Go declaration, facing mimo-v2.5 and mimo-v2.5-pro answering 410 and glm-5.2 answering 403 on 2026-10-30, we decided to keep them declared and mark each with date and status code, to achieve that a return of the model needs no new admission, accepting that prepare-loop keeps reporting them as failures. — 2026-10-30

## Q-4 · Where the seven models that could not be admitted are recorded

context: |
  Topic: the Go models read on 2026-10-30 that the runner cannot reach.
  Intention: two answer only on the Responses endpoint, one only on the
  Google endpoint, four are not in the Pi catalog.
  Today: each stands as a dated comment with its reason in model-endpoints.yaml.
  Repository change: the comments stay, or move into a bead.
  Architecture change: none.
asked: 2026-10-30, conversation 2026-10-30 (interview)
answer: "Kommentar lassen" — keep the dated comments where they are
answered_by: maintainer
status: answered

In the context of the Go declaration, facing seven models read on 2026-10-30 that the runner cannot reach, we decided to keep their dated comments with the reason in model-endpoints.yaml, to achieve that the next reading sees at once what is missing and why, accepting a longer file. — 2026-10-30

## Q-5 · Which tasks the Kimi models may take

context: |
  Topic: the role of kimi-k3 and kimi-k2.7-code after the exclusion is lifted.
  Intention: ADR 0007 also sets which model serves which phase.
  Today: admitted Go models serve only the review loop, ordered by requests
  per 5 hours; explore, implement and repair have their fixed models.
  Repository change: the amendment to ADR 0007, decision 3.
  Architecture change: none for the review loop alone; a fallback role would
  change the role split of ADR 0007.
asked: 2026-10-30, conversation 2026-10-30 (interview)
answer: "Nur Review-Loop" — the review loop only, like every other Go model
answered_by: maintainer
status: answered

In the context of ADR 0007's role split, facing the Kimi models newly admitted, we decided that they serve the review loop only, to achieve that no role of explore, implement or repair changes, accepting that a Kimi fallback for implement would need its own change. — 2026-10-30
