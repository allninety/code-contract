# verified-execution-zh —— 走一遍(一次实跑)

你有一份工作清单 —— parity-audit 缺口清单、实现计划、任意 checklist —— 需要每条都**真的做完(被独立验收)**,而不只是声称做完。

## 你做什么(全部用户动作)
```
/verified-execution-zh "<清单路径,例如 parity-audit 缺口文档>"
```
然后:**把 DoD 清单一次性签字**(A 步),和**最后读一遍账本**(C 步)。这就是你的全部参与。你**不**跑 python —— Claude 替你跑 harness + 驱动。

## 一步步发生了什么

**A 步 —— 建契约 → 🟦 你唯一的前置 CHECKPOINT。**
Claude 读你的清单,把每条变成一行契约:`{ id, title, 底座/规格 ref, DoD }` —— 其中 **DoD = 一个"真完成"的*可观测*测试**(你能跑或能看的东西),不是"代码看着对"。一份 88 条缺口的文档就是 88 行。Claude 把 DoD 清单给你;你瞄一眼并 OK(或改某条 DoD)。**这是它唯一需要你提前介入的地方,因为牙齿咬在 DoD 上。**
底层 Claude 跑:`harness.py init`,然后 `harness.py import items.jsonl`(所有条目一把导入)。

**B 步 —— 驱动(自动 —— 一个 workflow,你啥也不做)。**
驱动对每条跑:一个 **worker** 做最小改动,然后一个**独立验收方**(全新上下文、对抗、读真实代码 + 跑 DoD)经 harness 记 `PASS`/`FAIL`。条目并行、隔离跑,免得改动打架。你不在这个循环里。一个 *claim* 永远不是"完成" —— 只有验收方的 PASS 才是。

**C 步 —— 读账本 → 🟦 你的最终闸门。**
你会看到(示例):
```
  62/88 VERIFIED
  ✓ VERIFIED  G1    anim 选择器已接通
  ✗ FAIL      G7    2K/4K 仍渲染成 1080p —— scale 没传给 renderMedia
  ◐ CLAIMED   G31   已实现,等结论
  ⚠ STALE     G44   PASS 后门柱被挪 —— 请重验
  ...
```
`gate` 只要有一条不是 `VERIFIED` 就非零退出 —— 实打实地拦,不是提醒。FAIL 项会被**重新打开** —— 重跑它们(随包的驱动是单趟的,所以对失败项重新调一次;它不是自动重试循环)。你**抽查几条**(比如"给我看 G1 的证据")然后做 go/no-go 决定。

## 诚实的那部分(别跳)
因为 harness 是 Claude 跑的,**你读账本 + 抽查样本就是最后一颗牙。** 两种方式:
- 让 Claude 把 `status` 贴给你(方便 —— 但你读的是 Claude 对账本的呈现),或
- 自己跑 `python3 ~/.claude/skills/verified-execution-zh/scripts/harness.py status` / `gate` —— 一条只读命令,但你直接看到**原始账本**(独立性更高一档)。它只打印,什么都不改。

## 一句话的牙齿
claim 永远不是"完成";只有**独立验收方的 PASS** —— 记在一本只追加、带篡改标记的账本里,挡在一道会拦的闸门后,且全程对你可见 —— 才是。技能是 Claude 照着做的指令;*牙齿*是独立验收方 + 确定性闸门 + 你。

## 也适用于
不只 parity-audit 的产出 —— 任何**实现计划**或**任务清单**,只要每条都有一个可观测的 DoD。
