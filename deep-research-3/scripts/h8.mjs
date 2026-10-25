const [tree, root] = process.argv.slice(2);
const lock = await import(`${tree}/scripts/stage2_repository_pathlock.mjs`);
const pu = await import(`${tree}/tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/tools/path-utils.js`);
for (const [tool, input] of [["read", { path: "/etc/hostname" }], ["read", { path: "file:///etc/hostname" }], ["ls", { path: "file:///etc" }], ["grep", { pattern: "root", path: "file:///etc" }], ["find", { pattern: "*", path: "file:///root" }]]) {
  const v = lock.gate(tool, input, root);
  console.log(tool, JSON.stringify(input), "lock:", v === null ? "ALLOWED" : "blocked", "| Pi resolves to:", pu.resolveToCwd(input.path, root));
}
