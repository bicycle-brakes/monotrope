<!--
Skeleton for the description of one system's architecture, in arc42's twelve
sections. Copy it to where the instance keeps that description, for example
`docs/architecture/<system>.md`. This comment is not copied.

1. The yaml block below is the header of the copy: put its lines between two
   `---` lines at the top and replace every `<...>`. It carries no header of
   its own here (`provenance.yaml`, prefix `templates/`). In the body a
   placeholder stands in backticks, so that GitHub shows it: replace it,
   backticks included.
2. Everything below the block is copied, down to the credit at the end. The
   credit stays in every copy: it is what the licence asks for.
-->

```yaml
title: "Architecture — <system>"
category: architecture
status: proposed
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <role>
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: <agent>, version: "<YYYY-MM-DD>"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [architecture, <topic>]
```

# Architecture — `<system>`

Fill in only what a named reader needs, and name that reader here: `<who reads
this, and for which decision>`. Where a section has nothing for that reader,
say so in one line under its heading and go on; an empty heading says nothing.

Give every number its commit or date, so that a later reader can tell whether
it still holds. What is not known is marked open, with the person who can
answer it, and is never filled in with a guess.

## 1. Introduction and Goals

What the system is for, who uses it, and the few aims that decide its shape.
Keep to as many as the named reader can hold in mind, and rank them.

## 2. Architecture Constraints

What the team did not choose and may not change: technical, organisational and
legal limits, each with the place it comes from.

## 3. Context and Scope

Where the system ends. Show who and what it talks to, people and other
systems alike, and what crosses each line, so that a reader can tell what lies
inside and what does not.

## 4. Solution Strategy

The few decisions that shape everything else, one sentence each, with the aim
each one serves. This is the page to read before the rest.

## 5. Building Block View

How the system divides into parts, from the whole down to the parts that
matter, and what each part is responsible for. A change that moves a part
shows the move in the Architecture delta of `templates/design.md`, in the form
ADR 0009 sets; this section shows the state after it.

## 6. Runtime View

How the parts work together in the few cases that matter: who calls whom, in
what order, and what happens when a call fails.

## 7. Deployment View

Where the parts run: machines, environments and networks, and which part runs
on which. Say where a test or staging environment differs from the real one.

## 8. Cross-cutting Concepts

The rules that hold across several parts, such as how errors, logging, security
or configuration are handled. Write each once here and point to it from the
parts.

## 9. Architecture Decisions

Decisions are not written here. Point to the records under `docs/adr/` and list
the ones a reader of this description must know, each with its number, its
title and its status.

## 10. Quality Requirements

What the system must be good at besides its function, such as speed, safety or
ease of change. Give each as a scenario: what happens, and the measurable
answer. The aims of section 1 are the heads of these.

## 11. Risks and Technical Debts

What may go wrong, and what was left undone on purpose. Give each its cost, its
owner and what would bring it back. A debt is a decision still to be paid, not
a complaint.

## 12. Glossary

Each word used in a special sense in this description, with its meaning here:
the words of the domain and the technical ones, each defined once.

**Credit.** The structure and the headings of this file are an adaptation of
arc42 under CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
arc42 is the template for architecture communication and documentation,
© Dr. Peter Hruschka, Dr. Gernot Starke and contributors, here in its English
version 9.0 of July 2025 (https://arc42.org). The licensors do not endorse this
file. What was changed: the explanatory text is written anew in this
repository's words, the opening rules were added, and sections 5 and 9 point to
this repository's records. What is written into a copy of this file stays its
author's: the licence covers the skeleton, not the description made with it.
