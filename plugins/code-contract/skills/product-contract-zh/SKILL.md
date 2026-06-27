---
name: product-contract-zh
description: >-
  把一个软件产品**到底是什么**冻结成一份持久、业主↔代码可追溯的契约:把用户可见的能力和实现它们的代码,变成一张双语功能**词典**
  (中文/English/大白话语义/在哪触达)、面向业主的 Feature Atom、面向代码的 Capability Atom,以及多对多的 trace link ——
  每条都挂在稳定 atom-ID 上 —— 外加覆盖率与 next-pass 缺口。当你想清点 / 分类 / 冻结**一个**产品的完整能力集(不需要对比对象)、
  想做一份功能词典消灭术语混乱、想把 UI 行为映射到实现它的文件、想让需求业主↔代码可追溯、或想在重构 / 迁移 / 重写 / 交接给 agent /
  做对账之前立一个"这产品到底承诺什么"的唯一真相源时使用。触发:冻结规格、做功能词典、清点这应用能干啥、把功能追到代码、
  对齐产品与代码、把能力全分类。它是三件套里的**结构**层,喂给 parity-audit-zh(证据引擎)与 verified-execution-zh(闸门),共享同一 atom-ID 主线。
license: MIT
metadata:
  version: 0.1.0
  lang: zh
  english_skill: product-contract
---

# 产品契约(Product Contract)

> 中文版,对应英文版 `product-contract`。三件套同主线(共享同一 atom-ID):`product-contract-zh`(结构,本技能)· `parity-audit-zh`(证据)· `verified-execution-zh`(闸门)。
> 本文中的"业主"指**产品 owner / 业务负责人 / 非技术决策者**(不是房产业主)。

本技能把**一个**产品冻结成一份持久契约,把**业主体验到什么**和**代码在哪实现它**连起来 —— 让一个不懂技术的业主和一个写代码的 agent 能指着*同一个东西*、两边都能倒查。

## 这是干什么的
每个产品都横跨两个会逐渐脱节的维度:**应用**维度(业主触达的 —— 控件、输出、承诺)和**代码**维度(实现它们的 —— 文件、组件、服务)。最伤的缺口活在两者*之间*:业主看得见的控件没有代码读它;代码有的行为业主从没命名。而且业主和 agent 用不同的词描述同一个功能,于是各说各话。

本技能产出那座桥:一份**冻结、分好类**的产品能力清单,每个能力都是**一条同时带两张脸**的记录,用一个**稳定 ID** 连起来。这套记录同时是**规格**("这产品是什么")、**词典**(业主大白话里约定的名字 *和* 代码锚点)和**业主↔代码索引**(业主 Ctrl-F 一个名字 → ID → 代码;agent grep 一个 ID → 业主能懂的含义)。

## 它**不是**什么(边界 —— 不要混淆)
三个技能、三份活、一条共享 atom-ID 主线。保持分开:
- **product-contract-zh(本技能)** = **结构 / 持久**层。它把*一个产品*冻结成有命名、可追溯的持久契约。它**不**深审重写,也**不**把关执行。
- **`parity-audit-zh`** = **深度 / 证据**引擎。给定底座 + target,做穷尽、file:line、按严重度的缺口发现。**密度和证据来自那里,不是这里。**
- **`verified-execution-zh`** = **闸门**。用独立、对抗的结论关闭没通过的 atom。

所以:想要重写上的最深细节 / 证据?→ 那是 parity-audit-zh。想要一个产品的持久、业主可读、可追溯的地图?→ 在这里。它们经共享 atom 登记表**组合**;**不合并、不冗余**。

## 契约的三层
1. **User Feature Atom** —— 面向业主的产品承诺(业主体验到 / 能验证的)。
2. **Code Capability Atom** —— 面向 agent 的实现*职责边界*(不是文件清单 —— 见下)。
3. **Traceability Link** —— 多对多、带关系类型的链,从功能连到拥有它的代码,以及反向。

## 核心流程
1. **钉死地基。** 项目根、当前 worktree、底座(若有)、目标输出文件夹 —— *在动笔前*。
2. **命名前先看真实代码 + UI。** 先读真源码和真控件面。给你没看过的东西命名,正是词典出错的根源。
3. **若已有契约** → 把它的 atom 登记表当共享主线;**扩展它,别另开第二份清单。** (atom-ID 是跨次、跨另两个技能的连接键。)
4. **若有可信底座但没契约** → 先跑或消费一次 **`parity-audit-zh`**,用它审过的能力(不只缺口)**引导**出草稿 atom,再在这里归一化命名 / 锚点。(完全没底座 → 退化成自包含的发现过程,并标低置信度。)
5. **先建双语词表**,当命名有歧义时(通常都有)—— 见下面的词典。
6. **登记 User Feature Atom**:每个用户可见 / 可导出验证 / 被持久化的产品承诺。
7. **登记 Code Capability Atom**:每个实现职责边界。
8. **加 Trace Link**:用下面的关系动词把两者连起来。
9. **跑一遍覆盖**:计数 + 未接线缺口 + next-pass。
10. **存成文件夹包**,不只是对话总结(它得活过这次会话 —— 见输出包)。

