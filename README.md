# Investment Research

Public, auditable A-share and Hong Kong Stock Connect research project. All published reports are free to read; voluntary sponsorship does not change access or research conclusions.

Website: https://seekerthinker.github.io/investment-research/ (free report archive and voluntary support; payment link not yet enabled).

## Workbench

- Research workbench: [`dashboard/`](dashboard/)
- Latest market-behavior snapshot: [`data/market/latest.md`](data/market/latest.md)
- Latest news monitor summary: [`data/news/latest.md`](data/news/latest.md)
- Latest daily research: [`latest/daily.md`](latest/daily.md)
- Latest weekly research: [`latest/weekly.md`](latest/weekly.md)
- Latest monthly research: [`latest/monthly.md`](latest/monthly.md)

## System architecture

The research system no longer treats news as the only discovery entry point.

`Market Behavior + Leading Indicators + Narrative/Attention + Verification/Confirmation -> EVT -> THM -> HYP/CAT -> securities -> Model Audit -> daily/weekly/monthly review`

The repository uses a Research OS to keep market behavior, evidence quality, thesis maturity, company exposure, fundamental realization and model consistency separate.

### Research OS

- Research framework and lifecycle: [`metadata/research-os.md`](metadata/research-os.md)
- Market behavior methodology: [`metadata/market-behavior.md`](metadata/market-behavior.md)
- Source and evidence policy: [`metadata/source-policy.md`](metadata/source-policy.md)
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

NEWS candidates are discovery inputs only. Daily and weekly research must verify material candidates against primary/independent sources before promoting them into structured research.

## Reports

- Daily research: `reports/daily/`
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
