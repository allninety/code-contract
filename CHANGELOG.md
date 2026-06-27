# Changelog

All notable changes to this pack are documented here. Versioning is per-skill (each `SKILL.md` carries `metadata.version`); this file tracks the pack as a whole.

## [0.1.0] — 2026-06-27

Initial public packaging of three skills that were developed and battle-tested on a real renderer migration.

### product-contract (0.1.0)
- Freeze one product into a durable owner↔code contract: User Feature Atoms, Code Capability Atoms, many-to-many trace links (typed relations), a bilingual 4-face dictionary, coverage + next-pass.
- Single-writer-per-folder co-located package; the dictionary `状态` is a single-product snapshot, per-target status lives in `audit-results/`.

### parity-audit (0.1.0)
- Exhaustive baseline-vs-target gap audit: orthogonal dimensions, parallel one-auditor-per-dimension fan-out, `file:line` evidence on both sides, severity + root-cause synthesis.
- Output rule **enumerate, don't bundle**, backed by a shipped A/B test (`references/ab-test-enumerate-vs-patterns.md`).
- Contract-led mode: when a `product-contract` exists, audits atom-by-atom against it rather than re-deriving dimensions.

### verified-execution (0.1.0)
- Independent-verifier gate over a work list; append-only contract + ledger; hashed DoD.
- Harness teeth: `--dir` co-location, `status --write` snapshot, **self-certification flag** (`--by`), **stale-PASS downgrade** (a DoD changed after a PASS drops the item to `STALE` and blocks the gate).

### Chinese skills — zh (0.1.0)
- `product-contract-zh`, `parity-audit-zh`, `verified-execution-zh` — **fully localized**: SKILL.md, every `references/` doc, the orchestration skeletons' comments/prompts, and the harness's output/help are all in Chinese. Descriptions trigger on Chinese prompts; spec-valid (well under 1024); self-contained (own `references/`/`scripts/`). Modeled on khazix-skills' all-Chinese style.
- The zh harness keeps English **status tokens** (PASS/VERIFIED/STALE…) and **JSON ledger keys**, so its `contract.jsonl`/`ledger.jsonl` stay format-compatible with the English harness (verified by cross-reading a zh ledger with the English `harness.py`).
