# Three-skill coordination — the shared atom-ID spine

The canonical protocol for using **product-contract + parity-audit + verified-execution** together. All three key off
**one stable atom-ID**; this file is the single source of truth for how they hand off. (parity-audit and
verified-execution point here rather than restating it, so the protocol can't drift between copies.)

## The spine
The shared artifact is the **product-contract atom registry**. Atom-ID is the join key.

```text
product-contract atom  (the question: "does this product promise X?")
  ├─ parity status + evidence for target A   (the answer for impl A)
  ├─ parity status + evidence for target B   (the answer for impl B)
  └─ verified-execution claim/verdict ledger (the independent gate, per target + DoD)
```

**Where it all lives — one co-located package, three writers, no shared file** (full shape:
`product-contract/references/package-template.md`):
```text
docs/product-contract-v1/
  dictionary/ registries/ coverage/ workflows/   # product-contract writes
  audit-results/   ATOM-STATUS-<target>.md ...    # parity-audit writes (per-target status lives HERE, not in the dictionary)
  execution-ledger/  contract.jsonl ledger.jsonl status.md   # verified-execution writes (harness.py --dir here)
```
The dictionary's `状态` column is product-contract's **single-product snapshot**; **per-target** status is a separate
parity-audit artifact keyed by the same atom-ID. That separation is what makes `status` single-writer-per-file.

## Read/write protocol
| skill | reads | writes |
|---|---|---|
| **product-contract** | project source, UI, docs, optional parity findings | atoms, trace links, dictionary, coverage gaps, next-pass |
| **parity-audit** | the atom registry, trace links, a target's source/runtime | per-target atom status + evidence |
| **verified-execution** | atoms whose target status is not passing | independent claims/verdicts keyed by atom-ID |

Who owns what: **product-contract owns STRUCTURE** (the durable, named, traceable map). **parity-audit owns DEPTH** (the
exhaustive, file:line, severity evidence). **verified-execution owns the GATE** (independent adversarial verdicts). They
compose; they are not merged and not redundant.

## Contract-led parity (when a contract exists)
parity-audit audits **atom-by-atom against the registry** — it does NOT re-derive its own dimension checklist:
1. Read `USER-FEATURE-ATOMS`, `CODE-CAPABILITY-ATOMS`, `TRACEABILITY-LINKS`, and the dictionary.
2. Treat the User Feature Atoms as the audit checklist.
3. Use trace links to find the target's code anchors.
4. Run or inspect each atom's observable DoD against the target.
5. Write a status per atom — to `audit-results/ATOM-STATUS-<target>.md`, **not** the dictionary `状态`:
   `✅ 保留` / `🟠 未接线` / `🔴 回归` / `缺失` / `🟡 待验证`.
6. **Preserve atom-IDs** so target A and target B are directly comparable, run over run (each target = its own status file).

Grouping for readability is fine, but **the audited unit stays the atom.** If parity-audit finds a real product promise
that **no atom represents**, it records that as a **contract gap for the next product-contract pass** — it does not
silently expand its own audit universe. (That feedback loop is how the contract's density climbs over iterations.)

## Cold start (no contract yet)
1. parity-audit runs baseline-led discovery (its full method).
2. It emits **draft atoms** as a bootstrap artifact (from audited capabilities, not only gaps).
3. product-contract normalizes the names, glossary, code atoms, and trace links into the real registry.

## Verified execution
verified-execution uses **atom-IDs as its contract item IDs**. A PASS verdict closes the atom **only for the named target
and DoD** — it does not delete the atom or erase parity evidence for other targets. The owner can trace any verdict back
to the feature they recognize, because it's the same ID end to end: freeze → audit → close → verify.
