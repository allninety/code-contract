---
name: parity-audit
description: >-
  Run a COMPLETE capability-parity audit comparing a known-good BASELINE (the old / currently-shipping system) against
  a REWRITE, MIGRATION, PORT, or REFACTOR — surfacing EVERY gap at once (missing / partial / divergent behaviors),
  with file:line evidence on both sides, severity-ranked and grouped by ROOT CAUSE, instead of one at a time. Use when
  migrating or rewriting a working system and you need to know what the new version still does not match, when the new
  build still doesn't do what the old one did or feels behind, when gaps surface piecemeal, when porting across
  engines / frameworks / languages / platforms, or before declaring a rewrite delivery-ready. Also trigger on: feature
  parity, regression sweep, compare old vs new, what did we lose in the rewrite, migration-completeness check, did the
  port miss anything, or auditing a fork/clone against upstream. Prefer this over an ad-hoc read-through when a
  trustworthy reference exists — one exhaustive map, not a lucky spot-check.
license: MIT
metadata:
  version: 0.1.0
---

# Parity Audit

## What this is for

A rewrite, migration, port, or refactor almost always **silently loses things the original did** — a control that no
longer affects output, a duration that gets clamped differently, an export option that became a no-op. The original
("baseline") often encodes *days of tuning* that don't transfer for free. The expensive failure mode is discovering
those losses **one at a time**, over weeks, each as a fresh surprise ("oh, that's missing too?"). That erodes trust and
makes the work feel bottomless.

This skill produces the opposite: **one exhaustive, evidence-backed, severity-ranked, root-cause-grouped gap list**, so
the full scope is on the table at once and the remaining work is *scoped, not dribbled*. It also collapses a scary-looking
pile of gaps (e.g. "88 findings") into a handful of root fixes (e.g. "6 causes; the biggest one fix kills ~half").

## The core idea

The baseline is the **standard of truth**. The job is to find every place the new implementation **fails to match it** —
and to do it by *reading the actual code on both sides*, not by trusting either side's docs or your memory. The value
comes from three things, in order: **coverage** (no dimension left unchecked), **evidence** (file:line on both sides, or
it isn't a finding), and **synthesis** (N scattered findings → a few root causes).

## This skill is the COMPARE engine — freeze the spec with `product-contract`
parity-audit is the **depth/evidence** half of a pair. Its job is to COMPARE an implementation against a reference and
emit the severity-ranked, file:line gap list. The *durable spec* — freezing one product's capabilities into a named,
owner↔code-traceable contract — is the **`product-contract`** skill's job (the structure half). They share one stable
atom-ID and compose; don't rebuild the contract here.

Two ways this audit starts:
- **Contract exists → audit against it (preferred).** Read the `product-contract` atom registry and audit
  **atom-by-atom** — the atoms ARE your checklist, their trace links point you at the target's code. Do NOT re-derive
  your own dimensions; re-derivation drift is exactly why two audits of one product disagree on granularity. Write each
  atom's per-target status + evidence to `audit-results/ATOM-STATUS-<target>.md` (keyed by atom-ID — never into the
  contract's dictionary `状态`, which is product-contract's single-product snapshot). If you find a real promise **no atom
  represents**, record it as a contract
  gap for the next `product-contract` pass — don't silently expand the audit universe. (Protocol: `product-contract`'s
  `references/three-skill-coordination.md`.)
- **No contract → derive the map yourself (cold start), then optionally bootstrap one.** Run the discovery below to build
  the dimensions/inventory. If a durable spec is wanted afterward, emit your audited capabilities (not just the gaps) as
  **draft atoms** for `product-contract` to normalize. This is also the "scope a migration before building it" move.

## When to run it (timing) + the one precondition
- **Mid/late in a migration** (primary mode) — when the new impl has *attempted* most features, so gaps are real
  divergence rather than "not built yet."
- **Early, to scope before building** — run just Phase 1 (inventory + dimensions) up front; the output is the checklist
  the rewrite must hit. For a *durable* up-front spec (named, traceable, reusable across runs), use `product-contract` to
  FREEZE it instead, then audit against that.
- **Recurring, as a regression gate** — re-run after big changes to catch newly-introduced drift.

The one precondition: a **trustworthy, identifiable baseline must exist.** This skill is only as good as its reference.
If the "baseline" is itself buggy/incomplete, or you genuinely can't tell which side is authoritative, say so — the
audit degrades to a self-review / spec-check, still useful but with weaker findings. Don't dress a shaky reference up as
ground truth.

