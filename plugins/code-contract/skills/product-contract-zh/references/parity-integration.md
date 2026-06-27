# parity 集成 —— 把 parity-audit-zh 的产出转成契约产物

当为一次重写 / 迁移 / 重构 / fork / clone 建契约、且存在可信底座时使用。

## 边界(别把两个技能合并)
- **parity-audit-zh** 发现底座与 target 之间带证据的差异(深度 / 证据引擎)。
- **product-contract-zh** 把这些差异转成持久词表、atom、trace link 和覆盖义务(结构 / 持久层)。

## 顺序
1. 对底座 + target 跑或消费一次 parity-audit-zh。
2. 抽出**审过的能力**(不只缺口)—— 对齐的项也是 atom。
3. 把每个 blocker/major/minor 发现 → 受影响的 **User Feature Atom**。
4. 把 底座/新版 `file:line` 证据 → **词典代码锚点** + trace-link 备注。
5. 把每个**根因** → 一个 **Code Capability Atom** 职责(或一条缺失的 trace link)。
6. 把每个**验证限制** → 一个**覆盖缺口** / `🟡 待验证` 状态。
7. 为头部缺口建 **OWNER-TO-CODE** 和 **CODE-TO-OWNER** 工作流条目。

## 映射表
| parity-audit-zh 产物 | product-contract-zh 产物 |
|---|---|
| 能力维度 | 功能类别 / 领域 |
| 能力条目 | User Feature Atom |
| 底座 `file:line` | 底座证据 / 词典代码锚点 |
| target `file:line` | Code Capability Atom 源文件 / trace 备注 |
| blocker / major / minor | 按 target 的 `audit-results/ATOM-STATUS-<target>` 条目(🔴/🟠)+ 覆盖优先级 |
| 根因 | Code Capability 职责缺口 |
| 对齐项 | `ATOM-STATUS-<target>` 里的 `✅`(atom 不变) |
| 验证限制 | `🟡 待验证` + 覆盖缺口 |
| 推荐修复顺序 | `NEXT-PASS.md` + 工作流任务 |

## 质量门(契约不完整,直到)
- 每个 **blocker** 至少映射到一个 User Feature Atom **和**一个 Code Capability Atom;
- 每处可见的 UI/导出 **回归**都出现在词典里;
- 每个高风险的 **导出 / 持久化 / 原生桥** 项都有一条 trace link;
- 每个 parity **验证限制**都作为缺口或人工检查出现在覆盖里。
