#!/usr/bin/env python3
"""verified-execution harness —— 只追加的 契约 + 账本 + 闸门。

牙齿:一个 独立验收方(单独的 agent)把结论写在这里;本脚本 确定性地 算出状态,
让实施者糊弄不了"完成"。契约只追加、DoD 做哈希,所以挪门柱会被看见。由人读
`status` / 用 `gate` 当最终拦截。

文件默认在 ./.harness/ —— 用 `--dir <path>` 或 $HARNESS_DIR 改(比如指到
docs/product-contract-v1/execution-ledger,把账本和产品契约放一起)。纯标准库。

(状态机内部用英文 token:PLANNED/CLAIMED/VERIFIED/FAIL/STALE;显示时映射成中文。
 JSON 字段名、子命令名、PASS/FAIL 保持英文,以便与英文版 harness 的账本互通。)
"""
import argparse, hashlib, json, os, sys
from datetime import datetime

DIR = os.environ.get("HARNESS_DIR", ".harness")
def CONTRACT(): return os.path.join(DIR, "contract.jsonl")
def LEDGER():   return os.path.join(DIR, "ledger.jsonl")

# 状态 token → 中文显示
LABEL = {"PLANNED": "待办", "CLAIMED": "已声称", "VERIFIED": "已验收", "FAIL": "未过", "STALE": "已过期"}

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
    for it in _read(CONTRACT()):   # 同一 id 最后一次 add 生效(并在 add 时被标出)
        m[it["id"]] = it
    return m

def cmd_init(a):
    os.makedirs(DIR, exist_ok=True)
    for p in (CONTRACT(), LEDGER()):
        if not os.path.exists(p): open(p, "a").close()
    print(f"harness 就绪:{DIR}/(contract.jsonl, ledger.jsonl)")

def cmd_add(a):
    existing = _contract_map().get(a.id)
    h = _hash(a.dod)
    if existing and existing.get("dodHash") != h:
        print(f"⚠️  条目 {a.id} 用 不同的 DoD 重新加入(挪门柱)—— 作为一次可见的修订保留。", file=sys.stderr)
    _append(CONTRACT(), {"id": a.id, "title": a.title, "ref": a.ref, "dod": a.dod, "dodHash": h, "at": _now()})
    print(f"已加入 {a.id}(DoD 哈希 {h})")

def cmd_import(a):
    """从 JSONL 文件批量加入条目:每行一个 {id,title,ref,dod}。"""
    cm = _contract_map(); n = 0
    for it in _read(a.file):
        if not all(k in it for k in ("id", "title", "ref", "dod")):
            print(f"跳过(需要 id/title/ref/dod): {it}", file=sys.stderr); continue
        h = _hash(it["dod"]); ex = cm.get(it["id"])
        if ex and ex.get("dodHash") != h:
            print(f"⚠️  {it['id']} 用不同的 DoD 重新导入 —— 作为一次可见的修订保留。", file=sys.stderr)
        _append(CONTRACT(), {"id": it["id"], "title": it["title"], "ref": it["ref"], "dod": it["dod"], "dodHash": h, "at": _now()})
        n += 1
    print(f"已从 {a.file} 导入 {n} 条")

def cmd_claim(a):
    _append(LEDGER(), {"item": a.id, "event": "claim", "what": a.what, "by": a.by, "at": _now()})
    print(f"已记录 claim {a.id}(claim 不等于'完成' —— 它在等一个独立结论)")

def cmd_verdict(a):
    cm = _contract_map()
    if a.id not in cm:
        print(f"✗ 没有契约条目 {a.id} —— 先 `add` 它", file=sys.stderr); sys.exit(2)
    v = a.verdict.upper()
    if v not in ("PASS", "FAIL"):
        print("verdict 必须是 PASS 或 FAIL", file=sys.stderr); sys.exit(2)
    tampered = a.dod is not None and _hash(a.dod) != cm[a.id]["dodHash"]
    if tampered:
        print(f"⚠️  给 verdict 的 DoD 和 {a.id} 契约里的 DoD 不一致(可能在挪门柱)。", file=sys.stderr)
    # 自证守卫:由 CLAIM 了这活的同一身份做的 verdict,没有牙齿。
    workers = {ev.get("by") for ev in _read(LEDGER())
               if ev.get("item") == a.id and ev.get("event") == "claim" and ev.get("by")}
    self_cert = a.by is not None and a.by in workers
    if self_cert:
        print(f"⚠️  验收方 '{a.by}' 同时也 CLAIM 了 {a.id} —— 自己验自己没有牙齿;去找一个独立验收方。", file=sys.stderr)
    _append(LEDGER(), {"item": a.id, "event": "verdict", "verdict": v, "evidence": a.evidence,
                       "by": a.by, "dodTampered": tampered, "selfCertified": self_cert,
                       "dodHashAtVerdict": cm[a.id]["dodHash"], "at": _now()})  # 记下当时生效的 DoD,好让日后的改动可被发现
    print(f"已记录 {a.id}: {v}"
          f"{'  (DoD 篡改标记)' if tampered else ''}{'  (⚠自证)' if self_cert else ''}")

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
            flags = ("⚠DoD被改 " if ev.get("dodTampered") else "") + ("⚠自证 " if ev.get("selfCertified") else "")
            st[it]["note"] = flags + (ev.get("evidence") or "")
            # stale-PASS 牙齿:若契约 DoD 在这次 PASS 之后变了,结论就不再覆盖当前门柱 ——
            # 把 VERIFIED 降级为 STALE,让 status/gate 暴露挪过的门柱(不只在 add 时打 stderr)。
            if st[it]["status"] == "VERIFIED":
                vh = ev.get("dodHashAtVerdict")
                if vh is not None and vh != cm[it]["dodHash"]:
                    st[it]["status"] = "STALE"
                    st[it]["note"] = "⚠PASS 后门柱被挪 —— 请重验。 " + (ev.get("evidence") or "")
    return cm, st

