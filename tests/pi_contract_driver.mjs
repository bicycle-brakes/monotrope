// The driver of the offline Pi contracts (ADR 0019).
//
// Two modes:
//  - Loaded by the installed Pi as an extension (`-e <this file>`): registers
//    one custom tool, `contract-echo`, through the installed Pi's own
//    extension API - no mock stands in for it. Its execute() logs the
//    structured input it received and returns a fixed structured result, so
//    the suite can check both ends of the real tool exchange.
//  - Run directly by the suite (`node --import pi_network_guard.mjs
//    <this file> network-guard <loopback-url>`): planted connection attempts
//    under the preloaded guard; prints one JSON line per attempt. The
//    external targets are reserved/unresolvable names, so even a broken guard
//    would reach no real destination.

import fs from "node:fs";
import http from "node:http";
import net from "node:net";
import tls from "node:tls";

export const ECHO_PREFIX = "echo:";

export default function main(pi) {
  if (typeof pi?.registerTool !== "function") {
    throw new Error(
      "contract driver: the installed Pi exposes no registerTool; the extension contract cannot be measured",
    );
  }
  pi.registerTool({
    name: "contract-echo",
    label: "Contract echo",
    description: "Test tool of the offline Pi contracts: echoes its structured input back.",
    parameters: {
      type: "object",
      properties: {
        sentence: { type: "string" },
        count: { type: "number" },
        deep: {
          type: "object",
          properties: { nested: { type: "boolean" } },
          required: ["nested"],
        },
      },
      required: ["sentence", "count", "deep"],
    },
    // The installed Pi's declared signature (types.d.ts, ToolDefinition.execute):
    // execute(toolCallId, params, signal, onUpdate, ctx) -> { content, details }.
    async execute(_toolCallId, args) {
      const log = process.env.CONTRACT_ECHO_LOG;
      if (!log) throw new Error("contract driver: CONTRACT_ECHO_LOG is not set");
      fs.appendFileSync(log, `${JSON.stringify(args)}\n`);
      const result = `${ECHO_PREFIX}${args.sentence}:${args.count}:${JSON.stringify(args.deep)}`;
      return { content: [{ type: "text", text: result }], details: { echoed: true } };
    },
  });
}

// --- the network-guard self test: planted attempts, no real destination ---

function verdict(name, error) {
  const message = String(error?.message ?? error);
  const outcome = message.includes("pi-network-guard") ? "denied" : `other: ${message}`;
  return { attempt: name, outcome };
}

function attempt(name, fn) {
  try {
    return fn().then(
      () => ({ attempt: name, outcome: "allowed" }),
      (error) => verdict(name, error),
    );
  } catch (error) {
    return Promise.resolve(verdict(name, error));
  }
}

async function networkGuard(baseUrl) {
  return Promise.all([
    attempt("loopback-fetch", () => fetch(baseUrl)),
    attempt("external-fetch", () => fetch("https://opencode-go.invalid/zen/go/v1")),
    attempt(
      "external-http",
      () =>
        new Promise((resolve, reject) => {
          http.get("http://example.invalid/", (response) => resolve(response)).on("error", reject);
        }),
    ),
    attempt(
      "external-net",
      () =>
        new Promise((resolve, reject) => {
          const socket = net.connect({ host: "192.0.2.1", port: 443 }); // TEST-NET-1, never routed
          socket.on("ready", () => resolve(socket));
          socket.on("error", reject);
        }),
    ),
    attempt(
      "external-tls",
      () =>
        new Promise((resolve, reject) => {
          const socket = tls.connect({ host: "example.invalid", port: 443 });
          socket.on("secureConnect", () => resolve(socket));
          socket.on("error", reject);
        }),
    ),
  ]);
}

// Only when node runs this file directly; when Pi loads it as an extension,
// argv[1] is Pi's own entry, not this file.
if (process.argv[1]?.endsWith("pi_contract_driver.mjs") && process.argv[2] === "network-guard") {
  const lines = await networkGuard(process.argv[3] ?? "http://127.0.0.1:9/");
  for (const line of lines) console.log(JSON.stringify(line));
}
