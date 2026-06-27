# User Feature Atoms — example

One atom = one smallest observable promise. The "observable acceptance" is the DoD seed for verified-execution.

| ID     | English           | semantic (plain owner-language)                  | observable acceptance (DoD seed)                       | domain | status   |
|--------|-------------------|--------------------------------------------------|--------------------------------------------------------|--------|----------|
| F-401  | Reject no-token   | unauthenticated requests are refused             | `GET /me` without a token → `401 {error:'unauthorized'}` | auth   | ✅ ok    |
| F-cap  | Page-size cap     | over-large page requests are capped              | `GET /items?limit=9999` → returns at most 100 rows      | list   | 🔴 broken |
| F-idem | Idempotent charge | the same charge submitted twice charges once     | `POST /charge` twice with one idem key → exactly 1 charge | billing | 🟡 unverified |
