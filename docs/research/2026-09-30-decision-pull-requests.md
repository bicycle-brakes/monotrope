---
title: "Decision pull requests — marking, templates and merge guards"
category: research
status: proposed
created: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-30"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, pull-request, decision, adr, accessibility, permissions]
---

# Decision pull requests — marking, templates and merge guards

## Result first

Mark a decision pull request in three ways at once, each carrying one job:

1. **Label `decision`** (purple `8250df`): machines and the PR list can
   filter on it.
2. **Title `decide(<scope>): <the decision as a statement>`**: the first word
   says "your decision", the rest says which one.
3. **The first line of the body**, `Merging this PR decides: …`: this is
   what the maintainer reads on the phone before anything else.

Two templates share the same top: a decision template and a lighter ordinary
one (section 4). An agent merges only when the maintainer explicitly asks.
Before merging, it restates the decision block and binds the merge to the
restated commit (`gh pr merge --match-head-commit <sha>`). A
`permissions.ask` rule makes Claude Code prompt for every merge command in
every permission mode (section 4f).

The limit, stated plainly: ask rules match the command as it is written.
They are a brake against accidents, not a lock against intent. This
repository's `docs/WORKFLOW.md` §3 already says the same about deny rules.

## 1 · Starting point in this repository

What was decided on 2026-09-30:

- A decision (an ADR, the interview answers in `decisions.md`, an ADR
  answer) takes effect when the maintainer merges its PR. There is no
  commit signing.
- A PR that carries a decision is marked explicitly.
- Refinement from the same day: agents may merge, but only on the
  maintainer's explicit request and after restating the decision block.

What the repository has today (measured 2026-09-30 through the GitHub API;
files read in worktree `harness-decide-adr` at `665de68`, main at
`1c708f7`):

- **No PR templates.** `.github/` holds only `workflows/`.
- **Only GitHub's ten default labels.** None is used on PRs #34–#53.
- **No branch protection and no ruleset on `main`.** The API returns
  `404 Branch not protected` and `[]`. The repository is private and owned
  by a user account.
- **Merge settings.** Auto-merge is off. A merge commit's message is the PR
  title (`merge_commit_message: PR_TITLE`), so a title prefix ends up in
  `git log`.
- **No draft PR** among the last 100.
- **One ask rule.** `.claude/settings.json` has `ask` only for
  `mcp__omnigent__sys_advise_models`. Nothing covers merges.
- **Titles.** Recent PR titles follow Conventional Commits,
  `type(scope): …`.

Three texts in the repository now contradict the new rule. They are listed
in section 5.

## 2 · Findings

### 2.1 Marking a PR on GitHub

**Labels.** Labels apply to issues, PRs and discussions. Each has a name, a
colour and a description
([GitHub Docs, Managing labels][gh-labels], official). The description is
limited to 100 characters ([REST API, Create a label][gh-label-api],
official). The Shopware ADR process uses exactly this pattern: add the
`ADR` label to the merge request "so everyone can identify merge requests
containing an ADR" ([Shopware ADR 2020-06-25][shopware], established
practice). Rust tracks RFC states with labels such as
`final-comment-period` and `disposition-merge` (read from `rust-lang/rfcs`
through the API on 2026-09-30; established practice).

**Title prefixes.** GitHub's own 2015 advice is a `[WIP]` title prefix for
unfinished work ([GitHub blog, McMinn 2015, updated 2022][gh-blog-pr],
blog). Conventional Commits allows other types besides `feat` and `fix`.
Tools built on the spec simply skip an unknown type
([Conventional Commits 1.0.0][cc], specification). So a custom type
`decide` is allowed by the spec.

**Templates.** A single template can live at `pull_request_template.md` in
the root, `docs/` or `.github/`. Several templates go into a
`PULL_REQUEST_TEMPLATE/` subdirectory ([GitHub Docs, PR template][gh-tpl],
official).

- One of several is chosen only through the `template` query parameter.
  The docs describe no picker in the web UI
  ([GitHub Docs, query parameters][gh-query], official).
- Templates take effect only once they are on the default branch.
- Whether a root default template and the subdirectory work side by side is
  **not verified** in the docs I read.
- Agents do not use the web form. `gh pr create` has `--template`, `--label`,
  `--draft` and `--body-file` (gh 2.101.0, `--help` read locally). An agent
  therefore fills the template into a file and passes `--body-file`.

