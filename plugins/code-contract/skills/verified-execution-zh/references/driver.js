// verified-execution 驱动 —— 一个 Workflow 骨架,自动对很多条目跑 harness 循环,
// 免得你手动驱动 N 个周期。workflow 负责编排;agent 经 Bash 调 harness.py
//(workflow 的 JS 在沙箱里,碰不了文件系统)。之后由人读 `status` / `gate`。
//
// 前提:契约已填好。要么先 `harness.py import items.jsonl`,要么用一个 Phase 0 的 agent
// 读源(比如一份 parity-audit 缺口文档),每行产出一个 {id,title,ref,dod},再 `harness.py import` 那个文件。

export const meta = {
  name: 'verified-execution-driver',
  description: '自动关闭一份工作条目契约:每条先由 worker 实现,再由一个独立验收方把关',
  phases: [{ title: 'Close', detail: '每条:worker → 独立验收方 → harness verdict' }],
}

const HARNESS = 'python3 ~/.claude/skills/verified-execution-zh/scripts/harness.py'   // agent 经 Bash 调这个
const REPO = '<仓库绝对路径>'
// 要处理的条目。实际用时,从契约里读(agent 跑 `harness.py status`/读 .harness/contract.jsonl),
// 或经 `args` 传入。每条需要 id + DoD + 规格/底座 ref。
const ITEMS = args && args.length ? args : [
  // { id: 'G1', title: '...', ref: '底座 file:line', dod: '可观测测试' },
]

const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'evidence'],
  properties: { verdict: { type: 'string', enum: ['PASS', 'FAIL'] }, evidence: { type: 'string' } },
}

phase('Close')
// pipeline = 每条独立地走 worker→验收方,条目之间无栅栏(快)。
const results = await pipeline(
  ITEMS,
  // 阶段 1 —— worker:做 最小 改动,然后记一条 claim。isolation:'worktree' 让并行的真实改动不打架。
  // worker 不许给自己标完成。
  (item) => agent(
    `在 ${REPO} 里,你是 一条 条目的实施者。做 最小 改动满足它,然后跑:\n` +
    `  ${HARNESS} claim ${item.id} "<你改了什么:file:line>" --by worker\n` +
    `条目 ${item.id}: ${item.title}\n底座/规格 ref(标准): ${item.ref}\n完成定义(DoD): ${item.dod}\n` +
    `返回你做的确切 diff(文件 + 行号范围)。不要声称它能用 —— 那是验收方的事。`,
    { label: `worker:${item.id}`, phase: 'Close', isolation: 'worktree' }
  ).then((diff) => ({ item, diff })),

  // 阶段 2 —— 独立 验收方(牙齿):全新上下文、对抗、读 真实 代码 + 跑 DoD,
  // 然后自己经 harness.py 记结论。给它契约条目 + 原始 diff,不给叙述。
  (prev, item) => agent(
    `你是一个 没有任何前置上下文 的独立验收方。在真实代码/产物证明之前,默认条目 ${item.id} 没做完。` +
    `不要信实施者。\n` +
    `条目: ${item.title}\n底座/规格 ref(标准): ${item.ref}\n完成定义(跑/观察它): ${item.dod}\n` +
    `实施者做的原始 diff:\n${(prev && prev.diff || '(无)').slice(0, 4000)}\n` +
    `自己读 ${REPO},跑 或 观察 DoD,再判。然后记你的结论(--by verifier,和 worker 不同身份,\n` +
    `好让 harness 的自证守卫满足):\n` +
    `  ${HARNESS} verdict ${item.id} PASS|FAIL "<具体观测到的证据>" --dod ${JSON.stringify(item.dod)} --by verifier\n` +
    `返回 {verdict, evidence}。只有 你 独立确认 DoD 成立才 PASS。`,
    { label: `verify:${item.id}`, phase: 'Close', schema: VERDICT_SCHEMA }
  ).then((v) => ({ id: item.id, verdict: v && v.verdict, evidence: v && v.evidence })),
)

const done = results.filter(Boolean)
// 注意:这是 单趟(没有自动重试)。FAIL 项在账本里被重新打开,但这里不重做 ——
// 用失败的 ID 重新调一次驱动(或在 `failed` 上加 while 循环)来关闭它们。
return {
  processed: done.length,
  passed: done.filter((r) => r.verdict === 'PASS').length,
  failed: done.filter((r) => r.verdict === 'FAIL').map((r) => r.id),
  // 返回之后:跑 `harness.py status` 和 `harness.py gate`(只要有条目不是 VERIFIED 就非零退出)。
  // 由人读 status + 抽查样本。那 才是最终闸门。
}
