# Phase 5 · Verify

**Model:** none. This phase is deterministic.
**Result:** the test output, as evidence in the pull request.
**Gate:** `make verify` green; the stop hook blocks the end of the turn while
anything is red.

```bash
make verify        # every locally runnable gate — CI runs the same, minus a `writer` gate (here only)
make gates         # what CI runs, read from ci.yml; a `writer` gate is marked
make staleness     # hygiene of the plans/ artefacts
```

**The output is the evidence, not your summary of it.** A green run nobody saw
is not a result. A red run is reported, not worked around — including when the
cause is obviously somewhere else.

Every new gate comes with its mutation: plant the fault, watch it go red, take
it back. A gate that has never been red measures nothing.