## Method

### 1. Frame the audit — and define the truth standard
Pin down before any agent runs:
- **Baseline**: the reference (path / dir / branch / commit / tag — or a spec). What "correct" means.
- **New implementation**: the rewrite/migration under audit.
- **The truth standard** — *what observable artifact defines "matches"?* This matters more than it sounds. For a
  renderer it's the **exported output**, not the live preview (users receive the export; a baseline often has two paths —
  preview and exporter — that must agree, and the export is the one that ships). For an API it's the response contract;
  for a UI it's the rendered result + behavior. Audit against THAT artifact, not the nearest convenient surface — a cold
  auditor will otherwise compare previews and miss export-only divergence.

State plainly: baseline is the standard; the goal is to find divergence, **not** to redesign. Improvements come after
parity, deliberately (see Principles).

### 2. Discover the capability map — then CHECKPOINT before fanning out
This is the make-or-break step. (In an *informal* cold run — no human context — the framing + dimensions transferred
well when coverage was actively forced; the one miss was under-splitting the control surface. We kept no formal artifact
for this, so treat it as an observation, not a measured result — unlike the enumerate-vs-patterns A/B, which is.) Two parts:

**(a) Inventory → dimensions.** Read the baseline's source, build a capability inventory, and fold it into ~8–15
**orthogonal dimensions** that COVER the product with little overlap. Derive them from the baseline's OWN modules — never
a generic checklist. To *force* coverage, walk the baseline from four angles and confirm each is represented:
- **entry points / pipeline** — what runs start-to-finish;
- **the data model** — every field a user can set is a behavior that must render;
- **the CONTROL SURFACE** — every UI control / config option / flag (see the principle below — this is where rewrites
  silently die, and the easiest axis to under-count if you lump it into one coarse "settings" dimension);
- **the output formats** — every artifact emitted (file types, resolutions, exports, subtitles, side channels).
A dimension you forget is a permanent blind spot — the audit will never look there.

**(b) Checkpoint — STOP and WAIT (do not skip this).** Present the dimension list (with the baseline files each covers)
and **get the human's sign-off before spawning ANY auditor.** Do not call the fan-out tool until they reply — adding or
removing one axis here is how the user controls how many agents run and what gets covered. This step is *easy to skip*
(the agents launch and the list is never shown) — resist that; skipping it is a silent failure. Cheap insurance: someone
who knows the product spots a missing axis in seconds. If truly unattended, still emit the list + your own coverage
doubts so a skip is visible after the fact.

Examples of dimensions (adapt to the domain):
- *Media/render app*: timing & durations · transitions · text/captions · audio · color · layout variants · aspect &
  resolution · export · editor controls.
- *Web API*: endpoints · auth · request validation · error shapes · pagination · rate limits · webhooks · idempotency.
- *Data pipeline*: ingestion · transforms · schema/validation · dedup · scheduling · retries · outputs · observability.
- *UI/component lib*: each component's props · states · a11y · theming · events · responsive behavior.

