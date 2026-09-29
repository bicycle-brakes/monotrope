---
title: "Signed decisions — handing the practice to further repositories"
category: how-to
status: proposed
owner: framework-architect
last_reviewed: 2026-09-23
updated: 2026-09-29
tags: [signing, decisions, touch-id, lakeswitch, how-to]
created: 2026-09-23
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-23"}
review: {status: pending, approved_by: null, approved_at: null}
---

This guide hands the Touch-ID signing of decisions to every repository that is
to adopt it. It describes what holds, how it is set up on this machine, what
lakeswitch-ai already enforces and what a further repository has to do. As of
2026-09-23.

## The rule

There are two kinds of approval (lakeswitch-ai decision interview, D-55; D-55
is not ratified yet, it belongs to cluster 4 of that interview):

- **A decision** — a change to protected decision files, an ADR, a
  ratification — takes effect only through a commit the maintainer signs with
  the Touch-ID key. An assistant may prepare it; no agent's commit confirms
  it.
- **The approval of a gate** in a delivery stays what rule RB-M2 says: an
  approval in the pull request by a person who is neither its author nor its
  last pusher. A signed decision commit never replaces it.

## The key

| Property | Value |
| --- | --- |
| Location | Secure Enclave of this MacBook, app Secretive |
| Name | `lakeswitch-decisions` |
| Type | ECDSA (nistp256) |
| Fingerprint | `SHA256:LMqOFIm/waO3jemYoQjG8YWpM/iMQKEZW8D+S59QM7c` |
| Signs | only after a Touch-ID confirmation |
| GitHub | registered as a signing key since 2026-09-23 |

Public key:

```text
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBL60s+Y69G7SuhSPW78ckY9PlVR1KH3oNF4W5lLo/1OqPT5lN7cy4+1XD/ZQA341OkF078KKvrruCGgAusnSPZU=
```

The older software key `~/.ssh/id_ed25519` confirms **no** decision. Any
process with access to the SSH agent can sign with it; it proves the machine,
not the person. The global git setting `commit.gpgsign true` keeps signing
ordinary commits with it — that is intended and has nothing to do with
decisions.

## Signing: `git confirm`

Since 2026-09-23 the global alias `git confirm` is set up. It sets
Secretive's socket and the Touch-ID key for this one commit only:

```sh
git confirm -F <message-file>
git confirm -m "decisions: …"
```

The Touch-ID dialog appears; without a finger no commit is made. The
definition lives in `~/.gitconfig` (`alias.confirm`). Whoever needs it on
another machine creates a Secure Enclave key of their own and declares it as a
further signer — a key never leaves the Secure Enclave.

Checking:

```sh
git log -1 --format='%h %G? %GK %s'      # the fingerprint must be SHA256:LMqO…
gh api repos/<owner>/<repo>/commits/<sha> -q .commit.verification
```

Locally `%G?` shows `U` and `No principal matched` as long as the local file
`gpg.ssh.allowedSignersFile` does not know the key. That is harmless; the
checks that count are the repository's (see below) and GitHub's.

## Division of work between assistant and maintainer

1. The assistant prepares the change: in a worktree of its own, with tests
   and verify, and leaves the commit message as a file.
2. The assistant signs nothing. It puts the exact command in front of the
   maintainer.
3. The maintainer runs it personally (in Claude Code with a leading `!`),
   confirms with Touch ID, and the change is pushed.
4. The assistant then checks the signature, CI and the fingerprint.

The assistant cannot sign even if it tried: the key signs only on a Touch-ID
confirmation. Claude Code's permission layer also refused a session the
signed commit on 2026-09-23 (handover of that day). That refusal fits the
rule, but it is not the rule's guarantee — the guarantee is the Secure
Enclave.

## What lakeswitch-ai already enforces

Since pull request #40 (merged 2026-09-23), gate **M-30** in lakeswitch-ai holds
every commit that changes `decisions/` against the declared keys:

- Declaration: `decisions/signers.yaml` — anchor commit, signers with role,
  key and fingerprint. Its model is
  `lakeswitch.declared.signers.SignersDocument`.
- Check: `lakeswitch.signatures` (`examine`, `check`), offline with `git` and
  `ssh-keygen`.
- Anchor: `c02f11d`, the first Touch-ID-signed commit. Older commits count
  as "not examined", not as passed.
- Merges: only the combined diff is checked. A clean merge commit made by
  GitHub brings nothing of its own under `decisions/` and needs no signature;
  the commits it brings in are checked one by one. A squash or rebase merge
  by GitHub carries GitHub's own signature and is rejected — hence merge
  commits only there.
- What cannot be checked (no `ssh-keygen`, a shallow clone, a missing
  anchor) is a finding of its own, never a pass.
- Specification: `spec/gates.md`, invariant G-16, and the open decision in
  §9.6 (whether M-30 belongs to the floor).

## What a further repository has to do

1. **Name the protected paths.** Which files are decisions (decision folder,
   ADRs, gate list, provenance map)?
2. **Declare the signers.** A file inside the protected area with anchor,
   role, key and fingerprint, following `decisions/signers.yaml` in
   lakeswitch-ai. The anchor is the first commit the maintainer signs in that
   repository with `git confirm`.
3. **Build in the check.** Take over the code of `lakeswitch.signatures` or —
   once it exists — obtain it from the coding-harness kit (D-45: a pinned
   copy, no dependency). Tests follow
   `tests/signatures/test_the_signatures.py` in lakeswitch-ai.
4. **Check CI.** `fetch-depth: 0` in the checkout and `ssh-keygen` available
   (shown on `ubuntu-latest` in lakeswitch-ai: M-30 ran green there).
5. **Fix the merge method.** Merge commits only — no squash or rebase merges
   for pull requests that change protected paths.
6. **Check open branches.** Unsigned commits under protected paths on
   branches not yet merged turn the gate red after the merge. In
   lakeswitch-ai this concerns `feat/agent-definitions` (two commits).

## State per repository (2026-09-23)

| Repository | State |
| --- | --- |
| lakeswitch-ai | enforced: gate M-30, anchor `c02f11d` |
| coding-harness | signed, not checked (details below) |
| further repositories | not read |

In coding-harness the acceptances of ADR 0004 (`d4b1d47`) and ADR 0005
(`8fc92e4`) are Touch-ID-signed. Whether the rule holds here is open; there
is neither a gate nor a signers file.

## Open

- Ratify D-55 (cluster 4 of the lakeswitch decision interview).
- Decide whether coding-harness adopts the rule for its own decision files,
  and then add to RB-M2 in the rule set the sentence that it governs the
  approval of gates, not the confirmation of decisions.
- Take the check into the coding-harness kit as a mechanism, so instances do
  not copy it one by one.
