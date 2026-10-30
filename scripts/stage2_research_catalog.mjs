#!/usr/bin/env node
/** Pinned-Pi metadata bridge. No model operation, user config or credential file.
 *
 * Python checks duplicate identities, policy and capabilities from the raw
 * bodies before dispatch. The CLI uses fixed public sources; exported options
 * allow offline contracts to replace those sources with loopback servers.
 */
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";

const PROVIDER = "opencode-go";
const REDIRECT_STATUSES = new Set([301, 302, 303, 307, 308]);
const stamp = () => new Date().toISOString();

/** A redirect refused before its target is contacted, or a blocked second hop. */
class RedirectRefused extends Error {}

export async function collectCatalog({
  catalogBaseUrl = "https://pi.dev",
  metadataUrl = "https://models.dev/api.json",
  deadlineMs = 60_000,
  seedStore = {},
} = {}) {
  const started = performance.now();
  const controller = new AbortController();
  const sources = {
    pi: { url: new URL(`/api/models/providers/${PROVIDER}`, catalogBaseUrl).href, outcome: "not-checked" },
    models_dev: { url: metadataUrl, outcome: "not-checked" },
  };
  const entries = new Map(Object.entries(structuredClone(seedStore)));
  const originalFetch = globalThis.fetch;
  let requests = 0;
  let timedOut = false;
  let piState, metadataState, version;
  let baseline = [];
  let runtimeResult = { errors: [], aborted: false };
  const record = async (name, response) => {
    const body = await response.text();
    Object.assign(sources[name], {
      status: response.status, retrieved_at: stamp(), body,
      sha256: createHash("sha256").update(body).digest("hex"),
      outcome: response.status === 200 ? "ok" : "http-error",
    });
    return body;
  };
  const failed = (name, error) => {
    Object.assign(sources[name], {
      outcome: timedOut ? "timeout" : "request-failed",
      retrieved_at: stamp(), error: String(error?.message ?? error).slice(0, 500),
    });
  };

  // The admitted target: same origin and path as the request, credential- and fragment-free,
  // whose query is the original multiset plus exactly one pi-version equal to the already
  // validated manifest pin. The original itself carries no pi-version, and ordering or encoding
  // of equal values is free.
  const admittedTarget = (location, requested) => {
    if (typeof location !== "string" || location.trim() === "") {
      throw new RedirectRefused("the catalog redirect carries no usable Location header");
    }
    let target;
    try {
      target = new URL(location, requested);
    } catch {
      throw new RedirectRefused(`the catalog redirect Location is not a usable URL: ${location.slice(0, 200)}`);
    }
    const original = [...new URLSearchParams(requested.search).entries()];
    const changed = [...new URLSearchParams(target.search).entries()];
    const versions = changed.filter(([name]) => name === "pi-version");
    // Each pair is encoded on its own before sorting, so a comma inside a name or value can
    // never make two different multisets compare equal (review rows L1-4, L1-6).
    const canonical = (pairs) => JSON.stringify(pairs.map((pair) => JSON.stringify(pair)).sort());
    const samePairs = (left, right) => canonical(left) === canonical(right);
    if (
      target.origin !== requested.origin || target.pathname !== requested.pathname ||
      target.username !== "" || target.password !== "" || target.hash !== "" ||
      original.some(([name]) => name === "pi-version") ||
      versions.length !== 1 || versions[0][1] !== version ||
      !samePairs(changed.filter(([name]) => name !== "pi-version"), original)
    ) {
      throw new RedirectRefused(`the catalog redirect Location is not an admitted target: ${target.href}`);
    }
    return target;
  };
  // Pi's pinned management client normally retries and applies a four-second
  // attempt timeout. This isolated adapter admits one catalog call from Pi and
  // uses the shared deadline instead; a second call is aborted before I/O.
  // Inside that one call it makes at most two real GETs through the saved
  // `originalFetch`: the request, and the one measured redirect — same origin
  // and path, adding exactly the pinned version. The hop must not go through
  // `globalThis.fetch`, whose counter would refuse it (review row L3-1); every
  // other redirect is refused before its target is contacted.
  globalThis.fetch = async (input, init = {}) => {
    const url = new URL(typeof input === "string" || input instanceof URL ? input : input.url);
    if (url.origin !== new URL(catalogBaseUrl).origin ||
        url.pathname !== `/api/models/providers/${PROVIDER}` ||
        (init.method && init.method !== "GET") || ++requests !== 1) {
      throw new DOMException("only one Go catalog request is permitted", "AbortError");
    }
    sources.pi.url = url.href;
    const answer = async (response) => {
      const body = await record("pi", response);
      return new Response([204, 205, 304].includes(response.status) ? null : body, {
        status: response.status, headers: response.headers,
      });
    };
    try {
      const first = await originalFetch(input, {
        ...init, signal: controller.signal, redirect: "manual", credentials: "omit",
      });
      if (!REDIRECT_STATUSES.has(first.status)) return await answer(first);
      try {
        await first.body?.cancel();
      } catch {
        // A redirect body that cannot be released must not fail the hop.
      }
      const target = admittedTarget(first.headers.get("location"), url);
      Object.assign(sources.pi, { redirected_to: target.href, redirect_status: first.status });
      // The second hop is read manually too: a further redirect is recognised by its status, not by
      // a library's error wording, and its Location stays unfollowed (review rows L1-1, L1-7).
      const response = await originalFetch(target, {
        ...init, signal: controller.signal, redirect: "manual", credentials: "omit",
      });
      if (REDIRECT_STATUSES.has(response.status)) {
        try {
          await response.body?.cancel();
        } catch {
          // A redirect body that cannot be released must not change the refusal.
        }
        throw new RedirectRefused(`the admitted catalog target ${target.href} redirected again`);
      }
      return await answer(response);
    } catch (error) {
      if (error instanceof RedirectRefused) {
        Object.assign(sources.pi, {
          outcome: "redirect-refused", retrieved_at: stamp(),
          error: String(error.message).slice(0, 500),
        });
      } else {
        failed("pi", error);
      }
      throw error;
    }
  };

  const pi = async () => {
    const manifest = JSON.parse(await readFile(new URL("../tools/pi/package.json", import.meta.url), "utf8"));
    version = manifest.dependencies["@earendil-works/pi-coding-agent"];
    const installed = JSON.parse(await readFile(
      new URL("../tools/pi/node_modules/@earendil-works/pi-coding-agent/package.json", import.meta.url), "utf8",
    ));
    if (!/^\d+\.\d+\.\d+$/.test(version) || installed.version !== version) {
      throw new Error("the installed Pi does not match the repository pin");
    }
    const { ModelRuntime } = await import(
      "../tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js"
    );
    const runtime = await ModelRuntime.create({
      // The public catalog is credential-free, but the pinned management
      // client skips refresh for unconfigured providers. This in-memory
      // sentinel enables that branch; the catalog request carries no auth.
      credentials: {
        async read(provider) {
          return provider === PROVIDER ? { type: "api_key", key: "catalog-only-not-a-credential" } : undefined;
        },
        async list() { return []; },
      },
      modelsPath: null, refreshOnCreate: false,
      modelsStore: {
        async read(provider) { return entries.get(provider); },
        async write(provider, entry) {
          if (provider !== PROVIDER) throw new Error("only Go catalog persistence is permitted");
          entries.set(provider, structuredClone(entry));
        },
        async delete(provider) { entries.delete(provider); },
      },
      catalogBaseUrl,
    });
    baseline = runtime.getAllModels(PROVIDER).map((model) => model.id);
    const result = await runtime.refresh({
      providers: [PROVIDER], allowNetwork: true, force: true, signal: controller.signal,
    });
    runtimeResult = {
      aborted: result.aborted,
      errors: [...result.errors].map(([provider, error]) => [provider, String(error?.message ?? error).slice(0, 500)]),
    };
    if (runtime.getError()) runtimeResult.errors.push([PROVIDER, runtime.getError()]);
    piState = { ok: !runtimeResult.aborted && runtimeResult.errors.length === 0 };
  };
  const metadata = async () => {
    try {
      const response = await originalFetch(metadataUrl, {
        signal: controller.signal, redirect: "error", credentials: "omit",
        headers: { accept: "application/json" },
      });
      await record("models_dev", response);
      metadataState = { ok: response.status === 200 };
    } catch (error) {
      failed("models_dev", error);
      metadataState = { ok: false };
    }
  };
  let timer;
  const expired = new Promise((resolve) => {
    timer = setTimeout(() => {
      timedOut = true;
      controller.abort();
      resolve();
    }, deadlineMs);
  });
  try {
    // Both readers start before either is awaited, with one shared timer.
    const piTask = pi().catch((error) => {
      piState = { ok: false };
      if (sources.pi.outcome === "not-checked") failed("pi", error);
      runtimeResult.errors.push([PROVIDER, String(error?.message ?? error).slice(0, 500)]);
    });
    const metadataTask = metadata();
    await Promise.race([Promise.all([piTask, metadataTask]), expired]);
    if (!piState) Object.assign(sources.pi, { outcome: "timeout", retrieved_at: stamp() });
    if (!metadataState) Object.assign(sources.models_dev, { outcome: "timeout", retrieved_at: stamp() });
    const ok = piState?.ok === true && sources.pi.outcome === "ok" &&
      sources.pi.status === 200 && entries.has(PROVIDER);
    return structuredClone({
      schema: 1, exit_code: ok ? 0 : 1,
      reason: ok ? null : (timedOut ? "pi-timeout" : "pi-refresh-failed"),
      pi_version: version ?? null, pi_runtime: runtimeResult, sources,
      baseline, models_store: entries.has(PROVIDER) ? { [PROVIDER]: entries.get(PROVIDER) } : {},
      elapsed_ms: Math.round(performance.now() - started),
    });
  } finally {
    clearTimeout(timer);
    controller.abort();
    globalThis.fetch = originalFetch;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const result = await collectCatalog();
  process.stdout.write(JSON.stringify(result) + "\n");
  process.exitCode = result.exit_code;
}
