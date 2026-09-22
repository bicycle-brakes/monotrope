---
title: "Open Code Review assessment for coding-harness"
category: research
status: proposed
created: 2026-09-18
last_reviewed: 2026-09-18
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex-sol
  version: "2026-09-18"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, code-review, evaluation]
---

# Open Code Review assessment for coding-harness

Source revision: upstream `main` as served by GitHub on 2026-09-18 14:53 UTC (moving ref; no commit SHA established). Desk review only; no upstream binary or action was run. The current architecture is `2026-09-17-omnigent-first-target.md`; the older `target-architecture.md` marks itself superseded. This assessment uses the [implementation plan](../architecture/2026-09-17-implementation-plan.md) and [current target](../architecture/2026-09-17-omnigent-first-target.md).

## Recommendation

**Adapt experimentally; defer adoption as a required reviewer or CI gate.** OCR is a credible candidate for an additional code-defect reviewer: it offers explicit Git ranges, JSON output, per-file rule selection, concurrent review, and a PR action. Those capabilities do not establish the harness's SPEC/MAINT judgment, findings lifecycle, or independent trust controls. Use a pinned CLI in a disposable synthetic repository first, as an advisory input to a fresh reviewer. Keep the canonical verifier and findings contract in coding-harness.

## Fit and gaps

