// parity-audit Workflow 骨架(用于 Workflow 工具 / 多 agent harness)。
// 一能力维度一个审计员散开,各读两棵树,返回结构化发现。
// 填 BASE、NEW、DIMENSIONS(维度从底座自己的模块里推 —— 别用通用清单)。
// 由调用方从返回的发现里综合(根因聚类、文档、摘要)。

export const meta = {
  name: 'parity-audit',
  description: '完整能力对账:底座 vs 重写 —— 一份完整、按严重度排序、带证据的缺口清单',
  phases: [{ title: 'Audit', detail: '一维度一审计员,读两棵树,逐行对比' }],
}

const BASE = '<BASELINE 源码绝对路径>'
const NEW = '<NEW/重写 源码绝对路径>'

const COMMON = `
你在审计同一产品两个实现之间的 能力对账(CAPABILITY PARITY)。
- BASELINE(已知良好 / 当前在用的标准): ${BASE}
- NEW(被审的重写/迁移):              ${NEW}
对于 你的 维度:读两棵树里的 真实代码,列举每个底座能力,核对 NEW 是否对上。
底座是参照标准 —— 找出 NEW 缺失(MISSING)、只部分(PARTIAL)、或实现分歧(DIVERGENT)的地方。
规则:两侧都标 file:line(缺失则 '—');在你的维度内穷尽;每条都扎在底座代码里(别编底座没有的能力);
对齐('full')项也列出,好让覆盖可见。
status: full|partial|missing|divergent。severity: blocker(破交付/出错输出)|major(可见缺口)|minor|ok。`

const SCHEMA = {
  type: 'object',
  required: ['dimension', 'items'],
  properties: {
    dimension: { type: 'string' },
    items: {
      type: 'array',
      items: {
        type: 'object',
        required: ['capability', 'status', 'severity', 'baseRef'],
        properties: {
          capability: { type: 'string' },
          status: { type: 'string', enum: ['full', 'partial', 'missing', 'divergent'] },
          severity: { type: 'string', enum: ['blocker', 'major', 'minor', 'ok'] },
          baseRef: { type: 'string' },
          newRef: { type: 'string' },
          detail: { type: 'string' },
        },
      },
    },
  },
}

// 这些从底座里推。每个都指向该轴对应的具体 底座+新版 文件/符号。
const DIMENSIONS = [
  { key: 'dimension-1', prompt: `${COMMON}\n维度: <名字>。底座: <文件/符号>。新版: <文件/符号>。<要比什么>。` },
  // ... 共 ~8–15 个维度,以小重叠覆盖整个产品 ...
]

phase('Audit')
const results = (await parallel(DIMENSIONS.map((d) => () =>
  agent(d.prompt, { label: `audit:${d.key}`, phase: 'Audit', schema: SCHEMA })
))).filter(Boolean)

const all = results.flatMap((r) => (r.items || []).map((it) => ({ dimension: r.dimension, ...it })))
const gaps = all.filter((it) => it.status !== 'full')
const bySev = (s) => gaps.filter((g) => g.severity === s)
return {
  capabilitiesChecked: all.length,
  atParity: all.length - gaps.length,
  gapCount: gaps.length,
  blockers: bySev('blocker'),
  major: bySev('major'),
  minor: bySev('minor'),
}
// 然后(在调用方):把 `gaps` 按根因聚类、写带版本的文档、给出摘要 + 修复顺序。
