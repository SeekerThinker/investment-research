#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

import pandas as pd
import yfinance as yf

try:
    import baostock as bs
except Exception:
    bs = None

try:
    import akshare as ak
except Exception:
    ak = None

ROOT = Path(__file__).resolve().parents[1]
HISTORY_DIR = ROOT / "data/market/history"
UTC = timezone.utc


def now_utc() -> datetime:
    return datetime.now(UTC)


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("empty market-data frame")
    rename = {
        "date": "Date", "日期": "Date",
        "open": "Open", "开盘": "Open",
        "high": "High", "最高": "High",
        "low": "Low", "最低": "Low",
        "close": "Close", "收盘": "Close", "latest": "Close",
        "volume": "Volume", "成交量": "Volume",
        "amount": "Amount", "成交额": "Amount",
        "turn": "Turnover", "换手率": "Turnover",
    }
    out = df.rename(columns={k: v for k, v in rename.items() if k in df.columns}).copy()
    if "Date" not in out.columns and isinstance(out.index, pd.DatetimeIndex):
        out = out.reset_index()
        out = out.rename(columns={out.columns[0]: "Date"})
    required = ["Date", "Open", "High", "Low", "Close"]
    missing = [c for c in required if c not in out.columns]
    if missing:
        raise ValueError(f"missing columns {missing}")
    out["Date"] = pd.to_datetime(out["Date"], errors="coerce").dt.tz_localize(None)
    for col in ["Open", "High", "Low", "Close", "Volume", "Amount", "Turnover"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    if "Volume" not in out.columns:
        out["Volume"] = 0.0
    out = out.dropna(subset=["Date", "Close"]).sort_values("Date")
    out = out.drop_duplicates(subset=["Date"], keep="last")
    cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
    cols += [c for c in ["Amount", "Turnover"] if c in out.columns]
    return out[cols]


def _cache_path(key: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", key)
    return HISTORY_DIR / f"{safe}.csv"


def load_cache(key: str) -> pd.DataFrame | None:
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        return normalize_df(pd.read_csv(path))
    except Exception:
        return None


def save_cache(key: str, df: pd.DataFrame) -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    normalize_df(df).tail(300).to_csv(_cache_path(key), index=False)


def incremental_start(existing: pd.DataFrame | None, default_days: int = 220) -> datetime:
    if existing is None or existing.empty:
        return now_utc() - timedelta(days=default_days)
    last = pd.Timestamp(existing["Date"].max()).to_pydatetime().replace(tzinfo=UTC)
    return min(now_utc(), last + timedelta(days=1)) - timedelta(days=10)


def merge_history(existing: pd.DataFrame | None, fresh: pd.DataFrame) -> pd.DataFrame:
    merged = fresh if existing is None or existing.empty else pd.concat([existing, fresh], ignore_index=True)
    return normalize_df(merged).tail(300)


def yahoo_symbol(code: str) -> str:
    raw, market = code.split(".")
    if market == "SH":
        return f"{raw}.SS"
    if market == "SZ":
        return f"{raw}.SZ"
    if market == "HK":
        return f"{int(raw):04d}.HK"
    raise ValueError(f"unsupported code: {code}")


def fetch_yahoo(symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
    frame = yf.Ticker(symbol).history(
        start=start.date().isoformat(),
        end=(end + timedelta(days=1)).date().isoformat(),
        interval="1d", auto_adjust=True, repair=False, timeout=10,
    )
    if frame is None or frame.empty:
        raise ValueError(f"Yahoo returned no rows for {symbol}")
    return normalize_df(frame.reset_index())


def baostock_code(code: str) -> str:
    raw, market = code.split(".")
    if market == "SH":
        return f"sh.{raw}"
    if market == "SZ":
        return f"sz.{raw}"
    raise ValueError(f"BaoStock unsupported code: {code}")


class BaoStockSession:
    def __init__(self) -> None:
        self.logged_in = False
        self.login_error: str | None = None

    def __enter__(self):
        if bs is None:
            self.login_error = "baostock package unavailable"
            return self
        try:
            login = bs.login()
        except Exception as exc:
            self.login_error = f"BaoStock login exception: {exc}"
            return self
        if getattr(login, "error_code", "1") != "0":
            self.login_error = f"BaoStock login failed: {getattr(login, 'error_msg', 'unknown')}"
            return self
        self.logged_in = True
        self.login_error = None
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.logged_in:
            try:
                bs.logout()
            except Exception:
                pass

    def fetch(self, code: str, start: datetime, end: datetime) -> pd.DataFrame:
        if not self.logged_in or bs is None:
            raise RuntimeError(self.login_error or "BaoStock session unavailable")
        fields = "date,code,open,high,low,close,volume,amount,turn,tradestatus"
        rs = bs.query_history_k_data_plus(
            baostock_code(code), fields,
            start_date=start.strftime("%Y-%m-%d"), end_date=end.strftime("%Y-%m-%d"),
            frequency="d", adjustflag="2",
        )
        if getattr(rs, "error_code", "1") != "0":
            raise RuntimeError(f"BaoStock query failed {code}: {getattr(rs, 'error_msg', 'unknown')}")
        rows = []
        while (rs.error_code == "0") and rs.next():
            rows.append(rs.get_row_data())
        if not rows:
            raise ValueError(f"BaoStock returned no rows for {code}")
        frame = pd.DataFrame(rows, columns=rs.fields)
        if "tradestatus" in frame.columns:
            frame = frame[frame["tradestatus"].astype(str) == "1"]
        return normalize_df(frame)


def fetch_akshare_hk(code: str, start: datetime, end: datetime) -> pd.DataFrame:
    if ak is None:
        raise RuntimeError("akshare package unavailable")
    raw = code.split(".")[0].zfill(5)
    return normalize_df(ak.stock_hk_hist(
        symbol=raw, period="daily",
        start_date=start.strftime("%Y%m%d"), end_date=end.strftime("%Y%m%d"), adjust="qfq",
    ))


def fetch_akshare_hk_sina(code: str, start: datetime, end: datetime) -> pd.DataFrame:
    if ak is None:
        raise RuntimeError("akshare package unavailable")
    raw = code.split(".")[0].zfill(5)
    frame = normalize_df(ak.stock_hk_daily(symbol=raw, adjust="qfq"))
    mask = (frame["Date"] >= pd.Timestamp(start.date())) & (frame["Date"] <= pd.Timestamp(end.date()))
    frame = frame.loc[mask]
    if frame.empty:
        raise ValueError(f"AKShare/Sina returned no rows for {code}")
    return frame


def fetch_akshare_hsi(start: datetime, end: datetime) -> pd.DataFrame:
    if ak is None:
        raise RuntimeError("akshare package unavailable")
    frame = normalize_df(ak.stock_hk_index_daily_em(symbol="HSI"))
    mask = (frame["Date"] >= pd.Timestamp(start.date())) & (frame["Date"] <= pd.Timestamp(end.date()))
    frame = frame.loc[mask]
    if frame.empty:
        raise ValueError("AKShare HSI returned no rows in requested window")
    return frame


def fetch_with_cache(
    key: str,
    providers: list[tuple[str, Callable[[datetime, datetime], pd.DataFrame]]],
    min_rows: int = 30,
) -> tuple[pd.DataFrame, str, list[str]]:
    existing = load_cache(key)
    start = incremental_start(existing)
    end = now_utc() + timedelta(days=1)
    attempts: list[str] = []
    for name, fn in providers:
        try:
            fresh = fn(start, end)
            merged = merge_history(existing, fresh)
            if len(merged) < min_rows:
                raise ValueError(f"only {len(merged)} usable rows")
            save_cache(key, merged)
            return merged, name, attempts
        except Exception as exc:
            attempts.append(f"{name}: {str(exc)[:220]}")
    if existing is not None and len(existing) >= min_rows:
        attempts.append("cache: using stale local history because all providers failed")
        return existing, "local_cache_stale", attempts
    raise RuntimeError("; ".join(attempts) or f"no provider for {key}")
