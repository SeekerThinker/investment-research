# 思想库与研究执行桥接规范（Philosophy Integration）

**上层入口**：[`../philosophy/README.md`](../philosophy/README.md) → [`../philosophy/core-beliefs.md`](../philosophy/core-beliefs.md) → [`../philosophy/research-constitution.md`](../philosophy/research-constitution.md)。增量参见 [`../philosophy/ideas.md`](../philosophy/ideas.md)、[`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md)、[`../philosophy/integration-map.md`](../philosophy/integration-map.md) 和 [`../philosophy/change-log.md`](../philosophy/change-log.md)。**当前意旨提炼草案 v0.3；v0.1 是历史基线，所有者尚未逐字审定全文。** 本规范是研究方法而非证券结论；可核验事实与反证优先。

## 1. 上游到下游的约束

思想/研究目的 → 宪章与证据纪律 → 专业 `metadata/` 方法 → `data/`、`index/`、`tracking/` → 有真实截止时间的新 `reports/` → 可变 `latest/` → 免费网页。不同意见先记录 IDEA 与冲突，不悄悄修改历史报告；所有者明确的执行要求可落实，但编辑者补充应标注来源。任何思想都不得过滤负面证据。

## 2. 具体研究执行合同

- **全市场日报与盘中增量（P07—P10）**：独立扫描九面和真实交易时段，披露数据缺口；同因果链先合并，按5—7面向、通常7—10条、最多12条编辑精要。正式摘要由研究者将每条标为 `【投资机遇·面向】` 或 `【风险规避·面向】`。前者问事实、传导、潜在预期差、成立条件、强度期限及验证；后者问事实、传导、潜在预期差、风险触发、强度期限及验证。**不对每条再强制重复机会和风险两个字段**，但完整报告要保留重大反例、双向传导、来源和历史。所有“重大预期差、极高潜在收益或亏损”必须分别核验市场预期、同日价格、财报/FCF和估值；不足时仅写潜在线索与未判定。执行 [`daily-coverage-policy.md`](daily-coverage-policy.md) 和 [`news-investment-impact-policy.md`](news-investment-impact-policy.md)。
- **行业、公司与估值**：实际供需与公司暴露、Industry Beta/Company Alpha、收入→毛利→利润→CFO/FCF、债务/稀释、真实复权回撤与20/60日量能；20年分段所有者现金流、50年竞争寿命压力测试，现价同日与保守/基准/乐观价值区间独立检验。缩量不是见底保证；缺数据写待估值。执行 [`research-os.md`](research-os.md)、[`source-policy.md`](source-policy.md)、[`long-horizon-value-policy.md`](long-horizon-value-policy.md) 和 [`market-behavior.md`](market-behavior.md)。
- **周报/月报**：继续分别独立出现在首页，日报条数上限不适用于它们。复盘两种关注方向的事实及预期差验证、条件兑现、传导失败、现金流与永久损失风险，保留反例；不要对每则消息机械填写对称套话，也不把市场涨跌当价值结论。

## 3. 报告、首页与版本

新研究注明当前思想库版本/关联 Pxx/证据缺口和例外，只说明使用研究方法，不意味着所有者逐字批准结论。`latest/daily.md` 是人工精选的可变阅读层，不能超出不可变原报告事实；`monitor/curate_homepage.py` 只验证日精选的数量、字段和显式两类标签，网站以白底单列、分析分行呈现「投资机遇」「风险规避」，在其后独立显示周报、月报。首页每条链接免费全文；不复制凭据、隐私或无许可材料。历史 `reports/` 不回写。

## 4. 后续自由讨论的全体系传播

新想法按 [`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md) 入台账，逐项查 [`../philosophy/integration-map.md`](../philosophy/integration-map.md)：思想核心、新闻/估值规范、日报/周报/月报任务、最新摘要、网页、自动检查及无需修改层级；在 [`../philosophy/change-log.md`](../philosophy/change-log.md) 记实际提交、任务回执、部署结果与待处理项，不把未完成事项写作完成。
