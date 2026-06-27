# code-contract(代码合约)

[English](README.md) | **中文**

三个相互组合的 **Claude Code 技能**(采用开放的 [Agent Skills](https://agentskills.io) `SKILL.md` 格式),让一次**重写 / 迁移 / 移植保持诚实** —— 把"完成"定义为*对着一份冻结的、业主可读的规格被独立验收过*,而不是"实施者说完成了"。

一次重写会悄悄丢掉原版做到的东西:一个不再影响输出的控件、一个变成空操作的导出选项、一个被不同地夹断的时长。你一条一条地发现它们,拖好几周,信任一点点磨掉。这套技能把它变成一个闭环:

```
 业主语言 ──►  product-contract  ──►  parity-audit  ──►  verified-execution  ──► 业主信得过的结果
 "应该做什么"   (冻结规格)            (找出缺口)           (在闸门后关闭它们)
                       └──────────────── 一条稳定的 atom-ID ────────────────┘
```

| 技能 | 角色 | 回答 |
|---|---|---|
| **product-contract** | *结构* —— 把**一个**产品冻结成持久、业主↔代码可追溯的契约(feature atom + code atom + trace link + 双语词典) | "这产品该做什么?每个功能叫什么?业主在哪触达?哪段代码拥有它?" |
| **parity-audit** | *深度* —— 把一个 target 对着底座穷尽对比,每处缺口都带 `file:line` 证据,按严重度排序、按根因归类 | "这个 target 真的做到契约承诺的每件事了吗?哪些缺失 / 回归 / 没接线?" |
| **verified-execution** | *闸门* —— 每个没通过的条目,只有当一个**独立**验收方对着一条书面、可观测的完成定义确认后才关闭 | "这些缺口*真的*修好了吗?证据在哪?账本在哪?" |

三者共享**一条稳定的 atom-ID**,所以业主能把任何结论倒查回他认得的功能,也能把任何代码改动正查到它影响的承诺。业主只碰功能名 + atom-ID;agent 只碰代码锚点 + DoD;trace link 把两者连起来。

## 这里真正新的是什么(以及什么不是)

大部分是对已知实践的称职运用 —— 需求可追溯、完成定义(DoD)、统一语言、回归排查。有三处比常见实践更锋利,也是用它的理由:

1. **一条被经验*推翻*的输出规则。** `parity-audit` 刻意**反着用**流行的"描述模式、而不是列表"那条建议 —— 因为一次 A/B 测试(对着 17 个已知控件回归做真值)表明:打包能保住召回,却把单项颗粒度砍掉约 30%,而缺口清单的存在就是为了逐行去动手。实验随包发布:[`ab-test-enumerate-vs-patterns.md`](plugins/code-contract/skills/parity-audit-zh/references/ab-test-enumerate-vs-patterns.md)。(多数技能在断言;这一条做了实验。)
2. **一条单写的 atom-ID 主线。** 按 target 的审计状态被强制写进它自己的文件、并*禁止*写进契约词典 —— 所以一份契约对着 N 个 target 审计时,永远不会双写同一个状态格。一个连接键,一文件一个写手。
3. **一道实施者糊弄不了的闸门。** `verified-execution` 随包带一个极小的纯标准库 harness,牙齿是机械的、不是文字的:一本只追加的账本、一个哈希过的 DoD、一个**自证标记**(由做这活的同一身份给出的结论会被标出来)、以及一个 **stale-PASS 降级**(PASS 之后改了 DoD,条目就从 ✓ 掉到 ⚠STALE,把闸门拦住)。它不能*阻止*一个铁了心的操作者(见[诚实的边界](#诚实的边界))—— 但它让两个经典的赖账动作**可见**。

## 安装

面向 **Claude Code**。(这些技能是纯 [Agent Skills](https://agentskills.io) `SKILL.md` 文件,原则上可移植到其它兼容 agent —— 但本包是在 Claude Code 上构建和测试的;见[平台与可移植性](#平台与可移植性)。)

**手动(推荐)** —— 把技能文件夹拷到 Claude Code 能发现的地方:
```bash
git clone https://github.com/allninety/code-contract.git
cp -R code-contract/plugins/code-contract/skills/* ~/.claude/skills/
```
然后开一个会话 —— Claude 按描述触发技能,或用 `/product-contract`、`/parity-audit`、`/verified-execution` 调用。

**中文版:** 同样三个技能也有**完整中文版** —— `product-contract-zh`、`parity-audit-zh`、`verified-execution-zh` —— 它们的 `SKILL.md`、`references/` 文档、编排骨架、harness 输出全部本地化,描述能被中文 prompt 触发(冻结规格 / 能力对账 / 独立验收)。上面的 `cp` 会把六个都装上;你用哪种语言提问就用哪套。(中文 harness 保留英文状态 token + JSON 账本字段,所以它的账本和英文 harness 互通。)

**插件方式** —— 本包也是一个 Claude Code marketplace:`/plugin marketplace add allninety/code-contract`,然后 `/plugin install code-contract`。

**依赖:** Claude Code;`verified-execution` 的 harness 需要 Python 3(纯标准库)。

## 快速上手

- **冻结规格:** "用 `product-contract` 把这个应用做的事冻结成契约。" → 一个 `product-contract-v1/` 包(词典 + 登记表 + 覆盖 + 工作流)。
- **审计重写:** "用 `parity-audit`:底座 = `<旧>/src`,target = `<新>/src`。" → 一份穷尽、带证据、按根因归类的缺口清单。
- **在闸门后关闭缺口:** "在那份缺口清单上用 `verified-execution`。" → 每条只在拿到独立 PASS 后才关闭,记在一本带篡改标记、挡着会拦的闸门后的账本里。

它们也能单独用 —— 不必三个都要。

## 示例

[`examples/verified-execution-run/`](examples/verified-execution-run/) 是一次**真实**的 harness 跑(不是摆拍),针对一个小的 web-API 契约,展示全部四种状态、包括"门柱被挪"那颗牙:

```
1/4 VERIFIED
✓ VERIFIED  A1   auth: 401 on missing token
✗ FAIL      A2   pagination: page size cap   └ limit=9999 returned 9999 rows — cap not enforced
◐ CLAIMED   A3   idempotency: repeated POST
⚠ STALE     A4   error shape: 422 body       └ goalpost moved since PASS — re-verify
```

另见 [`examples/product-contract-package/`](examples/product-contract-package/)(一份小契约)和 [`examples/parity-audit-gap-doc/`](examples/parity-audit-gap-doc/)(一份小缺口文档)。

## 诚实的边界

在单个 Claude 会话里,编排者仍然是 Claude —— `verified-execution` **不是**硬件级约束。它的牙齿是:一个*独立、对抗的*验收方(比自检难骗得多)、一本*确定性*的只追加账本 + 闸门(脚本的结论吵不动,而且改动可见)、以及*你*这个最终闸门。它让假"完成"难得多、且永远*可见* —— 不是不可能。这就是设计,把它明说出来好让你评判。

## 平台与可移植性

**本包面向 Claude Code** —— 那是它构建、运行、测试的地方。`SKILL.md` 用开放的 [Agent Skills](https://agentskills.io) 标准,harness(`harness.py`)是纯标准库 Python,所以*方法*原则上可移植到其它兼容 agent(Codex CLI、Cursor……)。但**自动编排是 Claude 专属的** —— `parity-audit` 的 workflow 骨架和 `verified-execution` 的驱动用了 Claude Code 的 Workflow/Agent 工具 —— 所以**本包不承诺跨平台**;把那些骨架当 Claude Code 的辅助工具看。欢迎贡献各平台的编排适配器。

README 叙事风格参考了 [khazix-skills](https://github.com/KKKKhazix/khazix-skills)(MIT)—— 感谢这个范式。

## 目录

```
plugins/code-contract/skills/
  product-contract(-zh)/      SKILL.md + references/                      (契约:atom、链、词典)
  parity-audit(-zh)/          SKILL.md + references/                       (审计:维度、并行展开、A/B 记录)
  verified-execution(-zh)/    SKILL.md + references/ + scripts/harness.py  (闸门)
examples/                     真实产出示例
```

共享交接协议在 [`product-contract-zh/references/three-skill-coordination.md`](plugins/code-contract/skills/product-contract-zh/references/three-skill-coordination.md)。

## 致谢

由 **Claude**([Claude Code](https://www.anthropic.com/claude-code),Opus 4.8)设计与构建;由 **OpenAI Codex** 多轮独立复查。

## 许可证

[MIT](LICENSE) © 2026 allninety。欢迎贡献 —— 见 [CONTRIBUTING.md](CONTRIBUTING.md)。
