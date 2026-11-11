---
title: "Findings — verify-step-limit"
category: findings
status: draft
implementation_status: none
date: 2026-11-11
created: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-xkvr
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-step-limit

Stage-2 call, 2026-11-11: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1019 files, 3951 commits, 12 rules.

Stage-2 call, 2026-11-11: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1022 files, 3953 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1022 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1022 files, 3962 commits, 12 rules.

Loop attempt: 2026-11-12 — no round was written; the review-loop calls above consumed no stage; audit calls: 2

Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).

Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.

Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).

Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.

Notice: the data terms of longcat-2.0 expire on 2026-11-16 (5 days left).

Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (5 days left).

Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (5 days left).

Notice: the data terms of gpt-6-luna expire on 2026-11-16 (5 days left).

Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (5 days left).

Notice: the data terms of minimax-m3 expire on 2026-11-16 (5 days left).

longcat-2.5-free was asked again with the format reminder: the first answer was malformed

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base

From longcat-2.5-free:

longcat-2.5-free's first answer, which was not in the required format:

The answer was not only six-cell rows; what is not one is kept below as it came.

> </longcat_think>
> No finding.
