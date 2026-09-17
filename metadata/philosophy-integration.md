# 思想库与研究执行桥接规范（Philosophy Integration）

**上层入口**：[`../philosophy/README.md`](../philosophy/README.md) → [`../philosophy/core-beliefs.md`](../philosophy/core-beliefs.md) → [`../philosophy/research-constitution.md`](../philosophy/research-constitution.md)。**增量变化**依 [`../philosophy/ideas.md`](../philosophy/ideas.md)、[`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md)、[`../philosophy/integration-map.md`](../philosophy/integration-map.md) 和 [`../philosophy/change-log.md`](../philosophy/change-log.md)。当前思想提炼版本：**v0.1（所有者意旨整理稿，尚未逐字审核）**。本文件将思想落实为程序要求；它并不声称理念是市场事实，也不代替专业方法或直接给出证券结论。

## 1. 研究层级与冲突

思想/研究目的 → 宪章/证据与风控 → 各专业 `metadata/` 方法 → `data/`、`index/`、`tracking/` 可核对材料 → 有截止时间的新 `reports/` → `latest/` 和免费网页。数据能修正模型和想法；研究过程不得用理念过滤负面证据。遇到新想法与旧原则冲突，先登记为 IDEA 和待确认项，不直接改写已有报告；如执行要求明确则可同步流程，但转述文本仍标注待逐字审阅。原则变化不改变已存在报告的历史版本。

## 2. 各类新稿的应用合同

- **全市场日报/盘中更新**：先独立扫描且标记最后完成交易日；逐条提供事实/来源、传导对象和正负方向、条件性机会/风险、影响强度与期限、定价程度及可证伪验证；保持首页单列摘要可直接阅读。执行 [`daily-coverage-policy.md`](daily-coverage-policy.md)、[`news-investment-impact-policy.md`](news-investment-impact-policy.md)。不得把前期事件重复包装成当期新闻。
- **行业/公司**：先明确行业变化再核对个股真实订单/暴露与收入→毛利→净利润→CFO/FCF，识别行业Beta与公司Alpha；记录相反事实及重大财务风险。执行 [`research-os.md`](research-os.md)、[`source-policy.md`](source-policy.md)。
- **长期估值/回撤**：20年分段所有者自由现金流，50年仅远端竞争寿命/终值敏感性；核查复权阶段回撤、20/60日量能及真实行情，和净债务、CAPEX、营运资本、股权稀释、现金流转换。没有足够数据则写待估值，不能由缩量推断必然反弹。执行 [`long-horizon-value-policy.md`](long-horizon-value-policy.md)、[`market-behavior.md`](market-behavior.md)。
- **周报/月报**：除了总结当期信息，还要复盘上期影响映射的兑现/证伪、估值假设与风险，保存失败案例；不得后验篡改历史。

## 3. 发布时的版本与证据说明

新正式研究末尾建议附：`思想库：v0.1（提炼稿）；参考原则：Pxx；一致性：已核对/存在冲突及理由；未决数据：……。` 该行是**引用和检查记录**，不是研究结论的背书。缺少该行时不能自动认定研报逻辑错误，但应在下一次新稿流程补上；不可追改已发布历史。对于 F/I/S/R、Model Audit、披露和公共仓库安全纪律，各专业规范继续有效。

## 4. 从新讨论到执行端传播

当所有者在对话中自由提出新想法并明确与本项目相关，依 [`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md) 提炼和入库；逐项检查 [`../philosophy/integration-map.md`](../philosophy/integration-map.md)，确实受影响的专业规范、报告模板、监测与站点、日报/周报/月报定时任务须更新；在 [`../philosophy/change-log.md`](../philosophy/change-log.md) 写实际提交/执行回执与未完成项目。**不能仅改思想库就宣称所有下游已自动同步**。仓库连接、权限或验证不可用时，如实标注未执行。

## 5. 网站边界

思想库是跨期方法而非实时资讯；网站若引用须设置独立思想入口、版本和“非即时行情”说明，不将思想条目混进当日新闻条数。所有已发布报告继续免费读，白色单列页面保持；不要向网站复制未经许可、凭据或私人信息。