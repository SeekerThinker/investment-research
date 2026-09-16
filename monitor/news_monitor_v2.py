#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import feedparser
import requests

import news_monitor as base


def _retry_after_seconds(response: requests.Response, default: float, cap: float) -> float:
    raw = response.headers.get("Retry-After")
    if raw:
        try:
            return min(cap, max(0.0, float(raw)))
        except ValueError:
            pass
    return min(cap, max(0.0, default))


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None,
    config: dict[str, Any],
    retries: int | None = None,
    backoff_seconds: float | None = None,
) -> requests.Response:
    http = config.get("http", {}) or {}
    timeout = int(http.get("timeout_seconds", 20))
    retries = int(http.get("retries", 2) if retries is None else retries)
    backoff = float(http.get("backoff_seconds", 2.0) if backoff_seconds is None else backoff_seconds)
    cap = float(http.get("max_retry_after_seconds", 20))
    retry_statuses = set(http.get("retry_statuses", [408, 425, 429, 500, 502, 503, 504]))

    last: requests.Response | None = None
    for attempt in range(retries + 1):
        response = session.get(url, params=params, timeout=timeout, headers={"User-Agent": base.UA})
        last = response
        if response.status_code not in retry_statuses:
            response.raise_for_status()
            return response
        if attempt >= retries:
            response.raise_for_status()
        delay = _retry_after_seconds(response, backoff * (2**attempt), cap)
        print(f"[warn] HTTP {response.status_code}; retrying after {delay:.1f}s: {response.url}")
        time.sleep(delay)

    assert last is not None
    last.raise_for_status()
    return last


