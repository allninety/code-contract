# 输出包 —— 文件夹形状 + 覆盖报告

把契约存成文件夹,不是对话总结(它得活过这次会话)。带版本:新一版是一个新文件(`-v2`),绝不就地重写旧的。

**一个共址的包、三个写手、一条 atom-ID 主线。** 三个技能是三个*工种*在同一个包上干活 —— 各占自己的子目录,所以没有两个技能写同一个文件:

```text
product-contract-v1/
  README.md            # 这产品是什么,业主先读的 ~5 行;链到其余
  MANIFEST.md          # 文件地图 + 各部分关系
  # ── product-contract-zh 写这些(底稿 / 出题集)──
  dictionary/
    FEATURE-DICTIONARY-v1.md     # 四面表(见 dictionary-template.md);状态 = 单产品快照
  registries/
    USER-FEATURE-ATOMS.md
    CODE-CAPABILITY-ATOMS.md
    TRACEABILITY-LINKS.md        # (见 traceability-template.md)
  coverage/
    COVERAGE-v1.md               # 下面的报告
  workflows/
    OWNER-TO-CODE.md
    CODE-TO-OWNER.md
    NEXT-PASS.md
  # ── parity-audit-zh 写这些(答题集,按 target)──
  audit-results/
    PARITY-<baseline>-vs-<target>-v1.md   # 落盘的缺口文档
    ATOM-STATUS-<target>-v1.md            # 按 target 的 ✅/🟡/🟠/🔴/🟣 状态,用 atom-ID 作键(不是词典的 状态)
    dimensions/<dimension>.md             # 可选的分维度发现
  # ── verified-execution-zh 写这些(闸门账本)──
  execution-ledger/
    contract.jsonl     # 条目 + 它们的 DoD(harness.py 存储)
    ledger.jsonl       # 只追加的 claim + verdict
    status.md          # 人类可读快照(harness.py status --write)
```
文件夹名可按仓库已有 docs 习惯改,但保持包完整。

**单写-每文件夹 —— 这正是让 `status` 不被双写的办法:**
- `product-contract-zh` 拥有 `dictionary/ registries/ coverage/ workflows/`。词典的 `状态` 列是它**自己的单产品快照**("这产品当前是否兑现承诺")—— 不是按 target 的字段。
- `parity-audit-zh` 拥有 `audit-results/`。**按 target** 的状态(target A vs B)放在 `audit-results/ATOM-STATUS-<target>-v1.md`,用 atom-ID 作键 —— 绝不写回词典的 `状态`。
- `verified-execution-zh` 拥有 `execution-ledger/`。用 `--dir docs/product-contract-v1/execution-ledger`(或 `HARNESS_DIR`)把 `harness.py` 指过去。

## 覆盖报告形状
```text
User Feature Atoms:      <n>
Code Capability Atoms:   <n>
Trace Links:             <n>
Linked Feature Atoms:    <n>   (未连: <n>  ← 这些是缺口)
Linked Code Atoms:       <n>   (未连: <n>)
High-risk gaps:          <列表 —— 缺消费者链的 导出/持久化/原生桥 atom>
Status tally:            ✅ <n> · 🟡 <n> · 🟠 <n> · 🔴 <n> · 🟣 <n>
Next pass:               <诚实 backlog>
```
未连计数和高风险缺口正是覆盖这一步的**意义** —— 摊出来;绝不为了看着完成而把它们抹成零。
