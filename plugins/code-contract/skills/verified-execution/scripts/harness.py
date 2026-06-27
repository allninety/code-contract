#!/usr/bin/env python3
"""verified-execution harness — append-only contract + ledger + gate.

Teeth: an INDEPENDENT verifier (a separate agent) writes verdicts here; this script
computes state DETERMINISTICALLY so the implementer can't fudge "done". The contract is
append-only and the DoD is hashed, so moving the goalposts is visible. The human reads
`status` / uses `gate` as the final block.

Files live in ./.harness/ by default — override with `--dir <path>` or $HARNESS_DIR (e.g. point at
docs/product-contract-v1/execution-ledger to co-locate the ledger with the product contract). Stdlib only.
"""
import argparse, hashlib, json, os, sys
from datetime import datetime

DIR = os.environ.get("HARNESS_DIR", ".harness")
def CONTRACT(): return os.path.join(DIR, "contract.jsonl")
def LEDGER():   return os.path.join(DIR, "ledger.jsonl")

def _now():  return datetime.now().isoformat(timespec="seconds")
def _hash(s): return hashlib.sha256((s or "").strip().encode()).hexdigest()[:12]
def _append(path, obj):
    os.makedirs(DIR, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
def _read(path):
    out = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try: out.append(json.loads(line))
                    except Exception: pass
    return out

def _contract_map():
    m = {}
    for it in _read(CONTRACT()):   # latest add for an id wins (and is flagged at add time)
        m[it["id"]] = it
    return m

def cmd_init(a):
    os.makedirs(DIR, exist_ok=True)
    for p in (CONTRACT(), LEDGER()):
        if not os.path.exists(p): open(p, "a").close()
    print(f"harness ready in {DIR}/  (contract.jsonl, ledger.jsonl)")

def cmd_add(a):
    existing = _contract_map().get(a.id)
    h = _hash(a.dod)
    if existing and existing.get("dodHash") != h:
        print(f"⚠️  item {a.id} re-added with a DIFFERENT DoD (goalpost move) — kept as a visible amendment.", file=sys.stderr)
    _append(CONTRACT(), {"id": a.id, "title": a.title, "ref": a.ref, "dod": a.dod, "dodHash": h, "at": _now()})
    print(f"added {a.id}  (DoD hash {h})")

def cmd_import(a):
    """Bulk-add items from a JSONL file: one {id,title,ref,dod} per line."""
    cm = _contract_map(); n = 0
    for it in _read(a.file):
        if not all(k in it for k in ("id", "title", "ref", "dod")):
            print(f"skip (need id/title/ref/dod): {it}", file=sys.stderr); continue
        h = _hash(it["dod"]); ex = cm.get(it["id"])
        if ex and ex.get("dodHash") != h:
            print(f"⚠️  {it['id']} re-imported with a different DoD — kept as a visible amendment.", file=sys.stderr)
        _append(CONTRACT(), {"id": it["id"], "title": it["title"], "ref": it["ref"], "dod": it["dod"], "dodHash": h, "at": _now()})
        n += 1
    print(f"imported {n} item(s) from {a.file}")

def cmd_claim(a):
    _append(LEDGER(), {"item": a.id, "event": "claim", "what": a.what, "by": a.by, "at": _now()})
    print(f"claimed {a.id}  (a claim is NOT 'done' — it awaits an independent verdict)")

def cmd_verdict(a):
    cm = _contract_map()
    if a.id not in cm:
        print(f"✗ no contract item {a.id} — `add` it first", file=sys.stderr); sys.exit(2)
    v = a.verdict.upper()
    if v not in ("PASS", "FAIL"):
        print("verdict must be PASS or FAIL", file=sys.stderr); sys.exit(2)
    tampered = a.dod is not None and _hash(a.dod) != cm[a.id]["dodHash"]
    if tampered:
        print(f"⚠️  DoD given to verdict does NOT match the contract's DoD for {a.id} (possible goalpost move).", file=sys.stderr)
    # self-certification guard: a verdict from the same identity that CLAIMED the work has no teeth.
    workers = {ev.get("by") for ev in _read(LEDGER())
               if ev.get("item") == a.id and ev.get("event") == "claim" and ev.get("by")}
    self_cert = a.by is not None and a.by in workers
    if self_cert:
        print(f"⚠️  verifier '{a.by}' also CLAIMED {a.id} — self-certification has no teeth; get an independent verifier.", file=sys.stderr)
    _append(LEDGER(), {"item": a.id, "event": "verdict", "verdict": v, "evidence": a.evidence,
                       "by": a.by, "dodTampered": tampered, "selfCertified": self_cert,
                       "dodHashAtVerdict": cm[a.id]["dodHash"], "at": _now()})  # record the DoD in force, so a later change is detectable
    print(f"recorded {a.id}: {v}"
          f"{'  (DoD TAMPER FLAG)' if tampered else ''}{'  (⚠SELF-CERT)' if self_cert else ''}")

def _state():
    cm = _contract_map()
    st = {i: {"status": "PLANNED", "note": ""} for i in cm}
    for ev in _read(LEDGER()):
        it = ev.get("item")
        if it not in st: continue
        if ev.get("event") == "claim":
            if st[it]["status"] in ("PLANNED", "FAIL", "STALE"): st[it]["status"] = "CLAIMED"
        elif ev.get("event") == "verdict":
            st[it]["status"] = "VERIFIED" if ev.get("verdict") == "PASS" else "FAIL"
            flags = ("⚠DoD-tampered " if ev.get("dodTampered") else "") + ("⚠self-certified " if ev.get("selfCertified") else "")
            st[it]["note"] = flags + (ev.get("evidence") or "")
            # stale-PASS teeth: if the contract DoD changed AFTER this PASS, the verdict no longer covers the
            # current goalpost — downgrade VERIFIED→STALE so status/gate surface the moved goalpost (not just stderr at add).
            if st[it]["status"] == "VERIFIED":
                vh = ev.get("dodHashAtVerdict")
                if vh is not None and vh != cm[it]["dodHash"]:
                    st[it]["status"] = "STALE"
                    st[it]["note"] = "⚠goalpost moved since PASS — re-verify. " + (ev.get("evidence") or "")
    return cm, st

def cmd_status(a):
    cm, st = _state()
    if not cm: print("no contract items yet — `add` some."); return
    order = list(cm.keys())
    n = len(order); verified = sum(1 for i in order if st[i]["status"] == "VERIFIED")
    icon = {"PLANNED": "·", "CLAIMED": "◐", "VERIFIED": "✓", "FAIL": "✗", "STALE": "⚠"}
    lines = [f"{verified}/{n} VERIFIED", ""]
    for i in order:
        s = st[i]["status"]
        lines.append(f"{icon.get(s, '?')} {s:9} {i:10} {cm[i]['title'][:48]}")
        note = st[i]["note"].strip()
        if note: lines.append(f"    └ {note[:96]}")
    print("\n  " + "\n  ".join(lines) + "\n")
    if getattr(a, "write", False):  # --write: drop a human-readable snapshot into the ledger dir (execution-ledger/status.md)
        os.makedirs(DIR, exist_ok=True)
        path = os.path.join(DIR, "status.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# verified-execution status — {verified}/{n} VERIFIED\n\n```\n" + "\n".join(lines) + "\n```\n")
        print(f"  (wrote {path})")

def cmd_gate(a):
    cm, st = _state()
    bad = [i for i in cm if st[i]["status"] != "VERIFIED"]
    n = len(cm); ok = n - len(bad)
    if bad:
        print(f"GATE: BLOCKED — {ok}/{n} verified; NOT done: {', '.join(bad)}")
        sys.exit(1)
    print(f"GATE: OPEN — {ok}/{n} verified")
    sys.exit(0)

def main():
    p = argparse.ArgumentParser(description="verified-execution harness (append-only contract + ledger + gate)")
    common = argparse.ArgumentParser(add_help=False)  # --dir on every subcommand → co-locate under the contract package
    common.add_argument("--dir", default=os.environ.get("HARNESS_DIR", ".harness"),
                        help="output dir for contract.jsonl/ledger.jsonl/status.md (default .harness or $HARNESS_DIR; "
                             "e.g. docs/product-contract-v1/execution-ledger to co-locate with the product contract)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", parents=[common], help="create the harness dir").set_defaults(fn=cmd_init)
    s = sub.add_parser("add", parents=[common], help="append a contract item"); s.add_argument("id"); s.add_argument("title"); s.add_argument("ref", help="baseline/spec reference"); s.add_argument("dod", help="observable definition-of-done"); s.set_defaults(fn=cmd_add)
    s = sub.add_parser("import", parents=[common], help="bulk-add items from a JSONL file"); s.add_argument("file", help="JSONL: one {id,title,ref,dod} per line"); s.set_defaults(fn=cmd_import)
    s = sub.add_parser("claim", parents=[common], help="worker logs intent (not done)"); s.add_argument("id"); s.add_argument("what", help="what was changed (file:line)"); s.add_argument("--by", default=None, help="identity of who did the work; enables the self-certification guard"); s.set_defaults(fn=cmd_claim)
    s = sub.add_parser("verdict", parents=[common], help="record the independent verifier's PASS/FAIL"); s.add_argument("id"); s.add_argument("verdict", help="PASS|FAIL"); s.add_argument("evidence"); s.add_argument("--dod", default=None, help="the DoD the verifier checked (tamper-checked vs contract)"); s.add_argument("--by", default=None, help="identity of the verifier; flagged if it matches the worker who claimed"); s.set_defaults(fn=cmd_verdict)
    s = sub.add_parser("status", parents=[common], help="human-readable state"); s.add_argument("--write", action="store_true", help="also write status.md into the harness dir"); s.set_defaults(fn=cmd_status)
    sub.add_parser("gate", parents=[common], help="exit 1 if any item not VERIFIED").set_defaults(fn=cmd_gate)
    a = p.parse_args()
    global DIR; DIR = a.dir
    a.fn(a)

if __name__ == "__main__":
    main()
