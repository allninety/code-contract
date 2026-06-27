# Parity integration — turning parity-audit output into contract artifacts

Use when building a contract for a rewrite / migration / refactor / fork / clone where a trustworthy baseline exists.

## Boundary (do not merge the two skills)
- **parity-audit** discovers evidence-backed differences between baseline and target (the depth/evidence engine).
- **product-contract** turns those differences into durable vocabulary, atoms, trace links, and coverage obligations
  (the structure/durability layer).

## Sequence
1. Run or consume a parity-audit against the baseline + target.
2. Extract the **audited capabilities** (not only the gaps) — the at-parity items are atoms too.
3. Convert every blocker/major/minor finding → affected **User Feature Atom**.
4. Convert baseline/new `file:line` evidence → **dictionary code anchors** + trace-link notes.
5. Convert each **root cause** → a **Code Capability Atom** responsibility (or a missing trace link).
6. Convert each **verification limit** → a **coverage gap** / `🟡 待验证` status.
7. Create **OWNER-TO-CODE** and **CODE-TO-OWNER** workflow items for the top gaps.

## Mapping table
| parity-audit artifact | product-contract artifact |
|---|---|
| capability dimension | feature category / domain |
| capability item | User Feature Atom |
| baseline `file:line` | baseline evidence / dictionary code anchor |
| target `file:line` | Code Capability Atom source / trace note |
| blocker / major / minor | per-target `audit-results/ATOM-STATUS-<target>` entry (🔴/🟠) + coverage priority |
| root cause | Code Capability responsibility gap |
| at-parity item | `✅` in `ATOM-STATUS-<target>` (the atom is unchanged) |
| verification limit | `🟡 待验证` + coverage gap |
| recommended fix order | `NEXT-PASS.md` + workflow tasks |

## Quality gate (the contract isn't complete until)
- every **blocker** maps to at least one User Feature Atom **and** one Code Capability Atom;
- every visible UI/export **regression** appears in the dictionary;
- every high-risk **export / persistence / native-bridge** item has a trace link;
- every parity **verification limit** appears in coverage as a gap or a manual check.