**Required-label checks.** A CI job can fail when labels are missing, for
example the third-party action `mheap/github-action-required-labels`
(v5.x). It fetches labels through the API and can comment on the PR
([repository README][mheap], community tool).

- **Caveat (official):** by default a `pull_request` workflow runs only on
  `opened`, `synchronize` and `reopened`. A label or body check must also
  list `labeled`, `unlabeled` and `edited`
  ([GitHub Docs, events][gh-events]).
- **Measured caveat:** `main` has no protection (2026-09-30). A red check
  is therefore visible but does not block the merge.

**Draft status.** "Draft pull requests cannot be merged", and "No one can
merge the pull request until you mark the pull request as ready for review
again" ([GitHub Docs, about PRs][gh-about-pr];
[changing the stage][gh-stage], official). This is the only server-side
merge block that needs no branch protection. Whether drafts work in this
private, user-owned repository is **not verified**: it depends on the plan,
and no draft has been used here.

### 2.2 "Merged = accepted": how ADR and RFC processes handle it

There are two models. Coding Harness chose the first.

| Model | Who uses it | What the merge means |
|---|---|---|
| **Merge is acceptance** | Rust RFCs, GOV.UK GDS, Shopware | The PR state is the decision state |
| **Merge publishes, a field decides** | Python PEPs, AWS guidance | A status field or an owner's step decides |

**Merge is acceptance:**

- **Rust:** an RFC is accepted when "merged into the RFC repository",
  after a ten-day final comment period with a disposition of merge, close
  or postpone ([Rust RFC process][rust], official process).
- **GDS:** "The status of your ADR's pull request (PR) reflects the status
  of the decision until it has been accepted. An ADR in the `main` branch
  of your GitHub repository is accepted." The GDS Way advises against
  marking status in the file during review. Page last reviewed
  5 March 2026 ([GDS Way][gds], official UK government practice).
- **Shopware:** the merge request "is also the approval process for the
  ADR". Accepted ADRs are immutable, and changes need a superseding ADR
  ([Shopware][shopware], established practice).

**Merge publishes, a field decides:**

- **PEP 1:** merging a PEP pull request makes it a Draft, "_not_ the same
  as accepting your PEP". Acceptance is written into the `Status` header
  ([PEP 1][pep1], official process).
- **AWS guidance:** acceptance is a state the ADR owner sets after a review
  meeting. Accepted ADRs are immutable ([AWS Prescriptive Guidance][aws],
  vendor guidance).

What this means for Coding Harness:

- **The PR must say what it decides.** In the first model, nothing outside
  the PR tells a reader that merging it is a decision. That is exactly the
  maintainer's "explicitly marked" requirement.
- **Close means reject.** In the GDS reading, a closed decision PR is a
  rejected decision. The template says so.
- **Frontmatter tension (open).** ADRs here carry `status` and `review`
  frontmatter, and ADR 0006 records acceptance "in a commit signed with the
  maintainer's Touch-ID key". Rule RB-M1 (a gate record's state is derived,
  not set) points the same way as GDS: derive acceptance from the merge
  commit rather than from text an agent typed. This is left for the spec
  (section 5).

MADR 4.0.0 (17 September 2024) gives the decision content: context,
considered options, outcome, consequences and confirmation
([MADR][madr], template standard). joelparkerhenderson's collection adds
"one ADR = one decision" and timestamps
([architecture-decision-record][jph], community reference). adr-tools
supports superseding (`-s`); its README says nothing about PRs
([adr-tools][adrtools], tool).

### 2.3 What a good PR description does

- **Google:** the first line is "a short, focused summary" that stands on
  its own. The body says what problem is solved and why this approach, and
  names shortcomings. The description becomes "a permanent part of our
  version control history". Review it before submitting, because PRs
  change during review ([Google eng-practices, CL descriptions][google],
  published practice, no date on the page).
- **GitHub Docs:** a good description gives "why the change is needed, what
  changed, and where reviewers should pay special attention". Keep PRs
  small and focused; do a self-review first
  ([Helping others review your changes][gh-review], official).
- **GitHub blog:** state the purpose, and say what feedback you want and
  when ([McMinn 2015/2022][gh-blog-pr], blog).
- **Research, agent-written PRs:** in 23,000+ PRs from five coding agents,
  1.7 % had a strong mismatch between description and code. Those PRs had
  28.3 % acceptance against 80.0 %, and took 3.5 times longer to merge. The
  most common mismatch (45.4 %) was a description claiming changes that
  were never made ([Gong et al., arXiv 2601.04886, Jan 2026][mci],
  preprint). Consequence: "What your merge confirms" must match the diff,
  and evidence names a command, its result and the commit it ran on.
