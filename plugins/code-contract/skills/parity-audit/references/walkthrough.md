# parity-audit — walkthrough (a worked run)

You have a known-good **baseline** and a **rewrite/migration**, and you need the COMPLETE list of what the rewrite still
doesn't match — all at once, not discovered piecemeal.

## What YOU do (the whole user action)
```
/parity-audit
```
then tell it the two paths if it doesn't already know them, e.g.
> baseline = `<old-system>/src` (the known-good original), new = `<rewrite>/src` (the migration under audit)

Everything below is what the skill does FOR you. There is exactly **one checkpoint** where it pauses for your sign-off.

## What happens, step by step

**Step 1 — Frame (seconds).** It decides which side is the baseline (the standard of truth) vs the rewrite, and the
"truth standard" — *what observable artifact counts as "matches"* (for a renderer: the EXPORTED output, not the live
preview). No input from you.

**Step 2 — Discover the capability map → 🟦 YOUR ONE CHECKPOINT.** It reads the baseline and proposes ~8–15 capability
*dimensions* that cover the whole product (e.g. timing · captions · audio · color · transitions · export · the editor
control surface · …). It shows you the list. You glance for ~30s: *"did it miss an axis?"* → OK, or add one. **This tiny
checkpoint is what stops a whole area from becoming a permanent blind spot.**

**Step 3 — Audit (parallel, automatic).** One independent auditor per dimension runs at the same time, each reading
BOTH codebases and reporting every *missing / partial / divergent* behavior, with `file:line` on **both** sides +
a severity. You do nothing here.

**Step 4 — Synthesize (automatic).** It collapses the scattered findings into a few **root causes**, ranks by severity,
writes the complete list to `docs/audit/parity-<baseline>-vs-<new>-v1.md`, and gives you a digest.

## What you get (illustrative — figures from one real run; the audit doc itself isn't shipped in this pack)
> **188 capabilities checked · 100 at parity · 88 gaps** (5 blocker / 48 major / 34 minor). The 88 collapse to **6 root
> causes**; the biggest — a *lossy style contract* — explains ~half. Plus the doc listing every gap (file:line on both
> sides) and a recommended fix order (blockers → the dominant root cause → the rest).

## Then what
Hand that doc straight to **`/verified-execution "<doc path>"`** to actually close the gaps, each one confirmed by an
independent verifier (see that skill's walkthrough).

## If there's no trustworthy baseline
Say so — the audit weakens to a self/spec review. parity-audit is only as good as the reference it's measuring against.
```
