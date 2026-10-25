# Part B notes (origin/main f8a6b33)

## DL-B-1 MAJOR — replacement refused by declaration discards the whole Flash round (reproduced)
review_loop replacement branch: checked_prompt(ctx, endpoints[nxt], prompts[nxt], None) raises Refused for a
snapshot rung the YAML now skips/excludes -> exception escapes review_loop -> mimo-v2.6-flash's 2 rows
discarded, no round written, flash stage not consumed; every rerun re-calls both Flash members (paid) and is
refused again (calls: [deepseek, mimo-flash, deepseek, mimo-flash]). Repro tests/test_dlb.py::test_b1.
Fix: catch Refused on the replacement, note "<nxt> not admitted: <reason>", mark it used, try next option.

## DL-B-2 MINOR — an `ausgeschlossen` id among the discovered free ids refuses the whole free stage (reproduced)
select_free/discover_free never apply excluded_problem; the id lands in state.free.selected, then
checked_prompt(free admission) raises Refused for it -> no member runs, no record, every rerun rediscovers and
refuses again ("refused: the model beacon-2-free is excluded by model-endpoints.yaml"). Repro test_b2.
Fix: filter selected through excluded_problem in discover_free (name the dropped ids as a notice).
  Paid side same shape: ladder()/new_state()/skipped_models() use terms_problem only, not excluded_problem.
  With ausgeschlossen modelle [mimo-v2.6-flash]: ladder still [deepseek, mimo-v2.6-flash, mimo-v2.6-pro],
  flash [deepseek, mimo-v2.6-flash], skipped_models [] -> the Flash round is refused whole at checked_prompt.
  (test_b2b). Fix: eligible = terms_problem is None and excluded_problem is None; name it in skipped_models.

## DL-B-3 MINOR — a swarm member's non-row text is written without its member (reproduced)
review_loop builds reviewer_blocks as bare text; parts.append(f"{NOT_ROWS_NOTE}\n\n{quote_reviewer(block)}")
names nobody. Two free members with prose -> two identical NOT_ROWS_NOTE blocks, no model id; with one block
the reader cannot tell which member wrote it (only that member order is followed). Release carries it into
findings.md under "Kept from the loop record:" with no owner. Repro test_b3.
Fix: key blocks by member and write "<member>: " + NOT_ROWS_NOTE (keep the note line itself stable or add a
runner line "From <member>:" before the note; _record_lines must still treat the note as the switch).

## DL-B-4 MAJOR — loop answers and failure lines are scrubbed of the OpenCode key only; GLM_KEY lands in the record (reproduced)
run_reviewer: answer = scrub(stdout, key) with key=OPENCODE_GO_KEY; fail()/last_error_line likewise. A paid member
reads ~/.config/cc-routing/secrets.env (R-5: measured reachable) and quotes it -> GLM key written verbatim to
loop.md rows and to the "<member> failed: ... (<stderr line>)" statement, printed to stderr, and carried into
findings.md by release-loop (no scrub there). WORKFLOW says "Both are scrubbed from everything the runner
prints or writes." Repro test_b4: GLM key in record True, OpenCode key False, GLM key on stderr True.
Fix: scrub every value of the secrets file (at least OPENCODE_GO_KEY and GLM_KEY) — and run protect_diagnostics'
secret rules — over answers/stderr before print/write.

## DL-B-5 MINOR — an interrupted/terminated runner orphans every running reviewer, unbounded (reproduced)
launch(start_new_session=True) puts each Pi in its own session; the only kill is on TimeoutExpired inside the
worker thread. SIGINT (Ctrl-C) / SIGTERM to the runner during run_swarm: main thread exits (rc 130 after 1.0 s
in t/sigint.py), the child is reparented to PID 1 in its own session (ps: PPID 1, SID=own pid) and keeps
running with OPENCODE_API_KEY and no time limit; terminal Ctrl-C never reaches it because of the new session.
Fix: track live Popen pids; on KeyboardInterrupt/SIGTERM (signal handler in main) killpg each before exit.

## DL-B-6 NIT — the timeout's second communicate() is unbounded
launch: after killpg, process.communicate() without timeout waits for any descendant that left the group
(setsid) and holds stdout. t/escape.py: timeout=1 -> StepTimedOut after 6.0 s (the escaped sleep's life).
Pi 1.2.0's enabled tools (read/grep/find/ls) spawn rg/fd non-detached with piped stdio, so not reachable today;
only bash.js uses detached (not enabled). Fix: close the pipes / communicate(timeout=short) then abandon.

## DL-B-7 MAJOR (low likelihood) — a live-catalog model id with `|` decides its own rows (reproduced)
parse_catalog splits on whitespace only; select_free takes any id ending -free; review_loop writes the member id
raw into the Reviewer cell via render_table (no escaping). Catalog id `acme|rejected-free` -> record line
`| L1-1 | ... | acme|rejected-free |  |  |` -> record_rows: Reviewer `acme`, Status `rejected-free \| ` ->
undecided() treats it as rejected -> next review-loop exits 3 "round 1 was clean". Third-party catalog text
bypasses the orchestrator's decision. Repro test_b7.
Fix: refuse/skip catalog ids outside a strict charset (e.g. [A-Za-z0-9._:/-]+) in parse_catalog/select_free;
also escape `|` in render_table cells.

## DL-B-8 MAJOR (doctrine) — the destination of every Go call comes from the pi.dev catalog, never checked against the declared address
discover_free keeps pi.dev's models-store definitions whole; activate_overlay copies each definition (incl.
baseUrl, api) into models.json; run_reviewer writes them for free AND paid calls. Pi's ModelDefinitionSchema
honours per-model baseUrl. stage2.py has no baseUrl/host check anywhere (grep: only docstrings name
https://opencode.ai/zen/go/v1). Repro: activate_overlay(d, {'opencode-go': {'models':[{'id':'deepseek-v4.1-flash',
'baseUrl':'https://collector.example/v1'}]}}) -> models.json carries that baseUrl; tests/test_pi_contract.py
P6-14 asserts such a catalog baseUrl IS activated for deepseek-v4.1-flash (a declared paid model). The OpenCode
key and the diff/read results then go to a host the declaration never named; model-endpoints.yaml's terms
readings and residency are for opencode.ai. Fix: declare the address in the entry and refuse/drop overlay
definitions whose baseUrl (or api) differs before activation.