## 什么是好 atom
### User Feature Atom —— 一个最小的*可观测*承诺
好 atom 是用户可见 / 可导出验证 / 被持久化 / 运营上有意义的;有一个**稳定 ID**;映射到语义 / 领域;**可追到代码**;且**由一条可观测验收规则可测**(这条规则正是 `verified-execution-zh` 之后要查的 DoD 的种子 —— 写成可观测的,见 DoD 桥)。

**拆开宽标签。**"字幕系统" / "导出系统"是*类别*,不是 atom。拆成最小承诺:`CAPTION.fxKeywordWindow`、`EXPORT.resolution`、`AUDIO.noAudio`、`PERSIST.apiKey`。一个 atom = 业主能指着说"这个好使 / 这个不好使"的一件事。粗 atom 是契约看着完整其实不完整的头号原因。

### Code Capability Atom —— 一个职责边界
写明源文件 / 目录、职责、接受的输入 / 输出、改动时的风险,以及它影响的 feature atom。**文件清单不是职责:**一个文件可承载多个职责,一个职责可横跨多个文件。按*职责*原子化,不按文件。

## Trace link(一致地用这些关系)
`declared-by`(类型/schema/契约声明该字段)· `edited-by`(UI/API 编辑它)· `stored-by`(持久层存 / 恢复它)· `resolved-by`(解析器导出规范模型)· `rendered-by`(渲染器显示 / 播放它)· `exported-by`(导出器把它作为交付物产出)· `validated-by`(预检 / 守卫 / 运行时校验它)· `tested-by`(测试 / 探针 / fixture 验它)· `documented-by`(文档定义其工作流 / 语义)。

**规则:**每个高风险功能至少要有一条*来源*关系(edited/declared)**和**一条*终点消费*关系(rendered/exported/stored)。每个导出功能要有 `exported-by` + `tested-by`,**或一个显式缺口**。一个有来源却没消费者的功能就是经典的 🟠 未接线(模型/UI 里接好了,下游却没人读)。

## 统一词典(四面表 —— 这是业主↔代码的桥)
当术语引起混乱时(默认假设它会),建一张表。每行一个 atom,两张脸用 ID 连起来:
```text
ID | 中文名 | English | 语义(大白话:它管什么/你会看到什么) | 在哪(你触达) | Feature Atom | 代码锚点(file:line) | Code Atom | 状态
└──────────────── 业主侧(业主读 / 操作这些)────────────────┘ └──── agent 侧 ────┘ └ 快照 ┘
```
用能撑过讨论的短 ID:`F-res`、`F-floor`、`F-fx`、`F-srt-source`。**业主侧** = `中文/English/语义/在哪/Feature-Atom`(业主操作这些);**agent 侧** = `代码锚点/Code-Atom`(agent 操作这些);**ID** 是两边共享的。**`状态` 是 product-contract-zh 自己的单产品快照**("这产品当前是否兑现了这个承诺")—— 它**不是**按 target 的字段。当你审 A/B 多个 target 时,parity-audit-zh 把各 target 的状态写到 `audit-results/ATOM-STATUS-<target>.md`(同一 ID 作键)—— 绝不写回这个 `状态` 列(这正是让该列单写的办法)。DoD **不在**词典里;它作为每个 User Feature Atom 的"可观测验收"活在登记表里(面向业主、大白话)—— 见 `references/traceability-template.md`。

### 业主脸纪律 —— agent 在这里最容易翻车,所以顶住
把 `中文名` / `English` / `语义` / `在哪` 写成**大白话的"你做什么 / 你会看到什么 / 结果是什么" —— 不是控件路径、变量名或术语。** agent 老是滑回系统命名(写 `style.anim` 而不是"字幕怎么出现");每一行都顶住。检验:*一个从没看过代码的业主,能看懂这句吗?* 看不懂就是术语,重写。
- **不拿截图当主要机制。** 太慢、也不作为可复用文本留存。一句好的大白话更快、可 grep、可复用。(截图可以*帮忙*讲清一个难点 —— 但那句话才是产物。)

### 机制 —— 默认可用、遇阻才改(**不**按条逐一签字)
agent 比业主更懂系统,所以**由 agent 把词典写成默认可用、立即上线。** 业主**不**逐条确认措辞(太慢、也毁了整件事的意义)。改成:
- 业主只标他**看不懂**的条目,agent 去修*那些*;
- 一个名字定了,agent **必须复用** —— 绝不给同一个东西起第二个名字。这份命名一致性,比任何单条完美措辞更能真正减少误解。

## 状态分类(少而一致 —— 每个 atom 带一个)
- `✅ 保留` —— 在且可追溯(承诺兑现且你能追到代码)。
- `🟡 待验证` —— 已映射,但还需要一个 fixture / 运行时证据 / 人工检查才能信。
- `🟠 未接线` —— 模型或 UI 在,但消费链不完整(显示出来了,下游却没人读)。
- `🔴 回归` —— 产品承诺**没**兑现(回归 / 坏 / 空操作)。
- `🟣 新增` —— 底座之外的新能力;需要独立验收(它不是"对齐",是新增范围)。

