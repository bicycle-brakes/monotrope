// Test-only network guard of the offline Pi contracts (ADR 0019).
//
// Preloaded with `node --import <this file>`, it denies every non-loopback
// connection attempt before it is made: fetch, http, https, net and tls. The
// contracts reach the loopback stand-in on 127.0.0.1 only; anything else
// throws. This file is never preloaded by production code, and its denials
// are proven with planted attempts (tests/pi_contract_driver.mjs), never with
// a real outbound request.

import http from "node:http";
import https from "node:https";
import net from "node:net";
import tls from "node:tls";

const GUARD = "pi-network-guard";
const LOOPBACK = new Set(["127.0.0.1", "::1", "localhost"]);

function hostText(value) {
  return String(value ?? "").trim().replace(/:\d+$/, "");
}

function targetHost(target, options) {
  try {
    if (target instanceof URL) return hostText(target.hostname);
    if (typeof target === "string") return hostText(new URL(target).hostname);
    if (typeof target === "object" && target !== null && typeof target.url === "string") {
      return hostText(new URL(target.url).hostname); // a fetch(Request)
    }
    if (typeof target === "number") return hostText(options); // net.connect(port, host)
    return hostText(target?.hostname ?? target?.host ?? options?.hostname ?? options?.host);
  } catch {
    return "unparseable";
  }
}

function deny(kind, target, options) {
  const host = targetHost(target, options);
  if (host === "" || LOOPBACK.has(host)) return;
  throw new Error(`${GUARD}: ${kind} to ${host} is denied; the offline contracts reach the loopback only`);
}

const rawFetch = globalThis.fetch;
globalThis.fetch = (input, init) => {
  deny("fetch", input, init);
  return rawFetch(input, init);
};

const PATCHES = [
  [http, "http", ["request", "get"]],
  [https, "https", ["request", "get"]],
  [net, "net", ["connect", "createConnection"]],
  [tls, "tls", ["connect"]],
];

for (const [mod, kind, names] of PATCHES) {
  for (const name of names) {
    const original = mod[name];
    mod[name] = (...args) => {
      deny(`${kind}.${name}`, args[0], args[1]);
      return original.apply(mod, args);
    };
  }
}
