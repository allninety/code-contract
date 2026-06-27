# Traceability links — example

Many-to-many, typed relations. Every high-risk feature needs a source relation AND a final-consumer relation.

| feature | relation     | code            | note (file:line, what the link asserts)             |
|---------|--------------|-----------------|-----------------------------------------------------|
| F-401   | validated-by | CODE.authGuard  | auth.py:40 — rejects when no bearer token present   |
| F-cap   | declared-by  | CODE.schema     | schema.py:12 — `limit` max is 100                   |
| F-cap   | rendered-by  | CODE.listPaging | list.py:88 — **bug:** clamps only when limit unset (🔴) |
| F-idem  | stored-by    | CODE.chargeDedup | store.py:55 — dedup table keyed by idem key        |
| F-idem  | edited-by    | CODE.chargeDedup | charge.py:120 — looks up idem key before charging  |

`F-cap` has a source (declared-by) but its consumer (rendered-by) doesn't honor the cap → that's the 🔴 in the dictionary,
and the gap parity-audit reports below.