- **Research, description revisions (weak):** a quarter of PR descriptions
  get revised, and following reviewers' suggestions correlates with
  4.31 times higher odds of acceptance (TOSEM 2026). This rests on a search
  summary only; the paper was **not read** (HTTP 403).
- **Rollback / undo:** the "one-way / two-way door" test is verified in
  Amazon's 2015 shareholder letter ([Bezos 2015][bezos], primary source),
  and `docs/WORKFLOW.md` already uses it. No strong source on "rollback
  sections in PRs" was read.

### 2.4 Cognitive accessibility and ADHD

The strongest source is the W3C Working Group Note *Making Content Usable
for People with Cognitive and Learning Disabilities*, 29 April 2021
([W3C COGA][coga], W3C Note, not normative). It names AD(H)D explicitly and
has patterns that apply directly:

- **4.2.1, make the purpose clear.** A clear heading helps people "easily
  distracted due to … AD(H)D" who come back to a screen and have forgotten
  what they were doing. This is the phone situation.
- **4.4.5, keep text succinct.** One topic per paragraph, "the aim of the
  paragraph or chunk at the beginning", one point per sentence, lists,
  short headings. The example given is a user with AD(H)D.
- **4.4.8, give a summary** of long documents: a few sentences or bullets.
- **4.4.9, separate each instruction:** numbered steps.
- **4.4.10, use white space** between chunks.
- **4.6.3, avoid too much content:** "five or less main choices on each
  screen"; the important information "is the first thing I read".
- **4.7.5, don't rely on memory:** each step carries the information needed
  to act. Instructions come before the call to action.
- **4.8.3, state the results and disadvantages** of each option, especially
  when an action cannot be undone.

Plain-language sources agree:

- **GOV.UK.** People "only read 20 to 28% of text on a webpage" and read in
  an F-shape. "Put the most important information first." Frontload
  headings; at most 5 sentences per paragraph; split sentences over
  25 words; active voice ([GOV.UK clear structure][govuk-structure];
  [clear language][govuk-language], official; no date shown).
- **US Army AR 25-50** (10 Oct 2020, revised 29 Jun 2023), para 1-38:
  writing is "understood by the reader in a single rapid reading". Its two
  essential requirements are the main point first ("bottom line up front")
  and active voice ([AR 25-50][ar2550], official regulation).
- **Nielsen Norman Group:** in the inverted pyramid, readers "can stop
  reading at any point … and still come away with the main point"
  ([NN/g, Schade 2018][nng], expert practice).
- **Not read:** the HBR article on BLUF email keywords (Sehgal 2016) is
  paywalled. Digital.gov carried plainlanguage.gov forward, but its writing
  page did not contain the "most important first" guidance.

"One decision per ask" is repository doctrine (`AGENTS.md`, communication
rules). COGA 4.6.3 (five or fewer choices) and 4.8.3 (consequences per
option) support it. No source was found that names ADHD specifically for
this.

### 2.5 Reading PRs in the GitHub Mobile app

- **The first lines carry the PR (official).** GitHub Mobile puts the PR
  description in the header. "Longer descriptions are truncated and can be
  expanded inline with a tap" ([GitHub changelog, 12 May 2021][gh-mobile],
  official). So everything decisive belongs in the first three lines.
- **Alerts (`> [!IMPORTANT]`).** They are officially defined, with the
  advice to use them "only when they are crucial … limit them to one or two
  per article" and never back to back ([GitHub Docs, alerts][gh-alerts];
  [changelog 14 Dec 2023][gh-alerts-cl], official). Whether GitHub Mobile
  renders them in a PR body is **not verified**. Search results claiming
  mobile support were about third-party apps. If it is not supported, the
  reader sees the literal `[!IMPORTANT]` above a plain quote, and the
  sentence still reads. The templates use one alert only.
