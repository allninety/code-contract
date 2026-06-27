---
name: verified-execution
description: >-
  Execute a list of work items (a parity-audit gap list, an implementation plan, any checklist) so that done means an
  INDEPENDENT verifier confirmed it against a written definition-of-done — NEVER the implementer's own claim. Use
  whenever completeness and honesty matter and the implementer (you / Claude) must not self-certify: closing audit
  gaps, executing a multi-step plan, make sure each item is ACTUALLY done, preventing said-100-did-40-drifted-to-15,
  any task where the user has been burned by claimed-but-not-real completion or by plans/tasks getting silently
  changed mid-flight. Closes items keyed to a shared atom-ID spine: product-contract freezes the atoms, parity-audit
  produces the gap list this closes, and this harness gates them. Prefer this over a plain TODO list or a promise to
  follow the plan whenever a soft checklist would just be edited or ignored — the whole point is a gate the
  implementer does not control.
license: MIT
metadata:
  version: 0.1.0
---

# Verified Execution (an enforcement harness)

## What this is for
The failure mode this kills: an implementer (human or AI) says "100 done," but actually did 40, discounted, got
sidetracked fixing a small bug, and landed at 15 — and **nobody could see it**, because the plan/checklist was owned by
the same implementer who could silently edit or abandon it. A promise, a TODO list, a memory, or "I'll follow the plan"
are all **soft** — the implementer controls them, so they aren't constraints.

This harness makes "done" mean: **an independent verifier, reading the real code/output, confirmed the item against a
written, observable definition-of-done — and the verdict went into a ledger the implementer can't fudge.**

## The one principle that gives it teeth
**The implementer does not control the gate.** Teeth come from exactly three places — everything else is theater:
1. **An independent verifier** — a *separate, fresh-context* agent with an *adversarial* prompt that reads REALITY (the
   actual code/output), not the implementer's summary.
2. **Deterministic, un-fudgeable plumbing** — the contract and the pass/fail ledger are FILES + a SCRIPT, not an agent's
   say-so. Verdicts flow verifier → script → ledger. (`scripts/harness.py`.)
3. **The human as final gate** — you read the ledger; nothing ships without you. The harness's job is to make the
   implementer's real state *impossible to hide from you*.

Corollary (respect it): **agents are for judgment, scripts are for the un-fudgeable parts.** Adding more agents adds
handoffs and more places to drift. Keep the agent count minimal; push the immutable parts into scripts.

## Minimal roles (don't add more)
| role | agent or mechanism | does |
|---|---|---|
| **Worker / implementer** (often the main session) | agent | one item at a time, minimal change, writes a CLAIM. **May NOT mark itself done.** |
| **Verifier** | agent — *separate, fresh context, adversarial* | reads the contract item + the raw diff + RUNS the DoD; returns structured PASS/FAIL + evidence. **The teeth.** |
| **Contract + ledger + gate** | **mechanism** (`scripts/harness.py`, append-only files) | records claims/verdicts deterministically; computes the gate; can't be talked out of it. |
| **You** | human | final gate — read `status`, reject anything. |

Scale-only (skip for a few items; add when MANY items interact): an **integration auditor** — a periodic system-level
sweep checking that closing item A didn't break B and that the ledger matches reality. Don't add 5th/6th roles otherwise.

