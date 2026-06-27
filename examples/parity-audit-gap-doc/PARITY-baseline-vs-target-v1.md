# Parity audit: payments-api (baseline) vs payments-api-rewrite (target) — v1 (example)

> Generated: 6 dimensions audited in parallel · 12 capabilities checked · 9 at parity · 3 gaps
> (blocker 1 / major 1 / minor 1). Baseline = the delivery standard; this lists only where the target diverges.
> *(Illustrative example — small and synthetic to show the shape.)*

## Root-cause synthesis (the 3 gaps collapse to 2 causes)
1. **Lossy request-validation adapter** — the rewrite's middleware drops constraints the baseline enforced (explains F-cap + the 422 shape). Fix the adapter once → closes 2.
2. **Idempotency not ported** — a whole behavior left unimplemented (F-idem).

## BLOCKER (1)
### 1. Page-size cap not enforced  [divergent]  · atom `LIST.pageCap` (F-cap)
- baseline: `list.py:88` clamps `limit` to 100 always · target: `list_v2.py:60` clamps only when `limit` is unset
- `GET /items?limit=9999` returns 9999 rows in the target — the cap is a no-op. Must clamp on every request.

## MAJOR (1)
### 2. Idempotent charge missing  [missing]  · atom `CHARGE.idempotent` (F-idem)
- baseline: `charge.py:120` + `store.py:55` dedupe by idem key · target: `—` (no dedup path)
- Two identical `POST /charge` with one idem key charge the card twice. Must dedupe before charging.

## MINOR (1)
### 3. 422 error body lost `fields[]`  [partial]  · atom `ERROR.shape`
- baseline: `errors.py:55` returns `{error, fields[]}` · target: `errors_v2.py:31` returns `{error}` only
- Clients that surfaced per-field messages now get none. Restore `fields[]`.

## At parity (9) — not listed individually here; e.g. AUTH.rejectMissing (F-401) ✅, plus 8 others.