def cmd_status(a):
    cm, st = _state()
    if not cm: print("还没有契约条目 —— 先 `add` 一些。"); return
    order = list(cm.keys())
    n = len(order); verified = sum(1 for i in order if st[i]["status"] == "VERIFIED")
    icon = {"PLANNED": "·", "CLAIMED": "◐", "VERIFIED": "✓", "FAIL": "✗", "STALE": "⚠"}
    lines = [f"{verified}/{n} 已验收", ""]
    for i in order:
        s = st[i]["status"]
        lines.append(f"{icon.get(s, '?')} {LABEL.get(s, s):6} {i:10} {cm[i]['title'][:48]}")
        note = st[i]["note"].strip()
        if note: lines.append(f"    └ {note[:96]}")
    print("\n  " + "\n  ".join(lines) + "\n")
    if getattr(a, "write", False):  # --write:把人类可读快照落到账本目录(execution-ledger/status.md)
        os.makedirs(DIR, exist_ok=True)
        path = os.path.join(DIR, "status.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# verified-execution 状态 — {verified}/{n} 已验收\n\n```\n" + "\n".join(lines) + "\n```\n")
        print(f"  (已写 {path})")

def cmd_gate(a):
    cm, st = _state()
    bad = [i for i in cm if st[i]["status"] != "VERIFIED"]
    n = len(cm); ok = n - len(bad)
    if bad:
        print(f"闸门:已拦 —— {ok}/{n} 通过;未完成:{', '.join(bad)}")
        sys.exit(1)
    print(f"闸门:放行 —— {ok}/{n} 通过")
    sys.exit(0)

def main():
    p = argparse.ArgumentParser(description="verified-execution harness(只追加的 契约 + 账本 + 闸门)")
    common = argparse.ArgumentParser(add_help=False)  # 每个子命令都带 --dir → 共址到契约包下
    common.add_argument("--dir", default=os.environ.get("HARNESS_DIR", ".harness"),
                        help="contract.jsonl/ledger.jsonl/status.md 的输出目录(默认 .harness 或 $HARNESS_DIR;"
                             "比如 docs/product-contract-v1/execution-ledger,和产品契约放一起)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", parents=[common], help="建账本目录").set_defaults(fn=cmd_init)
    s = sub.add_parser("add", parents=[common], help="追加一条契约条目"); s.add_argument("id"); s.add_argument("title"); s.add_argument("ref", help="底座/规格参照"); s.add_argument("dod", help="可观测的完成定义"); s.set_defaults(fn=cmd_add)
    s = sub.add_parser("import", parents=[common], help="从 JSONL 文件批量加入条目"); s.add_argument("file", help="JSONL:每行一个 {id,title,ref,dod}"); s.set_defaults(fn=cmd_import)
    s = sub.add_parser("claim", parents=[common], help="worker 记录意图(不是完成)"); s.add_argument("id"); s.add_argument("what", help="改了什么(file:line)"); s.add_argument("--by", default=None, help="干这活的身份;启用自证守卫"); s.set_defaults(fn=cmd_claim)
    s = sub.add_parser("verdict", parents=[common], help="记录独立验收方的 PASS/FAIL"); s.add_argument("id"); s.add_argument("verdict", help="PASS|FAIL"); s.add_argument("evidence"); s.add_argument("--dod", default=None, help="验收方核对的 DoD(对着契约做防篡改校验)"); s.add_argument("--by", default=None, help="验收方身份;若与 claim 的 worker 相同会被标出"); s.set_defaults(fn=cmd_verdict)
    s = sub.add_parser("status", parents=[common], help="人类可读状态"); s.add_argument("--write", action="store_true", help="同时把 status.md 写到账本目录"); s.set_defaults(fn=cmd_status)
    sub.add_parser("gate", parents=[common], help="只要有条目不是 VERIFIED 就以 1 退出").set_defaults(fn=cmd_gate)
    a = p.parse_args()
    global DIR; DIR = a.dir
    a.fn(a)

if __name__ == "__main__":
    main()
