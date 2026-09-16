#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
UTC = timezone.utc


def now_utc() -> datetime:
    return datetime.now(UTC)


def iso(dt: datetime) -> str:
    return dt.astimezone(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(UTC)
    except Exception:
        return None


def markdown_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    lines = [ln.strip() for ln in path.read_text(encoding='utf-8').splitlines() if ln.strip().startswith('|')]
    if len(lines) < 3:
        return []
    headers = [x.strip() for x in lines[0].strip('|').split('|')]
    out: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [x.strip() for x in line.strip('|').split('|')]
        if len(cells) == len(headers):
            out.append(dict(zip(headers, cells)))
    return out


def expand_codes(cell: str) -> list[str]:
    return re.findall(r'\b\d{5,6}\.(?:SH|SZ|HK)\b', cell.upper())


def yahoo_symbol(code: str) -> tuple[str, str, str]:
    raw, market = code.split('.')
    if market == 'SH':
        return f'{raw}.SS', 'A', '000300.SS'
    if market == 'SZ':
        return f'{raw}.SZ', 'A', '000300.SS'
    if market == 'HK':
        return f'{int(raw):04d}.HK', 'HK', '^HSI'
    raise ValueError(f'unsupported code: {code}')


def pct_change(close, periods: int) -> float | None:
    if close is None or len(close) <= periods:
        return None
    old = float(close.iloc[-periods - 1])
    new = float(close.iloc[-1])
    if not old or math.isnan(old) or math.isnan(new):
        return None
    return new / old - 1.0


def round_pct(value: float | None) -> float | None:
    return None if value is None else round(value * 100.0, 2)


def volume_percentile(volume, window: int = 60) -> float | None:
    if volume is None or len(volume) < 5:
        return None
    values = [float(v) for v in volume.tail(window).tolist() if v is not None and not math.isnan(float(v))]
    if not values:
        return None
    current = values[-1]
    return sum(1 for v in values if v <= current) / len(values)


def volume_ratio(volume, window: int = 20) -> float | None:
    if volume is None or len(volume) < 3:
        return None
    current = float(volume.iloc[-1])
    prior = [float(v) for v in volume.iloc[max(0, len(volume) - window - 1):-1].tolist() if v is not None and not math.isnan(float(v))]
    if not prior:
        return None
    avg = sum(prior) / len(prior)
    return None if avg <= 0 else current / avg


def distance_from_high(close, high, window: int = 20) -> float | None:
    if close is None or high is None or len(close) < 2:
        return None
    highest = float(high.tail(window).max())
    current = float(close.iloc[-1])
    return None if highest <= 0 else current / highest - 1.0


def realized_vol(close, window: int = 20) -> float | None:
    if close is None or len(close) < 5:
        return None
    returns = close.pct_change().dropna().tail(window)
    if len(returns) < 3:
        return None
    std = float(returns.std())
    return None if math.isnan(std) else std * math.sqrt(252.0)


def phase_hint(rs5: float | None, rs20: float | None, vol_pct: float | None, vol_ratio20: float | None) -> str:
    rs5 = rs5 or 0.0
    rs20 = rs20 or 0.0
    vol_pct = vol_pct or 0.0
    vol_ratio20 = vol_ratio20 or 0.0
    if rs20 >= 0.20 and vol_pct >= 0.85:
        return 'M3'
    if rs20 >= 0.10 and (vol_pct >= 0.75 or vol_ratio20 >= 1.5):
        return 'M2'
    if rs20 >= 0.04 and vol_pct >= 0.60:
        return 'M1'
    if rs5 >= 0.03 and rs20 < 0.08 and vol_pct >= 0.60:
        return 'M0'
    return '未判定'


def crowding_hint(rs20: float | None, vol_pct: float | None) -> str:
    rs20 = rs20 or 0.0
    vol_pct = vol_pct or 0.0
    if rs20 >= 0.20 and vol_pct >= 0.90:
        return '极高'
    if rs20 >= 0.10 and vol_pct >= 0.80:
        return '高'
    if rs20 >= 0.05 or vol_pct >= 0.70:
        return '中'
    return '低'


def gap_hint(verification_stage: str, phase: str, rs20: float | None) -> str:
    stage_num = None
    if verification_stage.startswith('V') and verification_stage[1:].isdigit():
        stage_num = int(verification_stage[1:])
    if phase == 'M3' and (stage_num is None or stage_num <= 2):
        return 'PF3'
    if phase == 'M2' and (stage_num is None or stage_num <= 2):
        return 'PF2'
    if phase in {'M0', 'M1'} and (stage_num is None or stage_num <= 1):
        return 'PF1'
    if stage_num is not None and stage_num >= 4 and rs20 is not None:
        if rs20 < -0.05:
            return 'PF-1'
        if abs(rs20) <= 0.05:
            return 'PF0'
    return '未判定'


def distribution_risk_hint(crowding: str, rs5: float | None, dist_high20: float | None) -> str:
    if crowding in {'高', '极高'}:
        if (rs5 is not None and rs5 < 0) or (dist_high20 is not None and dist_high20 <= -0.05):
            return '高' if crowding == '高' else '极高'
        return '中'
    if crowding == '中' and rs5 is not None and rs5 < -0.03:
        return '中'
    return '低'


def fetch_history(symbol: str):
    ticker = yf.Ticker(symbol)
    # Do not enable yfinance's optional repair pipeline here. In recent yfinance
    # releases it can import heavy optional SciPy/sklearn dependencies; the
    # monitor only needs ordinary adjusted daily OHLCV for relative behavior.
    df = ticker.history(period='6mo', interval='1d', auto_adjust=True, repair=False, timeout=10)
    if df is None or df.empty or 'Close' not in df.columns:
        raise ValueError(f'no usable daily history for {symbol}')
    df = df.dropna(subset=['Close'])
    if df.empty:
        raise ValueError(f'empty close history for {symbol}')
    return df


def should_skip(state_path: Path, cache_minutes: int, force: bool) -> bool:
    if force or not state_path.exists():
        return False
    try:
        state = json.loads(state_path.read_text(encoding='utf-8'))
        last = parse_iso(state.get('last_success'))
    except Exception:
        return False
    if not last:
        return False
    fresh = now_utc() - last < timedelta(minutes=cache_minutes)
    return fresh and (ROOT / 'data/market/latest.json').exists() and (ROOT / 'data/market/health.json').exists()


def build_latest_md(payload: dict[str, Any]) -> str:
    lines = [
        '# Market Behavior — Latest Machine Snapshot', '',
        f"- Collected at: `{payload['collected_at']}`",
        f"- Securities legs: **{payload['health']['success']} ok / {payload['health']['failed']} failed**",
        '- Source: Yahoo Finance public market-data interface via yfinance; research convenience layer, not exchange-official data.', '',
        '> Machine hints are not trading signals. Formal M0–M5 / Price–Fundamental Gap decisions must combine price-volume behavior with narrative, leading indicators and fundamental verification.', '',
        '| 标的 | 代码 | 5D | 20D | 相对基准5D | 相对基准20D | 量比20D | 成交量60D分位 | 距20D高点 | phase_hint | gap_hint | crowding | distribution risk |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|',
    ]
    for item in payload['items']:
        def f_pct(key: str) -> str:
            v = item.get(key)
            return 'N/A' if v is None else f'{v:.2f}%'
        def f_num(key: str) -> str:
            v = item.get(key)
            return 'N/A' if v is None else f'{v:.2f}'
        lines.append(
            f"| {item['name']} | {item['code']} | {f_pct('return_5d_pct')} | {f_pct('return_20d_pct')} | "
            f"{f_pct('relative_5d_pct')} | {f_pct('relative_20d_pct')} | {f_num('volume_ratio_20d')} | "
            f"{f_pct('volume_percentile_60d_pct')} | {f_pct('distance_from_20d_high_pct')} | {item['phase_hint']} | "
            f"{item['gap_hint']} | {item['crowding_hint']} | {item['distribution_risk_hint']} |"
        )
    if payload['errors']:
        lines += ['', '## Failed legs', '']
        for error in payload['errors']:
            lines.append(f"- `{error['code']}`: {error['error']}")
    return '\n'.join(lines).rstrip() + '\n'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache-minutes', type=int, default=90)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    data_dir = ROOT / 'data/market'
    data_dir.mkdir(parents=True, exist_ok=True)
    state_path = data_dir / 'state.json'
    if should_skip(state_path, args.cache_minutes, args.force):
        print('market behavior cache is fresh; skipping external fetch')
        return 0

    securities = markdown_rows(ROOT / 'index/securities.md')
    legs: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in securities:
        for code in expand_codes(row.get('代码', '')):
            if code in seen:
                continue
            seen.add(code)
            yahoo, market, benchmark = yahoo_symbol(code)
            legs.append({
                'code': code,
                'name': row.get('名称', code),
                'verification_stage': row.get('verification_stage', 'N/A'),
                'research_stage': row.get('research_stage', ''),
                'yahoo_symbol': yahoo,
                'market': market,
                'benchmark': benchmark,
            })

    cache: dict[str, Any] = {}
    errors: list[dict[str, str]] = []
    items: list[dict[str, Any]] = []

    def history(symbol: str):
        if symbol not in cache:
            cache[symbol] = fetch_history(symbol)
        return cache[symbol]

    for leg in legs:
        try:
            df = history(leg['yahoo_symbol'])
            bench = history(leg['benchmark'])
            r5 = pct_change(df['Close'], 5)
            r20 = pct_change(df['Close'], 20)
            b5 = pct_change(bench['Close'], 5)
            b20 = pct_change(bench['Close'], 20)
            rs5 = None if r5 is None or b5 is None else r5 - b5
            rs20 = None if r20 is None or b20 is None else r20 - b20
            vol_pct = volume_percentile(df['Volume']) if 'Volume' in df.columns else None
            vol_ratio20 = volume_ratio(df['Volume']) if 'Volume' in df.columns else None
            dist_high20 = distance_from_high(df['Close'], df['High']) if 'High' in df.columns else None
            rv20 = realized_vol(df['Close'])
            phase = phase_hint(rs5, rs20, vol_pct, vol_ratio20)
            crowding = crowding_hint(rs20, vol_pct)
            gap = gap_hint(leg['verification_stage'], phase, rs20)
            distribution = distribution_risk_hint(crowding, rs5, dist_high20)
            last_date = str(df.index[-1].date())
            items.append({
                **leg,
                'last_market_date': last_date,
                'last_close': round(float(df['Close'].iloc[-1]), 4),
                'return_5d_pct': round_pct(r5),
                'return_20d_pct': round_pct(r20),
                'benchmark_return_5d_pct': round_pct(b5),
                'benchmark_return_20d_pct': round_pct(b20),
                'relative_5d_pct': round_pct(rs5),
                'relative_20d_pct': round_pct(rs20),
                'volume_ratio_20d': None if vol_ratio20 is None else round(vol_ratio20, 2),
                'volume_percentile_60d_pct': None if vol_pct is None else round(vol_pct * 100.0, 2),
                'distance_from_20d_high_pct': round_pct(dist_high20),
                'realized_volatility_20d_pct': round_pct(rv20),
                'phase_hint': phase,
                'gap_hint': gap,
                'crowding_hint': crowding,
                'distribution_risk_hint': distribution,
            })
        except Exception as exc:
            errors.append({'code': leg['code'], 'symbol': leg['yahoo_symbol'], 'error': str(exc)[:300]})

    success = len(items)
    failed = len(errors)
    total = success + failed
    operational = success >= max(1, math.ceil(total * 0.60)) if total else False
    payload = {
        'collected_at': iso(now_utc()),
        'source': 'Yahoo Finance public API via yfinance',
        'source_role': 'research_convenience_market_data',
        'items': items,
        'errors': errors,
        'health': {'operational': operational, 'success': success, 'failed': failed, 'total': total},
    }
    (data_dir / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (data_dir / 'latest.md').write_text(build_latest_md(payload), encoding='utf-8')
    health = {
        'status': 'ok' if operational and not failed else ('degraded' if operational else 'down'),
        'operational': operational,
        'checked_at': payload['collected_at'],
        'source': payload['source'],
        'success': success,
        'failed': failed,
        'errors': errors,
    }
    (data_dir / 'health.json').write_text(json.dumps(health, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state_path.write_text(json.dumps({'last_attempt': payload['collected_at'], 'last_success': payload['collected_at'] if operational else None}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"market_behavior status={health['status']} success={success} failed={failed}")
    return 0 if operational else 2


if __name__ == '__main__':
    raise SystemExit(main())