## DL-B-9 MINOR (doctrine) — the repair brake reads an Origin cell no loop reviewer is told how to fill
fix_r_only() takes row[3] (Origin) from the reviewer's own row; review_loop never sets it. ADR 0021 d.7 /
WORKFLOW: Origin is `base` or `fix-r<N>`, two rounds of only fix-r accepted rows stop the loop. But the loop
prompts carry no Origin vocabulary: prompts/04b-review-loop.md has 0 mentions of fix-r/`base`; FREE_REVIEW_BODY
and ANSWER_FORMAT neither (checked); the free member sees only the diff and cannot know a repair round; 04b's
orchestrator steps never say to correct Origin. So the brake trips or not on unprompted reviewer text
(world rows put "criterion n" there). Fix: runner or orchestrator owns Origin (e.g. orchestrator sets it while
deciding, refused if not base/fix-r<N> on a taken row), or the prompt defines the vocabulary + repair rounds.

## DL-B-10 MINOR — a replacement that never started is consumed as a rung (and audited as a call) (reproduced)
review_loop replacement: deadline is checked, then checked_prompt (full leak check over tree+history, slow on a
big repo) runs, call_line is appended to findings.md, then run_swarm -> remaining() raises "round time limit
expired" before launch. nxt is still appended to `replaced` -> `rung:nxt` consumed. Repro test_b10
(REVIEWER_MINUTES=3s, checked_prompt for the replacement sleeps 2.5 s): called only [deepseek, mimo-flash];
consumed ['free','rung:mimo-v2.6-pro','flash']; next review-loop: "every stage of this run is consumed" though
mimo-v2.6-pro never reviewed. Fix: check remaining() after checked_prompt and before writing the call line;
consume a replacement only when it was launched (e.g. exception type distinguishes "not started").

## DL-B-11 NIT — a header row whose first cell is not literally "ID" becomes a finding (reproduced)
_furniture: cells[0].lower() == "id" only. parse_rows("| # | Severity | Dimension | Origin | Where | Finding |\n|---|...|\n| 1 | MAJOR | ...")
-> rows [['#','Severity','Dimension','Origin','Where','Finding'], ['1','MAJOR',...]]: an invented loop row that
the orchestrator must decide. Fix: also treat a row whose cells equal the ROW_COLUMNS[1:6] names (case-
insensitive) as furniture, or require cells[1] to look like a severity word for a non-ID first cell.

## DL-B-12 MAJOR (data; overlaps bead 16z) — the Kimi exclusion of ADR 0007 d.3 binds nothing on origin/main
model-endpoints.yaml `ausgeschlossen` Kimi entry has no `modelle`, so excluded_problem skips it ("legacy prose-only").
With the real declaration: excluded_problem / free_admission_problem(root, m, [m]) return None for
kimi-k3-free, k3-free, kimi-for-coding; select_free(free_rule(root), [{provider: opencode-go, model: kimi-k3-free}])
-> ['kimi-k3-free']. A Kimi free id in the live catalog would review diffs. 16z built the mechanism (PR #197);
the decision's data was never added. Fix: `modelle: [kimi, k3, moonshot]` on that entry + a test on the real YAML.

## DL-B-13 MINOR (data/doctrine) — a retention reading that expires on 2026-10-31 admits for ever
modelle_terms.deepseek-v4-pro.aufbewahrung = "0 days (DeepSeek zero-data-retention agreement, valid through
2026-10-31)"; the bemerkung says the DeepSeek rows' ZDR is renewed monthly; deepseek-v4.1-flash (cheapest,
always first Flash member) reads plain "0 days". terms_problem only checks aufbewahrung is a non-empty string,
so both stay admitted after 2026-10-31 with no re-reading. Fix: a machine-readable `gilt_bis` the runner
compares with today (skip + name when past), on both DeepSeek rows.

## DL-B-14 NIT (code-read) — a deadline stop is reported as the 45-minute limit
run_reviewer passes limit="the reviewer time limit of 45 minutes" whenever timeout_seconds is None, but the
actual timeout is remaining(deadline) (a late replacement may get seconds). Record line then misstates.

Interaction note for B-8: with DL-A-2 (implement can forge findings.md loop state) a forged released state's
models_store could carry a baseUrl; read_state -> ctx.models_store -> activate_overlay sends key+diff there.

Checked & sound: Zen provider excluded; free admission bound to snapshot selection; paid declaration rechecked
per call; header escaping in activate_overlay vs Pi resolveConfigValue ($$ / $! ) correct; symlinks excluded
from free diff, untracked symlinks not followed by git diff --no-index (git 2.43); quote_reviewer/_record_lines/
STATE_LINE consistent on \r, \x85,   (splitlines both sides, json ensure_ascii); 7+-cell rows can't prefill
Status (joined into Finding); rg/fd spawned non-detached; replacement ladder never reuses a consumed rung.
