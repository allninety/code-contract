# verified-execution — walkthrough (a worked run)

You have a list of work — a parity-audit gap list, an implementation plan, any checklist — and you need each item
**actually done (independently verified)**, not just claimed done.

## What YOU do (the whole user action)
```
/verified-execution "<path to the list, e.g. the parity-audit gap doc>"
```
Then: **sign off the DoD list once** (Step A), and **read the account at the end** (Step C). That's your entire
involvement. You do **NOT** run python — Claude runs the harness + driver for you.

## What happens, step by step

**Step A — Build the contract → 🟦 YOUR ONE UP-FRONT CHECKPOINT.**
Claude reads your list and turns each item into a contract line:
`{ id, title, baseline/spec ref, DoD }` — where **DoD = an *observable* test of "truly done"** (something you can run or
see), not "the code looks right." For an 88-gap doc that's 88 lines. Claude shows you the DoD list; you glance and OK it
(or fix a DoD). **This is the only place it needs you up front, because the DoD is where the teeth bite.**
Under the hood Claude runs: `harness.py init`, then `harness.py import items.jsonl` (all items in one shot).

**Step B — Drive (automatic — one workflow, you do nothing).**
The driver runs each item: a **worker** makes the minimal change, then an **independent verifier** (fresh context,
adversarial, reads the REAL code + RUNS the DoD) records `PASS`/`FAIL` via the harness. Items run in parallel, isolated
so edits don't collide. You are NOT in this loop. A *claim* is never "done" — only the verifier's PASS is.

**Step C — Read the account → 🟦 YOUR FINAL GATE.**
You see (illustrative):
```
  62/88 VERIFIED
  ✓ VERIFIED  G1    anim selector wired through
  ✗ FAIL      G7    2K/4K still renders 1080p — scale not passed to renderMedia
  ◐ CLAIMED   G31   implemented, awaiting verdict
  ⚠ STALE     G44   goalpost moved since PASS — re-verify
  ...
```
`gate` exits non-zero while anything isn't `VERIFIED` — a real block, not a reminder. FAIL items are **reopened** — re-run
them (the bundled driver is single-pass, so re-invoke it for the failed items; it is not an automatic retry loop). You
**spot-check a few** (e.g. "show me G1's evidence") and make the go/no-go call.

## The honest part (don't skip)
Because Claude runs the harness, **your reading the account + spot-checking a sample is the last tooth.** Two ways:
- let Claude paste the `status` to you (convenient — but you're reading Claude's rendering of the ledger), or
- run `python3 ~/.claude/skills/verified-execution/scripts/harness.py status` / `gate` yourself — one read-only line,
  but you see the **raw ledger** directly (one notch more independent). It only prints; it changes nothing.

## The teeth, in one line
A claim is never "done"; only an **independent verifier's PASS** — recorded in an append-only, tamper-flagged ledger,
behind a blocking gate, all visible to you — is. The skill is instructions Claude follows; the *teeth* are the
independent verifier + the deterministic gate + you.

## Also works on
Not just parity-audit output — any **implementation plan** or **task list**, as long as each item gets an observable DoD.
```
