# Parity audit — simplified one-shot prompt

A short, self-contained prompt that triggers the same audit without the full skill. Fill in the two paths and (optionally)
the dimensions, then paste.

---

```
Do a COMPLETE capability-parity audit: BASELINE (the known-good / shipping reference) vs NEW (the rewrite/migration).
The baseline is the standard of truth — find every place NEW fails to match it. Don't redesign or "improve" anything;
just map divergence.

- BASELINE: <path / branch / dir>
- NEW:      <path / branch / dir>

First decide the TRUTH STANDARD — what observable artifact defines "matches"? (For a renderer it's the EXPORTED output,
not the live preview; for an API the response contract; for a UI the rendered result.) Audit against that, not the
nearest convenient surface.

Steps:
1. Skim the baseline and split the product into ~8–15 orthogonal capability DIMENSIONS that cover it (derive from the
   baseline's own modules — adapt to the domain). Force coverage by walking four angles: pipeline/entry points, the data
   model, the CONTROL SURFACE (every UI control / option / flag — enumerate these finely; a control that still shows but
   no longer affects output is the most common silent rewrite loss — don't bury them in one coarse "settings" dimension),
   and the output formats. List the dimensions and get my quick sign-off BEFORE the expensive fan-out.
2. For EACH dimension, run an independent auditor IN PARALLEL (one subagent per dimension). Each one reads the ACTUAL
   code in BOTH trees, enumerates every baseline capability in its dimension, checks NEW, and returns findings:
       { dimension, capability, status: full|partial|missing|divergent, severity: blocker|major|minor|ok,
         baseRef: "file:line", newRef: "file:line" or "—", detail }
   Hard rules: cite file:line on BOTH sides or it's not a finding; don't invent capabilities the baseline lacks; report
   the at-parity (ok) items too so coverage is visible.
3. SYNTHESIZE: cluster the scattered findings by ROOT CAUSE (scattered gaps usually share a few causes — a lossy adapter
   between layers, a config never plumbed through, a whole mode unimplemented); surface the dominant cause (fix once,
   kill many). Rank by severity.
4. WRITE the complete list to a versioned doc (docs/audit/parity-<baseline>-vs-<new>-v1.md): every finding with file:line
   on both sides, grouped by root cause + severity.
5. PRESENT a digest: headline counts (checked / at-parity / gaps by severity) → the root-cause synthesis FIRST → the
   blockers listed → the majors grouped by theme (not a flat dump) → a recommended fix order (blockers → dominant root
   cause → rest), each step to be verified against the baseline.

Where you can, verify behavior empirically (run both, diff the real output) rather than trusting code-reading alone.
```

---

## Even shorter (one-liner)

> Audit BASELINE `<path>` vs NEW `<path>` for complete capability parity: split into ~10 capability dimensions, run one
> parallel auditor per dimension reading both codebases, report every missing/partial/divergent behavior with file:line
> on both sides + severity, then group the gaps by root cause and give me a severity-ranked list with a fix order.
