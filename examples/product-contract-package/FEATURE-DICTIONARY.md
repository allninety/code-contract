# Feature dictionary — example (payments API, English-only)

Owner block on the left, agent block on the right, atom-ID shared, `status` = single-product snapshot.
(中文 columns dropped — this owner is monolingual.)

| ID     | English            | semantic (plain: what it does / what you'd see)            | where (owner touches)   | Feature Atom        | code anchor (file:line)        | Code Atom          | status   |
|--------|--------------------|-----------------------------------------------------------|-------------------------|---------------------|--------------------------------|--------------------|----------|
| F-401  | Reject no-token    | A request with no login token is refused, not served      | any protected endpoint  | AUTH.rejectMissing  | auth.py:40                     | CODE.authGuard     | ✅ ok    |
| F-cap  | Page-size cap      | Asking for more rows than allowed still returns at most 100 | list endpoints, ?limit | LIST.pageCap        | list.py:88                     | CODE.listPaging    | 🔴 broken |
| F-idem | Idempotent charge  | Submitting the same charge twice charges the card once     | POST /charge, idem key  | CHARGE.idempotent   | charge.py:120 · store.py:55    | CODE.chargeDedup   | 🟡 unverified |

Status: `✅ ok` present & traceable · `🟡 unverified` needs a runtime check · `🟠 unwired` model exists, nothing consumes it · `🔴 broken` promise not honored · `🟣 new` outside baseline.
