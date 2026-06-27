---
name: product-contract
description: >-
  FREEZE what a software product IS into a durable, owner↔code-traceable contract: turn user-visible capabilities and
  the code that implements them into a bilingual feature DICTIONARY (中文/English/大白话语义/在哪触达), owner-facing Feature
  Atoms, code-facing Capability Atoms, and many-to-many trace links — each on a stable atom-ID — plus coverage and
  next-pass gaps. Use to inventory, classify, or freeze ONE product's full capability set (no comparison target
  needed), build a feature dictionary to kill terminology confusion, map UI behavior to the files that implement it,
  or set ONE source of truth for what a product promises before a refactor, migration, rewrite, agent handoff, or
  parity audit. Triggers: freeze the spec, build a feature dictionary, inventory what this app does, make features
  traceable to code, align product with code, classify all the capabilities. The STRUCTURE layer of a trio on one
  atom-ID spine, feeding parity-audit (the evidence engine) and verified-execution (the gate).
license: MIT
metadata:
  version: 0.1.0
---

# Product Contract

This skill freezes **one** product into a durable contract that connects **what the owner experiences** with **where the
code implements it** — so a non-technical owner and a coding agent can point at the *same thing* and trace either way.

## What this is for
Every product spans two dimensions that drift apart: the **application** dimension (what the owner touches — controls,
outputs, promises) and the **code** dimension (what implements them — files, components, services). The most damaging
gaps live *between* them: a control the owner sees that no code reads; a behavior the code has that the owner never named.
And the owner and the agent describe the same feature in different words, so they talk past each other.

