---
title: "Spec — isolated-attempts"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, isolation, containers]
class: architectural
appetite: 24
adr_files: [docs/adr/0018-isolated-writing-attempts.md]
---

# Spec — isolated-attempts

Every writing call runs behind a tested container boundary, and a failed
attempt leaves the maintainer's worktree ready for another run
(bead coding-harness-s9r). Research: [research.md](research.md).
Decisions: [decisions.md](decisions.md), Q-1 to Q-5; the failed-run cleanup
also delivers the work absorbed from bead coding-harness-b5w (Q-4).

## Problem

- The writing model and the runner's recovery share mutable worktree paths.
  An attempt can replace an input's parent or `findings.md` with a link or
  directory; recovery can then write outside the worktree or crash before
  recording diagnostics. These are the accepted phase-6 limits F-15 to F-17
  of the preceding repair change, collected in research on 2026-10-14.
- CLI permissions are configured, rather than measured confinement of the
  model's reads and writes. The host home, other checkouts and shared Git
  metadata remain outside the protection that Git restoration can offer;
  interactive Pi also uses a sign-in directory containing other logins
  (research, "What exists today — what confines an attempt"; repository
  check at `36e4349`, 2026-10-14).
- A failed post-check leaves both model edits and runner edits behind:
  index rendering, document stamps, formatting and the route block. A fresh
  invocation refuses that tree, although its evidence lists only the model's
  edits. The absorbed exploration establishes this at `c8b009b`; the two
  current attempt loops retain it at `36e4349` (research, "Draft repository
  checks — 2026-10-14").
- The proposed portable container boundary has not been measured. Research
  records that no container program was installed on the maintainer's Mac
  at 18:40 on 2026-10-14; command construction alone cannot prove isolation.

## Terms

**Attempt** means one automatic model call or one interactive `session`
lifetime, including its result checks; every retry is a different attempt.

**Host worktree** means the change's real checkout and its actual Git
metadata; **candidate** means the private repository snapshot an attempt may
edit, with independent Git metadata and disposable runtime files.

**Run baseline** means the accepted state at invocation entry, including any
permitted existing `findings.md` content; later attempts receive that state
plus trusted diagnostics, never a failed candidate's edits.

**Passed inputs** means the explicit repository snapshot, prompt, selected
login and runtime files needed by the call. Container system files and its
own temporary home are available; host homes, sibling checkouts, ignored
host state and the host Git directory are not passed inputs.

**Selected API** means the exact model-service host or hosts declared for the
chosen endpoint, excluding unrelated providers, telemetry and sign-in sites.
The boundary does not prevent data from leaving through this approved API.

**Failure evidence** means runner-owned audit lines, quoted diagnostics and
changed-path evidence in `findings.md`, including its date stamp; it is the
intentional exception to a failed run leaving the baseline unchanged.

The existing routing contract stays in force:

| Verb | Automatic route | Model-call failure |
|---|---|---|
| `draft` | Codex, fresh Codex retry, then GLM 5.3 | advances the existing chain |
| `implement` | Flash, Flash repair, then Sonnet 5.5 | stops |
| `repair` | Codex, fresh Codex retry, then Sonnet 5.5 | stops |
| `session` | the declared Codex or OpenCode Go model chosen at launch | no fallback |

Automatic fallback otherwise follows failed post-checks; explicit
`--stage2-off <reason>` remains a single Sonnet route for `implement` and
`repair`. Effort, CLI pins, official subscription clients and review routes
are unchanged. A boundary, declaration or leak refusal never advances this
table.

## Acceptance criteria

1. When `draft`, `implement`, `repair` or `session` starts a writing attempt,
   it uses a fresh container and private candidate for that attempt.
   *Refuted by:* a writing CLI running on the host or a later attempt reusing
   an earlier attempt's writable volume, home or container.

2. While the writing process runs, host files outside the passed inputs are
   unreadable through both file tools and shell commands.
   *Refuted by:* reading a sentinel in the host home, a sibling directory or
   the actual Git directory, including through a planted link.

3. While the writing process runs, its writes cannot alter host state outside
   its private candidate and disposable runtime resources.
   *Refuted by:* changing a host sentinel, the real worktree, its index,
   configuration, hooks or refs from inside the attempt.

4. When a call receives authentication, it receives only the selected
   endpoint's login material.
   *Refuted by:* another provider's token, a complete host sign-in directory,
   caller secrets or an authentication agent socket appearing in the call.

5. While a writing process runs, its external network access is limited to
   the selected API.
   *Refuted by:* reaching an unapproved host, the host gateway, a service
   socket or an external address by bypassing the approved network path.

6. When the container-program setting is absent or selects `podman`, `docker`
   or Apple `container`, the runner chooses the corresponding backend with
   Podman as the default under the same boundary requirements.
   *Refuted by:* ignoring the setting, changing the model route or using
   weaker requirements for an alternative backend.

7. If a selected backend, image, login or required boundary capability is
   unavailable or unproven, the writing call is refused before it starts.
   *Refuted by:* a host launch, a broader network or mount, an automatic
   backend substitution, or a Stage-1 call escaping this refusal.

8. When a writing call starts, its endpoint authorization and clean leak
   verdict cover the exact prompt and repository material made visible.
   *Refuted by:* a retry or interactive launch sending unscanned inputs, or
   any model call after a declaration refusal or leak-check BLOCK.

9. When an automatic retry starts, its repository inputs match the run
   baseline apart from the runner's accumulated evidence and route metadata.
   *Refuted by:* a failed attempt's source edits, changed instructions,
   statuses, ignored files or private Git changes reaching the next model.

10. If a run fails before publication, the host worktree matches its run
    baseline except for failure evidence.
    *Refuted by:* leftover model edits, index rendering, document stamps,
    formatting, route blocks or newly created ignored files blocking the next
    invocation; the allowed evidence's own stamp is excepted.

11. If a candidate output contains an escaping path, an aliased changed path
    or a non-regular replacement, publication rejects that output.
    *Refuted by:* importing a traversal, absolute path, symlink, hard link,
    special file or file-to-directory replacement, or following a replaced
    parent during recovery; ordinary new directories remain allowed.

12. When a draft is published, its changed paths stay within its change
    folder excluding `decisions.md`, plus at most the change's one new ADR.
    *Refuted by:* a changed interview answer, an existing unrelated ADR,
    another outside path or two new ADRs being published; a second draft may
    revise or rename its own unmerged ADR under the existing whole-change rule.

13. When candidate preparation, formatting, gates or repair proofs execute,
    they run in isolation without model credentials or external network.
    *Refuted by:* candidate-controlled code executing on the host, reading a
    live tracker database or receiving a model token during verification.

14. When candidate files reach the host, all checks required by their verb
    have passed for those exact files.
    *Refuted by:* publishing a red, unmeasured or credential-bearing result,
    or publishing bytes changed after their validation.

15. If the host baseline changes while an attempt runs, publication refuses
    to overwrite the intervening work.
    *Refuted by:* losing a concurrent edit, silently resetting a new HEAD,
    or replacing changed index or pre-existing evidence content.

16. If publication fails before an automatic checkpoint succeeds, the runner
    restores only its own partial publication to the host baseline.
    *Refuted by:* leaving a partial file delta or index update, rewriting
    unrelated refs, or deleting work the invocation did not own.

17. When an automatic writing run succeeds, it creates exactly one clean
    descendant checkpoint containing only the validated result and evidence.
    *Refuted by:* a model-controlled host commit, multiple runner commits,
    unverified files in the checkpoint or a dirty result after success.

18. When repair publishes a code finding as fixed, its named, defined test
    has been demonstrated red against baseline code and green on the candidate.
    *Refuted by:* an absent test, a baseline-green proof or a candidate-red
    test producing `fixed — tests/<path>::<function>`; rows taken as
    `not a test` retain their separate review proof and existing status form.

19. When `implement` or `repair` succeeds, its plan carries a new measured
    time entry attributable to that successful attempt.
    *Refuted by:* reusing an earlier attempt's line, silently inventing a
    duration or losing the successful attempt's measurement on publication.

20. When an interactive session exits normally with a candidate that passes
    its checks, its edits are returned to the host worktree uncommitted.
    *Refuted by:* losing valid session edits, exposing edits before
    verification, making an automatic host commit, or treating Terminal
    dispatch as verified completion.

21. When an attempt fails or succeeds, runner-owned evidence preserves its
    audit and distinguishes model-changed paths from runner-derived paths.
    *Refuted by:* lost prior audit lines, failed-model statuses surviving,
    missing diagnostics or a derived write attributed to the model.

22. When an attempt ends, or the next invocation recovers an interrupted
    attempt, its containers, volumes, network helpers and copied login are
    removed without deleting user-owned resources.
    *Refuted by:* reusable login or candidate state remaining after cleanup,
    or recovery deleting an unrelated container or volume; abrupt host loss
    is recovered at the next invocation, not claimed as immediate cleanup.

23. When this change is declared done, live Podman probes on macOS and Linux
    have measured the production launch boundary at named commits.
    *Refuted by:* command-only assertions, skipped probes or missing evidence
    for filesystem access, credential selection, allowed and denied network
    paths, retry separation and cleanup on either platform.

24. When writing calls use the new boundary, the existing routing and
    non-isolation proof contracts described above remain in force.
    *Refuted by:* altered efforts, client pins, fallback triggers, reviewer
    routes, review-round budgets, fixed-status forms or the draft's single
    missing-ADR-answer tolerance being broadened.

## Non-goals

- Containerising the read-only `explore`, `spec-review`, `review-loop` and
  `review` calls; Q-2 scopes the four writing verbs, and Q-3 applies read
  confinement to those calls. Their existing limitations remain stated.
- Native Windows execution or a new Windows/Linux interactive terminal
  dispatcher. Automatic Podman use on Windows is through WSL; `session`
  retains its current macOS transport.
- A VM per attempt, a cluster runner, kernel-escape resistance or preventing
  data from leaving through the approved model API. Podman's shared machine
  VM is the tradeoff accepted in Q-5.
- Live authentication within the attempt, new billing paths or an automatic
  switch to an API key when a subscription login cannot be passed safely.
- Keeping or automatically completing failed candidate trees. Failure
  diagnostics are retained; Q-4 deliberately replaces failed-tree carry-over.
- Changing model selection, review roles, the loop budget, tracker ownership
  or the meaning and enforcement of existing gates.

## Protected areas

- The host home, sibling repositories and shared tracker database remain
  outside the model and verifier boundary; only a fresh tracker render needed
  by the gates is passed through the existing render access point.
- Existing ADR bodies, interview answers, ADR-answer records and adoption
  decisions are preserved; the new ADR amends only the stated boundary and
  failed-attempt behaviour, with acceptance by merge.
- Host Git hooks, configuration, unrelated refs, user-owned ignored files
  and unrelated runtime resources are never a restoration surface.

## Definition of Done

- `make verify` is green and all 24 criteria have their ledger evidence.
- The same decision PR carries `AGENTS.md`, `docs/WORKFLOW.md`, the endpoint
  declaration, `prompts/04-implement.md`, the image/setup documentation and
  `docs/adr/0018-isolated-writing-attempts.md` alongside the runner change;
  `plan.md` names the complete file list and generated CI/index updates.
- The PR file list demonstrates that protected areas and non-goals stand.
- The PR names and closes both the isolation work and the absorbed failed-run
  cleanup work, with closing trailers for `coding-harness-s9r` and
  `coding-harness-b5w`; tracker changes remain the orchestrator's responsibility.
- Special runs: live default-Podman boundary reports on macOS and Linux,
  identifying commit, runtime version, platform and image digest; each
  configured alternative must pass its boundary preflight before a real call.
- A missing runtime or unmeasured platform is a remaining qualification task,
  never evidence that the change is done.

## Open decisions

None open. Q-1 to Q-5 supply the intent; no maintainer or ADR answer is
recorded by this draft.

- [DETAIL] Use the architectural class because this introduces an execution
  subsystem and changes the model-to-host trust boundary; phase 2b and one
  new ADR are therefore required.
- [DETAIL] Set the phase-4 appetite to 24 hours including repairs because
  four entry points, safe result publication and live qualification are one
  change; neither the interview nor an earlier spec sets a smaller appetite.
- [DETAIL] Publish interactive edits after normal exit and verification,
  without committing them, because a private session needs a return path
  while preserving the session verb's existing lack of automatic commits.
- [DETAIL] Preserve explicit failure evidence while discarding failed trees
  because diagnostics remain needed by the established retry routes and Q-4
  requires a fresh invocation to start without manual restoration.

These reversible details are chosen here with their reasons visible.
