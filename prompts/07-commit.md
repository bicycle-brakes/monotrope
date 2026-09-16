# Phase 7 · Commit

**Model:** Haiku 4.5 — cheap and sufficient.
**Result:** pull request.
**Gate:** CI green.

- **Conventional Commits with a work-item reference:** `feat(<bead>): …`
- **Subject in English, body in German.** The body says *why* — the *what* is
  in the diff.
- **Provenance is declared:** `Co-Authored-By:` or `Assisted-by:` where an
  assistant took part. Concealing that share does not make the result more
  dependable; it makes the question unanswerable.
- **The pull request text explains itself.** It is read by someone who does not
  have the artefacts open beside it: what this is about, what was broken, what
  holds now and why, how it was checked — with numbers measured at the state of
  this pull request. Spec, plan and verification evidence are named as
  references at the end; shorthand from the artefacts (D1, A-5, G-3, work-item
  ids) carries no sentence. The same goes for the commit body.
- **If this commit finishes the work item, say so:** a `Closes-Bead: <id>`
  trailer, like GitHub's `Closes #123`. The scope names only *what was worked
  on* — a work item usually has several commits, and the last is rarely the
  finish. Without the trailer the item stays open; that is the right default,
  because a merged pull request often leaves work behind.

Then the end of the artefact lifecycle: the delta into the living capability
spec, lasting decisions as an ADR under `docs/adr/`, the rest into
`plans/changes/archive/YYYY-MM-DD-<name>/`.

After the merge, `make close-merged ARGS=--write` closes what was declared and
what is an ancestor of the integration branch — both are checked, not claimed.
Without `--write` the command only reports; writing is required, not forgotten.
It runs locally: the tracker writes to a database this repository does not
carry. CI only reports — a declared closure nobody carried out is a finding, not
a job for the machine.

**You do not sign off your own work.** The merge belongs to a human.
