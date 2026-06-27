# Output package — folder shape + coverage report

Save the contract as a folder, not a chat summary (it must outlive the conversation). Versioned: a new revision is a new
file (`-v2`), never an in-place rewrite of the old one.

**One co-located package, three writers, one atom-ID spine.** The three skills are three *trades* working the same
package — each owns its own subfolder, so no two skills write the same file:

```text
product-contract-v1/
  README.md            # what this product is, in ~5 lines the owner reads first; links to the rest
  MANIFEST.md          # file map + how the pieces relate
  # ── product-contract writes these (the "底稿" / question set) ──
  dictionary/
    FEATURE-DICTIONARY-v1.md     # the 4-face table (see dictionary-template.md); 状态 = single-product snapshot
  registries/
    USER-FEATURE-ATOMS.md
    CODE-CAPABILITY-ATOMS.md
    TRACEABILITY-LINKS.md        # (see traceability-template.md)
  coverage/
    COVERAGE-v1.md               # the report below
  workflows/
    OWNER-TO-CODE.md
    CODE-TO-OWNER.md
    NEXT-PASS.md
  # ── parity-audit writes these (the answer set, per target) ──
  audit-results/
    PARITY-<baseline>-vs-<target>-v1.md   # the persisted gap doc
    ATOM-STATUS-<target>-v1.md            # per-target ✅/🟡/🟠/🔴/🟣 status keyed by atom-ID (NOT the dictionary 状态)
    dimensions/<dimension>.md             # optional per-dimension findings
  # ── verified-execution writes these (the gate ledger) ──
  execution-ledger/
    contract.jsonl     # the items + their DoD (harness.py store)
    ledger.jsonl       # append-only claims + verdicts
    status.md          # human-readable snapshot (harness.py status --write)
```
Adapt the folder name to the repo's existing docs convention, but keep the package complete.

**Single-writer-per-folder — this is what keeps `status` from being double-written:**
- `product-contract` owns `dictionary/ registries/ coverage/ workflows/`. The dictionary's `状态` column is its **own
  single-product snapshot** ("does this product, as it stands, honor the promise?") — NOT a per-target field.
- `parity-audit` owns `audit-results/`. **Per-target** status (target A vs B) lives in
  `audit-results/ATOM-STATUS-<target>-v1.md`, keyed by atom-ID — never written back into the dictionary's `状态`.
- `verified-execution` owns `execution-ledger/`. Point `harness.py` at it with
  `--dir docs/product-contract-v1/execution-ledger` (or `HARNESS_DIR`).

## COVERAGE report shape
```text
User Feature Atoms:      <n>
Code Capability Atoms:   <n>
Trace Links:             <n>
Linked Feature Atoms:    <n>   (Unlinked: <n>  ← these are gaps)
Linked Code Atoms:       <n>   (Unlinked: <n>)
High-risk gaps:          <list — export/persistence/native-bridge atoms missing a consumer link>
Status tally:            ✅ <n> · 🟡 <n> · 🟠 <n> · 🔴 <n> · 🟣 <n>
Next pass:               <the honest backlog>
```
The unlinked counts and high-risk gaps are the **point** of the coverage pass — surface them; never zero them out to look
finished.
