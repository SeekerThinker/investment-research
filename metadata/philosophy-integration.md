# 思想库与研究执行桥接规范（Philosophy Integration）

**上层入口**：[`../philosophy/README.md`](../philosophy/README.md) → [`../philosophy/core-beliefs.md`](../philosophy/core-beliefs.md) → [`../philosophy/research-constitution.md`](../philosophy/research-constitution.md)。**增量变化**依 [`../philosophy/ideas.md`](../philosophy/ideas.md)、[`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md)、[`../philosophy/integration-map.md`](../philosophy/integration-map.md) 和 [`../philosophy/change-log.md`](../philosophy/change-log.md)。当前思想提炼版本：**v0.2（v0.1为历史基线；所有者意旨整理稿尚未逐字审核）**。本文件将思想落实为程序要求，不把理念当市场事实，不代替专业方法或直接给出证券结论。

## 1. 研究层级与冲突

思想/研究目的 → 宪章/证据与风控 → 各专业 `metadata/` 方法 → `data/`、`index/`、`tracking/` 可核对材料 → 有截止时间的新 `reports/` → `latest/` 和免费网页。事实能修正模型和想法，不得用理念过滤负面证据。新观点与旧原则冲突时先记录 IDEA 和未决项，不倒写旧报告；明确执行要求可以落实，但提炼措辞仍可等待所有者逐字审阅。

## 2. 新研究应用合同

- **全市场日报/盘中更新（P07—P09）**：后台独立扫描九类市场信息并披露覆盖与数据缺口，**正式资讯先合并同一投资因果链，再以约5—7面向、通常7—10且最多12条呈现**。每条保留真实日期/来源、具体正负传导、条件性机会与风险、强度/期限、已定价及可证伪验证；不得将旧闻重新包装。细则见 [`daily-coverage-policy.md`](daily-coverage-policy.md)、[`news-investment-impact-policy.md`](news-investment-impact-policy.md)。关键资料虽未精选仍可在免费完整报告、来源和覆盖记录追溯。
- **行业/公司**：明确真实供需、公司暴露与收入→毛利→净利→CFO/FCF，分清行业Beta与公司Alpha，记录反例和重大财务风险。执行 [`research-os.md`](research-os.md)、[`source-policy.md`](source-policy.md)。
- **长期估值/回撤**：20年分段所有者现金流，50年竞争寿命与终值敏感性；复权回撤、20/60日量能、同日价格、净债务、CAPEX、营运资本、股本稀释都须核实。证据不足写待估值，缩量非反弹保证。执行 [`long-horizon-value-policy.md`](long-horizon-value-policy.md)、[`market-behavior.md`](market-behavior.md)。
- **周报/月报**：回顾各期限影响映射的兑现/失效、价值假设及永久损失风险，保留证伪，不以正文数量代替分析质量；周/月详细资料保留于免费报告页，而非叠加成首页“今日”资讯。

## 3. 版本、摘要与公开呈现

新正式研究可注明：`思想库：v0.2（提炼草案）；参考原则：Pxx；一致性/例外与证据缺口：……。` 引用只说明检查过研究方法，不代表结论受思想背书；不能追改旧报告。最新摘要 `latest/daily.md` 是可变的**研究者明确精选**阅读层，不改变不可变的报告原文。网站 `monitor/curate_homepage.py` 仅从该摘要抽取最多12条、最多7面向，不按完整报告出现顺序硬截，也不自动生成投资判断；量价、独立风险、周/月细节仍在免费报告和归档中。网站维持白底单列和思想库独立入口，不复制凭据、个人隐私或未获许可内容。

## 4. 新讨论的全体系传播

项目相关新想法依 [`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md) 登记；逐项检查 [`../philosophy/integration-map.md`](../philosophy/integration-map.md)，仅修改确有影响的专业规范、网站和日/周/月任务；将实际提交、回执、验证失败与无需修改理由写入 [`../philosophy/change-log.md`](../philosophy/change-log.md)。不得仅写思想库就声称全部下游已同步。