def _rotated_queries(gdelt: dict[str, Any]) -> list[dict[str, Any]]:
    queries = list(gdelt.get("queries", []) or [])
    if not queries:
        return []
    limit = max(1, min(int(gdelt.get("max_queries_per_run", 1)), len(queries)))
    rotation_seconds = max(300, int(gdelt.get("rotation_seconds", 1800)))
    slot = int(base.now_utc().timestamp() // rotation_seconds)
    start = slot % len(queries)
    return [queries[(start + i) % len(queries)] for i in range(limit)]


def fetch_gdelt(config: dict[str, Any], session: requests.Session) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    health: list[dict[str, Any]] = []
    gdelt = config.get("gdelt", {}) or {}
    if not gdelt.get("enabled", True):
        return items, health

    endpoint = gdelt.get("endpoint", "https://api.gdeltproject.org/api/v2/doc/doc")
    timespan = gdelt.get("timespan", "3h")
    maxrecords = int(gdelt.get("maxrecords", 50))
    spacing = float(gdelt.get("min_interval_seconds", 4.0))
    circuit_break_on_429 = bool(gdelt.get("circuit_break_on_429", True))
    selected = _rotated_queries(gdelt)

    for idx, spec in enumerate(selected):
        query = spec["query"] if isinstance(spec, dict) else str(spec)
        label = spec.get("label", "gdelt") if isinstance(spec, dict) else "gdelt"
        params = {
            "query": query,
            "mode": "ArtList",
            "maxrecords": maxrecords,
            "format": "json",
            "sort": "HybridRel",
            "timespan": timespan,
        }
        try:
            response = get_with_retry(
                session,
                endpoint,
                params=params,
                config=config,
                retries=int(gdelt.get("retries", 0)),
                backoff_seconds=float(gdelt.get("backoff_seconds", 3.0)),
            )
            payload = response.json()
            articles = payload.get("articles", []) or []
            health.append({
                "source": f"gdelt:{label}",
                "status": "ok",
                "items": len(articles),
                "tier": int(spec.get("tier", 3)) if isinstance(spec, dict) else 3,
                "role": "broad_discovery",
            })
            for article in articles:
                items.append({
                    "title": base.clean_text(article.get("title")),
                    "url": article.get("url", ""),
                    "published_at": base.parse_dt(article.get("seendate")),
                    "source": article.get("domain") or "GDELT",
                    "source_country": article.get("sourcecountry"),
                    "language": article.get("language"),
                    "summary": "",
                    "source_type": "gdelt",
                    "source_tier": int(spec.get("tier", 3)) if isinstance(spec, dict) else 3,
                    "discovery_query": label,
                })
        except requests.HTTPError as exc:
            code = exc.response.status_code if exc.response is not None else None
            health.append({
                "source": f"gdelt:{label}",
                "status": "error",
                "items": 0,
                "tier": int(spec.get("tier", 3)) if isinstance(spec, dict) else 3,
                "role": "broad_discovery",
                "error": f"HTTP {code}: {base.clean_text(str(exc))[:240]}",
            })
            print(f"[warn] GDELT query failed ({label}): {exc}")
            if code == 429 and circuit_break_on_429:
                print("[warn] GDELT circuit breaker opened after HTTP 429; remaining GDELT queries skipped this run")
                break
        except Exception as exc:
            health.append({
                "source": f"gdelt:{label}",
                "status": "error",
                "items": 0,
                "tier": int(spec.get("tier", 3)) if isinstance(spec, dict) else 3,
                "role": "broad_discovery",
                "error": base.clean_text(str(exc))[:300],
            })
            print(f"[warn] GDELT query failed ({label}): {exc}")

        if idx + 1 < len(selected):
            time.sleep(spacing)

    return items, health


def fetch_rss(config: dict[str, Any], session: requests.Session) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    health: list[dict[str, Any]] = []
    now = base.now_utc()

    for src in config.get("rss", []) or []:
        if not src.get("enabled", True):
            continue
        name = src.get("name") or src.get("url", "rss")
        tier = int(src.get("tier", 2))
        try:
            response = get_with_retry(session, src["url"], params=None, config=config)
            feed = feedparser.parse(response.content)
            raw_entries = list(feed.entries)
            max_entries = max(1, int(src.get("max_entries", 100)))
            entries = raw_entries[:max_entries]
            max_age_hours = src.get("max_age_hours")
            accepted = 0
            for entry in entries:
                published = base.parse_dt(entry.get("published") or entry.get("updated"))
                if max_age_hours is not None and published is not None:
                    age_hours = max(0.0, (now - published).total_seconds() / 3600.0)
                    if age_hours > float(max_age_hours):
                        continue
                accepted += 1
                items.append({
                    "title": base.clean_text(entry.get("title")),
                    "url": entry.get("link", ""),
                    "published_at": published,
                    "source": name,
                    "source_country": src.get("country"),
                    "language": src.get("language"),
                    "summary": base.clean_text(entry.get("summary") or entry.get("description"))[:500],
                    "source_type": "rss",
                    "source_tier": tier,
                    "discovery_query": name,
                })
            if getattr(feed, "bozo", False) and not raw_entries:
                raise ValueError(f"RSS parse failed: {getattr(feed, 'bozo_exception', 'unknown parser error')}")
            health.append({
                "source": f"rss:{name}",
                "status": "ok",
                "items": accepted,
                "scanned_items": len(entries),
                "raw_items": len(raw_entries),
                "tier": tier,
                "role": src.get("role", "direct_feed"),
            })
        except Exception as exc:
            health.append({
                "source": f"rss:{name}",
                "status": "error",
                "items": 0,
                "tier": tier,
                "role": src.get("role", "direct_feed"),
                "error": base.clean_text(str(exc))[:300],
            })
            print(f"[warn] RSS failed ({name}): {exc}")

    return items, health


def write_health_v2(
    path: Path,
    *,
    fetched: int,
    candidates: int,
    new_seen: int,
    source_health: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok_sources = [s for s in source_health if s.get("status") == "ok"]
    failed_sources = [s for s in source_health if s.get("status") == "error"]
    primary_ok = [s for s in ok_sources if int(s.get("tier", 9)) == 1]
    health_cfg = config.get("health", {}) or {}
    min_sources_ok = int(health_cfg.get("min_sources_ok", 3))
    min_primary_ok = int(health_cfg.get("min_primary_sources_ok", 2))
    operational = len(ok_sources) >= min_sources_ok and len(primary_ok) >= min_primary_ok

    if not operational:
        status = "down"
    elif failed_sources:
        status = "degraded"
    else:
        status = "ok"

    health = {
        "status": status,
        "operational": operational,
        "checked_at": base.iso(base.now_utc()),
        "items_fetched": fetched,
        "newly_seen": new_seen,
        "candidates": candidates,
        "sources_ok": len(ok_sources),
        "sources_failed": len(failed_sources),
        "primary_sources_ok": len(primary_ok),
        "health_thresholds": {
            "min_sources_ok": min_sources_ok,
            "min_primary_sources_ok": min_primary_ok,
        },
        "sources": source_health,
    }
    path.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return health


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="monitor/config.yaml")
    parser.add_argument("--state", default="data/news/state.json")
    args = parser.parse_args()

    config = base.load_config(Path(args.config))
    state_path = Path(args.state)
    state = base.load_state(state_path)
    base.prune_state(
        state,
        days=int(config.get("dedup", {}).get("state_days", 14)),
        max_items=int(config.get("dedup", {}).get("max_seen_items", 12000)),
    )

    session = requests.Session()
    rss_items, rss_health = fetch_rss(config, session)
    gdelt_items, gdelt_health = fetch_gdelt(config, session)
    source_health = rss_health + gdelt_health
    items = rss_items + gdelt_items
    candidates, new_seen = base.process(items, state, config)
    day = base.now_utc().strftime("%Y-%m-%d")

    base.append_jsonl(Path(f"data/news/candidates/{day}.jsonl"), [c.data for c in candidates])
    base.write_latest(Path("data/news/latest.md"), candidates, len(items), new_seen, source_health)

    state["updated_at"] = base.iso(base.now_utc())
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    health = write_health_v2(
        Path("data/news/health.json"),
        fetched=len(items),
        candidates=len(candidates),
        new_seen=new_seen,
        source_health=source_health,
        config=config,
    )

    print(
        f"status={health['status']} operational={health['operational']} fetched={len(items)} "
        f"new_seen={new_seen} candidates={len(candidates)} sources_ok={health['sources_ok']} "
        f"sources_failed={health['sources_failed']} primary_ok={health['primary_sources_ok']}"
    )
    return 0 if health["operational"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
