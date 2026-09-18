# Market Perspectives · 市场经纬

跨周期财经监测与投资研究。公开、可追溯的 A 股及港股通研究项目；所有已发布报告免费阅读，自愿赞助不影响研究结论或访问权。

**目前可用网站：** https://seekerthinker.github.io/investment-research/ 。Cloudflare Pages 的候选项目名为 `market-perspectives`，真实生产网址须以 Cloudflare 后台及页面核验结果为准，不能将候选网址视为已经上线。GitHub 仓库仍叫 `SeekerThinker/investment-research`。

## 从这里接手项目 · Start here

**新协作者／新 AI／跨对话继续工作：先打开 [`START_HERE.md`](START_HERE.md)，再读 [`AGENTS.md`](AGENTS.md) 与 [`docs/project-state.md`](docs/project-state.md)。** 这三份文件分别解释读取顺序、权限和证据边界、目前阻碍与下一步；它们不代替最新报告或平台的真实状态。本项目对外部 HARC 协作协议的选择性评估见 [`docs/collaboration-review.md`](docs/collaboration-review.md)。

网站托管配置见 [`docs/cloudflare-pages.md`](docs/cloudflare-pages.md)；Cloudflare 的实际创建、部署成功和分配网址须独立确认，不能凭 GitHub 构建检查推断。当前报告目录为日／盘中／周／月；季度与年度独立发布尚未建立，不能将规划写成已上线。

## Investment philosophy · 可持续演进的投资思想库

**从这里开始**：[`philosophy/README.md`](philosophy/README.md) → [`philosophy/core-beliefs.md`](philosophy/core-beliefs.md) → [`philosophy/research-constitution.md`](philosophy/research-constitution.md)。这里收纳项目所有者随时讨论提出的长期价值、价格、风险与研究原则，**与每日新闻和有日期的研究结论分离**。核心文本是意旨整理稿，编辑者的操作化建议单独标注，不冒充所有者逐字确认或确定的市场事实。

想法与追溯：[`philosophy/ideas.md`](philosophy/ideas.md) · [`philosophy/intake-and-propagation.md`](philosophy/intake-and-propagation.md) · [`philosophy/integration-map.md`](philosophy/integration-map.md) · [`philosophy/change-log.md`](philosophy/change-log.md)。执行桥梁：[`metadata/philosophy-integration.md`](metadata/philosophy-integration.md)。新思想经忠实提炼和版本记录后，检查其对市场/行业/公司/估值规范、报告结构、网站及日报/周报/月报任务的影响；只更新确实受影响的下游，明确未完成项。证据可推翻假设，历史报告保持不可变；没有可靠资料时不制造投资结论。

## Workbench

- Research workbench: [`dashboard/`](dashboard/)
- Latest market-behavior snapshot: [`data/market/latest.md`](data/market/latest.md)
- Latest news monitor summary: [`data/news/latest.md`](data/news/latest.md)
- Latest daily research: [`latest/daily.md`](latest/daily.md)
- Latest weekly research: [`latest/weekly.md`](latest/weekly.md)
- Latest monthly research: [`latest/monthly.md`](latest/monthly.md)

## System architecture

The research system no longer treats news as the only discovery entry point.

`Philosophy / Research Constitution → Market Behavior + Leading Indicators + Narrative/Attention + Verification/Confirmation → EVT → THM → HYP/CAT → securities → Model Audit → daily/weekly/monthly review`

The philosophy governs research questions and evidence discipline, **not predetermined market outcomes**. The Research OS keeps market behavior, evidence quality, thesis maturity, company exposure, fundamental realization and model consistency separate.

### Research OS

- Philosophy-to-execution bridge: [`metadata/philosophy-integration.md`](metadata/philosophy-integration.md)
- Research framework and lifecycle: [`metadata/research-os.md`](metadata/research-os.md)
- Market behavior methodology: [`metadata/market-behavior.md`](metadata/market-behavior.md)
- Source and evidence policy: [`metadata/source-policy.md`](metadata/source-policy.md)
- Whole-market independent daily: [`metadata/daily-coverage-policy.md`](metadata/daily-coverage-policy.md)
- Per-news investment impact: [`metadata/news-investment-impact-policy.md`](metadata/news-investment-impact-policy.md)
- Long-horizon owner value: [`metadata/long-horizon-value-policy.md`](metadata/long-horizon-value-policy.md)
- Evidence types: `F / I / S / R`
- Fundamental realization stages: `V0–V5` (`N/A` where not applicable)
- Market phases: `M0–M5`
- Price–Fundamental Gap: `PF-2 / PF-1 / PF0 / PF1 / PF2 / PF3`
- Research stages: `新发现 / 待验证 / 活跃研究 / 降级复核 / 关闭`
- Thesis status: `观察 / 强化 / 弱化 / 部分兑现 / 兑现 / 证伪 / 结束`