This skill produces the bridge: a **frozen, classified inventory** of one product's capabilities, where each capability is
**one record carrying both faces**, joined by a **stable ID**. That record set is simultaneously the **spec** ("what this
product IS"), the **dictionary** (the agreed name in plain owner-language *and* the code anchor), and the **owner↔code
index** (owner Ctrl-Fs a name → ID → code; agent greps the ID → the owner-facing meaning).

## What this is NOT (the boundary — do not blur it)
Three skills, three jobs, one shared atom-ID spine. Keep them separate:
- **product-contract (this)** = the **STRUCTURE / durability** layer. It *freezes one product* into the durable, named,
  traceable contract. It does **not** deeply audit a rewrite, and it does **not** gate execution.
- **`parity-audit`** = the **DEPTH / evidence** engine. Given a baseline + a target, it does the exhaustive, file:line,
  severity-ranked discovery of gaps. **Density and evidence come from there, not here.**
- **`verified-execution`** = the **GATE**. It closes non-passing atoms with independent, adversarial verdicts.

So: want max detail/evidence on a rewrite? → that's parity-audit. Want a durable, owner-readable, traceable map of one
product? → that's here. They **compose** via the shared atom registry; they are **not** merged and **not** redundant.

## The three layers of the contract
1. **User Feature Atoms** — owner-facing product promises (what the owner experiences / can verify).
2. **Code Capability Atoms** — agent-facing implementation *responsibility boundaries* (not file lists — see below).
3. **Traceability Links** — many-to-many, relation-typed links from a feature to the code that owns it, and back.

## Core workflow
1. **Pin the ground.** Project root, active worktree, baseline (if any), and the target output folder — *before* writing.
2. **Inspect live code + UI before inventing names.** Read the real source and the real control surface first. Naming
   things you haven't looked at is how the dictionary ends up wrong.
3. **If a contract already exists** → treat its atom registry as the shared spine; **extend it, do not fork a second
   checklist.** (Atom-ID is the join key across runs and across the other two skills.)
4. **If a trustworthy baseline exists but no contract** → run or consume a **`parity-audit`** first and use its
   audited capabilities (not just the gaps) to **bootstrap** draft atoms. Then normalize names/anchors here.
   (No baseline at all → degrade to a self-contained discovery pass and label confidence lower.)
5. **Build the bilingual glossary first** when naming is ambiguous (it usually is) — see the dictionary below.
6. **Register User Feature Atoms** for every user-visible / export-verifiable / persisted product promise.
7. **Register Code Capability Atoms** for each implementation responsibility boundary.
8. **Add Trace Links** between them with the relation verbs below.
9. **Run a coverage pass** → counts + unlinked gaps + next-pass.
10. **Save as a folder package**, not just a chat summary (it has to outlive the conversation — see Output package).

## What makes a good atom
### User Feature Atom — one smallest *observable* promise
A good atom is user-visible, export-verifiable, persisted, or operationally meaningful; has a **stable ID**; maps to a
semantic/domain; is **traceable to code**; and is **testable by one observable acceptance rule** (this rule is the seed of
the DoD that `verified-execution` will later check — write it observably, see the DoD bridge).

**Split broad labels.** "caption system" / "export system" are *categories*, not atoms. Split into the smallest promises:
`CAPTION.fxKeywordWindow`, `EXPORT.resolution`, `AUDIO.noAudio`, `PERSIST.apiKey`. One atom = one thing the owner could
point at and say "this works / this doesn't." Coarse atoms are the #1 way a contract looks complete but isn't.

### Code Capability Atom — one responsibility boundary
Name the source files/dirs, the responsibility, accepted inputs/outputs, the risk when modified, and the feature atoms it
affects. **A file list is not a responsibility:** one file can hold several responsibilities and one responsibility can
span several files. Atomize by *responsibility*, not by file.

## Trace links (use these relations consistently)
`declared-by` (a type/schema/contract declares the field) · `edited-by` (UI/API edits it) · `stored-by` (persistence
stores/restores it) · `resolved-by` (a resolver derives the canonical model) · `rendered-by` (renderer displays/plays it)
· `exported-by` (exporter emits it as a deliverable) · `validated-by` (preflight/guard/runtime checks it) · `tested-by`
(a test/probe/fixture verifies it) · `documented-by` (docs define the workflow/semantics).

**Rule:** every high-risk feature needs at least one *source* relation (edited/declared) **and** one *final-consumer*
relation (rendered/exported/stored). Every export feature needs an `exported-by` + `tested-by`, **or an explicit gap**.
A feature with a source but no consumer is the classic 🟠 未接线 (wired in the model/UI but nothing downstream reads it).

## The unified dictionary (the 4-face table — this is the owner↔code bridge)
When terminology causes confusion (the default assumption), build one table. Each row is one atom, both faces joined by ID:

```text
ID | 中文名 | English | 语义(大白话:它管什么/你会看到什么) | 在哪(你触达) | Feature Atom | 代码锚点(file:line) | Code Atom | 状态
└───────────────── OWNER side (the owner reads/operates these) ─────────────────┘ └──── AGENT side ────┘ └ snapshot ┘
```

Use short IDs that survive discussion: `F-res`, `F-floor`, `F-fx`, `F-srt-source`. **Owner side** = `中文/English/语义/在哪
/Feature-Atom` (the owner operates these); **agent side** = `代码锚点/Code-Atom` (the agent operates these); the **ID** is
what they share. **`状态` is product-contract's own single-product snapshot** ("does this product, as it stands, honor the
promise?") — it is **not** a per-target field. When you audit targets A/B, parity-audit writes their per-target status to
`audit-results/ATOM-STATUS-<target>.md` keyed by the same ID — never back into this `状态` column (that's what keeps the
column single-writer). DoD is **not** a dictionary column; it lives as the "observable acceptance" of each User Feature
Atom in the registry (owner-facing, plain language) — see `references/traceability-template.md`.

### Owner-face discipline — this is where agents fail, so hold the line
Write `中文名` / `English` / `语义` / `在哪` in **plain "what you do / what you'd see / the outcome" language — NOT
control-paths, variable names, or jargon.** The agent keeps sliding back into system-naming (writing `style.anim` instead
of "how the caption appears"); resist it every row. The test: *would the owner, who has never seen the code, understand
this sentence?* If not, it's agent-jargon — rewrite it.
- **No screenshots as the primary mechanism.** They're too slow and don't survive as reusable text. A good plain sentence
  is faster, greppable, and reusable. (A screenshot may *clarify* a hard one — but the sentence is the artifact.)

### Mechanism — default-usable, refined on friction (do NOT gate on per-entry sign-off)
The agent knows the system better than the owner, so **the agent authors the dictionary default-usable and it is live
immediately.** The owner does **not** confirm every wording (that's too slow and kills the whole point). Instead:
- the owner flags only the entries they **can't understand**, and the agent fixes *those*;
- once a name is set, the agent **must reuse it** — never invent a second name for the same thing. That naming
  consistency is what actually cuts miscommunication, more than any single perfect phrasing.

## Status taxonomy (few, consistent — every atom carries one)
- `✅ 保留` — present and traceable (the promise is honored and you can trace it to code).
- `🟡 待验证` — mapped, but needs a fixture / runtime proof / manual check before you trust it.
- `🟠 未接线` — model or UI exists, but the consumer chain is incomplete (it shows, but nothing downstream reads it).
- `🔴 回归` — the product promise is **not** honored (regressed / broken / no-op).
- `🟣 新增` — a new capability outside the baseline; requires independent acceptance (it's not "parity," it's new scope).

## Coverage pass + next-pass
Sweep across: UI surfaces & controls · state & persisted fields · import/export paths · render/preview paths · native
bridges / service APIs · QA/probe/test scripts · docs & handoff materials. Then report (see `references/package-template.md`):
counts of feature atoms / code atoms / trace links · linked vs **unlinked** on each side · high-risk gaps · **next pass**.
Unlinked atoms and high-risk gaps are the contract's honest edge — never hide them to make coverage look finished.

## The DoD bridge to verified-execution
Each User Feature Atom's **observable acceptance rule** *is* the seed of a Definition-of-Done. State it in
owner-observable terms ("set X, render frame N; caption enters with blur ≠ fade") yet checkable against the **code** — so
the same sentence serves the owner (recognizable) and the agent (runnable). When you hand non-passing atoms to
`verified-execution`, **reuse the atom-ID as the contract item ID**: freeze → audit → close → verify all key off the same
ID, and the owner can trace any verdict back to the feature they recognize. (Details: that skill's "DoD is the owner↔code
bridge" section.)

## Coordinating with the other two skills (the shared atom-ID spine)
The shared artifact is **this contract's atom registry**; atom-ID is the join key. Full protocol:
`references/three-skill-coordination.md`. The short version:

| skill | reads | writes |
|---|---|---|
| **product-contract** (this) | project source, UI, docs, optional parity findings | atoms, trace links, dictionary, coverage gaps, next-pass — *the question set* |
| **parity-audit** | this contract's atoms + trace links + a target's source/runtime | per-target status + evidence per atom — *the answer set* |
| **verified-execution** | atoms whose target status is not passing | independent claims/verdicts keyed by atom-ID — *the gate* |

**Contract-led parity (the key rule):** when this contract exists, parity-audit audits **atom-by-atom against it** — it
does **not** re-derive its own dimension checklist (re-derivation drift is exactly why two audits of one product disagree
on granularity). If parity-audit finds a promise that **no atom represents**, that's a **contract gap for the next
product-contract pass** — recorded here, not silently bolted onto the audit. See `references/parity-integration.md` for
converting parity findings into contract artifacts, and the quality gate that pass must clear.

## Output package (save this, not a chat summary)
**One co-located package, three writers, one atom-ID spine** — each skill owns its own subfolder so nothing is
double-written (full shape + the single-writer rules: `references/package-template.md`):
```text
product-contract-v1/
  README.md  ·  MANIFEST.md
  dictionary/ registries/ coverage/ workflows/   # product-contract writes (the 底稿 / question set)
  audit-results/                                  # parity-audit writes (per-target answers, keyed by atom-ID)
  execution-ledger/                               # verified-execution writes (the gate ledger; harness.py --dir here)
```
- **product-contract** → `dictionary/ registries/ coverage/ workflows/`. The dictionary `状态` is a single-product snapshot.
- **parity-audit** → `audit-results/{PARITY-…-v1.md, ATOM-STATUS-<target>-v1.md, dimensions/}` — **per-target** status here,
  never in the dictionary `状态`.
- **verified-execution** → `execution-ledger/{contract.jsonl, ledger.jsonl, status.md}` via
  `harness.py --dir docs/product-contract-v1/execution-ledger`.

Versioned (`-v1`): a new revision is a **new file** (`-v2`), never an in-place rewrite of the old one. Adapt the folder
name to the repo's convention, but keep the package complete. Templates: `references/package-template.md`,
`references/dictionary-template.md`, `references/traceability-template.md`.

## Pitfalls
- **Atoms too coarse.** "export system" as one atom hides ten promises. Split to the smallest observable thing. (#1 way a
  contract looks done but isn't.)
- **File lists masquerading as code atoms.** Atomize by *responsibility*, not file. One file ≠ one responsibility.
- **Owner-face written in jargon.** `style.anim` is not "what the owner does." Rewrite until a non-coder understands it.
- **Gating the dictionary on per-entry sign-off.** Kills throughput. Default-usable + refine-on-friction is the mechanism.
- **Forking a second checklist when a contract exists.** Extend the atom registry; don't create a parallel universe — that
  destroys the comparability the spine exists to give.
- **Coverage that hides the gaps.** Unlinked atoms and 🟠/🔴 items are the point of the coverage pass; surface them.
- **Letting it live only in chat.** Un-saved, it dies at compaction. Write the folder package.

## Verification (of the contract itself)
- **Spot-check anchors** — pull random dictionary rows; confirm the cited `file:line` exists and does what the row claims.
- **Trace both ways** — pick a feature atom, follow its links to code and back; pick a code atom, follow it to the
  promises it affects. Dangling links = a real gap, not a typo.
- **Owner-readability** — read 5 `语义` cells as if you'd never seen the code. Any that need code knowledge fail the bar.
- **Coverage honesty** — is the unlinked/high-risk list plausibly complete, or suspiciously empty? Empty is a smell.
