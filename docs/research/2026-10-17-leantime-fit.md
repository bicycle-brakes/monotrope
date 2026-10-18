---
title: "Leantime fit — an optional human planning view over the harness"
status: draft
implementation_status: none
date: 2026-10-17
last_reviewed: 2026-10-17
updated: 2026-10-17
supersedes: null
superseded_by: null
bead: coding-harness-al8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, leantime, planning, beads, human-interface]
---

# Recommendation

**Proposed:** assess Leantime as an additional human planning and status view.
Keep Beads/Dolt authoritative for tasks and repository files authoritative for
research, decisions, specifications, plans and reviews. Do not adopt a second
writable tracker through this assessment.

The maintainer requested one subagent's feasibility check on 2026-10-17.
A read-only Codex subagent inspected official Leantime sources and the harness
instructions and workflow at `6029bbf`. The parent recorded its findings here;
this note is based on that delegated research, not an installation or live API
test. The note's branch starts at `origin/main` `6477d04`.

## Options

| Option | Benefit | Cost or limitation | Assessment |
|---|---|---|---|
| Keep the current setup | One task authority and no extra service | The human overview remains spread across chat, handovers and command-line views | Reasonable when stability is the priority |
| Add a Leantime view | Boards, priorities, dependencies and a visible place for decisions awaiting the maintainer | A projection and its freshness must be maintained | Recommended only as a bounded pilot |
| Replace Beads with Leantime | One visual task surface for humans and agents | Migration of tasks, transport, gates and instructions; conflicting states during transition | Not recommended now; requires its own architecture decision |

The fit recommendation is an inference from the harness's existing boundaries.
Leantime can display work; its presence does not enforce the seven phases,
interview answers, review gates or the maintainer's merge authority.

## Verified capabilities and limits

Read on **2026-10-17**. The release page identifies **v3.12.0**, commit
`9d09091`, as current at that reading; no claim about a later release is made.

- The project describes Kanban, table, list and calendar views, dependencies,
  milestones and project overviews. It explicitly names ADHD as a design goal.
  Whether the interface actually helps this maintainer has not been tested.
  Sources: [repository](https://github.com/Leantime/leantime),
  [release](https://github.com/Leantime/leantime/releases/tag/v3.12.0).
- A JSON-RPC API is documented; API keys can be constrained by roles and
  projects. CSV import and export are documented. Exact field mappings,
  read-only permissions and repeatable updates without duplicates were not
  tested. Sources: [API](https://github.com/Leantime/docs/blob/master/api/usage.md),
  [CSV import](https://support.leantime.io/en/article/importing-data-via-csv-1v941gy/),
  [CSV export release notes](https://github.com/Leantime/leantime/releases/tag/v3.10.3).
- Current documentation describes direct HTTP MCP, the protocol for connecting
  agent tools, through a separate MCP-server plugin for self-hosted Leantime.
  A separate bridge process is no longer required by that documented route.
  A simple one-way task projection can start with the ordinary API instead.
  Sources: [MCP documentation](https://github.com/Leantime/docs/blob/master/installation/leantime-mcp.md),
  [plugin offering](https://marketplace.leantime.io/product/mcp-server/).
- External notifications and personal webhooks are described. A complete,
  reliable change-event interface for every task mutation was not verified;
  do not design bidirectional synchronization on that assumption.
  Source: [webhook release notes](https://github.com/Leantime/leantime/releases/tag/v3.10.1).

## Operation and licensing

The official self-hosting setup has an application and MySQL/MariaDB, with
Docker Compose and persistent data directories. Deployment would also need
updates and backups and, depending on exposure, HTTPS, mail and background
jobs. Basic authentication, OpenID Connect and LDAP are documented. Sources:
[Compose](https://github.com/Leantime/docker-leantime/blob/master/docker-compose.yml),
[authentication](https://github.com/Leantime/docs/blob/master/installation/authentication-configuration.md).

The core license is AGPLv3; plugins can have separate, including commercial,
terms. The MCP-server plugin is sold separately. The AGPL text includes a
source-offer obligation for modified versions used over a network. This note
does not establish compliance for a particular deployment, and complete plugin
terms were not read. Sources: [core license](https://github.com/Leantime/leantime/blob/master/LICENSE),
[plugin offering](https://marketplace.leantime.io/product/mcp-server/).

The largest expected integration burden is duplicate state. A two-way bridge
would need conflict handling, deletions and stable identity mappings between
systems. This is an engineering assessment, not a measured effort estimate.
Native AI features and MCP access are not admitted by this proposal; normal
harness endpoint, permission and leak-check rules still apply.

## Small reversible pilot — proposed, not started

1. Use a separate test instance and five synthetic examples: ready, in
   progress, blocked, awaiting a maintainer decision, and awaiting merge.
2. Show the task title and links to its bead, pull request and repository
   artifacts. Provide no write-back to Beads and copy no full documents.
3. Check whether the maintainer can identify the immediate priority and the
   decisions needing their attention more easily. Only then design automatic
   one-way updates as a separately scoped change.

Not read or not tested: complete plugin terms; exact import/update mappings;
conflict-free repeated imports; live API permissions; usability; deployment
and operations in this environment. Nothing was installed, deployed, integrated
or adopted. The maintainer then requested a task: the follow-up qualification
is open at priority 2 (coding-harness-al8). Before that write, the current
configured session scan was rerun with process access and returned no other
interactive session; a Leantime search found no existing task. Earlier in the
session tracker writes were held because the startup hook had reported a
waiting session. The completed research subagent made no tracker writes.
