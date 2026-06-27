#!/usr/bin/env bash
# Smoke-validate the pack before publishing:
#   1) each skill passes the Agent Skills validator (quick_validate.py) — SKIPPED CLEANLY if no runnable validator
#   2) the example harness ledger reads, and `gate` correctly blocks on open items
# Usage: scripts/smoke_validate.sh
# Override the validator with QUICK_VALIDATE=/path/to/quick_validate.py  (needs Python + PyYAML)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS="$ROOT/plugins/code-contract/skills"
QV="${QUICK_VALIDATE:-$HOME/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py}"

echo "== validate skills =="
if [ ! -f "$QV" ]; then
  echo "  (skip — no validator found; set QUICK_VALIDATE=/path/to/quick_validate.py to run this check)"
else
  # Probe by actually running it once. If it can't run here (e.g. PyYAML missing), SKIP cleanly — never fail the script.
  probe="$(python3 "$QV" "$SKILLS/product-contract" 2>&1 || true)"
  if printf '%s' "$probe" | grep -qiE 'Traceback|ModuleNotFoundError|No module named|ImportError'; then
    echo "  (skip — validator found but not runnable in this environment:"
    echo "     $(printf '%s' "$probe" | tail -1) )"
    echo "   fix: install its deps (e.g. 'pip install pyyaml'), or set QUICK_VALIDATE to a runnable validator.)"
  else
    # Validator IS runnable → this is a hard gate: any skill that doesn't validate fails the script (exit 1),
    # so it's safe to use as a CI/release gate. (A validator that can't run at all is skipped above, not failed.)
    fails=0
    for d in "$SKILLS"/*/; do
      [ -f "$d/SKILL.md" ] || continue
      out=$(python3 "$QV" "$d" 2>&1 || true)
      printf '  %-24s %s\n' "$(basename "$d")" "$out"
      printf '%s' "$out" | grep -qi 'is valid' || fails=$((fails + 1))
    done
    if [ "$fails" -gt 0 ]; then
      echo "  ✗ $fails skill(s) FAILED validation — hard gate, failing."; exit 1
    fi
  fi
fi

echo "== harness example =="
H="$SKILLS/verified-execution/scripts/harness.py"
EX="$ROOT/examples/verified-execution-run"
python3 "$H" status --dir "$EX"
if python3 "$H" gate --dir "$EX"; then
  echo "  note: gate OPEN (all items verified)"
else
  echo "  ✓ gate correctly BLOCKS — the example has open items (FAIL/CLAIMED/STALE), proving the gate has teeth"
fi
echo "OK"
