# Feature dictionary — template + rules

The dictionary is the owner↔code bridge: one row per atom, both faces joined by a stable ID. Columns are grouped so the
**owner block is contiguous on the left** (ID + 中文/English/语义/在哪 + Feature Atom), the **agent block is on the right**
(代码锚点 + Code Atom), and `状态` is a single-product snapshot at the end.

> The example rows below are from a render/export app — **illustrative**, adapt to your domain. The **中文 columns are
> optional**: keep the bilingual pair only if your owner works across two languages; an English-only project drops 中文名.

## Table
```text
|       ┌──────────────── OWNER side ─────────────────┐        ┌── AGENT side ──┐  snapshot
| ID    | 中文名      | English          | 语义(大白话:它管什么/你会看到什么)        | 在哪(你触达)       | Feature Atom      | 代码锚点(file:line)        | Code Atom         | 状态     |
|-------|------------|------------------|------------------------------------------|-------------------|-------------------|---------------------------|-------------------|----------|
| F-res | 导出分辨率  | Export resolution | 出片的清晰度:1080/2K/4K,挑哪个出片就多大  | 导出面板·分辨率下拉 | EXPORT.resolution | Film.tsx:36 · render.cjs:54 | CODE.exportPipe   | 🔴 回归  |
| F-fx  | 特效字幕    | FX caption       | 字幕用关键词大字+特效入场,而不是整句平铺    | 样式·字幕模式       | CAPTION.fxKeyword | buildCaption.ts:101        | CODE.captionBuild | 🟡 待验证 |
```

## Rules
- **Short, durable IDs** that survive discussion: `F-res`, `F-floor`, `F-fx`, `F-srt-source`. The ID is the join key
  across the dictionary, the atom registries, parity status, and verified-execution verdicts — never renumber it.
- **语义 / 在哪 / names in plain owner-language**, never jargon. Test: would someone who has never seen the code understand
  it? `style.anim` fails; "how the caption appears" passes.
- **代码锚点 is the agent's face** — `file:line`, may list several. This is the only column allowed to be technical.
- **`状态` is a single-product snapshot, single-writer.** It answers "does *this* product, as it stands, honor the
  promise?" — it is NOT a per-target field. When you audit targets A/B, **parity-audit** writes their per-target status to
  `audit-results/ATOM-STATUS-<target>.md` (same atom-ID), never back into this `状态` column.
- **DoD is not here.** A row's observable-acceptance test (the DoD seed) lives in `USER-FEATURE-ATOMS.md` (owner-facing,
  plain language), not in this dictionary — see `traceability-template.md`.
- **One row = one atom.** If a row needs "and" to describe two promises, split it into two rows.
- **Default-usable, refined on friction.** The agent authors every row usable and live immediately; the owner flags only
  the rows they can't understand; the agent fixes those. **No per-row sign-off.** Once a name is set, reuse it — never a
  second name for the same thing.

## Status labels (few + consistent)
- `✅ 保留` — present and traceable.
- `🟡 待验证` — mapped but needs a fixture / runtime proof / manual check.
- `🟠 未接线` — model/UI exists but the consumer chain is incomplete.
- `🔴 回归` — the product promise is not honored.
- `🟣 新增` — new capability outside baseline; needs independent acceptance.
