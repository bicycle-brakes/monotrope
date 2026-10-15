// Runs scripts/stage2_research_tools.mjs against scripted cases, without Pi and
// without network. Used by tests/test_stage2_research_tools.py: reads one JSON
// request on stdin, writes one JSON answer per case on stdout.
//
// A case is one of:
//   { mode: "load" }                  — the extension as Pi loads it (fake host)
//   { mode: "load-without-host" }     — the extension where registerTool is absent
//   { mode: "handler", toolName }     — the tool_call gate of a loaded extension
//   { mode: "validate", url }         — the destination check alone
//   { mode: "private-ip", ip }        — the address classification
//   { mode: "fetch", url, transport } — a retrieval over a scripted transport
//   { mode: "search", query, transport }
//   { mode: "parse", html }           — the result parser
//
// A scripted transport is { lookups: [[ip, ...], ...], responses: [{status, location, body}, ...] }.
// Each call consumes the next entry, repeating the last one — so a redirect chain
// can be given a fresh lookup per hop, which is exactly what the extension must do.
import { pathToFileURL } from "node:url";

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const request = JSON.parse(Buffer.concat(chunks).toString("utf8"));
const extension = await import(pathToFileURL(request.module).href);

function fakeTransport(spec) {
  let lookupCall = 0;
  let getCall = 0;
  const seen = { lookups: [], gets: [] };
  return {
    seen,
    lookup: async (hostname) => {
      const entry = spec.lookups[Math.min(lookupCall++, spec.lookups.length - 1)];
      seen.lookups.push({ hostname, addresses: entry });
      return entry;
    },
    get: async (options) => {
      const entry = spec.responses[Math.min(getCall++, spec.responses.length - 1)];
      seen.gets.push(options);
      return {
        statusCode: entry.status,
        headers: entry.location ? { location: entry.location } : {},
        resume() {},
        destroy() {},
        on(name, fn) {
          if (name === "data") fn(Buffer.from(entry.body ?? ""));
          if (name === "end") fn();
        },
      };
    },
  };
}

const answers = [];
for (const item of request.cases) {
  let seen = null; // the transport's record, reported even when the case throws
  try {
    if (item.mode === "load" || item.mode === "load-without-host") {
      const tools = [];
      const handlers = [];
      const host = item.mode === "load" ? { registerTool: (t) => tools.push(t.name), on: (n) => handlers.push(n) } : {};
      extension.default(host);
      answers.push({ tools, handlers });
    } else if (item.mode === "handler") {
      const handlers = {};
      extension.default({ registerTool: () => {}, on: (n, h) => { handlers[n] = h; } });
      const result = await handlers.tool_call({ toolName: item.toolName, input: {} }, {});
      answers.push({ result: result === undefined ? null : result });
    } else if (item.mode === "validate") {
      const url = extension.validateDestination(item.url);
      answers.push({ ok: url.hostname });
    } else if (item.mode === "private-ip") {
      answers.push({ private: extension.isPrivateIp(item.ip) });
    } else if (item.mode === "fetch") {
      const deps = fakeTransport(item.transport);
      seen = deps.seen;
      const lines = [];
      const json = await extension.executeFetch(item.url, deps, (line) => lines.push(JSON.parse(line)));
      answers.push({ receipt: JSON.parse(json), receipts: lines, seen: deps.seen });
    } else if (item.mode === "search") {
      const deps = fakeTransport(item.transport);
      seen = deps.seen;
      const lines = [];
      const json = await extension.executeSearch(item.query, deps, (line) => lines.push(JSON.parse(line)));
      answers.push({ results: JSON.parse(json), receipts: lines });
    } else if (item.mode === "parse") {
      answers.push({ results: extension.parseResults(item.html) });
    } else {
      answers.push({ threw: `unknown mode ${item.mode}` });
    }
  } catch (error) {
    const threw = String((error && error.message) || error);
    answers.push(seen ? { threw, seen } : { threw });
  }
}
process.stdout.write(JSON.stringify(answers));
