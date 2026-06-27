# A/B test — why this skill ENUMERATES (and rejects "patterns over lists")

This records the experiment behind two output rules, so the decisions are defensible if later challenged.

## Why we ran it
Two techniques came from GSD's `codebase-mapper` agent (a common code-mapping approach) and needed validating before being trusted:
- **②** "describe the **pattern**, not a bare list" (output discipline)
- **①** auditors write findings to disk and return only **counts** (context-lean)

A reasonable-sounding principle from a proven project is not evidence it fits THIS job. So we tested, rather than asserted.

## Design (one pass, ground-truthed)
- **Vehicle**: the editor **control-surface** dimension of a real baseline-vs-rewrite (a renderer migration), where the
  baseline UI is unchanged but the rewrite's render contract silently drops/renames many controls.
- **Ground truth**: 17 distinct dead/divergent UI controls (each *should* be one actionable finding).
- **Auditors**: cold subagents (no prior context), all reading the **same** files in both trees.
- **Test ②**: 3× **ENUMERATE** ("one finding per control, exhaustive, never bundle") vs 3× **PATTERNS** (the ② wording).
  Metric: **recall** (of 17 controls) + **granularity** (total findings). *(One ENUMERATE run failed a structured-output
  retry → that arm is n=2; the separation is still clean.)*
- **Test ①**: a fixed 12-finding set → 2× **FULL** (findings inline) vs 2× **COUNTSDOC** (counts only, must read a doc).
  Metric: cluster count + whether the **dominant root cause** matches.

## Results
**② patterns-not-lists — recall-neutral, granularity-harmful**

| arm | granularity (findings) | recall (of 17) | hallucinated |
|---|---|---|---|
| ENUMERATE | 33, 34 → mean **33.5** | **17/17** | 0 |
| PATTERNS | 28, 23, 19 → mean **23.3** | **17/17** | 0 |

Both arms *mention* all 17 controls (recall preserved). But PATTERNS **bundles** distinct controls into single findings
(e.g. folds the 4 cover-scale sliders into one; folds caption-mode + 4 FX controls into one), cutting granularity ~30% —
and it worsens monotonically as the prose gets more "pattern-y" (28→23→19). A parity audit's deliverable is **one
actionable row per gap**, so bundling is a real loss.

**① counts+read-doc — neutral on quality**

FULL → 5 / 4 clusters; COUNTSDOC → 5 / 4 clusters; **same dominant root cause** ("lossy style contract"); judge verdict
**neutral**. Reading findings back from a doc clusters as well as inline — info is preserved, so it's a safe context valve.

## Decisions (now in SKILL.md)
- **Reject** "patterns over lists" for parity-audit. Enforce **one finding per distinct gap, exhaustive enumeration**.
  (`codebase-mapper`'s "patterns over lists" is right for *describing* a codebase, wrong for *enumerating* an audit —
  this skill deliberately inverts it.)
- **Keep** counts+write-to-disk as a **default-OFF scaling valve** — only when an audit won't fit the orchestrator's
  context.

## Meta-lesson
The harmful rule came from a well-regarded, widely-used tool. Reputation did not make it fit a different context — and
only the A/B caught it; the pre-test *assertion* (mine) guessed the wrong failure mode (predicted lower recall; the real
damage was lower granularity). **Test absorbed techniques against ground truth before trusting them.**
