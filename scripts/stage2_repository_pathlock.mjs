// The path lock of the swarm's repository seats (decisions.md Q-16, finding F-24).
//
// A repository seat reads the worktree with Pi's four read-only file tools
// (read, grep, find, ls). Those tools accept absolute paths, `..` and symbolic
// links, so a seat could read the model's home directory or the research state
// store (spec criterion 52). This extension is the ONLY one a repository seat
// loads, copied to a generic scratch path before loading. Its `tool_call` gate
// resolves every path argument — with `..` collapsed and symbolic links followed
// (realpath) — and blocks the call unless the result lies inside the worktree
// the seat was started in (its working directory). It is plain JavaScript, so
// the lock holds on every platform Pi runs on; no operating-system sandbox.
//
// Limits, stated: the lock checks the path a tool is called with, not what the
// tool then walks. A symbolic link INSIDE the worktree that points out is
// refused when named directly, but a directory walk (grep, find) does not
// follow links by default in Pi's backends (ripgrep, fd). A glob or search
// pattern is refused when it is absolute, begins with `~` or has a `..` segment.
//
// The pure helpers are exported so tests can drive them without Pi.
import { realpathSync } from "node:fs";
import path from "node:path";

const LOCKED_TOOLS = ["read", "grep", "find", "ls"];
const PATH_FIELDS = ["path"];
// The glob of grep's file filter and the glob pattern of find. A grep `pattern` is a regular expression, not a path.
const GLOB_FIELDS = { grep: ["glob"], find: ["pattern"], read: [], ls: [] };

// Resolves the longest existing prefix of `target` (following links) and
// re-appends the rest, so a path that does not exist yet is judged by where it
// would be created.
export function realTarget(target) {
  let existing = target;
  const rest = [];
  for (;;) {
    try {
      return path.join(realpathSync(existing), ...rest.reverse());
    } catch (error) {
      const parent = path.dirname(existing);
      if (parent === existing) throw error;
      rest.push(path.basename(existing));
      existing = parent;
    }
  }
}

function normalize(text) {
  // Pi strips a leading "@" and maps unicode spaces to a plain space.
  return String(text).replace(/[  -   　]/g, " ").replace(/^@/, "");
}

export function confinementError(rawPath, root) {
  if (typeof rawPath !== "string") return "the path must be a string";
  const text = normalize(rawPath);
  if (text.startsWith("~")) return `the path '${rawPath}' begins with ~, which names a home directory outside the worktree`;
  const realRoot = realTarget(root);
  let real;
  try {
    real = realTarget(path.resolve(root, text));
  } catch {
    return `the path '${rawPath}' cannot be resolved inside the worktree`;
  }
  const relative = path.relative(realRoot, real);
  const escapes = relative === ".." || relative.startsWith(".." + path.sep) || path.isAbsolute(relative);
  if (!escapes) return null;
  return `the path '${rawPath}' resolves outside the worktree: repository seats read only inside it`;
}

export function patternError(pattern) {
  if (typeof pattern !== "string") return null;
  const text = normalize(pattern);
  if (text.startsWith("~") || path.isAbsolute(text) || /^[a-zA-Z]:[\\/]/.test(text)) {
    return `the pattern '${pattern}' is absolute or begins with ~: repository seats search only inside the worktree`;
  }
  if (text.split(/[\\/]/).includes("..")) {
    return `the pattern '${pattern}' contains a '..' segment: repository seats search only inside the worktree`;
  }
  return null;
}

// The verdict for one tool call: null when allowed, else the reason.
export function gate(toolName, input, root) {
  if (!LOCKED_TOOLS.includes(toolName)) {
    return `the tool '${toolName}' does not exist in a repository seat: only read, grep, find and ls are available`;
  }
  const args = input && typeof input === "object" ? input : {};
  for (const field of PATH_FIELDS) {
    if (args[field] !== undefined && args[field] !== null) {
      const error = confinementError(args[field], root);
      if (error) return error;
    }
  }
  for (const field of GLOB_FIELDS[toolName]) {
    const error = patternError(args[field]);
    if (error) return error;
  }
  if (toolName === "read" && typeof args.path !== "string") return "read needs a path inside the worktree";
  return null;
}

export function registerPathLock(pi, root = process.cwd()) {
  if (!pi || typeof pi.on !== "function") {
    throw new Error("this extension needs a Pi host with on(); it refuses to load anywhere else");
  }
  pi.on("tool_call", async (event) => {
    const reason = gate(event && event.toolName, event && event.input, root);
    return reason === null ? undefined : { block: true, reason };
  });
}

export default function (pi) {
  registerPathLock(pi);
}
