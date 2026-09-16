# Market Data Layer

本目录保存量价研究所需的机器快照。它与 `tracking/market-behavior.md` 的研究判断严格分离。

## Files

- `latest.json`：最新机器量价快照。
- `latest.md`：供工作台阅读的最新摘要。
- `health.json`：市场数据源健康状态。
- `state.json`：低频抓取节流状态。

## Metrics

每个证券腿尽量计算：5D/20D收益、相对基准5D/20D收益、成交量相对20日均值、近60日成交量分位、距20日高点、20日年化实现波动率，以及机器 `phase_hint` / `gap_hint` / `crowding_hint` / `distribution_risk_hint`。

这些 hint 只是可复现的筛选器，不是交易信号，也不能替代 M0–M5 与 Price–Fundamental Gap 的研究判断。

## Source policy

当前自动行情适配器使用 Yahoo Finance 的公开行情接口（通过 yfinance）作为研究便利层，并非交易所官方行情。关键价格、成交或异常交易结论应在正式日报/周报中用交易所或其他可信市场数据交叉验证。
