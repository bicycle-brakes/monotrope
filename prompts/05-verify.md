# Phase 5 · Verify

**Model:** none. This phase is deterministic.
**Result:** the test output, as evidence in the pull request.
**Gate:** `make verify` green; the stop hook blocks the end of the turn while
anything is red.

```bash
make verify        # every locally runnable gate: the unmarked seconds-class gates first, without the verify slot, then the minutes-class gates and any seconds-class gate marked `needs_admission: true` inside it — CI runs the same, minus a `writer` gate (here only)
make gates         # what CI runs, read from ci.yml; a `writer` gate is marked
make staleness     # hygiene of the plans/ artefacts
```

The seconds-class gates the gate list does not mark `needs_admission: true`
run before the run asks for the machine's verify slot, all of them, and report
every red one together; a red blocking one ends the run there, without
waiting. The minutes-class gates and every marked seconds-class gate run inside
the slot, and there a red run stops at the first red blocking gate. Either way
the run names the gates it did not run; those were not measured, and a fix is
followed by a fresh full run, never by a claim about the rest. The hosted CI
runs every gate.

**The output is the evidence, not your summary of it.** A green run nobody saw
is not a result. A red run is reported, not worked around — including when the
cause is obviously somewhere else.

Every new gate comes with its mutation: plant the fault, watch it go red, take
it back. A gate that has never been red measures nothing.
