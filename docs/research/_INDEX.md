# Research Index

The research corpus behind the coding workflow. Every document carries
frontmatter (category: research); provenance classes follow the five-class
enum in `provenance.yaml` — the maintainer corrects a class by editing the
frontmatter, never by deleting the claim.

| Document | Internal stand | Focus | Tags |
|---|---|---|---|
| [`arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md`](arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md) | Version 1.2 · 17.09.2026 | arc42 reference architecture „Agentischer Delivery-Workflow“ (ADW), tool-neutral conventions, Omnigent as target runtime | arc42, adw, omnigent |
| [`Lake-Switch-Architektur-arc42.md`](Lake-Switch-Architektur-arc42.md) | 2026-09 | arc42 documentation of the toolchain/working environment Lake Switch is developed in (the product's own arc42 lives in `lakeswitch-ai`) | arc42, lakeswitch, toolchain |
| [`Migrationsplan_Omnigent_Referenzarchitektur.md`](Migrationsplan_Omnigent_Referenzarchitektur.md) | 2026-09 | stepwise instantiation of the ADW reference architecture into a productive Omnigent topology — no big bang, abort criteria per stage | migration, omnigent |
| [`2026-09-16-review-corpus-vs-running-workflow.md`](2026-09-16-review-corpus-vs-running-workflow.md) | read at `5a950c2` · 2026-09-16 | review of the three documents above against the running workflow: adopt / keep / decide per topic, contradictions between the sources, eight decisions for the maintainer, proposed corrections | review, adw, lakeswitch, omnigent |

Intake note: copied in by the maintainer on 2026-09-16 (Phase 2 of the
separation, bead `coding-harness-anw`). Provenance is set to
`ai-drafted-reviewed` with review pending — the maintainer corrects the class
where the hand differs.
