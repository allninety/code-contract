# Contributing

Thanks for considering a contribution.

## Principles this pack holds itself to
- **Test absorbed ideas before trusting them.** If you change an output rule or a method step, back it with evidence (a ground-truthed comparison, a repro), the way `parity-audit/references/ab-test-enumerate-vs-patterns.md` does. Reputation of a source ≠ fit for this job.
- **No unbacked empirical claims.** "An A/B showed…", "a test confirmed…", star counts — every such claim must point at an inspectable artifact in-repo, or be softened to a clearly-labeled observation.
- **Owner-face language stays plain.** In `product-contract` dictionaries, the owner columns must be readable by someone who has never seen the code. `style.anim` is not "what the owner does."
- **The gate keeps its teeth.** Don't weaken `verified-execution` so the implementer can self-certify silently. Changes to `harness.py` should preserve: append-only ledger, hashed DoD, self-cert flag, stale-PASS downgrade.

## How to propose a change
1. Open an issue describing the gap and (for behavior changes) how you'll verify it.
2. Keep changes surgical — match surrounding style; don't refactor unrelated prose.
3. For `harness.py`, include a smoke test in the PR description (init → add → claim → verdict → status → gate) showing the new behavior.
4. Bump the version in `metadata.version` of the affected `SKILL.md` (the Agent Skills spec rejects a top-level `version` key — keep it under `metadata`), and add a `CHANGELOG.md` entry. The `plugin.json` version tracks the pack.

## Scope
This pack is intentionally three focused skills, not a framework. New skills should compose with the atom-ID spine, not duplicate the depth/structure/gate split.