## 覆盖 + next-pass
横扫:UI 表面与控件 · 状态与持久字段 · 导入 / 导出路径 · 渲染 / 预览路径 · 原生桥 / 服务 API · QA / 探针 / 测试脚本 · 文档与交接材料。然后上报(见 `references/package-template.md`):feature atom / code atom / trace link 的计数 · 两侧 linked vs **未连** · 高风险缺口 · **next pass**。未连的 atom 和高风险缺口是契约诚实的边缘 —— 永远摊出来,别为了让覆盖看着完成而抹掉它们。

## 通往 verified-execution-zh 的 DoD 桥
每个 User Feature Atom 的**可观测验收规则***就是* DoD 的种子。用业主可观测的话来写("设 X,渲染第 N 帧;字幕带模糊入场 ≠ fade"),但对着**代码**可校验 —— 于是同一句既服务业主(认得出)又服务 agent(跑得了)。当你把没通过的 atom 交给 `verified-execution-zh` 时,**复用 atom-ID 当契约条目 ID**:冻结 → 审计 → 关闭 → 验收全围着同一个 ID 转,业主能把任何结论倒查回他认得的功能。(细节见该技能的"DoD 是业主↔代码的桥"一节。)

## 与另两个技能协调(共享 atom-ID 主线)
共享产物是**本契约的 atom 登记表**;atom-ID 是连接键。完整协议:`references/three-skill-coordination.md`。简版:

| 技能 | 读 | 写 |
|---|---|---|
| **product-contract-zh**(本技能) | 项目源码、UI、文档、可选的 parity 发现 | atom、trace link、词典、覆盖缺口、next-pass —— *出题集* |
| **parity-audit-zh** | 本契约的 atom + trace link + 某 target 的源码/运行时 | 每 target 每 atom 的状态 + 证据 —— *答题集* |
| **verified-execution-zh** | 状态未通过的 atom | 用 atom-ID 作键的独立 claim/verdict —— *闸门* |

**契约引导对账(关键规则):** 有本契约时,parity-audit-zh **逐 atom 对着它审** —— **不**自己另派维度清单(再推导的漂移正是两份审计在颗粒度上吵架的根因)。若 parity-audit-zh 发现一个**没有 atom 代表**的承诺,那是**下一轮 product-contract-zh 的契约缺口** —— 记在这里,不私自塞进审计。把 parity 发现转成契约产物、以及那一轮要过的质量门,见 `references/parity-integration.md`。

## 输出包(存这个,不是对话总结)
```text
product-contract-v1/
  README.md            # 这产品是什么,业主先读的 5 行
  MANIFEST.md          # 文件地图 + 各部分关系
  dictionary/
    FEATURE-DICTIONARY-v1.md
  registries/
    USER-FEATURE-ATOMS.md
    CODE-CAPABILITY-ATOMS.md
    TRACEABILITY-LINKS.md
  coverage/
    COVERAGE-v1.md
  workflows/
    OWNER-TO-CODE.md   # 业主提一个需求 → 该动哪些 atom/代码
    CODE-TO-OWNER.md   # 一处代码改动 → 影响哪些业主承诺
    NEXT-PASS.md       # 未连 / 未验 atom 的诚实 backlog
  audit-results/                    # parity-audit-zh 写(按 target,同 atom-ID)
  execution-ledger/                 # verified-execution-zh 写(harness.py --dir 指到这)
```
带版本(`-v1`):新一版是一个**新文件**(`-v2`),绝不就地重写旧的。文件夹名可按仓库习惯改,但保持包完整。模板:`references/package-template.md`、`references/dictionary-template.md`、`references/traceability-template.md`。

## 坑
- **atom 太粗。** 把"导出系统"当一个 atom,会藏住十个承诺。拆到最小可观测的一件事。(契约看着完成其实没完成的头号原因。)
- **文件清单冒充 code atom。** 按*职责*原子化,不按文件。一个文件 ≠ 一个职责。
- **业主脸写成术语。** `style.anim` 不是"业主做什么"。重写到非程序员能懂。
- **把词典卡在逐条签字上。** 拖垮吞吐。默认可用 + 遇阻才改才是机制。
- **有契约时另开第二份清单。** 扩展 atom 登记表;别造平行宇宙 —— 那会毁掉主线存在的可比性。
- **覆盖藏住缺口。** 未连 atom 和 🟠/🔴 项正是覆盖这一步的意义;摊出来。
- **只活在对话里。** 不存盘,compact 一来就死。写文件夹包。

## 验收(对契约本身)
- **抽查锚点** —— 随机抽几行词典;确认所引 `file:line` 存在、且如该行所述。
- **两向追** —— 挑一个 feature atom,顺它的链到代码再回来;挑一个 code atom,顺它到它影响的承诺。悬空的链是真缺口,不是笔误。
- **业主可读性** —— 当作从没看过代码,读 5 个 `语义` 格。任何需要代码知识才懂的都不合格。
- **覆盖诚实度** —— 未连 / 高风险清单是合理地完整,还是可疑地空?空是个坏味道。