### 3. Fan out one auditor per dimension (in parallel)
Each dimension gets its own auditor agent. They're independent, so run them concurrently for the whole map fast.
Give each auditor:
- the baseline path + the new-impl path, and the **specific files/symbols** to compare for its dimension;
- the instruction to **read the actual code in BOTH trees** before judging;
- the finding schema (below) and the taxonomy;
- a hard rule: **cite file:line on both sides**, and **don't invent** capabilities the baseline doesn't have;
- output discipline: **one finding per distinct gap — enumerate exhaustively; never bundle several controls/behaviors
  into a single "pattern" finding.** (An A/B test on this skill showed bundling keeps *recall* but cuts per-item
  *granularity* ~30% — folding 4 cover-scale sliders into one row, etc. — and the gap list exists to be acted on
  row-by-row, so that loss is real.) For each finding, write the **current state only** (no "used to / was") and be
  **prescriptive** (say what the new impl must do to match). *Note: the common "patterns over lists" heuristic for
  code-mapping (e.g. GSD's `codebase-mapper`) is correct for **describing** a codebase, wrong for **enumerating** an
  audit, so this skill deliberately inverts it (validated by an A/B test, `references/ab-test-enumerate-vs-patterns.md`).*

**Scaling valve — context-lean (default OFF).** Default: auditors return their FULL
findings to the orchestrator — it needs them inline to cluster well. ONLY when an audit is too large to fit the
orchestrator's context, switch to: each auditor WRITES its findings to `docs/audit/<dimension>.md` and returns just
counts + the blocker/major items; the synthesis (Step 4) then READS the per-dimension docs. An A/B test confirmed this
preserves synthesis quality (same clusters, same dominant root cause), so it's a *safe* valve — but it adds a write→read
hop, so don't reach for it unless context actually forces you to.

Implementation, in order of preference:
- **Workflow tool available** → one `agent(...)` per dimension inside a `parallel([...])`, each with the structured-output
  schema. (Skeleton: `references/workflow-skeleton.js`.) This is the cleanest path.
- **Subagents available (Agent tool)** → spawn the dimension auditors in a single message so they run concurrently.
- **Neither** → do the dimensions sequentially. Slower, same rigor.

### 4. Synthesize (the highest-value step)
Collect all findings, then:
- **Root-cause clustering** — scattered gaps usually share a few causes (a lossy adapter/contract between two layers; a
  config value never plumbed through; a whole mode left unimplemented). Group findings by cause. This is what turns "88
  gaps" into "6 fixes" and surfaces the **dominant** cause — fix once, kill many. Do this *before* you present anything.
- **Severity ranking** — `blocker` (breaks delivery / wrong output) > `major` (visible capability gap) > `minor`
  (cosmetic / edge). 
- **Persist a versioned doc** — write the COMPLETE list (every finding, file:line on both sides), grouped by root cause
  and severity, to a dated/versioned file under the repo's docs (e.g. `docs/audit/parity-<baseline>-vs-<new>-v1.md`).
  Nothing gets lost; the scope lives in one referenceable place.
- **Present a digest** — in chat, give: headline counts (checked / at-parity / gaps by severity); the **root-cause
  synthesis** first (it's the most useful part); the blockers listed out; the majors **grouped by theme** (not 50 flat
  bullets); and a **recommended fix order** (blockers → the dominant root cause → the rest), each step verified against
  the baseline. Link the full doc.

## The finding schema
Each auditor returns items shaped like this (use structured output if the harness supports it):

```
{
  "dimension":  "<the axis being audited>",
  "capability": "<one specific baseline behavior/feature>",
  "status":     "full | partial | missing | divergent",
  "severity":   "blocker | major | minor | ok",
  "baseRef":    "<file:line in the BASELINE>",
  "newRef":     "<file:line in the NEW impl, or '—' if missing>",
  "detail":     "<the concrete difference: what the baseline does vs what the new impl does/lacks>"
}
```

## Status & severity taxonomy
- **status** — `full`: new matches baseline behavior. `partial`: present but incomplete. `missing`: baseline has it, new
  doesn't. `divergent`: present but behaves/computes differently (always state the difference).
- **severity** — `blocker`: blocks delivery or produces wrong output (e.g. a setting that silently does nothing, a path
  that corrupts/cuts output). `major`: a real, user-visible capability gap. `minor`: cosmetic or edge-case. `ok`: at
  parity — **still report these**, so coverage is visible (the reader sees what's *done*, not only what's broken).

## Owner↔code traceability lives in `product-contract`
A capability has two faces — the **application** face (what the owner touches) and the **code** face (what implements it),
joined by a stable ID so an owner and an agent point at the same thing — and the most damaging gaps live *between* them (a
control the owner sees but no code reads). Building that durable, named, bilingual record (the feature dictionary, the
owner-face plain-language discipline, default-usable / refine-on-friction) is **`product-contract`'s** job, not this
skill's. When a contract exists, this audit writes each atom's per-target **status + evidence** to its own
`audit-results/ATOM-STATUS-<target>.md` (keyed by atom-ID) — the dictionary `状态` stays product-contract's single-product
snapshot, so each target gets its own status file and nothing is double-written. When it doesn't, your findings can
bootstrap one. Either way, keep the IDs stable so the owner can trace any finding back to the feature they recognize.

## Principles (the why)
- **The baseline is the standard — port faithfully, don't re-derive.** The most common way rewrites lose ground is the
  author re-inventing core logic instead of carrying it over, discarding tuning baked into the original. During the
  audit, *describe* divergence; don't "fix it better" on the fly. A divergence that you think is an improvement is still
  a finding — flag it, decide deliberately later.
- **The control surface is where rewrites silently die.** A rewrite's most common *invisible* loss is a control that
  still exists in the UI but no longer affects the output — a slider that does nothing, a setting that's a no-op, an
  option the new contract quietly strips (often via a lossy adapter that renames/drops fields). Enumerate the controls
  and verify each one actually drives the output; do NOT lump them into one coarse "settings/authoring" dimension. In
  practice this is frequently the single largest gap cluster *and* the easiest to under-count when dimensions are coarse.
- **Evidence on both sides or it isn't a finding.** file:line in baseline AND new (or `—` for missing). This is what
  makes the list trustworthy and immediately actionable, and what stops hand-wavy "feels different" noise.
- **Report parity, not just gaps.** Listing the `ok` items shows coverage and proportion — it reassures and calibrates.
- **Synthesis beats enumeration.** A flat list of 88 items is demoralizing and unactionable; the same 88 grouped into 6
  root causes is a plan. Always cluster.
- **Verify behavior empirically — adversarially.** Code-reading misjudges runtime behavior, and "I implemented X" is not
  evidence X works — a claim documents what you *said* you did, not what the code does, and the two often differ. Where
  feasible, run both and diff the actual output (a frame, a response, a file). When verifying a gap is *closed*, take the
  goal-backward stance: assume it is NOT fixed until the new impl's real output matches the baseline's. (This is the
  standard independent-verifier discipline.)
- **Don't invent capabilities the baseline lacks.** Every finding is grounded in baseline code. The new impl having
  *extra* things is fine and not a gap.

## Pitfalls (known failure modes — and the fix)
- **Over-transplanting a principle from another context.** A rule that's right elsewhere can be wrong here. *Real case:*
  "patterns over lists" is correct for *describing* a codebase but harmful for *enumerating* an audit — an A/B test
  caught it cutting per-item granularity ~30% (`references/ab-test-enumerate-vs-patterns.md`). **Fix:** test an absorbed
  technique against ground truth before trusting it; reputation of the source ≠ fit for your job.
- **Coarse dimensions hide the biggest cluster.** Folding the control surface into one "settings" axis under-counts the
  most common rewrite loss — controls that still show but no longer drive output. **Fix:** split the control surface
  finely (Step 2) and checkpoint the dimensions before fanning out.
- **Trusting code-reading over behavior.** "It looks wired up" ≠ "it works." **Fix:** run both and diff the real output,
  at least for blockers.
- **No trustworthy baseline.** If the reference is itself shaky, every finding inherits that doubt. **Fix:** say so;
  degrade to an explicit self/spec review rather than pretending it's ground truth.
- **Declaring the audit done from counts.** Counts are not coverage, and a claim is not evidence. **Fix:** the
  Verification step below.

## Verification — confirm the audit before anyone acts on it
An audit people will act on must itself be trustworthy; "I produced a list" is not evidence the list is right. Before
delivering or acting:
- **Spot-check evidence** — pull a random sample of findings and confirm the cited `file:line` exists and says what the
  finding claims, on BOTH sides. A finding without verifiable evidence is noise.
- **Sanity-check coverage** — is the at-parity count plausible? Did every dimension actually run (no silent agent
  failures)? A dimension returning zero findings is suspicious — confirm it, don't assume parity.
- **Pressure-test the dominant root cause** — does it actually explain the findings assigned to it? If you closed it,
  would those findings really close?
- **Empirically verify the blockers** — for each blocker, run both implementations and diff the real artifact (a frame,
  a response, a file). Don't hand over a blocker list you only read into existence.

## Output template (the persisted doc)
```
# Parity audit: <baseline> vs <new> — v1
> Generated: <N> dimensions audited in parallel · <X> capabilities checked · <Y> at parity · <Z> gaps
> (blocker B / major M / minor m). Baseline = the delivery standard; this lists only where <new> diverges.

## Root-cause synthesis (the Z gaps collapse to ~K causes)
1. <dominant cause> — <which findings it explains, est. count> — <one-line fix direction>
2. ...

## BLOCKER (B)
### 1. <capability>  [status]
- baseline: `file:line`  ·  new: `file:line`
- <detail>
...
## MAJOR (M)  — grouped by root cause/theme
## MINOR (m)
```

## A note on tone when delivering
If this audit was triggered because the rewrite "feels behind," the honest full count may sting — but a complete map
*validates* that feeling and shows you take it seriously, far better than dribbling gaps out. Pair the bad news with the
root-cause synthesis and the fix order so it reads as a route, not a verdict.

## Simplified one-shot version
For a quick copy-paste audit without invoking this skill, see `references/quick-prompt.md`.
