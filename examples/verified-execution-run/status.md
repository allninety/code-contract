# verified-execution status — 1/4 VERIFIED

```
1/4 VERIFIED

✓ VERIFIED  A1         auth: 401 on missing token
    └ curl without token → 401 {error:unauthorized}; matches spec
✗ FAIL      A2         pagination: page size cap
    └ limit=9999 returned 9999 rows — cap not enforced
◐ CLAIMED   A3         idempotency: repeated POST
⚠ STALE     A4         error shape: 422 body
    └ ⚠goalpost moved since PASS — re-verify. 422 body had {error,fields}; matches
```
