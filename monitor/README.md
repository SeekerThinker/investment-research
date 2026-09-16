# Market Research Monitor

A lightweight, Git-native discovery and market-behavior layer for the private `investment-research` repository.

## Purpose

The monitor supports four parallel research inputs rather than treating news as the only starting point:

`Market Behavior + Leading Indicators + Narrative/Attention + Verification/Confirmation`

It does **not** produce mechanical buy/sell decisions. Machine outputs are discovery and diagnostic inputs for the daily/weekly research process.

Research methodology is defined in `metadata/research-os.md` and `metadata/market-behavior.md`.

## Collectors

### News / verification discovery

`monitor/news_monitor_v2.py` collects official RSS and broad discovery sources, normalizes and deduplicates them, and writes an unverified `NEWS-*` candidate queue.

Primary direct feeds currently include NBS, HKEX, Federal Reserve and ECB. GDELT is a degradable broad-discovery supplement rather than the operational backbone.

### Market behavior

`monitor/market_behavior.py` reads the securities research index and collects low-frequency daily market data for tracked A/H legs. It calculates:

- 5D / 20D returns;
- 5D / 20D relative returns versus CSI 300 for A-shares and Hang Seng Index for HK legs;
- current volume versus prior 20-day average;
- 60-day volume percentile;
- distance from the 20-day high;
- 20-day annualized realized volatility;
- machine `phase_hint`, `gap_hint`, `crowding_hint` and `distribution_risk_hint`.

Market data is cached so frequent news-monitor runs do not repeatedly download six months of daily prices. The market adapter uses Yahoo Finance public market data through yfinance as a research convenience layer; it is not exchange-official data.

Formal M0–M5 / PF Gap decisions remain in `tracking/market-behavior.md` and require research interpretation.

## Output

News layer:

- `data/news/candidates/YYYY-MM-DD.jsonl`
- `data/news/latest.md`
- `data/news/state.json`
- `data/news/health.json`

Market layer:

- `data/market/latest.json`
- `data/market/latest.md`
- `data/market/health.json`
- `data/market/state.json`

Research layer:

- `tracking/market-behavior.md`
- `tracking/leading-indicators.md`
- `tracking/model-audit.md`
- `index/events.md`, `index/themes.md`, `index/securities.md`, `tracking/hypotheses.md`, `tracking/catalysts.md`

Presentation layer:

- `dashboard/README.md`

## Research OS validation

`monitor/validate_research_os.py` protects the structured research database against schema drift. Each workflow run verifies:

- required methodology and tracking files exist;
- F/I/S/R evidence labels are valid;
- V0–V5/N/A verification stages are valid;
- M0–M5 market phases and PF Gap vocabulary are valid;
- crowding / distribution-risk vocabulary is controlled;
- active or pending securities link to a valid `MBH-*` market-behavior record;
- active hypotheses have leading-indicator links;
- catalyst A/B/C classifications and Model Audit results are valid.

A structural failure stops the workflow rather than silently publishing a malformed workbench.

## Scheduling and concurrency

`.github/workflows/news-monitor.yml` runs in `Asia/Shanghai` time:

- 07:00–18:59: minute 17 and 47 of each hour;
- 19:00–06:59: minute 17 of each hour;
- manual `workflow_dispatch` is available;
- relevant research/monitor code changes trigger an immediate validation run.

The workflow uses `cancel-in-progress: true`, so a stale run cannot block a newly deployed collector version.

## Health semantics

News health uses `ok / degraded / down` plus `operational=true/false`. Broad discovery can fail while the primary official-source backbone remains operational.

Market health is tracked independently. Market-data failure produces a warning and does not erase or override the research database; formal research should mark market behavior unavailable rather than inventing values.

## Research discipline

- NEWS candidates are unverified discovery records.
- Machine market hints are not M0–M5 conclusions.
- Media attention is a Narrative/Attention input, not a Truth Layer.
- Official information is especially important for Verification, but it is not the only discovery channel.
- Volume alone must not be interpreted as institutional accumulation/distribution.
- Formal Distribution Risk requires corroborating price, crowding, leading-indicator, narrative and fundamental evidence.
- Historical reports under `reports/` remain immutable.

## Run locally

```bash
python -m pip install -r monitor/requirements.txt
python monitor/validate_research_os.py
python monitor/news_monitor_v2.py
python monitor/market_behavior.py --force
python monitor/render_dashboard.py
```

News source configuration is in `monitor/config.yaml`.
