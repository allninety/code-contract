# code-contract

**English** | [中文](README.zh.md)

Three composing **Claude Code skills** (in the open [Agent Skills](https://agentskills.io) `SKILL.md` format) that keep a **rewrite, migration, or port honest** — by making "done" mean *independently verified against a frozen, owner-readable spec*, not "the implementer says so."

A rewrite silently loses things the original did: a control that no longer affects output, an export option that became a no-op, a duration clamped differently. You discover these one at a time, over weeks, and trust erodes. This pack turns that into a closed loop:

```
 OWNER language ──►  product-contract  ──►  parity-audit  ──►  verified-execution  ──► result the owner trusts
 "what it should do"   (freeze the spec)     (find the gaps)     (close them, gated)
                              └──────────────── one stable atom-ID ────────────────┘
```

| skill | role | answers |
|---|---|---|
| **product-contract** | *structure* — freeze ONE product into a durable, owner↔code-traceable contract (feature atoms + code atoms + trace links + a bilingual dictionary) | "What should this product do? What is each feature called? Where does the owner touch it? Which code owns it?" |
| **parity-audit** | *depth* — exhaustively compare a target against a baseline, every gap with `file:line` evidence, severity-ranked, grouped by root cause | "Does this target actually do each thing the contract promises? What's missing / regressed / not wired up?" |
| **verified-execution** | *gate* — close each non-passing item only when an **independent** verifier confirms it against a written, observable definition-of-done | "Are the gaps *really* fixed? Where's the evidence? Where's the ledger?" |

The three share **one stable atom-ID**, so the owner can trace any verdict back to the feature they recognize, and any code change forward to the promises it affects. The owner only ever touches feature names + atom-IDs; the agent only ever touches code anchors + DoDs; trace links bridge them.

## What's actually new here (and what isn't)

Most of this is competent application of known practice — requirements traceability, definition-of-done, ubiquitous language, regression sweeps. Three parts are sharper than common practice, and they're the reason to use it:

1. **An empirically *refuted* output rule.** `parity-audit` deliberately **inverts** the popular "describe patterns, not lists" advice — because an A/B test (ground-truthed against 17 known control regressions) showed bundling preserves recall but cuts per-item granularity ~30%, and a gap list exists to be acted on row-by-row. The experiment is shipped: [`ab-test-enumerate-vs-patterns.md`](plugins/code-contract/skills/parity-audit/references/ab-test-enumerate-vs-patterns.md). (Most skills assert; this one tested.)
2. **A single-writer atom-ID spine.** Per-target audit status is forced into its own file and *forbidden* from the contract dictionary — so a contract audited against N targets never double-writes one status cell. One join key, one writer per artifact.
3. **A gate the implementer can't quietly fool.** `verified-execution` ships a tiny stdlib harness whose teeth are mechanical, not prose: an append-only ledger, a hashed DoD, a **self-certification flag** (a verdict from the same identity that did the work is flagged), and a **stale-PASS downgrade** (change a DoD after it passed and the item drops from ✓ to ⚠STALE, blocking the gate). It does not *prevent* a determined operator — see [Honest limits](#honest-limits) — it makes the two classic dodges **visible**.

## Install

Targeted at **Claude Code**. (The skills are plain [Agent Skills](https://agentskills.io) `SKILL.md` files, so they're portable to other compatible agents in principle — but this pack is built and tested on Claude Code; see [Platforms](#platforms--portability).)

**Manual (recommended)** — copy the skill folders where Claude Code discovers them:
```bash
git clone https://github.com/allninety/code-contract.git
cp -R code-contract/plugins/code-contract/skills/* ~/.claude/skills/
```
Then start a session — Claude triggers a skill by its description, or invoke `/product-contract`, `/parity-audit`, `/verified-execution`.

**中文版 / Chinese:** the same three skills also ship **fully in Chinese** — `product-contract-zh`, `parity-audit-zh`, `verified-execution-zh` — whose `SKILL.md`, `references/` docs, orchestration skeletons, and harness output are all localized, and whose description triggers on Chinese prompts (冻结规格 / 能力对账 / 独立验收). The `cp` above installs all six; use whichever language you prompt in. (The zh harness keeps English status tokens + JSON ledger keys, so its ledger stays interoperable with the English harness.)

**Plugin** — the pack is also a Claude Code marketplace: `/plugin marketplace add allninety/code-contract` then `/plugin install code-contract`.

**Requirements:** Claude Code; Python 3 (stdlib only) for `verified-execution`'s harness.

## Quickstart

- **Freeze a spec:** "Use `product-contract` to freeze what this app does into a contract." → a `product-contract-v1/` package (dictionary + registries + coverage + workflows).
- **Audit a rewrite:** "Use `parity-audit`: baseline = `<old>/src`, target = `<new>/src`." → one exhaustive, evidence-backed, root-cause-grouped gap list.
- **Close the gaps, gated:** "Use `verified-execution` on that gap list." → each item closed only on an independent PASS, in a tamper-flagged ledger behind a blocking gate.

They also work standalone — you don't need all three.

## Example

[`examples/verified-execution-run/`](examples/verified-execution-run/) is a **real** harness run (not a mockup) over a small web-API contract, showing all four states including the goalpost-moved tooth:

```
1/4 VERIFIED
✓ VERIFIED  A1   auth: 401 on missing token
✗ FAIL      A2   pagination: page size cap   └ limit=9999 returned 9999 rows — cap not enforced
◐ CLAIMED   A3   idempotency: repeated POST
⚠ STALE     A4   error shape: 422 body       └ goalpost moved since PASS — re-verify
```

See also [`examples/product-contract-package/`](examples/product-contract-package/) (a tiny contract) and [`examples/parity-audit-gap-doc/`](examples/parity-audit-gap-doc/) (a tiny gap doc).

## Honest limits

In a single Claude session the orchestrator is still Claude — `verified-execution` is **not** a hardware-enforced constraint. Its teeth are: an *independent, adversarial* verifier (far harder to fool than self-checking), a *deterministic* append-only ledger + gate (a script's verdict can't be argued with, and changes are visible), and *you* as the final gate. It makes false "done" much harder and always *visible* — not impossible. That's the design, stated plainly so you can judge it.

## Platforms & portability

**This pack targets Claude Code** — that's where it's built, run, and tested. The `SKILL.md` files use the open [Agent Skills](https://agentskills.io) standard and the harness (`harness.py`) is pure-stdlib Python, so the *method* is portable to other compatible agents (Codex CLI, Cursor, …) in principle. But the **automated orchestration is Claude-specific** — `parity-audit`'s workflow skeleton and `verified-execution`'s driver use Claude Code's Workflow/Agent tools — so **cross-platform support is not a promise of this pack**; treat those skeletons as Claude-Code helpers. Per-platform orchestration adapters are a welcome contribution.

README narrative style modeled on [khazix-skills](https://github.com/KKKKhazix/khazix-skills) (MIT) — thanks for the pattern.

## Layout

```
plugins/code-contract/skills/
  product-contract/      SKILL.md + references/        (the contract: atoms, links, dictionary)
  parity-audit/          SKILL.md + references/         (the audit: dimensions, fan-out, A/B record)
  verified-execution/    SKILL.md + references/ + scripts/harness.py   (the gate)
examples/                real worked outputs
```

The shared handoff protocol lives in [`product-contract/references/three-skill-coordination.md`](plugins/code-contract/skills/product-contract/references/three-skill-coordination.md).

## Acknowledgments

Designed and built with **Claude** ([Claude Code](https://www.anthropic.com/claude-code), Opus 4.8); independently reviewed across several passes with **OpenAI Codex**.

## License

[MIT](LICENSE) © 2026 allninety. Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
