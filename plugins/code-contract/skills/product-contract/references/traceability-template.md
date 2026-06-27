# Registries + trace links — template

Three files under `registries/`. Each atom has a stable ID; trace links are many-to-many. Example rows are **illustrative**
(a render/export app) — adapt to your domain; the **中文名 column is optional** (drop it for a monolingual project).

## USER-FEATURE-ATOMS.md
```text
| ID        | 中文名     | English          | semantic (plain owner-language)        | observable acceptance (DoD seed)                  | domain   | status  |
|-----------|-----------|------------------|----------------------------------------|---------------------------------------------------|----------|---------|
| F-res     | 导出分辨率 | Export resolution | clarity of the exported file: 1080/2K/4K | export at 4K → file is 3840-wide, not 1920         | export   | 🔴 回归 |
```
One atom = one smallest observable promise. The "observable acceptance" column is the seed of the verified-execution DoD —
write it as something you can RUN or SEE, tied to the baseline/spec. **`status` here is the single-product snapshot**
(same as the dictionary `状态`); a *target's* per-target status is written by parity-audit to
`audit-results/ATOM-STATUS-<target>.md`, keyed by this ID — not into this column.

## CODE-CAPABILITY-ATOMS.md
```text
| ID              | responsibility (one boundary)              | source (files/dirs)              | inputs → outputs            | risk when modified            | affects features      |
|-----------------|--------------------------------------------|----------------------------------|-----------------------------|-------------------------------|-----------------------|
| CODE.exportPipe | turns props+resolution into the rendered file | electron/render.cjs, Film.tsx    | InputProps,res → mp4        | wrong size / dropped controls | F-res, F-aspect, ...  |
```
Atomize by **responsibility**, not by file. One file may hold several; one responsibility may span several.

## TRACEABILITY-LINKS.md
```text
| feature | relation     | code            | note (file:line, what the link asserts)        |
|---------|--------------|-----------------|------------------------------------------------|
| F-res   | exported-by  | CODE.exportPipe | render.cjs:54 emits at composition.width/height |
| F-res   | declared-by  | CODE.schema     | schema.ts: res enum 1080/2k/4k                  |
```
Relations: `declared-by` · `edited-by` · `stored-by` · `resolved-by` · `rendered-by` · `exported-by` · `validated-by` ·
`tested-by` · `documented-by`.

**Rule:** every high-risk feature needs ≥1 source relation (edited/declared) **and** ≥1 final-consumer relation
(rendered/exported/stored). Every export feature needs `exported-by` + `tested-by`, or an explicit gap. A feature with a
source but no consumer = 🟠 未接线.

## workflows/
Both loops are spelled out end-to-end (not just named), because the value is the **hand-off across the trades**. The
owner only ever touches the LEFT of the table (中文问题 / 词典 / atom-ID); the agent only ever touches the RIGHT
(代码锚点 / DoD); trace links bridge them; verified-execution closes them.

### OWNER-TO-CODE.md — owner has a complaint → confirmed fix
> *"我发现 4K 导出不对" →*
1. **Find the atom.** Look the complaint up in the dictionary by 中文名/语义 → the **ID** (e.g. `F-res` / `EXPORT.resolution`).
2. **Trace to code.** Follow `TRACEABILITY-LINKS` for that ID → the **Code Atom** + `代码锚点` (file:line) that own it.
3. **Read current status.** Check the atom's per-target status in `audit-results/ATOM-STATUS-<target>.md` (✅/🟠/🔴/缺失)
   and the evidence behind it — is it truly broken, and how?
4. **Hand to the gate (if not ✅).** Pass the **atom-ID** to `verified-execution` as a contract item, with the atom's
   **observable acceptance** as the DoD: `harness.py add F-res "<title>" "<baseline ref>" "<DoD>"`.
5. **Fix** — the minimal change at the traced `代码锚点`.
6. **独立验收.** Close ONLY on an **independent** verified-execution PASS against that DoD (a separate verifier reads the
   real output) — never the implementer's self-claim. The verdict is keyed to the same atom-ID, so the owner can trace it
   back to the feature they recognize.

### CODE-TO-OWNER.md — agent changed code → which promises to re-check
> *改了导出代码 →*
1. **Land on the Code Atom.** The file you touched → its `CODE-CAPABILITY-ATOM` (via `source` / `代码锚点`).
2. **Fan out via trace links.** That code atom's `affects features` (and reverse trace links) → every **User Feature
   Atom** it touches.
3. **List affected promises** in owner language (so the owner knows what might have moved).
4. **Regression-verify** each affected atom against its observable acceptance — re-run the DoD; downgrade any that no
   longer hold to 🔴/🟠 and feed them into NEXT-PASS / verified-execution.

### NEXT-PASS.md
- The honest backlog: unlinked atoms, 🟡/🟠/🔴 items, and **contract gaps fed back from parity-audit** (a promise the
  target revealed that no atom yet covers → a new atom for the next product-contract pass, not a silent audit expansion).
