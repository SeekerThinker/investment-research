# 思想库与研究执行桥接规范（Philosophy Integration）

**上层入口**：[`../philosophy/README.md`](../philosophy/README.md) → [`../philosophy/core-beliefs.md`](../philosophy/core-beliefs.md) → [`../philosophy/research-constitution.md`](../philosophy/research-constitution.md)。增量参见 [`../philosophy/ideas.md`](../philosophy/ideas.md)、[`../philosophy/idea-20260919-01.md`](../philosophy/idea-20260919-01.md)、[`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md)、[`../philosophy/integration-map.md`](../philosophy/integration-map.md) 和 [`../philosophy/change-log.md`](../philosophy/change-log.md)。**当前意旨提炼草案 v0.4；v0.1 是历史基线，所有者尚未逐字审定全文。** 本规范是研究方法而非证券结论；可核验事实与反证优先。

## 1. 上游到下游的约束

思想/研究目的 → 宪章与证据纪律 → 专业 `metadata/` 方法 → `data/`、`index/`、`tracking/` → 有真实截止时间的新 `reports/` → 可变 `latest/` → 免费网页。不同意见先记录 IDEA 与冲突，不悄悄修改历史报告；所有者明确的执行要求可落实，但编辑者补充应标注来源。任何思想都不得过滤负面证据。

## 2. 具体研究执行合同

- **全市场日报与盘中增量（P07—P10）**：独立扫描九面和真实交易时段，披露数据缺口；同因果链先合并，按5—7面向、通常7—10条、最多12条编辑精要。正式摘要由研究者将每条标为 `【投资机遇·面向】` 或 `【风险规避·面向】`。前者问事实、传导、潜在预期差、成立条件、强度期限及验证；后者问事实、传导、潜在预期差、风险触发、强度期限及验证。**不对每条再强制重复机会和风险两个字段**，但完整报告要保留重大反例、双向传导、来源和历史。所有“重大预期差、极高潜在收益或亏损”必须分别核验市场预期、同日价格、财报/FCF和估值；不足时仅写潜在线索与未判定。执行 [`daily-coverage-policy.md`](daily-coverage-policy.md) 和 [`news-investment-impact-policy.md`](news-investment-impact-policy.md)。
- **行业、公司与估值**：实际供需与公司暴露、Industry Beta/Company Alpha、收入→毛利→利润→CFO/FCF、债务/稀释、真实复权回撤与20/60日量能；20年分段所有者现金流、50年竞争寿命压力测试，现价同日与保守/基准/乐观价值区间独立检验。缩量不是见底保证；缺数据写待估值。执行 [`research-os.md`](research-os.md)、[`source-policy.md`](source-policy.md)、[`long-horizon-value-policy.md`](long-horizon-value-policy.md) 和 [`market-behavior.md`](market-behavior.md)。对于确有上游投入传导关系的 AI 基础设施/半导体等专题，另按 [`multi-horizon-capex-method.md`](multi-horizon-capex-method.md) 检查不同期限的 CAPEX、库存价格、公司订单、资本结构及 FCF；**这是一项选择性方法补充，不取代通用估值、其他行业研究或已有情景敏感性。**
- **AI 长期研究判断（P11，IDEA-20260919-01）**：所有者认为 AI 有长期生产力/需求潜力，并认为中美战略竞争可能支持研发及基础设施投入持续性。将此作为**可挑战的研究起点，不是既成事实或自动看多评级**。遇到与 AI 相关且本期有实质新证据的事件时，分别核查：（1）可观察应用、支付意愿、生产率与需求兑现；（2）有日期的一手政府预算、采购、政策与实际支出，区分明确披露和对未来政策/动机的推测；（3）芯片、网络、电力、数据中心、模型与应用等环节的供需、竞争、资本开支及利润/现金流归属；（4）算力效率提高、供给过剩、政策/财政变化、能源约束、估值过高等反证。将产业成长、企业盈利与证券价格/估值分别检验，保留数据截止时间和不确定性；缺乏可比预期、同日价格或 FCF 模型时，不得断言重大预期差、确定收益或政府投入保证。有关可验证上游投入→公司现金流的专题采用 [`multi-horizon-capex-method.md`](multi-horizon-capex-method.md)，但不能因为 P11 而强制每日刊登 AI 主题、挤占更重要的其他市场线索，或修改过往报告。
- **周报/月报**：继续分别独立出现在首页，日报条数上限不适用于它们。复盘两种关注方向的事实及预期差验证、条件兑现、传导失败、现金流与永久损失风险，保留反例；不要对每则消息机械填写对称套话，也不把市场涨跌当价值结论。涉及 AI 的较长周期研究可按 P11 追踪需求/政策实际投入/企业经营兑现与反证，不把重复旧消息冒充新证据。对于已建立证据链的专题，可用多期限方法做增量复核，缺证据不生成假数字。

## 3. 报告、首页与版本

新研究注明当前思想库版本/关联 Pxx/证据缺口和例外，只说明使用研究方法，不意味着所有者逐字批准结论。`latest/daily.md` 是人工精选的可变阅读层，不能超出不可变原报告事实；`monitor/curate_homepage.py` 只验证日精选的数量、字段和显式两类标签，网站以白底单列、分析分行呈现「投资机遇」「风险规避」，在其后独立显示周报、月报。首页每条链接免费全文；不复制凭据、隐私或无许可材料。历史 `reports/` 不回写。P11 及新的专题方法只影响**后续相关研究的问题与证据检查**，不重编既有摘要/报告、不预先创建季度或年度自动发布流程。三份历史投研资料的取舍另见 [`../docs/research-material-review-20260920.md`](../docs/research-material-review-20260920.md)，其中历史标的数值和建议不得自动提升为今日事实。

## 4. 后续自由讨论的全体系传播

新想法按 [`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md) 入台账，逐项查 [`../philosophy/integration-map.md`](../philosophy/integration-map.md)：思想核心、新闻/估值规范、日报/周报/月报任务、最新摘要、网页、自动检查及无需修改层级；在 [`../philosophy/change-log.md`](../philosophy/change-log.md) 记实际提交、任务回执、部署结果与待处理项，不把未完成事项写作完成。