A high-confidence conclusion should be traceable through market behavior, leading indicators, source evidence, causal mechanism, company exposure, financial confirmation and Model Audit. Machine-generated hints must not silently become investment conclusions.

### Market behavior layer

- Collector: `monitor/market_behavior.py`
- Latest machine snapshot: `data/market/latest.json`
- Readable snapshot: `data/market/latest.md`
- Market-data health: `data/market/health.json`
- Research judgments: `tracking/market-behavior.md`

The machine layer calculates price/volume facts such as 5D/20D returns, relative strength, volume ratio, volume percentile, distance from the 20-day high and realized volatility. It may provide `phase_hint`, `gap_hint`, `crowding_hint` and `distribution_risk_hint`, but formal M0–M5 and PF Gap decisions require research interpretation.

The automated market-data adapter is a research convenience layer and is not exchange-official data. Material conclusions should be cross-checked against reliable market/exchange data in formal research.

### News / verification discovery layer

- Implementation: `monitor/news_monitor_v2.py`
- GitHub Actions: `.github/workflows/news-monitor.yml`
- Latest monitor run: `data/news/latest.md`
- Candidate queue: `data/news/candidates/YYYY-MM-DD.jsonl`
- Operational health: `data/news/health.json`
- Research OS validator: `monitor/validate_research_os.py`
- Philosophy/link integrity validator: `monitor/validate_philosophy.py`
- Collaboration/handoff validator: `monitor/validate_collaboration.py`

NEWS candidates are discovery inputs only. Daily and weekly research must verify material candidates against primary/independent sources before promoting them into structured research.

## Reports

- Daily research: `reports/daily/`
- Intraday additive research: `reports/intraday/`
- Weekly research: `reports/weekly/`
- Monthly research: `reports/monthly/`
- Latest daily: `latest/daily.md`
- Latest weekly: `latest/weekly.md`
- Latest monthly: `latest/monthly.md`

Historical reports under `reports/` are immutable research records. New evidence updates indexes and later reports instead of rewriting prior conclusions.

## Structured research

- Major events: `index/events.md`
- Themes: `index/themes.md`
- Securities / ETFs: `index/securities.md`
- Market behavior judgments: `tracking/market-behavior.md`
- Falsifiable hypotheses: `tracking/hypotheses.md`
- Catalysts and outcomes: `tracking/catalysts.md`
- Leading indicators: `tracking/leading-indicators.md`
- Model audit: `tracking/model-audit.md`
- Rolling risk calendar: `tracking/risk-calendar.md`

## Research discipline

- Separate machine discovery from research judgment. NEWS scores and market `*_hint` fields are not conclusions.
- Treat media primarily as Discovery / Narrative / Attention; treat official and first-party information primarily as Verification; treat orders, margins, profit and cash flow as Confirmation.
- Never infer “主力吸筹/出货” from volume alone. Distribution Risk requires multiple corroborating signals.
- Track price behavior and fundamental realization separately. A stronger business thesis can coexist with a worse price/reward setup when PF Gap and crowding rise.
- Separate industry Beta from company Alpha.
- Active HYP entries should have observable leading indicators and falsification windows.
- Catalysts are classified as A (direct profit change), B (higher realization probability), or C (industry-level).
- High-confidence company conclusions should pass or explicitly disclose Model Audit gaps.
- Preserve failed and falsified theses so weekly/monthly review measures research quality rather than hiding mistakes.
- Scoring, M phases and PF Gap are diagnostic only; they are not mechanical buy/sell or position-sizing rules.

## Index

### Daily

_Reports will be added automatically._

### Weekly

_Reports will be added automatically._

### Monthly

_Reports will be added automatically._

> Research only. Not personalized investment advice and not a guarantee of returns.