| Requirement | Evidence and assessment |
|---|---|
| Independent review | The [README](https://github.com/alibaba/open-code-review) describes a separate agent with codebase search and line comments; its model endpoint is configurable. Independent *process* is plausible, but cross-lineage independence depends on the selected model. The bundled [agent skill](https://github.com/alibaba/open-code-review/blob/main/skills/open-code-review/SKILL.md) and [command](https://github.com/alibaba/open-code-review/blob/main/.claude/commands/open-code-review.md) can filter findings and apply fixes automatically. Do not use that wrapper for the independent review gate: it merges reviewer and fixer roles and may silently discard low-confidence items. |
| SPEC / MAINT | OCR's [rules](https://github.com/alibaba/open-code-review#review-rules) select prompts by file path; `--background` can provide requirements ([command](https://github.com/alibaba/open-code-review/blob/main/.claude/commands/open-code-review.md)). These are inputs to a code reviewer, not evidence of coverage for the target's SPEC/MAINT dimensions, ambiguity, divergence, origin, disposition, or BLOCKER/MAJOR/MINOR semantics. A harness-owned adapter must translate candidates and require human/reviewer disposition. Never infer "no SPEC issue" from empty OCR comments. |
| Faulty and clean controls | The implementation plan requires faulty, correct, and ambiguous fixtures with three qualification runs, false-positive checks, and escalation. OCR's precision and large-scale performance statements are [vendor claims](https://github.com/alibaba/open-code-review), not results on these fixtures. Test the pinned candidate against the harness set before promotion. |
| Diff and evidence binding | CLI accepts `--from/--to/--commit` and JSON ([README](https://github.com/alibaba/open-code-review)); the [GitHub example](https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/README.md) computes merge-base and head. Neither establishes the harness report's base SHA, candidate SHA, contract/config hash, rule/version digest, and stale-result rejection. Capture and check these outside OCR. Disable optional `checkpoint_range` initially: the upstream action documents a bot-comment checkpoint and its writer-trust assumption. Re-review the complete candidate after any code, base, or rule change. |
| Trusted verifier and changed controls | Project rules in `.opencodereview/rule.json` outrank built-ins ([README](https://github.com/alibaba/open-code-review#review-rules)). PR authors may change that file and influence the review. Therefore load rules from an approved revision or external read-only path, record the digest, and have a trusted verifier reject attempts to weaken protected controls. OCR output is advisory and cannot approve its own rule/action changes. |
| Prompt injection / host access | Code and diff are attacker-controlled inputs to the agent. [Issue #90](https://github.com/alibaba/open-code-review/issues/90) documents a path traversal in the v1.3.0 workspace `file_read` path and a prompt-injection exfiltration scenario; it is marked closed, but this review has not verified the fix in a pinned build. Prefer range mode and test the selected version with safe traversal and injected-instruction fixtures. Run under sandbox and egress limits, with no secrets or tracker/control write credentials in the review process. |
| Endpoint privacy and cost | OCR sends code context to a configured LLM and can read full files ([README](https://github.com/alibaba/open-code-review)). This requires the target's declared endpoint, residency, disclosure, and leak-check decisions before any real data. Telemetry is documented as off by default, with optional prompt/response logging; still inspect files, process logs, and egress in the pilot. The CLI exposes concurrency and timeout, but the README does not establish a total cost cap across reviews; enforce aggregate budget externally. GitHub re-review comments can trigger billable runs, and the [example](https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/README.md) restricts them to collaborators. |
| CI | The [example action](https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/README.md) uses `pull_request_target`, secrets, and `pull-requests: write`, checks out trusted base then fetches PR blobs, posts comments, and by default uploads raw JSON/stderr artifacts and prints results to logs. It describes concurrency cancellation and a head-SHA input. A first pilot should use a local CLI in a trusted isolated verifier, with no write token, no automatic comments, and no raw artifact publishing. If a PR action is later justified, pin action and OCR by immutable version/digest, verify head/base at posting, minimize token scope, and set artifact retention/redaction. Do not copy `@main` into a required gate. |
| License and maintenance | The [repository](https://github.com/alibaba/open-code-review) declares Apache-2.0. The [action example](https://github.com/alibaba/open-code-review/blob/main/examples/github_actions/README.md) currently documents CLI >=1.9.6 and a 1.9.10 pin, illustrating active version coupling. Record exact commit, binary checksum, license notice, release date, and supported Git/runtime requirements at pilot time. Community popularity and claimed Alibaba deployment do not prove stable interfaces or current vulnerability status. |

## Smallest gated pilot

1. In a disposable synthetic repo, pin a reviewed upstream source commit and binary checksum; record `ocr version`, Git version, model ID, endpoint and rule digest. Use CLI range mode and `--format json --audience agent --concurrency 1`; no upstream skill/plugin, auto-fix command, or GitHub action.
2. Give the process only read access to the candidate and approved contract slice. Enforce filesystem and egress boundaries outside the agent; omit production secrets and write tokens. Use a declared endpoint and finite request/time/spend budget.
3. Run the existing faulty, correct, and ambiguous fixtures three times each. Add synthetic prompt-injection, traversal, changed-rule, stale-head and stale-base cases. A trusted wrapper records base/candidate SHAs and hashes, rejects stale output, maps OCR comments to proposed findings, and preserves raw evidence privately.
4. A fresh reviewer makes the SPEC/MAINT judgments and writes `findings.md`; OCR does not decide clean status or merge eligibility. Promote only if seeded defects are found, clean controls do not produce blocking false positives, ambiguity escalates, controls hold, and measured cost is acceptable. Otherwise retain it as an optional advisory diagnostic.

## Exact documentation additions proposed

* In `2026-09-17-omnigent-first-target.md` under **Common review contract**, add: "An external review engine may propose findings, but only the harness reviewer assigns SPEC/MAINT, origin, severity and disposition. Empty engine output is not a clean verdict. The reviewer records the engine/version, rules digest, endpoint and base/candidate SHAs."
* In the target's **Trusted enforcement** section, add project review rules, action definitions, and review adapters to protected controls; evaluate changes using an approved revision of the verifier and review rules.
* In `2026-09-17-implementation-plan.md` under **Quality evaluation and qualification for M2**, add an optional OCR pilot row with the synthetic cases and promotion conditions above. Explicitly keep it off the critical path and outside the canonical gate until qualification.
* In the plan's **M0 trust boundary** row, include an attacker-controlled diff instructing reviewer tool reads outside the repository; assert the sandbox and egress boundary holds even if the model obeys the instruction.

## Limits and evidence status

Upstream documentation was consulted online; the current implementation and the fix for issue #90 were not executed or audited. The precise JSON schema, exit semantics on partial review, rule-file trust behavior in the chosen release, and exact token/cost accounting require a pinned-build pilot. The GitHub README search index showed an older release snapshot than the action guide, so version claims above rely on the more recent action guide and must be reconfirmed when piloting.
