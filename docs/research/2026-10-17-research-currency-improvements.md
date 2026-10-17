---
title: "Research currency needs claim-level evidence"
category: research
created: 2026-10-17
updated: 2026-10-17
last_reviewed: 2026-10-17
status: draft
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Codex, version: "2026-10-17"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-pu9
tags: [research, currency, provenance]
---

# Research currency needs claim-level evidence

Read-only Sol subagent research on 2026-10-17 at `6477d04`. Today the checker
reports age, not semantic validity: top-level `last_reviewed` older than 90
days is due; invalid dates are due; missing/empty inventory is not measured.
The drift gate is report-only and performs no network/Git/tracker validation.

The recheck prompt already requires reading the whole note, checking at most
15 dated claims against primary sources and appending Holds/Overtaken/New/Not
read. A concrete gap remains: partial review may renew the whole note's date,
making unchecked claims appear younger. Do not repair currency by stamping dates.

Proposed native manual first slice: register source, version/commit, review
date, volatility/risk and dependent decisions per claim. Separate age-due,
source-changed, claim-revalidated and human-approved. Faster-changing prices,
terms and model availability need different revisit rules from historical
architecture rationale; exact thresholds remain interview decisions.

HTTP validators save transfers, but `304` proves a cached representation,
not a semantic conclusion. A changed page requires inspection, not automatic
rejection. Version facts differ from claims about the latest version.
Evidence can flag potentially stale decisions, never amend an ADR automatically.

Acceptance: offline fixtures prove that `304` does not renew semantic dates;
partial checks leave remaining claims due; changed sources require review;
timeout/429/5xx/invalid responses and absent validators remain not checked.
Bound time, response size and retries. No automatic tracker or decision writes.

## Sources and measured limits

- [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.4.5): conditional HTTP/cache semantics.
- [GitHub latest release](https://docs.github.com/en/rest/releases/releases#get-the-latest-release): excludes prereleases; not every notion of newest.
- [W3C PROV](https://www.w3.org/TR/prov-overview/): source, assertion, activity and responsibility attribution.

The parent ran the existing checker with the locked research-swarm environment:
29 notes, zero age-due on 2026-10-17; oldest reviewed 31 days earlier. This
does not establish semantic freshness. The subagent read 30 test functions
but ran none; its first inventory attempt lacked PyYAML. The full metadata
convention was not read. No file changes, credentials or customer access by
the subagent; no live model call or implementation.

Findings were added to the existing research-currency task (coding-harness-pu9),
preserving its deferred status. Hermes groundwork (coding-harness-i3y) and
ADR 0010 remain unchanged; runner replacement or unattended activation needs
separate treatment. The proposed manual native report is not that activation.
