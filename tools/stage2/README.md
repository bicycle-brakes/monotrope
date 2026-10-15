# Stage-2 isolated attempts — setup and operation

Every automatic writing attempt (`draft`, `implement`, `repair`) and every
interactive `session` runs in a fresh container with a private candidate, one
selected login and API-only egress; a failed attempt leaves only diagnostics
(ADR 0018, bead coding-harness-s9r). This directory holds what that boundary
is made of:

- `Containerfile` — the `model` and `verifier` images, non-root, read-only
  root filesystem.
- `runtime.lock.yaml` — every pin a launch needs, each with its `measured`
  flag. The supervisor reads this file at every launch and refuses while a
  needed identity is unmeasured.

Read-only verbs (`explore`, `spec-review`, `review-loop`, `review`) are not
containerised; their stated limitations stand (spec, non-goals).

## 1. Install a container program

The setting `STAGE2_CONTAINER_PROGRAM` names the backend; the default is
`podman`. `docker` and Apple `container` are supported through their own
adapters; an explicit executable path is accepted when its basename is one of
the three. A unknown name refuses the call — the runner never substitutes a
backend.

- **macOS:** install Podman Desktop or `brew install podman`, then
  `podman machine init && podman machine start`. Rootless is the default and
  is what the boundary assumes.
- **Linux:** `sudo apt install podman` (or the distribution's package).
  Rootless must work: `podman info` as your own user, no `sudo`.
- **Windows:** automatic writing verbs run through WSL — install Podman
  inside the WSL distribution and run the runner from there. The interactive
  `session` verb keeps its macOS transport and is not available on Windows
  (spec, non-goals).

Check: `podman info --format '{{.Host.Security.Rootless}}'` prints `true`.

## 2. Build and measure the images

    python3 scripts/check_stage2_isolation.py --program podman --build

This builds both targets of `Containerfile` from the lock's inputs, runs the
boundary probes against the production adapters with local test programs and
synthetic logins — no paid model call — and writes a scrubbed report naming
the commit, platform, runtime version, image digests, policy hash and every
probe outcome. The report qualifies calls only for exactly those identities;
a changed runtime, image or policy needs a new report. The hosted CI runs the
same command as the `stage2-isolation` gate.

A missing runtime or an unmeasured platform is remaining qualification work,
never a reason to widen the boundary.

## 3. Prepare the selected login

The attempt receives only the selected endpoint's login material — never a
host home, a full sign-in directory, a keychain or an agent socket:

- `glm-coding-plan`: the `GLM_KEY` line of the secrets file
  (`~/.config/cc-routing/secrets.env`), copied into the attempt's
  environment alone.
- `opencode-go`: the `OPENCODE_GO_KEY` line, likewise.
- `openai-codex` / `claude-code-plan`: the subscription login of the official
  client (`~/.codex/auth.json` resp. the Claude Code credential file), copied
  as the one secret input. Renew a lapsed subscription on the host, before
  retrying; the attempt neither opens sign-in sites nor switches to a
  token-billed substitute.

Endpoint API profiles live in `model-endpoints.yaml` as `api_hosts`. An
empty list refuses the endpoint: `openai-codex` and `claude-code-plan` stay
refused until their profiles are qualified with the official clients.

## 4. Run and clean up

Nothing changes for the caller: the verbs keep their routes, efforts, client
pins and fallbacks. The runner starts the supervisor, which creates
per-invocation volumes and networks, populates the candidate from the
baseline commit, launches the writer, stops it before inspecting anything,
checks the result in a credential-free verifier and publishes only validated
files.

On exit — and at the next invocation after a killed supervisor or a host
outage — the runner removes the resources its invocation recorded, and only
those. A cleanup that could not finish says so and stays visible; it never
claims completion and never prunes globally.

## 5. Refusals and remedies

| Refusal | Meaning | Remedy |
| --- | --- | --- |
| `container program ... not usable` | the backend is missing or not rootless | install per §1, check `podman info` |
| `image ... is not measured` | no qualification report for this image/platform | run §2 on this platform |
| `endpoint ... declares no api_hosts` | the profile is unmeasured or empty | qualify the client, then set `api_hosts` |
| `... login is not available` | the selected login is missing | prepare per §3 |
| `boundary preflight failed` | an adapter cannot express the required boundary | do not weaken it; fix or switch backend within the three |
| leak check BLOCK | the outgoing payload fails the scan | fix the tree; the call never starts |

A refusal never advances the routing table: no fallback starts because a
boundary, declaration or leak check refused (spec criterion 7, criterion 24).
