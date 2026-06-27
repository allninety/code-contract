# Examples

Three worked outputs, in a generic payments-API domain (English-only, to show the bilingual columns are optional).

- **`verified-execution-run/`** — a **real** harness run (`contract.jsonl` + `ledger.jsonl` + `status.md`), produced by `harness.py`, showing all four states: ✓ VERIFIED, ✗ FAIL, ◐ CLAIMED, and ⚠ STALE (a DoD changed after the item passed). Reproduce it by replaying the commands, or just read `status.md`.
- **`product-contract-package/`** — a tiny contract: a feature dictionary, user-feature atoms, and trace links, all sharing atom-IDs.
- **`parity-audit-gap-doc/`** — a tiny parity gap doc: findings with `file:line` on both sides, severity, and a root-cause synthesis.

These are illustrative and deliberately small. A real run on a non-trivial product produces dozens to hundreds of atoms/findings.
