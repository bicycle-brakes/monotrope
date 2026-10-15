// The public research tools of the swarm's free researchers (ADR 0018 draft).
//
// A free researcher runs in a fresh scratch context with every built-in local
// tool and discovery surface disabled; the ONLY extension loaded is this file,
// copied to a generic scratch path before loading (plans/changes/research-swarm/
// design.md). It exposes exactly two tools — public search and page retrieval —
// and blocks every other tool call, built-ins included. Destinations must be
// HTTPS, credential-free and public: every DNS result is checked, the connection
// is pinned to a validated address, and every redirect is re-validated with a
// fresh lookup, so a private address cannot enter through a redirect or a
// rebinding lookup. Web content is data; nothing here executes it.
//
// Source receipts (URL, final URL, status, title, retrieval time, excerpt,
// size) are appended as JSON lines to $STAGE2_PUBLIC_RECEIPTS; the runner
// validates public citations against them, never against a model's word.
//
// Search uses the DuckDuckGo HTML endpoint — no paid API, no new credential.
//
// The pure helpers are exported so tests can inject a scripted transport
// (tests/test_stage2_research_tools.py) and run without Pi and without network.
import https from "node:https";
import { appendFileSync } from "node:fs";
import { lookup as dnsLookup } from "node:dns/promises";

const MAX_REDIRECTS = 3;
const MAX_BYTES = 5 * 1024 * 1024;
const USER_AGENT =
  "research-swarm public researcher; retrieves public pages as data, no repository content";
const PUBLIC_TOOLS = ["public_search", "public_fetch"];

// --- destinations -------------------------------------------------------------------------------

// Address ranges that are never public: unspecified, this host, private,
// carrier-grade NAT, link-local, broadcast. Ordered [first address, bits].
const PRIVATE_V4 = [
  ["0.0.0.0", 8],
  ["10.0.0.0", 8],
  ["100.64.0.0", 10],
  ["127.0.0.0", 8],
  ["169.254.0.0", 16],
  ["172.16.0.0", 12],
  ["192.168.0.0", 16],
  ["255.255.255.255", 32],
];

function v4ToInt(text) {
  const parts = text.split(".");
  if (parts.length !== 4) return null;
  let value = 0;
  for (const part of parts) {
    const n = Number(part);
    if (!Number.isInteger(n) || n < 0 || n > 255) return null;
    value = value * 256 + n;
  }
  return value;
}

function isPrivateV4(ip) {
  const value = v4ToInt(ip);
  if (value === null) return true; // not a parseable v4 address — refuse it
  for (const [base, bits] of PRIVATE_V4) {
    const width = 32 - bits;
    if (width === 0 ? value === v4ToInt(base) : Math.floor(value / 2 ** width) === Math.floor(v4ToInt(base) / 2 ** width)) {
      return true;
    }
  }
  return false;
}

export function isPrivateIp(ip) {
  const lower = String(ip ?? "").toLowerCase();
  if (lower.startsWith("::ffff:")) return isPrivateV4(lower.slice(7)); // v4-mapped
  if (lower === "::" || lower === "::1") return true; // unspecified, loopback
  if (lower.startsWith("fc") || lower.startsWith("fd")) return true; // fc00::/7 unique local
  if (lower.startsWith("fe8") || lower.startsWith("fe9") || lower.startsWith("fea") || lower.startsWith("feb")) {
    return true; // fe80::/10 link-local
  }
  if (lower.includes(":")) {
    // Other IPv6: a well-formed hex-and-colon address past the private ranges
    // above is public; anything unparsable is refused as private.
    return !/^[0-9a-f:]+$/.test(lower);
  }
  return isPrivateV4(lower);
}

// Validates one destination: HTTPS only, no embedded credentials, port 443,
// a public hostname. Throws with the reason; the message travels to the
// researcher and the audit, so it states the rule, not the fix.
export function validateDestination(raw) {
  if (typeof raw !== "string" || !raw.trim()) throw new Error("a destination URL is required");
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new Error("the destination is not a valid URL");
  }
  if (url.protocol !== "https:") throw new Error("only https:// destinations are fetched — no http, no file");
  if (url.username || url.password) throw new Error("destinations with embedded credentials are refused");
  if (url.port && url.port !== "443") throw new Error("only port 443 is fetched");
  if (!url.hostname) throw new Error("the destination has no host");
  if (url.hostname === "localhost" || url.hostname.endsWith(".localhost") || url.hostname.endsWith(".local")) {
    throw new Error("local host names are refused");
  }
  return url;
}

// --- transports ---------------------------------------------------------------------------------

// The transport the tools use under Pi: real DNS, real TLS. `get` pins the
// connection to the pre-validated address by overriding the agent's lookup,
// so the certificate and SNI still name the requested host.
export function nodeTransport() {
  return {
    lookup: async (hostname) => (await dnsLookup(hostname, { all: true, verbatim: true })).map((r) => r.address),
    get: ({ url, pinnedIp, headers }) =>
      new Promise((resolve, reject) => {
        const request = https.get(
          url,
          {
            lookup: (_host, _options, callback) => callback(null, pinnedIp, 4),
            headers,
            timeout: 20000,
          },
          resolve,
        );
        request.on("error", reject);
        request.on("timeout", () => request.destroy(new Error("the request timed out")));
      }),
  };
}

