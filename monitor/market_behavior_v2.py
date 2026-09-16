#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from market_providers import (
    BaoStockSession,
    fetch_akshare_hk,
    fetch_akshare_hk_sina,
    fetch_akshare_hsi,
    fetch_with_cache,
    fetch_yahoo,
    yahoo_symbol,
)

ROOT = Path(__file__).resolve().parents[1]
UTC = timezone.utc


def now_utc() -> datetime:
    return datetime.now(UTC)


def iso(dt: datetime) -> str:
    return dt.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except Exception:
        return None


def markdown_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [x.strip() for x in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [x.strip() for x in line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def expand_codes(cell: str) -> list[str]:
    return re.findall(r"\b\d{5,6}\.(?:SH|SZ|HK)\b", cell.upper())


def pct_change(close: pd.Series, periods: int) -> float | None:
    if len(close) <= periods:
        return None
    old, new = float(close.iloc[-periods - 1]), float(close.iloc[-1])
    if not old or math.isnan(old) or math.isnan(new):
        return None
    return new / old - 1.0


def round_pct(value: float | None) -> float | None:
    return None if value is None else round(value * 100.0, 2)


def volume_percentile(volume: pd.Series, window: int = 60) -> float | None:
    values = [float(v) for v in volume.tail(window).tolist() if pd.notna(v)]
    if len(values) < 5:
        return None
    current = values[-1]
    return sum(1 for v in values if v <= current) / len(values)


def volume_ratio(volume: pd.Series, window: int = 20) -> float | None:
    if len(volume) < 3:
        return None
    current = float(volume.iloc[-1])
    prior = [float(v) for v in volume.iloc[max(0, len(volume) - window - 1):-1].tolist() if pd.notna(v)]
    if not prior:
        return None
    avg = sum(prior) / len(prior)
    return None if avg <= 0 else current / avg


def distance_from_high(close: pd.Series, high: pd.Series, window: int = 20) -> float | None:
    if len(close) < 2:
        return None
    highest = float(high.tail(window).max())
    current = float(close.iloc[-1])
    return None if highest <= 0 else current / highest - 1.0


def realized_vol(close: pd.Series, window: int = 20) -> float | None:
    returns = close.pct_change().dropna().tail(window)
    if len(returns) < 3:
        return None
    std = float(returns.std())
    return None if math.isnan(std) else std * math.sqrt(252.0)


def phase_hint(rs5: float | None, rs20: float | None, vol_pct: float | None, vol_ratio20: float | None) -> str:
    rs5, rs20 = rs5 or 0.0, rs20 or 0.0
    vol_pct, vol_ratio20 = vol_pct or 0.0, vol_ratio20 or 0.0
    if rs20 >= 0.20 and vol_pct >= 0.85:
        return "M3"
    if rs20 >= 0.10 and (vol_pct >= 0.75 or vol_ratio20 >= 1.5):
        return "M2"
    if rs20 >= 0.04 and vol_pct >= 0.60:
        return "M1"
    if rs5 >= 0.03 and rs20 < 0.08 and vol_pct >= 0.60:
        return "M0"
    return "未判定"


def crowding_hint(rs20: float | None, vol_pct: float | None) -> str:
    rs20, vol_pct = rs20 or 0.0, vol_pct or 0.0
    if rs20 >= 0.20 and vol_pct >= 0.90:
        return "极高"
    if rs20 >= 0.10 and vol_pct >= 0.80:
        return "高"
    if rs20 >= 0.05 or vol_pct >= 0.70:
        return "中"
    return "低"


def gap_hint(stage: str, phase: str, rs20: float | None) -> str:
    stage_num = int(stage[1:]) if stage.startswith("V") and stage[1:].isdigit() else None
    if phase == "M3" and (stage_num is None or stage_num <= 2):
        return "PF3"
    if phase == "M2" and (stage_num is None or stage_num <= 2):
        return "PF2"
    if phase in {"M0", "M1"} and (stage_num is None or stage_num <= 1):
        return "PF1"
    if stage_num is not None and stage_num >= 4 and rs20 is not None:
        if rs20 < -0.05:
            return "PF-1"
        if abs(rs20) <= 0.05:
            return "PF0"
    return "未判定"


def distribution_risk_hint(crowding: str, rs5: float | None, dist_high20: float | None) -> str:
    if crowding in {"高", "极高"}:
        if (rs5 is not None and rs5 < 0) or (dist_high20 is not None and dist_high20 <= -0.05):
            return "高" if crowding == "高" else "极高"
        return "中"
    if crowding == "中" and rs5 is not None and rs5 < -0.03:
        return "中"
    return "低"


def should_skip(state_path: Path, cache_minutes: int, force: bool) -> bool:
    if force or not state_path.exists():
        return False
    try:
        last = parse_iso(json.loads(state_path.read_text(encoding="utf-8")).get("last_success"))
    except Exception:
        return False
    return bool(last and now_utc() - last < timedelta(minutes=cache_minutes))


def build_latest_md(payload: dict[str, Any]) -> str:
    counts: dict[str, int] = {}
    for item in payload["items"]:
        counts[item["provider"]] = counts.get(item["provider"], 0) + 1
    provider_text = ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"
    lines = [
        "# Market Behavior — Latest Machine Snapshot", "",
        f"- Collected at: `{payload['collected_at']}`",
        f"- Securities legs: **{payload['health']['success']} ok / {payload['health']['failed']} failed**",
        f"- Provider mix: **{provider_text}**",
        "- A股：BaoStock 主源；港股：AKShare/Eastmoney → AKShare/Sina → Yahoo/yfinance；历史行情使用本地增量缓存。", "",
        "> Machine hints are not trading signals. Free third-party data can contain delays/errors; material anomalies require exchange or another reliable source verification.", "",
        "| 标的 | 代码 | provider | 5D | 20D | 相对基准5D | 相对基准20D | 量比20D | 成交量60D分位 | 距20D高点 | phase_hint | gap_hint | crowding | distribution risk |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for item in payload["items"]:
        def fp(key: str) -> str:
            v = item.get(key)
            return "N/A" if v is None else f"{v:.2f}%"
        def fn(key: str) -> str:
            v = item.get(key)
            return "N/A" if v is None else f"{v:.2f}"
        lines.append(
            f"| {item['name']} | {item['code']} | {item['provider']} | {fp('return_5d_pct')} | {fp('return_20d_pct')} | "
            f"{fp('relative_5d_pct')} | {fp('relative_20d_pct')} | {fn('volume_ratio_20d')} | {fp('volume_percentile_60d_pct')} | "
            f"{fp('distance_from_20d_high_pct')} | {item['phase_hint']} | {item['gap_hint']} | {item['crowding_hint']} | {item['distribution_risk_hint']} |"
        )
    if payload["errors"]:
        lines += ["", "## Failed legs", ""]
        for error in payload["errors"]:
            lines.append(f"- `{error['code']}`: {error['error']}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-minutes", type=int, default=360)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    data_dir = ROOT / "data/market"
    data_dir.mkdir(parents=True, exist_ok=True)
    state_path = data_dir / "state.json"
    if should_skip(state_path, args.cache_minutes, args.force):
        print("market behavior cache is fresh; skipping external fetch")
        return 0

    securities = markdown_rows(ROOT / "index/securities.md")
    legs, seen = [], set()
    for row in securities:
        for code in expand_codes(row.get("代码", "")):
            if code in seen:
                continue
            seen.add(code)
            legs.append({
                "code": code,
                "name": row.get("名称", code),
                "verification_stage": row.get("verification_stage", "N/A"),
                "research_stage": row.get("research_stage", ""),
                "market": "HK" if code.endswith(".HK") else "A",
            })

    items, errors = [], []
    provider_health: dict[str, dict[str, int]] = {}

    with BaoStockSession() as bao:
        benchmark_cache: dict[str, tuple[pd.DataFrame, str]] = {}

        def benchmark(market: str) -> tuple[pd.DataFrame, str]:
            if market in benchmark_cache:
                return benchmark_cache[market]
            if market == "A":
                df, provider, _ = fetch_with_cache("BENCHMARK_CSI300", [
                    ("baostock", lambda s, e: bao.fetch("000300.SH", s, e)),
                    ("yfinance", lambda s, e: fetch_yahoo("000300.SS", s, e)),
                ], min_rows=30)
            else:
                df, provider, _ = fetch_with_cache("BENCHMARK_HSI", [
                    ("akshare_eastmoney", fetch_akshare_hsi),
                    ("yfinance", lambda s, e: fetch_yahoo("^HSI", s, e)),
                ], min_rows=30)
            benchmark_cache[market] = (df, provider)
            return df, provider

        for leg in legs:
            try:
                if leg["market"] == "A":
                    providers = [
                        ("baostock", lambda s, e, code=leg["code"]: bao.fetch(code, s, e)),
                        ("yfinance", lambda s, e, code=leg["code"]: fetch_yahoo(yahoo_symbol(code), s, e)),
                    ]
                else:
                    providers = [
                        ("akshare_eastmoney", lambda s, e, code=leg["code"]: fetch_akshare_hk(code, s, e)),
                        ("akshare_sina", lambda s, e, code=leg["code"]: fetch_akshare_hk_sina(code, s, e)),
                        ("yfinance", lambda s, e, code=leg["code"]: fetch_yahoo(yahoo_symbol(code), s, e)),
                    ]
                df, provider, attempts = fetch_with_cache(leg["code"], providers, min_rows=1)
                bench, benchmark_provider = benchmark(leg["market"])
                r5, r20 = pct_change(df["Close"], 5), pct_change(df["Close"], 20)
                b5, b20 = pct_change(bench["Close"], 5), pct_change(bench["Close"], 20)
                rs5 = None if r5 is None or b5 is None else r5 - b5
                rs20 = None if r20 is None or b20 is None else r20 - b20
                vp = volume_percentile(df["Volume"])
                vr = volume_ratio(df["Volume"])
                dh = distance_from_high(df["Close"], df["High"])
                phase = phase_hint(rs5, rs20, vp, vr)
                crowd = crowding_hint(rs20, vp)
                provider_health.setdefault(provider, {"success": 0, "fallbacks": 0})
                provider_health[provider]["success"] += 1
                if attempts:
                    provider_health[provider]["fallbacks"] += 1
                items.append({
                    **leg, "provider": provider, "provider_attempts": attempts, "benchmark_provider": benchmark_provider,
                    "history_rows": len(df), "insufficient_history": len(df) < 21,
                    "last_market_date": str(pd.Timestamp(df["Date"].iloc[-1]).date()),
                    "last_close": round(float(df["Close"].iloc[-1]), 4),
                    "return_5d_pct": round_pct(r5), "return_20d_pct": round_pct(r20),
                    "benchmark_return_5d_pct": round_pct(b5), "benchmark_return_20d_pct": round_pct(b20),
                    "relative_5d_pct": round_pct(rs5), "relative_20d_pct": round_pct(rs20),
                    "volume_ratio_20d": None if vr is None else round(vr, 2),
                    "volume_percentile_60d_pct": None if vp is None else round(vp * 100.0, 2),
                    "distance_from_20d_high_pct": round_pct(dh),
                    "realized_volatility_20d_pct": round_pct(realized_vol(df["Close"])),
                    "phase_hint": phase, "gap_hint": gap_hint(leg["verification_stage"], phase, rs20),
                    "crowding_hint": crowd, "distribution_risk_hint": distribution_risk_hint(crowd, rs5, dh),
                })
            except Exception as exc:
                errors.append({"code": leg["code"], "error": str(exc)[:500]})

    success, failed = len(items), len(errors)
    total = success + failed
    operational = success >= max(1, math.ceil(total * 0.60)) if total else False
    policy = {
        "A_primary": "BaoStock",
        "HK_primary": "AKShare/Eastmoney",
        "HK_secondary": "AKShare/Sina",
        "fallback": "Yahoo Finance/yfinance",
        "cache": "data/market/history/*.csv incremental local cache",
        "tushare_validator": "optional/not configured; add only with TUSHARE_TOKEN",
    }
    payload = {
        "collected_at": iso(now_utc()), "source_role": "multi_provider_research_convenience_market_data",
        "provider_policy": policy, "provider_health": provider_health, "items": items, "errors": errors,
        "health": {"operational": operational, "success": success, "failed": failed, "total": total},
    }
    (data_dir / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (data_dir / "latest.md").write_text(build_latest_md(payload), encoding="utf-8")
    health = {
        "status": "ok" if operational and not failed else ("degraded" if operational else "down"),
        "operational": operational, "checked_at": payload["collected_at"], "provider_policy": policy,
        "provider_health": provider_health, "success": success, "failed": failed, "errors": errors,
    }
    (data_dir / "health.json").write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state_path.write_text(json.dumps({"last_attempt": payload["collected_at"], "last_success": payload["collected_at"] if operational else None}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"market_behavior_v2 status={health['status']} success={success} failed={failed} providers={provider_health}")
    return 0 if operational else 2


if __name__ == "__main__":
    raise SystemExit(main())
