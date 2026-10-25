const [tree, root] = process.argv.slice(2);
const lock = await import(`${tree}/scripts/stage2_repository_pathlock.mjs`);
const pu = await import(`${tree}/tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/tools/path-utils.js`);
const fs = await import("node:fs");
for (const p of ["notes’/secret.txt", "notes'/secret.txt"]) {
  const verdict = lock.gate("read", { path: p }, root);
  const resolved = pu.resolveReadPath(p, root);
  console.log(JSON.stringify(p), "lock:", verdict === null ? "ALLOWED" : "blocked", "| Pi reads:", resolved, "->", fs.existsSync(resolved) ? fs.readFileSync(resolved, "utf8").trim() : "(missing)");
}
