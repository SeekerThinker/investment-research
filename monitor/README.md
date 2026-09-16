# Market Research Monitor

A lightweight, Git-native discovery and market-behavior layer for the private `investment-research` repository.

## Purpose

The monitor supports four parallel research inputs rather than treating news as the only starting point:

`Market Behavior + Leading Indicators + Narrative/Attention + Verification/Confirmation`

It does **not** produce mechanical buy/sell decisions. Machine outputs are discovery and diagnostic inputs for the daily/weekly research process.

Research methodology is defined in `metadata/research-os.md`, `metadata/market-behavior.md`, and `metadata/source-policy.md`.

## Collectors

### News / verification discovery

`monitor/news_monitor_v2.py` collects official RSS and broad discovery sources, normalizes and deduplicates them, and writes an unverified `NEWS-*` candidate queue.

Primary direct feeds currently include NBS, HKEX, Federal Reserve and ECB. GDELT is a degradable broad-discovery supplement rather than the operational backbone. The scheduled workflow runs every two hours around the clock. GDELT rotates one query family per run with a 12-hour lookback so the five-family rotation overlaps without requiring high-frequency public-API calls.

### Market behavior

`monitor/market_behavior_v2.py` reads the securities research index and collects low-frequency daily market data for tracked A/H legs. It calculates:

- 5D / 20D returns;
- 5D / 20D relative returns versus CSI 300 for A-shares and Hang Seng Index for HK legs;
- current volume versus prior 20-day average;
- 60-day volume percentile;
- distance from the 20-day high;
- 20-day annualized realized volatility;
- machine `phase_hint`, `gap_hint`, `crowding_hint` and `distribution_risk_hint`.

Market history is cached incrementally under `data/market/history/`. A-shares use BaoStock as the primary convenience source, while HK legs use AKShare/Eastmoney then AKShare/Sina, with Yahoo Finance/yfinance as a fallback. These are research-convenience sources, not exchange-official data.

If all live providers fail for a leg but a local cache is available, the cached history may still be emitted for continuity, but the workflow marks market health `degraded`; stale cache must never masquerade as a fresh observation.

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
- `data/market/history/*.csv`

Research layer:

- `tracking/market-behavior.md`
- `tracking/leading-indicators.md`
- `tracking/model-audit.md`
- `index/events.md`, `index/themes.md`, `index/securities.md`, `tracking/hypotheses.md`, `tracking/catalysts.md`

Presentation layer:

- `dashboard/README.md`

## Research OS validation

`monitor/validate_research_os.py` protects the structured research database against schema drift. Workflows validate before collection and again before commit. The validator checks, among other things:

- required methodology and tracking files exist;
- F/I/S/R evidence labels are valid;
- V0–V5/N/A verification stages are valid;
- M0–M5 market phases and PF Gap vocabulary are valid;
- crowding / distribution-risk vocabulary is controlled;
- active or pending securities link to valid market-behavior records;
- active hypotheses have leading-indicator links;
- catalyst A/B/C classifications and Model Audit results are valid.

A structural failure stops publication rather than silently publishing a malformed workbench.

## Scheduling, commits and concurrency

### Market data

`.github/workflows/market-data.yml` runs at **16:25 Asia/Shanghai, Monday–Friday**, and supports manual `workflow_dispatch`.

It also runs when the market collector/workflow, validator, renderer, requirements, or tracked securities index changes. This provides an immediate self-test after infrastructure changes without recursively triggering on machine-data commits.

### News discovery

`.github/workflows/news-monitor.yml` runs at **minute 17 every two hours, Asia/Shanghai**, around the clock. In particular, the 06:17 run refreshes discovery data before the 07:00 daily-research automation.

It also runs when the news collector/workflow, source config, validator, renderer or requirements change.

### Shared write discipline

Both workflows use the same `research-machine-data` concurrency group so two machine collectors cannot push simultaneously. They:

1. install pinned monitor dependencies;
2. compile relevant Python modules;
3. validate the research database;
4. execute the real collector;
5. render `dashboard/README.md`;
6. validate again;
7. commit only if tracked machine/presentation files changed;
8. pull/rebase and push back to the private default branch.

If a collector reports `down`, the workflow still attempts to persist available health/output first, then fails visibly. A failed collection must not look like a successful refresh.

## Health semantics

News health uses `ok / degraded / down` plus `operational=true/false`. Broad discovery can fail while the primary official-source backbone remains operational.

Market health is tracked independently. Live-provider failure may leave stale cached history available for continuity, but stale-cache fallback is explicitly downgraded to `degraded`. Formal research should state data cutoffs and never manufacture a new 5D/20D or market-behavior observation when the underlying market data is stale.

## Research discipline

- NEWS candidates are unverified discovery records.
- Machine market hints are not M0–M5 conclusions.
- Media attention is a Narrative/Attention input, not a Truth Layer.
- Official information is especially important for Verification, but it is not the only discovery channel.
- Volume alone must not be interpreted as institutional accumulation/distribution.
- Formal Distribution Risk requires corroborating price, crowding, leading-indicator, narrative and fundamental evidence.
- Historical reports under `reports/` remain immutable.
- The private GitHub repository remains the canonical project state; public/member publication should be produced through a separate filtered publication layer rather than changing this repository to public.

## Run locally

```bash
python -m pip install -r monitor/requirements.txt
python monitor/validate_research_os.py
python monitor/news_monitor_v2.py
python monitor/market_behavior_v2.py --force
python monitor/render_dashboard.py
python monitor/validate_research_os.py
```

News source configuration is in `monitor/config.yaml`.
