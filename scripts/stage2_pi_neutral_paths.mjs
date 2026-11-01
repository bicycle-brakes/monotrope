// The neutral-path extension of every model-calling Pi launch (bead coding-harness-xul8).
//
// Pi 1.2.0 builds its system prompt itself: every run's <cwd> section carries the
// process working directory and the <docs> section names absolute paths inside the
// pinned installation (dist/core/system-prompt.js, read 2026-10-29). No CLI flag
// removes either section, and the runner's leak check scans only the prompt text
// the runner composed, so it never sees them. Every covered launch (research
// repository and public/free seats, review-loop members, availability probes and
// the interactive session) therefore copies this file next to its other launch
// files and loads the copy explicitly with `-e`, discovery still disabled.
//
// What it does, in Pi's two supported hooks:
//   - before_agent_start: sets the prompt's working-directory option to the neutral
//     value "." and returns the rendered prompt with only its <docs> block removed.
//     Returning `systemPrompt` is Pi's full-prompt override; setting only a custom
//     preamble would also drop the generated tools and rules. The installation
//     paths the docs block names are harvested before it is removed, so the payload
//     scan below can remove them anywhere else too.
//   - before_provider_request: removes remaining location metadata from a copy of
//     the outgoing payload - context labels, tool arguments, tool results and tool
//     errors can carry absolute local paths the prompt does not. Returning the
//     copy replaces the outgoing payload; the original is untouched.
//
// It removes nothing else: instructions, tool declarations, the appended task and
// the session's project context travel unchanged beyond their location identifiers,
// and a repository-relative file reference is preserved (a bare basename is never
// replaced). The tools keep the real working directory; only what the model sees
// is neutral. The pure helpers are exported so tests run them without Pi.

import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// The model-visible working directory: it conveys relative-path use without
// pretending that a new absolute tool root exists.
export const NEUTRAL_CWD = ".";
export const FLAG = "stage2-neutral-paths";

// The three lines Pi renders into its <docs> block; each value is an absolute
// installation path. `(extensions, custom tools, SDK)` follows the examples path,
// which is why the capture stops at the first whitespace.
const DOCS_LINE = /^\s*-\s*(?:Main documentation|Additional docs|Examples):\s*(\S+)/gm;

// The directory of `path`: everything before its last separator.
export function parentOf(path) {
  const text = String(path);
  const cut = Math.max(text.lastIndexOf("/"), text.lastIndexOf("\\"));
  return cut > 0 ? text.slice(0, cut) : "";
}

// The absolute installation paths a rendered docs block names, each with its
// directory: the paths are enough in the block itself, the directory catches
// every other mention of the installation anywhere in the payload.
export function docsPaths(prompt) {
  const found = [];
  for (const match of String(prompt ?? "").matchAll(DOCS_LINE)) {
    const path = match[1];
    found.push(path, parentOf(path));
    // Pi's docs live below the pinned install's node_modules. Cover the install
    // root itself too, rather than only the README/docs/examples directories.
    const install = path.search(/[\\/]node_modules[\\/]/);
    if (install > 0) found.push(path.slice(0, install));
  }
  return found;
}

// Only the <docs>…</docs> block is removed; preamble, tools and rules survive.
export function stripDocsBlock(prompt) {
  return String(prompt ?? "").replace(/\n*<docs>[\s\S]*?<\/docs>/g, "");
}

// The forms one local prefix takes: native, and with every separator normalized
// to a slash. Longest first, so the most specific location is removed and a
// shorter prefix cannot leave a tail of a longer one behind.
export function prefixForms({ home = "", cwd = "", extras = [] }) {
  const one = [];
  for (const prefix of [cwd, home, ...extras]) {
    const text = String(prefix ?? "");
    if (!text) continue;
    one.push(text, text.replace(/\\/g, "/"));
  }
  const seen = new Set(one.filter((text) => text.length > 1));
  return [...seen].sort((left, right) => right.length - left.length);
}

// Remove a local prefix only at a token boundary and when followed by a path
// separator, a delimiter or the end of the text. A hit inside another path or URL stays
// untouched. Boundaries are read from the original text, so stripping one
// prefix cannot make a later embedded occurrence look like a new token.
export function replacePrefix(text, form) {
  const original = String(text);
  let out = "";
  let cursor = 0;
  for (;;) {
    const at = original.indexOf(form, cursor);
    if (at < 0) return out + original.slice(cursor);
    const after = at + form.length;
    const previous = original[at - 1];
    const next = original[after];
    const boundary = at === 0 || /[\s"'`([{=,;]/.test(previous);
    const separator = next === "/" || next === "\\";
    // A period ends a sentence only when it is not a filename continuation.
    const delimiter = next === undefined || /[\s"'`()[\]{},;:!?]/.test(next) ||
      (next === "." && (original[after + 1] === undefined || /[\s"'`)\]}]/.test(original[after + 1])));
    if (boundary && (separator || delimiter)) {
      out += original.slice(cursor, at);
      if (separator) cursor = after + 1;
      else {
        out += ".";
        cursor = after;
      }
    } else {
      out += original.slice(cursor, after);
      cursor = after;
    }
  }
}

export function redactText(text, forms) {
  let out = String(text ?? "");
  for (const form of forms) out = replacePrefix(out, form);
  return out;
}

// A copy of `payload` with every string redacted. Objects and arrays are rebuilt,
// so the caller's payload is never mutated; any other value passes through.
export function redactPayload(payload, forms) {
  if (typeof payload === "string") return redactText(payload, forms);
  if (Array.isArray(payload)) return payload.map((item) => redactPayload(item, forms));
  if (payload !== null && typeof payload === "object") {
    return Object.fromEntries(Object.entries(payload).map(([key, value]) => [key, redactPayload(value, forms)]));
  }
  return payload;
}

export function registerNeutralPaths(pi, { home = process.env.HOME ?? "", cwd = process.cwd() } = {}) {
  if (!pi || typeof pi.on !== "function") throw new Error("stage2 neutral paths: no Pi extension API to register on");
  const configuredAgent = process.env.PI_CODING_AGENT_DIR || `${home}/.pi/agent`;
  const agent = configuredAgent.replace(/^~(?=[/\\]|$)/, () => home);
  // Each builder loads a private scratch copy. Its directory is a location in
  // its own right, even when HOME and the agent are distinct child directories.
  const scratch = dirname(fileURLToPath(import.meta.url));
  const agentPath = resolve(agent);
  // RPC/session captures can put the copies in a private child of the scratch
  // root. Sibling HOME/agent directories identify that root without treating
  // an ambient user's home parent as a scratch directory.
  const sharedRoot = home && dirname(resolve(home)) === dirname(agentPath) ? dirname(agentPath) : "";
  const harvested = new Set();
  const forms = () => prefixForms({ home, cwd, extras: [agentPath, scratch, sharedRoot, ...harvested] });
  pi.on("before_agent_start", (event) => {
    if (event.systemPromptOptions && typeof event.systemPromptOptions === "object") {
      event.systemPromptOptions.cwd = NEUTRAL_CWD;
    }
    const rendered = event.systemPrompt;
    for (const path of docsPaths(rendered)) harvested.add(path);
    return { systemPrompt: stripDocsBlock(rendered) };
  });
  pi.on("before_provider_request", (event) => redactPayload(event.payload, forms()));
}

export default function (pi) {
  // Listed by `pi --help` when this file is loaded: how the runner confirms the load.
  pi.registerFlag(FLAG, {
    description: "stage2 neutral paths: local machine locations stay out of the outgoing request",
    type: "boolean",
    default: true,
  });
  registerNeutralPaths(pi);
}
