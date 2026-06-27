# 登记表 + trace link —— 模板

`registries/` 下三个文件。每个 atom 有一个稳定 ID;trace link 是多对多。示例行**仅作示例**(一个渲染 / 导出类应用)—— 按你的领域改写;**中文名列可选**(单语项目去掉)。

## USER-FEATURE-ATOMS.md
```text
| ID        | 中文名     | English          | 语义(大白话)                            | 可观测验收(DoD 种子)                              | 领域     | 状态    |
|-----------|-----------|------------------|----------------------------------------|---------------------------------------------------|----------|---------|
| F-res     | 导出分辨率 | Export resolution | 出片清晰度:1080/2K/4K                   | 4K 导出 → 文件宽 3840,不是 1920                    | export   | 🔴 回归 |
```
一个 atom = 一个最小可观测承诺。"可观测验收"列是 verified-execution-zh DoD 的种子 —— 写成你能**跑**或**看**的东西,绑定底座/规格。**这里的 `状态` 是单产品快照**(和词典 `状态` 同义);某个 *target* 的按 target 状态由 parity-audit-zh 写到 `audit-results/ATOM-STATUS-<target>.md`(同一 ID 作键)—— 不写进这一列。

## CODE-CAPABILITY-ATOMS.md
```text
| ID              | 职责(一个边界)                       | 源(文件/目录)                  | 输入 → 输出                  | 改动风险                       | 影响的功能            |
|-----------------|--------------------------------------|----------------------------------|-----------------------------|-------------------------------|-----------------------|
| CODE.exportPipe | 把 props+分辨率 变成渲染好的文件        | electron/render.cjs, Film.tsx    | InputProps,res → mp4        | 尺寸错 / 控件被丢             | F-res, F-aspect, ...  |
```
按**职责**原子化,不按文件。一个文件可承载多个职责;一个职责可横跨多个文件。

## TRACEABILITY-LINKS.md
```text
| feature | relation     | code            | note(file:line,这条链断言了什么)            |
|---------|--------------|-----------------|------------------------------------------------|
| F-res   | exported-by  | CODE.exportPipe | render.cjs:54 按 composition.width/height 出片 |
| F-res   | declared-by  | CODE.schema     | schema.ts: res 枚举 1080/2k/4k                  |
```
关系:`declared-by` · `edited-by` · `stored-by` · `resolved-by` · `rendered-by` · `exported-by` · `validated-by` · `tested-by` · `documented-by`。

**规则:**每个高风险功能要有 ≥1 条来源关系(edited/declared)**和** ≥1 条终点消费关系(rendered/exported/stored)。每个导出功能要有 `exported-by` + `tested-by`,或一个显式缺口。有来源却没消费者的功能 = 🟠 未接线。

## workflows/
两条闭环都端到端写全(不只命名),因为价值在于**工种之间的交接**。业主只碰表的左侧(中文问题 / 词典 / atom-ID);agent 只碰右侧(代码锚点 / DoD);trace link 把两者连起来;verified-execution-zh 关闭它们。

### OWNER-TO-CODE.md —— 业主有个抱怨 → 确认修好
> *"我发现 4K 导出不对" →*
1. **找到 atom。** 在词典里按 中文名/语义 查 → 那个 **ID**(如 `F-res` / `EXPORT.resolution`)。
2. **追到代码。** 沿那个 ID 的 `TRACEABILITY-LINKS` → 拥有它的 **Code Atom** + `代码锚点`(file:line)。
3. **读当前状态。** 看该 atom 在 `audit-results/ATOM-STATUS-<target>.md` 里的按 target 状态(✅/🟠/🔴/缺失)和背后证据 —— 它真的坏了吗?怎么坏的?
4. **交给闸门(若不是 ✅)。** 把 **atom-ID** 当契约条目交给 `verified-execution-zh`,用该 atom 的**可观测验收**当 DoD:`harness.py add F-res "<标题>" "<底座 ref>" "<DoD>"`。
5. **修** —— 在追到的 `代码锚点` 处做最小改动。
6. **独立验收。** 只在对着那条 DoD 拿到 **独立的** verified-execution-zh PASS 时才算关闭(一个单独的验收方读真实产物)—— 绝不是实施者自证。结论挂在同一个 atom-ID 上,业主能把它倒查回自己认得的功能。

### CODE-TO-OWNER.md —— agent 改了代码 → 该回查哪些承诺
> *改了导出代码 →*
1. **落到 Code Atom。** 你动的文件 → 它的 `CODE-CAPABILITY-ATOM`(经 `source` / `代码锚点`)。
2. **沿 trace link 展开。** 那个 code atom 的 `影响的功能`(及反向 trace link)→ 它触及的每个 **User Feature Atom**。
3. **用业主语言列出受影响的承诺**(好让业主知道哪些可能动了)。
4. **回归验收**每个受影响 atom 对着它的可观测验收 —— 重跑 DoD;任何不再成立的降级为 🔴/🟠,喂进 NEXT-PASS / verified-execution-zh。

### NEXT-PASS.md
- 诚实 backlog:未连 atom、🟡/🟠/🔴 项,以及**从 parity-audit-zh 回灌的契约缺口**(target 暴露出一个还没 atom 覆盖的承诺 → 下一轮 product-contract-zh 的新 atom,不是私自扩大审计)。
