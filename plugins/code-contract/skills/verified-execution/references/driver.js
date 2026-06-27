// verified-execution DRIVER — a Workflow skeleton that auto-runs the harness loop over many items,
// so you DON'T drive N cycles by hand. The workflow orchestrates; the AGENTS call harness.py via Bash
// (the workflow JS is sandboxed and can't touch the filesystem). The human reads `status` / `gate` after.
//
// Prereq: the contract is populated. Either `harness.py import items.jsonl` first, or do it in a Phase 0
// agent that reads the source (e.g. a parity-audit gap doc) and emits one {id,title,ref,dod} per line,
// then `harness.py import` that file.

export const meta = {
  name: 'verified-execution-driver',
  description: 'Auto-close a contract of work items: per item, worker implements then an INDEPENDENT verifier gates it',
  phases: [{ title: 'Close', detail: 'per item: worker → independent verifier → harness verdict' }],
}

const HARNESS = 'python3 ~/.claude/skills/verified-execution/scripts/harness.py'   // agents call this via Bash
const REPO = '<absolute repo path>'
// Items to process. In real use, read these from the contract (the agent runs `harness.py status`/reads
// .harness/contract.jsonl) or pass them in via `args`. Each needs id + DoD + the spec/baseline ref.
const ITEMS = args && args.length ? args : [
  // { id: 'G1', title: '...', ref: 'baseline file:line', dod: 'observable test' },
]

const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'evidence'],
  properties: { verdict: { type: 'string', enum: ['PASS', 'FAIL'] }, evidence: { type: 'string' } },
}

phase('Close')
// pipeline = each item flows worker→verifier independently, no barrier between items (fast).
const results = await pipeline(
  ITEMS,
  // STAGE 1 — worker: implement the MINIMAL change, then log a claim. isolation:'worktree' so parallel
  // real edits don't collide. The worker may NOT mark itself done.
  (item) => agent(
    `In ${REPO}, you are the implementer for ONE item. Make the MINIMAL change to satisfy it, then run:\n` +
    `  ${HARNESS} claim ${item.id} "<what you changed: file:line>" --by worker\n` +
    `Item ${item.id}: ${item.title}\nBaseline/spec ref (the standard): ${item.ref}\nDefinition of done: ${item.dod}\n` +
    `Return the exact diff you made (files + line ranges). Do NOT claim it works — that's the verifier's call.`,
    { label: `worker:${item.id}`, phase: 'Close', isolation: 'worktree' }
  ).then((diff) => ({ item, diff })),

  // STAGE 2 — INDEPENDENT verifier (the teeth): fresh context, adversarial, reads REAL code + runs the DoD,
  // then records the verdict itself via harness.py. Give it the contract item + the raw diff, NOT a narrative.
  (prev, item) => agent(
    `You are an INDEPENDENT verifier with NO prior context. ASSUME item ${item.id} is NOT done until the real ` +
    `code/output proves it. Do NOT trust the implementer.\n` +
    `Item: ${item.title}\nBaseline/spec ref (the standard): ${item.ref}\nDefinition of done (run/observe it): ${item.dod}\n` +
    `Raw diff the implementer made:\n${(prev && prev.diff || '(none)').slice(0, 4000)}\n` +
    `Read ${REPO} yourself, RUN or OBSERVE the DoD, and decide. Then record your verdict (--by verifier, distinct from\n` +
    `the worker, so the harness's self-certification guard stays satisfied):\n` +
    `  ${HARNESS} verdict ${item.id} PASS|FAIL "<concrete observed evidence>" --dod ${JSON.stringify(item.dod)} --by verifier\n` +
    `Return {verdict, evidence}. PASS only if YOU independently confirmed the DoD holds.`,
    { label: `verify:${item.id}`, phase: 'Close', schema: VERDICT_SCHEMA }
  ).then((v) => ({ id: item.id, verdict: v && v.verdict, evidence: v && v.evidence })),
)

const done = results.filter(Boolean)
// NOTE: this is a SINGLE pass (no automatic retry). FAIL items are reopened in the ledger but not re-worked
// here — re-invoke the driver with the failed IDs (or add a while-loop on `failed`) to close them.
return {
  processed: done.length,
  passed: done.filter((r) => r.verdict === 'PASS').length,
  failed: done.filter((r) => r.verdict === 'FAIL').map((r) => r.id),
  // After this returns: run `harness.py status` and `harness.py gate` (gate exits non-zero if any item
  // isn't VERIFIED). The human reads status + spot-checks a sample. THAT is the final gate.
}
