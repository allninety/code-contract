// Parity-audit Workflow skeleton (for the Workflow tool / multi-agent harness).
// Fan out one auditor per capability dimension, each reads BOTH trees, returns structured findings.
// Fill in BASE, NEW, and DIMENSIONS (derive the dimensions from the baseline's own modules — don't use a generic list).
// The caller synthesizes (root-cause clustering, doc, digest) from the returned findings.

export const meta = {
  name: 'parity-audit',
  description: 'Complete capability parity audit: baseline vs rewrite — one full, severity-ranked, evidence-backed gap list',
  phases: [{ title: 'Audit', detail: 'one auditor per dimension, read BOTH trees, compare line-by-line' }],
}

const BASE = '<absolute path to BASELINE src>'
const NEW = '<absolute path to NEW/rewrite src>'

const COMMON = `
You are auditing CAPABILITY PARITY between two implementations of the same product.
- BASELINE (the known-good / shipping standard): ${BASE}
- NEW (the rewrite/migration under audit):        ${NEW}
For YOUR dimension: read the ACTUAL code in BOTH trees, enumerate every baseline capability, check whether NEW matches.
The baseline is the reference standard — find what NEW is MISSING, only PARTIAL, or implements DIVERGENTLY.
RULES: cite file:line on BOTH sides (or '—' if missing); be exhaustive within your dimension; ground every item in
baseline code (don't invent capabilities the baseline lacks); list at-parity ('full') items too so coverage is visible.
status: full|partial|missing|divergent. severity: blocker(breaks delivery/wrong output)|major(visible gap)|minor|ok.`

const SCHEMA = {
  type: 'object',
  required: ['dimension', 'items'],
  properties: {
    dimension: { type: 'string' },
    items: {
      type: 'array',
      items: {
        type: 'object',
        required: ['capability', 'status', 'severity', 'baseRef'],
        properties: {
          capability: { type: 'string' },
          status: { type: 'string', enum: ['full', 'partial', 'missing', 'divergent'] },
          severity: { type: 'string', enum: ['blocker', 'major', 'minor', 'ok'] },
          baseRef: { type: 'string' },
          newRef: { type: 'string' },
          detail: { type: 'string' },
        },
      },
    },
  },
}

// Derive these from the baseline. Point each at the specific baseline+new files/symbols for that axis.
const DIMENSIONS = [
  { key: 'dimension-1', prompt: `${COMMON}\nDIMENSION: <name>. Baseline: <file/symbols>. New: <file/symbols>. <what to compare>.` },
  // ... ~8–15 dimensions total, covering the product with little overlap ...
]

phase('Audit')
const results = (await parallel(DIMENSIONS.map((d) => () =>
  agent(d.prompt, { label: `audit:${d.key}`, phase: 'Audit', schema: SCHEMA })
))).filter(Boolean)

const all = results.flatMap((r) => (r.items || []).map((it) => ({ dimension: r.dimension, ...it })))
const gaps = all.filter((it) => it.status !== 'full')
const bySev = (s) => gaps.filter((g) => g.severity === s)
return {
  capabilitiesChecked: all.length,
  atParity: all.length - gaps.length,
  gapCount: gaps.length,
  blockers: bySev('blocker'),
  major: bySev('major'),
  minor: bySev('minor'),
}
// Then (in the caller): cluster `gaps` by root cause, write the versioned doc, present the digest + fix order.