## The contract & the Definition of Done (DoD)
Each item needs a DoD that is **observable** — a test you can RUN or SEE, tied to the baseline/spec it must match — not
"the code looks right." Code-reading misjudges behavior (that's how false "done" happens). Examples of a good DoD:
"set anim=Blur, render frame N; caption enters with blur (differs from anim=fade)"; "POST /x with bad body returns 422
with `{error}` matching the baseline"; "run test T, it passes." The contract is **append-only** — changing an item's DoD
after the fact is how the goalposts move, so the script hashes the DoD: it flags a mismatch at verdict time, **and if an
item's DoD changes *after* it passed, `status`/`gate` downgrade it from VERIFIED to STALE** — a moved goalpost can't hide
behind an old ✓.

## The DoD is the owner↔code bridge
A good DoD states the test in **owner-observable** terms (what you'd see or run) yet is checked against the **code** — so
it is the shared language between the *application* dimension (the owner) and the *code* dimension (the agent). When the
items come from a **`product-contract` atom registry** (the shared spine) — or a `parity-audit` gap list keyed to it —
**reuse the stable atom-IDs** as the contract item IDs. Then *freeze → audit → close → verify* all key off the same ID:
`product-contract` froze the atom, `parity-audit` found it non-passing on this target, this harness closes it. A PASS
closes the atom **only for the named target + DoD** — it does not delete the atom or erase parity evidence for other
targets. The owner can trace any verdict back to the feature they recognize, and any feature back to its verdict. (Spine
protocol: `product-contract`'s `references/three-skill-coordination.md`.)

## The loop (how to use it)
```
export HARNESS_DIR=docs/product-contract-v1/execution-ledger     # co-locate the ledger under the contract package
harness.py init                                  # create the ledger dir (contract.jsonl, ledger.jsonl); default ./.harness/
#   (HARNESS_DIR applies to every command below; per-command alt: `--dir <path>` on any subcommand)
harness.py import items.jsonl                     # bulk-add many items ({id,title,ref,dod} per line)
#   (or one at a time:)  harness.py add G1 "title" "baseline ref" "DoD"
# for each item:
harness.py claim G1 "what I changed (file:line)" # worker logs intent; cannot self-pass
#   → implement the minimal change
#   → spawn the VERIFIER subagent (fresh context) with: the contract item + the raw diff + the adversarial prompt below
harness.py verdict G1 PASS "evidence: rendered blur≠fade, matches baseline" \
           --dod "<the same DoD text>"           # records verifier's verdict; tamper-checks the DoD hash
harness.py status --write                        # human reads this; --write also drops status.md into the ledger dir
harness.py gate                                  # exits non-zero if ANY item isn't PASS — a literal block
```
- **FAIL → the item reopens; the worker redoes it. PASS → done.** The worker never types its own PASS — the verdict is
  the verifier's, recorded by the script.
- **Tangents go to the backlog, not inline.** A bug found mid-item → `harness.py add` it (or spawn_task) — do NOT drop
  the current item to chase it. Chasing tangents is the move that turns 100 into 15.

## The verifier prompt (paste this into the verifier subagent — the teeth live here)
> You are an independent verifier with NO prior context. **Assume the item is NOT done until the real code/output proves
> it.** You are given: the contract item (what + baseline/spec ref + the DoD) and the raw diff/files the worker touched.
> Do NOT trust the worker's claim — a claim documents what they SAID, not what the code does. Read the baseline/spec
> reference and the new code yourself, **RUN or OBSERVE the DoD**, and decide. Return `PASS` only if you independently
> confirmed the DoD holds; otherwise `FAIL` with concrete evidence of what is still wrong. Output structured: {verdict,
> evidence, dod}.

## Teeth-or-theater checklist (use this to judge ANY harness — including mine)
Any "no" means it's theater, with no teeth:
- Is the verifier a *different* agent that did NOT do the work (fresh context)?
- Does it read the *real code/output*, or the implementer's summary?
- Is "done" an *observable, runnable* test, or "looks right"?
- Is the contract/DoD safe from *silent* edits (append-only + hash-checked)?
- Does the gate actually *block* (FAIL stops progress), or just warn?
- Can *you* see the full state and reject it?

## Pitfalls
- **Verifier reads the claim, not reality.** Then it's a rubber stamp. Give it the raw diff + DoD, never my narrative.
- **DoD is "looks correct."** Unverifiable → false PASS. Make every DoD runnable/observable.
- **Silent contract edits.** Moving the DoD to fit what was done removes the teeth. Append-only + hash flag.
- **Advisory gate.** A gate that doesn't block is a reminder. Use `gate` exit code; the human enforces.
- **Skipping the human.** The agents make state visible *so you can reject it* — they don't replace you. Never delegate
  the final gate away.
- **Role inflation.** More agents = more drift. Two agents (worker, verifier) + scripts + you is the whole thing.

## Verification (of the harness itself)
- Confirm the verifier actually RAN the DoD — its verdict must contain concrete observed evidence, not "looks fine."
- Spot-check a PASS by re-running its DoD yourself; the ledger must match reality.
- Confirm no item's DoD changed since it was added (`harness.py` flags this).

## Honest limit
In a single Claude session, the orchestrator is still Claude (it spawns the verifier, runs the script). So this is not
a hardware-enforced constraint. Its real teeth are: (1) the verifier's *independence* (a fresh, adversarial agent
reading reality is far harder to fool than self-checking), (2) the *deterministic* contract/ledger/gate (a script's
verdict can't be argued with, and changes are visible — the two classic dodges are surfaced automatically: **grading your
own work** is flagged when `verdict --by` matches the worker who claimed, and **moving the goalpost after a PASS**
downgrades the item to STALE), and (3) *you* as the final gate. It makes false "done" much harder and always *visible* —
not impossible. That visibility, plus you, is the point.

## Scripts & the driver (so you don't run the loop N times by hand)
`scripts/harness.py` — stdlib Python, append-only `{contract,ledger}.jsonl` (default `./.harness/`; override with
`--dir <path>` on any subcommand or `$HARNESS_DIR` to co-locate under the contract package's `execution-ledger/`).
Subcommands: `init`, `add`, `import` (bulk-add from a JSONL of `{id,title,ref,dod}`), `claim`, `verdict`,
`status` (`--write` also emits `status.md`), `gate`. `--help` for usage.

For many items (e.g. an 88-gap list) you do **not** drive cycles manually. Use the **driver** —
`references/driver.js`, a Workflow skeleton that auto-runs `worker → independent verifier → harness verdict` over every
item (pipeline; worker runs in an isolated worktree so parallel edits don't collide). The driver orchestrates and the
agents call `harness.py`; **your effort stays batch-level**: bless the DoD list once, then read `status`, spot-check a
sample, and use `gate`. You're the final gate, not the loop runner.