- **`<details>` (weak).** In 2020, GitHub staff said the Android app did not
  support it. A 2024 user comment says it now works
  ([community discussion #2822][gh-details-mobile], weak). Only optional
  material (context, evidence) goes inside; if it renders open, nothing
  breaks. How it works on the web: [GitHub Docs][gh-details], official.
- **Tables and task lists.** No official statement about mobile was found.
  Templates use lists instead of tables. They avoid checkboxes, because
  ticking a box is not the decision; the merge is.
- **Recommendation:** test once on the maintainer's phone with a throwaway
  PR (5 minutes). That turns the three "not verified" points into facts.

### 2.6 Guarding merges in Claude Code

Sources: [Configure permissions][cc-perm], [Permission modes][cc-modes],
[Configure auto mode][cc-auto] and [Hooks][cc-hooks] (all official,
code.claude.com, read 2026-09-30). Local version measured: Claude Code
2.1.285.

**What an ask rule does:**

- **Order.** Rules are evaluated "deny, then ask, then allow". A matching
  ask rule prompts even when a narrower allow rule matches too.
- **Every mode.** An explicit ask rule is among the "Actions no mode
  auto-approves", **including `bypassPermissions`**. In auto mode,
  "content-scoped ask rules … always force a permission prompt"; the
  classifier "cannot auto-approve a matching action".
- **Unattended runs.** `dontAsk` mode and `-p` runs with no prompt host
  **deny** the call instead. An unattended agent therefore cannot merge.
- **Syntax.** `Bash(gh pr merge *)` also matches the bare command.
  `*` can stand anywhere, so `Bash(gh api *merge*)` works. `:*` is an
  equivalent trailing form.
- **Compound commands.** Ask rules apply to any subcommand
  (`cd x && gh pr merge 5`, `$(…)`, loops). They also match past any leading
  variable assignment (`GH_TOKEN=… gh pr merge`).
- **MCP tools.** Deny and ask accept tool-name globs, so
  `mcp__*__merge_pull_request` covers the GitHub MCP server's merge tool
  under any server name ([github-mcp-server][ghmcp]).
- **Where rules live.** Ask and deny rules in the project's
  `.claude/settings.json` apply without workspace trust, "since they only
  restrict".

**What an ask rule does not do (official):**

- **Other spellings pass.** "A Bash rule … isn't a security boundary around
  the program." `/usr/bin/…`, `sh -c '…'` and reordered flags are not
  matched. For merges that also means `python -c` with `subprocess`,
  `curl` with `$(gh auth token)`, a `gh alias` that renames `pr merge`, and
  a browser tool clicking the Merge button.
- **Case sensitivity** of the pattern match is not documented. That is the
  reason for writing both `*merge*` and `*Merge*` below.
- **Stronger check: a PreToolUse hook.** A hook can return `"ask"` with a
  `permissionDecisionReason`, which is "shown to the user but not Claude".
  The permission prompt itself can therefore show the decision line. A
  hook's `"ask"` also forces a prompt in auto mode, and deny and ask rules
  still apply whatever the hook returns.

**The auto-mode classifier** (`claude auto-mode defaults`, 2.1.285):

- **Default rule.** It has a soft-deny rule "Merge Without Review:
  Merging a PR before any human has approved it", cleared only when the
  user's message names it.
- **Why it matters here.** "Pull request authors cannot approve their own
  pull requests" ([GitHub Docs][gh-approve]). Agents act under the
  maintainer's account, so no PR here ever has an approval, and this rule
  would block every agent merge in auto mode.
- **With an ask rule, the classifier is never consulted.** The prompt
  resolves first. That is deterministic, which is better than depending on
  the wording of the request.

**The server side.** GitHub cannot tell an agent from the maintainer: same
account, same token. `merged_by` shows the maintainer either way. The only
record that an agent pressed the button is the restatement comment the
agent posts on the PR (section 4f). A server-side lock would need a second
GitHub identity for agents. It is not researched further here and is not
part of the 2026-09-30 decision.

## 3 · Design rules taken from the findings

1. **Decision in line one, then what the merge does.** Sources: Google
   first line, AR 25-50, GOV.UK, COGA 4.4.5; GitHub Mobile truncates.
2. **One alert, only for the decision line.** Source: GitHub's alert
   guidance.
3. **Every option shows its consequence; the recommended one comes first
   and is marked.** Sources: COGA 4.8.3, MADR, `docs/WORKFLOW.md` question
   form.
4. **At most three options and three decisions per PR.** Source: COGA
   4.6.3, which sets the ceiling at five; three is the stricter choice for
   a phone.
5. **Lists, not tables. Collapse only what is optional.** Sources: mobile
   uncertainty, COGA 4.4.10.
6. **Numbered next steps.** Source: COGA 4.4.9.
7. **Evidence names a command, its result and the commit.** Sources: the
   agent-mismatch study, and the repository rule that every number carries
   its cut-off.
8. **Ids are parenthetical suffixes, never the carrier of a sentence.**
   Source: `AGENTS.md` house rule 7.

## 4 · Proposal

All of the following is **proposed, not implemented, not tested**.

### (a) Label

- **Name:** `decision`
- **Colour:** `8250df` (purple). The intent is to match the purple GitHub
  uses for the IMPORTANT alert. That this is the same hex as GitHub's Primer
  colour is **not verified**. It is distinct from the existing default
  labels, though close to the unused `good first issue` (`7057ff`).
- **Description (74 characters, limit 100):** `Merging this PR accepts the
  decision stated at the top of its description.`
- **Create:** `gh label create decision --color 8250df --description "…"`
- **Scope:** one label, no state labels. Open = proposed, merged =
  accepted, closed = rejected (the GDS reading). Rust's state labels exist
  because many people vote; one maintainer does not need them.

### (b) Title convention

`decide(<scope>): <the decision as a statement>`

- Example: `decide(adr): decisions take effect when the maintainer merges`
- Several decisions: `decide(<scope>): 3 decisions on <topic>`
- **Why this form:** the first word says "your decision". The rest is the
  decision itself, so the title alone is the result-first summary (GOV.UK,
  AR 25-50). Conventional Commits permits the type. Because merge commits
  carry the PR title, decisions can later be found with
  `git log --grep 'decide('`.
- **Rejected alternative, `[DECISION]` prefix:** the repository's question
  protocol already uses `[DECISION]` for "open, needs the person". After
  the merge the tag would sit in `git log` although nothing is open any
  more.
- **Rejected alternative, emoji prefix:** it reads badly in screen readers
  and in `git log`.
- **Commits stay as they are.** Commits inside the PR keep their own types
  (`docs(adr): …`). Only the PR title carries `decide`.

### (c) Decision template — `.github/PULL_REQUEST_TEMPLATE/decision.md`

42 lines.

````markdown
> [!IMPORTANT]
> **Merging this PR decides:** <the decision in one plain sentence>.

**Your move:** merge (or ask an agent to) = accept · comment = change · close = reject.

## What your merge confirms
- <what becomes binding, and in which file>
- <what agents will do next because of it>
- **Undo:** <how to reverse it> / <why it cannot be reversed>

## Options
1. **<Option A> (recommended):** <its consequence>. Why: <one reason>.
2. <Option B>: <its consequence>.
3. <Do nothing>: <its consequence>.

## What changes for you
- <effect on your work, or "nothing you will notice">
- <effect on other repositories, or "none">

## Where it fits
Phase <n, name> of seven · stage <1> of three · touches: <component, path>

## After the merge
1. <next step> (<who>)
2. <next step> (<who>)

<details><summary>Context: why this came up</summary>

<Two to four sentences. Ids only in parentheses at the end.>
</details>

<details><summary>Evidence at <short sha></summary>

- `<command>`: <result> (<date>)
- Beads: <title> (<id>), opened / changed / closed
- Research, spec: `<paths>`
</details>

<!-- Decision PR: title "decide(<scope>): <decision>", label "decision".
Agent merge only on the maintainer's explicit request. Restate first, in chat and as a PR comment:
"Merging #<n> at <sha> on your request. It decides: <decision line>. It confirms: <bullets>. CI: <state>."
Then: gh pr merge <n> --merge --match-head-commit <sha> -->
````

Notes on the template:

- **Line one works on a phone** even if the alert does not render.
- **"Your move" names all three outcomes.** Following GDS, closing is a
  rejection.
- **"Undo" separates two-way from one-way doors** (Amazon 2015, and
  `docs/WORKFLOW.md`).
- **"Where it fits"** is one line tying the change to the seven phases and
  three stages. Decisions usually come from phase 1a (`decisions.md`) or
  from the ADR step of phase 7.
- **The restatement format sits in an HTML comment.** Agents read the raw
  body; the phone view stays clean. The visible "Your move" line tells the
  maintainer that an agent may merge on request.

### (d) Ordinary template — `.github/pull_request_template.md`

20 lines. Same top structure, and it says outright that nothing is decided.

````markdown
**In one line:** <what this PR changes, and why, in plain words>.

**Your move:** nothing to decide. Merge (or ask an agent to) when CI is green.

## What changes
- <behaviour that changed, and why it matters>
- <second change, if any>

## Where it fits
Phase <n, name> of seven · stage <1> of three · touches: <component, path>

## After the merge
1. <next step> (<who>), or "nothing"

<details><summary>Evidence at <short sha></summary>

- `make verify`: <result> (<date>)
- Beads: <title> (<id>), opened / changed / closed
- Spec, plan: `<paths>`
</details>
````

The "Beads" line meets house rule 4: a PR names every bead it opens,
changes or closes.

### (e) Several decisions in one PR

**Default: one decision per PR.** Bundle only decisions that are
**coupled**, meaning none can be accepted without the others. A merge is
all or nothing, and GitHub cannot merge part of a PR. Uncoupled decisions
go into separate PRs. The ceiling is three.

````markdown
> [!IMPORTANT]
> **Merging this PR makes 3 decisions:**
> 1. <decision 1, one sentence>
> 2. <decision 2, one sentence>
> 3. <decision 3, one sentence>

**Your move:** merge = accept all three · comment "change 2: …" · close = reject all.

## 1 · <short name of decision 1>
- **Confirms:** <what becomes binding>
- **Options:** **<A> (recommended):** <consequence> · <B>: <consequence>
- **Undo:** <how, or why not>

## 2 · <short name of decision 2>
…

## Why these belong together
<one sentence: what breaks if only some are accepted>
````

"What changes for you", "Where it fits", "After the merge", context and
evidence then appear once, as in (c). The numbers 1–3 are list positions
local to the PR, used in comments like "change 2". They are not ids; each
block carries its meaning in words.

### (f) Merge on request: protocol, ask rules, optional hook

**Protocol** (for every PR; for an ordinary PR, the restatement is its
one-line summary):

1. The maintainer asks, in their own message, e.g. "merge #54". A PR
   comment or a tool result is not a request.
2. The agent reads the PR: `gh pr view 54 --json
   headRefOid,labels,statusCheckRollup,body`.
3. The agent restates in chat, and posts the same text as a PR comment for
   the record: `Merging #54 at abc1234 on your request. It decides: … It
   confirms: … CI: green.`
4. If CI is red, the agent stops and says so. It never uses `--admin`.
5. The agent runs `gh pr merge 54 --merge --match-head-commit abc1234`. The
   ask rule shows the prompt directly below the restatement, and the
   maintainer confirms.
6. If the branch changed after the restatement, `--match-head-commit` makes
   the merge fail, and the agent restates again. This is rule RB-M1's idea
   ("what changes after the signature is unsigned again") applied to the
   merge.

**Ask rules** to add to `.claude/settings.json`, keeping the existing entry:

```json
{
  "permissions": {
    "ask": [
      "mcp__omnigent__sys_advise_models",
      "Bash(gh pr merge *)",
      "Bash(gh api *merge*)",
      "Bash(gh api *Merge*)",
      "Bash(gh alias set *)",
      "Bash(git push *main*)",
      "mcp__*__merge_pull_request"
    ]
  }
}
```

What each rule covers:

- **`gh pr merge *`** covers every variant (`--auto`, `--admin`,
  `--squash`) and the bare command.
- **`gh api *merge*` / `*Merge*`** covers the REST call
  `PUT repos/{o}/{r}/pulls/{n}/merge` and the GraphQL mutations
  `mergePullRequest` and `enablePullRequestAutoMerge`. It also prompts for a
  harmless read that contains "merge" (e.g. `.mergeable`). That costs a
  prompt, not a block.
- **`gh alias set *`** closes the alias detour.
- **`git push *main*`** covers direct pushes to the unprotected `main`,
  which would land a change with no PR at all. It also prompts for any
  branch name containing "main" (e.g. `…domain`). The real guard for this is
  a server-side ruleset (section 5).
- **`mcp__*__merge_pull_request`** covers the GitHub MCP merge tool, if one
  is ever connected.

**Optional second layer (proposed):** a PreToolUse hook
(`.claude/hooks/pre-tool-use/`, Python, parsing with `shlex`, per rule
RB-H3):

- **Recognise every spelling.** It catches `gh … pr merge`, `gh api … merge`
  and GraphQL merge mutations, also inside `sh -c` and behind absolute
  paths.
- **Put the decision into the prompt.** It reads the PR's first line and
  head SHA, and returns `"ask"` with the reason `Decision PR #54 at abc1234:
  <decision line>`.
- **Refuse unbound merges.** A merge command without `--match-head-commit`
  is denied, with a reason Claude sees.
- **Fail closed (rule RB-H2).** If it cannot read the PR, it asks, stating
  that it could not.
- **Still a brake.** It cannot see a script written to a file and run later.

### (g) Optional check: no unmarked decision

A gate in `decisions/gates.yaml`, keeping the one gate list (rule RB-G1),
with a mutation test (rule RB-G4):

- **Paths → mark.** A PR that touches a path whose `allowed` classes in
  `provenance.yaml` include `human-decided` (`docs/adr/`,
  `docs/governance/regelwerk.md`, `docs/decisions/`, `.claude/rules/`, …),
  or any `plans/changes/*/decisions.md`, must carry the `decision` label
  and the `Merging this PR decides` line.
- **Mark → line.** The label requires the line, and the line requires the
  label.
- **Event types.** It runs on `labeled`, `unlabeled` and `edited` as well
  as the defaults.
- **Not checked:** whether the CI generator can emit those event types.
- **Advisory only.** Without branch protection, a red result warns but does
  not block.

## 5 · Open points for the maintainer

Answer the first now. The rest can wait for the spec.

1. **Adopt (a)–(f) as proposed?** Recommendation: yes. The consequence is
   that every PR from then on states on line one whether it decides
   anything. The hook and the check (g) stay optional follow-ups.
2. **Three texts contradict the 2026-09-30 decision** and need amending:
   - `prompts/07-commit.md` says "The merge belongs to a human". Proposed
     wording: "The merge belongs to the maintainer: they merge, or
     explicitly ask an agent to, after the agent has restated the decision
     block."
   - The same file says "Subject in English, body in German", which
     contradicts house rule 1 of `AGENTS.md` (commits and PR bodies are
     English since 2026-09-29).
   - Rule RB-M2 in `docs/governance/regelwerk.md` says whoever approves is
     "neither author nor last pusher". Under one GitHub account this cannot
     be met: the maintainer is always author and last pusher, and authors
     cannot approve their own PRs. The rule set is `human-decided`, so an
     agent proposes text there and does not edit it.
3. **A server-side guard for `main`:** a ruleset with "require a pull
   request", no bypass. It would stop direct pushes; it cannot tell agents
   from the maintainer. Plan availability for a private, user-owned
   repository is **not verified**. The rulesets page names Team and
   Enterprise.
4. **Where acceptance is recorded** (for the spec, not a question now). GDS
   derives it from `main`. Here, frontmatter carries `review.status`.
   Proposal: the agent writes the file as it will read after the merge
   (`approved_by: maintainer, by merging PR #n`), and a check compares that
   with the merge commit. This follows RB-M1: accepted is derived, not set.

## 6 · Not read or not verified

- **GitHub Mobile rendering** of alerts, `<details>`, tables and task lists
  in a PR body: not verified. Phone test proposed (2.5).
- **A root default template beside `PULL_REQUEST_TEMPLATE/`:** not verified.
- **Drafts and rulesets** on a private, user-owned repository: plan not
  verified. The API showed no plan for the token (`plan: null`).
- **Case sensitivity** of Claude Code Bash pattern matching: not documented.
- **Whether `gh` accepts a global flag before the subcommand**
  (`gh -R x pr merge`): not verified.
- **HBR, Sehgal 2016** (BLUF email keywords): paywalled, not read.
- **TOSEM 2026, "Why Are My Pull Request Descriptions Constantly
  Revised?"**: HTTP 403, abstract seen only through a search summary.
- **Springer EMSE, "Pull request latency explained":** redirected to a
  login. The arXiv abstract does not contain the description-length claim
  a search summary attributed to it, so the claim is not used.
- **Showing permission prompts on a phone** (for a session run remotely):
  not researched.

## Sources

Strength: **official** = the vendor's or standards body's own docs;
**practice** = a documented process of a named organisation;
**research** = a peer-reviewed paper or preprint; **blog** = opinion or
community.

- **gh-tpl**: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository — official, read 2026-09-30
- **gh-query**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request — official
- **gh-labels**: https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels — official
- **gh-label-api**: https://docs.github.com/en/rest/issues/labels#create-a-label — official
- **gh-events**: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows — official
- **gh-about-pr**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests — official
- **gh-stage**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request — official
- **gh-approve**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews — official
- **gh-review**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/helping-others-review-your-changes — official
- **gh-alerts**: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax — official
- **gh-alerts-cl**: https://github.blog/changelog/2023-12-14-new-markdown-extension-alerts-provide-distinctive-styling-for-significant-content/ — official, 2023-12-14
- **gh-details**: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections — official
- **gh-mobile**: https://github.blog/changelog/2021-05-12-working-with-pull-requests-on-github-mobile-is-now-much-easier/ — official, 2021-05-12
- **gh-details-mobile**: https://github.com/community/community/discussions/2822 — blog/community, 2020-12-02 to 2024-02-09
- **gh-blog-pr**: https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/ — blog, 2015-01-21, updated 2022-12-06
- **mheap**: https://github.com/mheap/github-action-required-labels — community tool, v5.x
- **ghmcp**: https://github.com/github/github-mcp-server — official GitHub tool
- **cc**: https://www.conventionalcommits.org/en/v1.0.0/ — specification
- **rust**: https://rust-lang.github.io/rfcs/ — practice (official Rust process)
- **gds**: https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html — practice (UK government), last reviewed 2026-03-05
- **shopware**: https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records.html — practice, 2020-06-25
- **pep1**: https://peps.python.org/pep-0001/ — practice (official Python process)
- **aws**: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html — vendor guidance
- **madr**: https://adr.github.io/madr/ — template standard, MADR 4.0.0 of 2024-09-17
- **jph**: https://github.com/joelparkerhenderson/architecture-decision-record — community reference
- **adrtools**: https://github.com/npryce/adr-tools — tool
- **google**: https://google.github.io/eng-practices/review/developer/cl-descriptions.html — practice (published by Google), no date on the page
- **mci**: https://arxiv.org/abs/2601.04886 — research (preprint), 2026-01-08
- **bezos**: https://s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF — primary source, 2016 (letter for 2015); passage checked in the PDF
- **coga**: https://www.w3.org/TR/coga-usable/ — W3C Working Group Note, 2021-04-29
- **govuk-structure**: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/ — official, no date shown
- **govuk-language**: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/ — official, no date shown
- **ar2550**: https://armywriter.com/AR25-50.pdf — official regulation (mirror), 2020-10-10, revised 2023-06-29; para 1-38 checked in the PDF
- **nng**: https://www.nngroup.com/articles/inverted-pyramid/ — expert practice, 2018-02-11
- **cc-perm**: https://code.claude.com/docs/en/permissions — official
- **cc-modes**: https://code.claude.com/docs/en/permission-modes — official
- **cc-auto**: https://code.claude.com/docs/en/auto-mode-config — official
- **cc-hooks**: https://code.claude.com/docs/en/hooks — official
- `claude auto-mode defaults`, Claude Code 2.1.285, run locally 2026-09-30 — measured
- GitHub API reads of `MPAdesso/coding-harness` and `rust-lang/rfcs`, 2026-09-30 — measured

[gh-tpl]: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
[gh-query]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request
[gh-labels]: https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels
[gh-label-api]: https://docs.github.com/en/rest/issues/labels#create-a-label
[gh-events]: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
[gh-about-pr]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
[gh-stage]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request
[gh-approve]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews
[gh-review]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/helping-others-review-your-changes
[gh-alerts]: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
[gh-alerts-cl]: https://github.blog/changelog/2023-12-14-new-markdown-extension-alerts-provide-distinctive-styling-for-significant-content/
[gh-details]: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections
[gh-mobile]: https://github.blog/changelog/2021-05-12-working-with-pull-requests-on-github-mobile-is-now-much-easier/
[gh-details-mobile]: https://github.com/community/community/discussions/2822
[gh-blog-pr]: https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/
[mheap]: https://github.com/mheap/github-action-required-labels
[ghmcp]: https://github.com/github/github-mcp-server
[cc]: https://www.conventionalcommits.org/en/v1.0.0/
[rust]: https://rust-lang.github.io/rfcs/
[gds]: https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html
[shopware]: https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records.html
[pep1]: https://peps.python.org/pep-0001/
[aws]: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
[madr]: https://adr.github.io/madr/
[jph]: https://github.com/joelparkerhenderson/architecture-decision-record
[adrtools]: https://github.com/npryce/adr-tools
[google]: https://google.github.io/eng-practices/review/developer/cl-descriptions.html
[mci]: https://arxiv.org/abs/2601.04886
[bezos]: https://s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF
[coga]: https://www.w3.org/TR/coga-usable/
[govuk-structure]: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/
[govuk-language]: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
[ar2550]: https://armywriter.com/AR25-50.pdf
[nng]: https://www.nngroup.com/articles/inverted-pyramid/
[cc-perm]: https://code.claude.com/docs/en/permissions
[cc-modes]: https://code.claude.com/docs/en/permission-modes
[cc-auto]: https://code.claude.com/docs/en/auto-mode-config
[cc-hooks]: https://code.claude.com/docs/en/hooks
