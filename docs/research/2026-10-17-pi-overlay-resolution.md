---
title: "Pi overlay restoration depends on the server modification date"
category: research
created: 2026-10-17
updated: 2026-10-17
last_reviewed: 2026-10-17
status: draft
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Codex, version: "2026-10-17"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-4fk
tags: [research, pi, stage-2, model-catalog]
---

# Pi overlay restoration depends on the server modification date

Measured on 2026-10-17 against the repository-pinned Pi 1.2.0, while reviewing
the protocol-definition preservation repair later committed as `20f976e`.
Copying the freshly retrieved `models-store.json` alone does not guarantee
that an offline reviewer resolves the retrieved definitions.

## Reproduction and result

This is a resolver-only check: no model operation, network request, credential
file, user cache or customer repository is involved. `ModelRuntime` receives
an in-memory credential store and model store; `modelsPath: null` prevents
reading user model configuration. An explicit fetch trap rejects networking.

The same synthetic new text model was supplied twice. Only the saved
`lastModified` differed. The offline refresh returned no errors in either case:

| Saved modification date | Model resolved | Resolved API |
|---|---|---|
| `0` (Pi's representation of an absent/invalid HTTP Last-Modified) | false | absent |
| `2099-01-01T00:00:00Z` (synthetic positive control) | true | anthropic-messages |

Run the following from the repository root with its installed pinned runtime,
using Node in an environment containing no credentials and `PI_OFFLINE=1`:

```javascript
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
const location = resolve("tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js");
const { ModelRuntime } = await import(pathToFileURL(location));
globalThis.fetch = async () => { throw new Error("network forbidden"); };
const credentials = { async read() {}, async list() { return []; } };
const blank = { async read() {}, async write() {}, async delete() {} };
const options = { credentials, modelsPath: null, refreshOnCreate: false };
const base = await ModelRuntime.create({ ...options, modelsStore: blank });
const template = base.getModel("opencode-go", "deepseek-v4.1-flash");
if (!template) throw new Error("missing pinned template");
const model = { ...template, id: "synthetic-protocol-check-free", api: "anthropic-messages" };
for (const lastModified of [0, Date.parse("2099-01-01T00:00:00Z")]) {
  const entry = { models: [model], checkedAt: Date.now(), lastModified };
  const modelsStore = {
    ...blank,
    async read(provider) {
      return provider === "opencode-go" ? structuredClone(entry) : undefined;
    },
  };
  const runtime = await ModelRuntime.create({ ...options, modelsStore });
  const result = await runtime.refresh({ providers: ["opencode-go"], allowNetwork: false });
  const resolved = runtime.getModel("opencode-go", model.id);
  console.log(JSON.stringify({
    lastModified, aborted: result.aborted, errors: [...result.errors.keys()],
    resolved: Boolean(resolved), api: resolved?.api ?? null,
  }));
}
```

## Why copying the store is insufficient

The installed remote catalog wrapper sets an absent/invalid modification
header to zero. Its `remoteModels` restores entries only when that date is
newer than the model data shipped with Pi. A successful forced retrieval and
a successful offline refresh therefore do not prove that the retrieved model
is active. The repair copies definitions but leaves this restoration filter
in place, so the protocol-preservation finding reappears with this new case.

The next repair needs a real-pinned-runtime regression for missing/invalid and
older server dates, not only an assertion that a JSON file was copied. Preserve
the original retrieval evidence; do not claim an invented server date.
After activation, the actual resolved API and endpoint must match the admitted
definition. The final independent review remains pending.

## Source evidence

The following installed package files were read, not credential files:

- `@earendil-works/pi-coding-agent/dist/core/remote-catalog-provider.js`,
  SHA-256 `17e8f3482422aed20ba638b99a8862405f7d3be51c4ffc9eb7ffff1b030a421b`.
  Relevant functions: `readCatalog`, `isNewer`, `remoteModels`, `withRemoteCatalog`.
- `@earendil-works/pi-coding-agent/dist/core/model-runtime.js`,
  SHA-256 `578b742bea061fed029b8e139c6c0bcfe31e60665e9c0c6a08769761ef169dfd`.
  Relevant interfaces: `ModelRuntime.create`, `refresh`, `getModel`.

Limits: this experiment demonstrates local resolution, not a live provider
failure, billing behavior or future reachability. The future date is a
synthetic control, not a production configuration or observed HTTP header.