// Resolves a host and checks every address. Returns the first public address
// to pin the connection to.
async function validatedAddress(hostname, deps) {
  const addresses = await deps.lookup(hostname);
  if (!Array.isArray(addresses) || addresses.length === 0) {
    throw new Error(`the lookup of ${hostname} returned no address`);
  }
  for (const address of addresses) {
    if (isPrivateIp(address)) {
      throw new Error(`the lookup of ${hostname} returned the private address ${address} — refused`);
    }
  }
  return addresses[0];
}

function readBody(response) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    response.on("data", (chunk) => {
      size += chunk.length;
      if (size > MAX_BYTES) {
        response.destroy(new Error("the page exceeds the size limit"));
        reject(new Error("the page exceeds the size limit"));
        return;
      }
      chunks.push(chunk);
    });
    response.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    response.on("error", reject);
  });
}

// Retrieves one page. Every hop re-validates the destination and resolves it
// anew, so a redirect cannot smuggle in a private address and a rebinding
// lookup cannot swap one in after the check.
export async function fetchPage(raw, deps, depth = 0) {
  const url = validateDestination(raw);
  const pinnedIp = await validatedAddress(url.hostname, deps);
  const response = await deps.get({
    url,
    pinnedIp,
    headers: { host: url.hostname, "user-agent": USER_AGENT, accept: "text/html" },
  });
  const status = response.statusCode;
  const location = response.headers && (response.headers.location || "");
  if ([301, 302, 303, 307, 308].includes(status)) {
    if (depth >= MAX_REDIRECTS) throw new Error(`more than ${MAX_REDIRECTS} redirects`);
    response.resume();
    return fetchPage(new URL(location, url).href, deps, depth + 1);
  }
  if (status !== 200) {
    response.resume();
    throw new Error(`the page answered ${status}, not 200`);
  }
  const body = await readBody(response);
  return { finalUrl: url.href, status, body };
}

// --- search -------------------------------------------------------------------------------------

const ENTITIES = { "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#x27;": "'", "&#39;": "'" };

function unescapeText(text) {
  return text.replace(/&(?:amp|lt|gt|quot|#x27|#39);/g, (m) => ENTITIES[m] || m);
}

// Parses the DuckDuckGo HTML answer: result anchors of the class `result__a`.
export function parseResults(html) {
  const results = [];
  const pattern = /<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g;
  for (const match of html.matchAll(pattern)) {
    const snippetMatch = /<a[^>]*class="result__snippet"[^>]*>([\s\S]*?)<\/a>/.exec(html.slice(match.index, match.index + 2000));
    results.push({
      title: unescapeText(match[2].replace(/<[^>]*>/g, "")).trim(),
      url: unescapeText(match[1]).trim(),
      snippet: snippetMatch ? unescapeText(snippetMatch[1].replace(/<[^>]*>/g, "")).trim() : "",
    });
  }
  return results;
}

export async function searchWeb(query, deps) {
  const url = validateDestination(
    `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`,
  );
  const page = await fetchPage(url.href, deps);
  return parseResults(page.body);
}

// --- receipts -----------------------------------------------------------------------------------

function receiptPath() {
  const path = process.env.STAGE2_PUBLIC_RECEIPTS;
  if (!path) throw new Error("STAGE2_PUBLIC_RECEIPTS is not set — no receipt, no retrieval");
  return path;
}

function titleOf(body) {
  const match = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(body);
  return match ? unescapeText(match[1]).trim().slice(0, 300) : "";
}

export function recordReceipt(sink, receipt) {
  sink(`${JSON.stringify(receipt)}\n`);
}

// The full tool step: validate, retrieve, record the receipt, return JSON.
export async function executeFetch(raw, deps, sink = (line) => appendFileSync(receiptPath(), line)) {
  const page = await fetchPage(raw, deps);
  const receipt = {
    kind: "fetch",
    url: raw,
    final_url: page.finalUrl,
    status: page.status,
    title: titleOf(page.body),
    retrieved: new Date().toISOString(),
    excerpt: page.body.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim().slice(0, 400),
    bytes: Buffer.byteLength(page.body),
  };
  recordReceipt(sink, receipt);
  return JSON.stringify(receipt);
}

export async function executeSearch(query, deps, sink = (line) => appendFileSync(receiptPath(), line)) {
  const results = await searchWeb(query, deps);
  const receipt = {
    kind: "search",
    url: `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`,
    final_url: `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`,
    status: 200,
    title: "",
    retrieved: new Date().toISOString(),
    excerpt: JSON.stringify(results).slice(0, 400),
    bytes: results.length,
  };
  recordReceipt(sink, receipt);
  return JSON.stringify(results);
}

// --- the extension Pi loads ---------------------------------------------------------------------

export default function (pi) {
  if (!pi || typeof pi.registerTool !== "function") {
    throw new Error("this extension needs a Pi host with registerTool; it refuses to load anywhere else");
  }
  pi.registerTool({
    name: "public_search",
    description: "Search the public web with a query. Records a source receipt. No local access exists.",
    parameters: { query: "string" },
    execute: async ({ query }) => executeSearch(query, nodeTransport()),
  });
  pi.registerTool({
    name: "public_fetch",
    description: "Retrieve one public https page. Records a source receipt. No local access exists.",
    parameters: { url: "string" },
    execute: async ({ url }) => executeFetch(url, nodeTransport()),
  });
  pi.on("tool_call", async (event) => {
    const name = event && event.toolName;
    if (PUBLIC_TOOLS.includes(name)) return undefined;
    return {
      block: true,
      reason:
        `the tool '${name}' does not exist in a free researcher context: only ` +
        "public_search and public_fetch are available, and every file, shell and " +
        "network tool is blocked at the extension boundary",
    };
  });
}
