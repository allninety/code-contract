# 三技能协调 —— 共享 atom-ID 主线

把 **product-contract-zh + parity-audit-zh + verified-execution-zh** 一起用时的权威协议。三者都围着**一个稳定 atom-ID** 转;本文是它们如何交接的唯一真相源。(parity-audit-zh 和 verified-execution-zh 指向这里,而不是各自重述,免得协议在副本间漂移。)

## 主线
共享产物是 **product-contract-zh 的 atom 登记表**。atom-ID 是连接键。

```text
product-contract-zh 的 atom  (出题:"这产品是否承诺 X?")
  ├─ target A 的 parity 状态 + 证据   (实现 A 的答)
  ├─ target B 的 parity 状态 + 证据   (实现 B 的答)
  └─ verified-execution-zh 的 claim/verdict 账本 (独立闸门,按 target + DoD)
```

**一切落在哪 —— 一个共址的包、三个写手、不共享文件**(完整形状:`product-contract-zh/references/package-template.md`):
```text
docs/product-contract-v1/
  dictionary/ registries/ coverage/ workflows/   # product-contract-zh 写
  audit-results/   ATOM-STATUS-<target>.md ...    # parity-audit-zh 写(按 target 的状态在这,不在词典)
  execution-ledger/  contract.jsonl ledger.jsonl status.md   # verified-execution-zh 写(harness.py --dir 指这)
```
词典的 `状态` 列是 product-contract-zh 的**单产品快照**;**按 target** 的状态是 parity-audit-zh 的另一份产物,用同一 atom-ID 作键。这份分离正是让 `status` 单写-每文件的办法。

## 读 / 写协议
| 技能 | 读 | 写 |
|---|---|---|
| **product-contract-zh** | 项目源码、UI、文档、可选的 parity 发现 | atom、trace link、词典、覆盖缺口、next-pass |
| **parity-audit-zh** | atom 登记表、trace link、某 target 的源码/运行时 | 按 target 每 atom 的状态 + 证据 |
| **verified-execution-zh** | 状态未通过的 atom | 用 atom-ID 作键的独立 claim/verdict |

谁拥有什么:**product-contract-zh 拥有结构**(持久、有命名、可追溯的地图)。**parity-audit-zh 拥有深度**(穷尽、file:line、按严重度的证据)。**verified-execution-zh 拥有闸门**(独立、对抗的结论)。它们组合;不合并、不冗余。

## 契约引导对账(有契约时)
parity-audit-zh **逐 atom 对着登记表审** —— **不**自己另派维度清单:
1. 读 `USER-FEATURE-ATOMS`、`CODE-CAPABILITY-ATOMS`、`TRACEABILITY-LINKS` 和词典。
2. 把 User Feature Atom 当审计清单。
3. 用 trace link 找 target 的代码锚点。
4. 对着 target 跑或核查每个 atom 的可观测 DoD。
5. 每个 atom 写一个状态 —— 写到 `audit-results/ATOM-STATUS-<target>.md`,**不是**词典 `状态`:`✅ 保留` / `🟠 未接线` / `🔴 回归` / `缺失` / `🟡 待验证`。
6. **保持 atom-ID** 稳定,好让 target A 和 target B 直接可比、一轮一轮可比(每个 target = 自己的状态文件)。

为可读做分组没问题,但**被审的单元仍是 atom。** 若 parity-audit-zh 发现一个**没有 atom 代表**的真实承诺,把它记为**下一轮 product-contract-zh 的契约缺口** —— 不私自扩大自己的审计范围。(这条回环正是契约密度一轮轮往上爬的办法。)

## 冷启动(还没契约)
1. parity-audit-zh 跑底座引导的发现(它的完整方法)。
2. 它产出**草稿 atom** 当引导产物(来自审过的能力,不只缺口)。
3. product-contract-zh 把名字、词表、code atom、trace link 归一化进真正的登记表。

## verified-execution
verified-execution-zh 用 **atom-ID 当它的契约条目 ID**。一次 PASS **只对指定 target 和 DoD** 关闭这个 atom —— 不删 atom、也不抹掉其它 target 的 parity 证据。业主能把任何结论倒查回他认得的功能,因为端到端是同一个 ID:冻结 → 审计 → 关闭 → 验收。
