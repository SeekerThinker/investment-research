#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import requests
import yaml

UTC = timezone.utc
UA = "investment-research-news-monitor/1.1 (+https://github.com/seekerthinker/investment-research)"

CATEGORY_KEYWORDS = {
    "policy": ["policy", "regulation", "regulator", "tariff", "subsidy", "sanction", "export control", "政策", "监管", "关税", "补贴", "制裁", "出口管制"],
    "macro": ["inflation", "cpi", "ppi", "gdp", "pmi", "interest rate", "central bank", "fed", "ecb", "boj", "央行", "利率", "通胀", "国内生产总值", "采购经理"],
    "technology": ["semiconductor", "chip", "artificial intelligence", " ai ", "server", "datacenter", "data center", "hbm", "pcb", "robot", "半导体", "芯片", "人工智能", "服务器", "数据中心", "机器人"],
    "energy_materials": ["oil", "gas", "lng", "copper", "gold", "lithium", "rare earth", "coal", "uranium", "原油", "天然气", "铜", "黄金", "锂", "稀土", "煤", "铀"],
    "geopolitics": ["war", "ceasefire", "conflict", "election", "military", "geopolit", "nato", "战争", "停火", "冲突", "选举", "军事", "地缘"],
    "company": ["earnings", "guidance", "merger", "acquisition", "order", "contract", "approval", "launch", "recall", "财报", "业绩", "指引", "并购", "订单", "合同", "获批", "发布", "召回"],
}

CHINA_TERMS = [
    "china", "chinese", "beijing", "shanghai", "shenzhen", "hong kong", "hongkong", "renminbi", "yuan", "pboc", "a-share", "a share", "hang seng", "mainland",
    "中国", "北京", "上海", "深圳", "香港", "人民币", "央行", "沪深", "a股", "港股",
]
TRANSMISSION_TERMS = [
    "semiconductor", "chip", "server", "datacenter", "oil", "gas", "copper", "gold", "lithium", "rare earth", "shipping", "tariff", "sanction", "export control", "interest rate", "inflation", "commodity",
    "半导体", "芯片", "服务器", "数据中心", "原油", "天然气", "铜", "黄金", "锂", "稀土", "航运", "关税", "制裁", "出口管制", "利率", "通胀", "大宗商品",
]
HIGH_IMPACT_TERMS = [
    "emergency", "ban", "approve", "approval", "cut", "hike", "surge", "plunge", "record", "shortage", "default", "bankruptcy", "war", "ceasefire", "sanction", "tariff", "merger", "acquisition",
    "紧急", "禁令", "批准", "降息", "加息", "暴涨", "暴跌", "创纪录", "短缺", "违约", "破产", "战争", "停火", "制裁", "关税", "并购",
]


@dataclass
class Candidate:
    data: dict[str, Any]


def now_utc() -> datetime:
    return datetime.now(UTC)


def iso(dt: datetime) -> str:
    return dt.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_title(title: str) -> str:
    title = clean_text(title).lower()
    title = re.sub(r"\s*[-–—|]\s*[^-–—|]{2,40}$", "", title)
    title = re.sub(r"[^\w\u4e00-\u9fff]+", " ", title, flags=re.UNICODE)
    return re.sub(r"\s+", " ", title).strip()


def canonical_url(url: str) -> str:
    try:
        parts = urlsplit(url)
        tracking = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid", "mc_cid", "mc_eid"}
        query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in tracking]
        path = re.sub(r"/+$", "", parts.path) or "/"
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))
    except Exception:
        return url


def stable_id(title: str, url: str) -> str:
    raw = f"{normalize_title(title)}|{canonical_url(url)}".encode("utf-8")
    return "NEWS-" + hashlib.sha256(raw).hexdigest()[:16].upper()


def contains_any(text: str, terms: list[str]) -> list[str]:
    t = f" {text.lower()} "
    return [term for term in terms if term.lower() in t]


def categorize(text: str) -> list[str]:
    out = []
    for category, terms in CATEGORY_KEYWORDS.items():
        if contains_any(text, terms):
            out.append(category)
    return out or ["general"]


def resolve_source_tier(source: str | None, default_tier: int, config: dict[str, Any]) -> int:
    domain = (source or "").lower().removeprefix("www.")
    for tier_text, domains in (config.get("source_tiers", {}) or {}).items():
        try:
            tier = int(tier_text)
        except (TypeError, ValueError):
            continue
        if any(domain == d.lower().removeprefix("www.") or domain.endswith("." + d.lower().removeprefix("www.")) for d in domains or []):
            return tier
    return default_tier


def blocked_source(source: str | None, config: dict[str, Any]) -> bool:
    domain = (source or "").lower().removeprefix("www.")
    return any(domain == d.lower().removeprefix("www.") or domain.endswith("." + d.lower().removeprefix("www.")) for d in config.get("blocked_domains", []) or [])


def score_item(title: str, summary: str, source_tier: int, published_at: datetime | None) -> tuple[int, dict[str, Any]]:
    text = f"{title} {summary}"
    china = contains_any(text, CHINA_TERMS)
    transmission = contains_any(text, TRANSMISSION_TERMS)
    impact = contains_any(text, HIGH_IMPACT_TERMS)
    categories = categorize(text)

    score = 8
    score += max(0, 5 - source_tier) * 6
    score += min(30, len(china) * 10)
    score += min(20, len(transmission) * 5)
    score += min(15, len(impact) * 5)
    score += min(10, max(0, len(categories) - 1) * 3)

    freshness = 0
    if published_at:
        hours = max(0.0, (now_utc() - published_at).total_seconds() / 3600)
        if hours <= 2:
            freshness = 10
        elif hours <= 8:
            freshness = 7
        elif hours <= 24:
            freshness = 4
    score += freshness
    return min(100, score), {
        "china_terms": sorted(set(china))[:12],
        "transmission_terms": sorted(set(transmission))[:12],
        "impact_terms": sorted(set(impact))[:12],
        "categories": categories,
        "freshness_points": freshness,
    }


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)
        except ValueError:
            pass
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(value)
        return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)
    except Exception:
        return None


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"seen": {}, "updated_at": None}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(state.get("seen"), dict):
            raise ValueError("state.seen must be an object")
        return state
    except Exception as exc:
        print(f"[warn] invalid state reset: {exc}", file=sys.stderr)
        return {"seen": {}, "updated_at": None}


def prune_state(state: dict[str, Any], days: int = 14, max_items: int = 12000) -> None:
    cutoff = now_utc() - timedelta(days=days)
    kept = {}
    for k, v in state.get("seen", {}).items():
        dt = parse_dt(v)
        if dt and dt >= cutoff:
            kept[k] = v
    if len(kept) > max_items:
        kept = dict(sorted(kept.items(), key=lambda kv: kv[1], reverse=True)[:max_items])
    state["seen"] = kept


def fetch_gdelt(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    health: list[dict[str, Any]] = []
    gdelt = config.get("gdelt", {})
    if not gdelt.get("enabled", True):
        return items, health
    endpoint = gdelt.get("endpoint", "https://api.gdeltproject.org/api/v2/doc/doc")
    timespan = gdelt.get("timespan", "2h")
    maxrecords = int(gdelt.get("maxrecords", 75))
    timeout = int(config.get("http", {}).get("timeout_seconds", 20))
    for spec in gdelt.get("queries", []):
        query = spec["query"] if isinstance(spec, dict) else str(spec)
        label = spec.get("label", "gdelt") if isinstance(spec, dict) else "gdelt"
        params = {"query": query, "mode": "ArtList", "maxrecords": maxrecords, "format": "json", "sort": "HybridRel", "timespan": timespan}
        try:
            r = requests.get(endpoint, params=params, timeout=timeout, headers={"User-Agent": UA})
            r.raise_for_status()
            payload = r.json()
            articles = payload.get("articles", []) or []
            health.append({"source": f"gdelt:{label}", "status": "ok", "items": len(articles)})
            for a in articles:
                items.append({
                    "title": clean_text(a.get("title")),
                    "url": a.get("url", ""),
                    "published_at": parse_dt(a.get("seendate")),
                    "source": a.get("domain") or "GDELT",
                    "source_country": a.get("sourcecountry"),
                    "language": a.get("language"),
                    "summary": "",
                    "source_type": "gdelt",
                    "source_tier": int(spec.get("tier", 3)) if isinstance(spec, dict) else 3,
                    "discovery_query": label,
                })
        except Exception as exc:
            msg = clean_text(str(exc))[:300]
            health.append({"source": f"gdelt:{label}", "status": "error", "items": 0, "error": msg})
            print(f"[warn] GDELT query failed ({label}): {exc}", file=sys.stderr)
    return items, health


def fetch_rss(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    health: list[dict[str, Any]] = []
    timeout = int(config.get("http", {}).get("timeout_seconds", 20))
    for src in config.get("rss", []):
        if not src.get("enabled", True):
            continue
        name = src.get("name") or src.get("url", "rss")
        try:
            r = requests.get(src["url"], timeout=timeout, headers={"User-Agent": UA})
            r.raise_for_status()
            feed = feedparser.parse(r.content)
            entries = list(feed.entries)
            health.append({"source": f"rss:{name}", "status": "ok", "items": len(entries)})
            for e in entries:
                published = parse_dt(e.get("published") or e.get("updated"))
                items.append({
                    "title": clean_text(e.get("title")),
                    "url": e.get("link", ""),
                    "published_at": published,
                    "source": src.get("name") or clean_text(feed.feed.get("title")) or "RSS",
                    "source_country": src.get("country"),
                    "language": src.get("language"),
                    "summary": clean_text(e.get("summary") or e.get("description"))[:500],
                    "source_type": "rss",
                    "source_tier": int(src.get("tier", 2)),
                    "discovery_query": src.get("name", "rss"),
                })
        except Exception as exc:
            msg = clean_text(str(exc))[:300]
            health.append({"source": f"rss:{name}", "status": "error", "items": 0, "error": msg})
            print(f"[warn] RSS failed ({name}): {exc}", file=sys.stderr)
    return items, health


def is_fuzzy_duplicate(title_norm: str, accepted_titles: list[str], threshold: float) -> bool:
    if not title_norm:
        return True
    for old in accepted_titles[-500:]:
        if abs(len(old) - len(title_norm)) > max(30, int(0.4 * max(len(old), len(title_norm)))):
            continue
        if SequenceMatcher(None, old, title_norm).ratio() >= threshold:
            return True
    return False


def process(items: list[dict[str, Any]], state: dict[str, Any], config: dict[str, Any]) -> tuple[list[Candidate], int]:
    min_score = int(config.get("scoring", {}).get("candidate_threshold", 45))
    fuzzy = float(config.get("dedup", {}).get("title_similarity", 0.92))
    accepted_titles: list[str] = []
    candidates: list[Candidate] = []
    new_seen = 0

    for item in items:
        title = item.get("title", "")
        url = canonical_url(item.get("url", ""))
        if not title or not url:
            continue
        if blocked_source(item.get("source"), config):
            continue
        item["source_tier"] = resolve_source_tier(item.get("source"), int(item.get("source_tier", 3)), config)
        news_id = stable_id(title, url)
        title_norm = normalize_title(title)
        if news_id in state["seen"] or is_fuzzy_duplicate(title_norm, accepted_titles, fuzzy):
            continue

        collected = now_utc()
        state["seen"][news_id] = iso(collected)
        new_seen += 1
        accepted_titles.append(title_norm)

        score, explain = score_item(title, item.get("summary", ""), int(item.get("source_tier", 3)), item.get("published_at"))
        if score < min_score:
            continue

        record = {
            "news_id": news_id,
            "title": title,
            "url": url,
            "source": item.get("source"),
            "source_type": item.get("source_type"),
            "source_tier": item.get("source_tier"),
            "source_country": item.get("source_country"),
            "language": item.get("language"),
            "published_at": iso(item["published_at"]) if item.get("published_at") else None,
            "collected_at": iso(collected),
            "discovery_query": item.get("discovery_query"),
            "summary": item.get("summary", "")[:500],
            "relevance_score": score,
            "categories": explain["categories"],
            "signals": {
                "china_terms": explain["china_terms"],
                "transmission_terms": explain["transmission_terms"],
                "impact_terms": explain["impact_terms"],
            },
            "research_status": "unverified_candidate",
        }
        candidates.append(Candidate(record))

    candidates.sort(key=lambda c: (c.data["relevance_score"], c.data.get("published_at") or ""), reverse=True)
    return candidates, new_seen


def append_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_latest(path: Path, candidates: list[Candidate], scanned: int, new_seen: int, source_health: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok_sources = sum(1 for s in source_health if s.get("status") == "ok")
    failed_sources = sum(1 for s in source_health if s.get("status") == "error")
    lines = [
        "# News Monitor — Latest Run", "",
        f"- Collected at: `{iso(now_utc())}`",
        f"- Source checks: **{ok_sources} ok / {failed_sources} failed**",
        f"- Items fetched: **{scanned}**",
        f"- Newly seen: **{new_seen}**",
        f"- Research candidates: **{len(candidates)}**", "",
        "> Machine-ranked discovery queue only. Candidates are not investment conclusions; verify primary sources before research use.", "",
        "## Top candidates", "",
    ]
    if not candidates:
        lines.append("_No candidate crossed the configured threshold in this run._")
    else:
        for c in candidates[:30]:
            d = c.data
            cats = ", ".join(d["categories"])
            lines += [
                f"### {d['relevance_score']} — {d['title']}",
                f"- Source: {d['source']} (tier {d['source_tier']})",
                f"- Published: {d.get('published_at') or 'unknown'}",
                f"- Categories: {cats}",
                f"- URL: {d['url']}",
                f"- ID: `{d['news_id']}`", "",
            ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_health(path: Path, *, fetched: int, candidates: int, new_seen: int, source_health: list[dict[str, Any]]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok_sources = [s for s in source_health if s.get("status") == "ok"]
    failed_sources = [s for s in source_health if s.get("status") == "error"]
    status = "ok" if ok_sources and fetched > 0 else "degraded"
    health = {
        "status": status,
        "checked_at": iso(now_utc()),
        "items_fetched": fetched,
        "newly_seen": new_seen,
        "candidates": candidates,
        "sources_ok": len(ok_sources),
        "sources_failed": len(failed_sources),
        "sources": source_health,
    }
    path.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return health


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="monitor/config.yaml")
    parser.add_argument("--state", default="data/news/state.json")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    state_path = Path(args.state)
    state = load_state(state_path)
    prune_state(
        state,
        days=int(config.get("dedup", {}).get("state_days", 14)),
        max_items=int(config.get("dedup", {}).get("max_seen_items", 12000)),
    )

    gdelt_items, gdelt_health = fetch_gdelt(config)
    rss_items, rss_health = fetch_rss(config)
    source_health = gdelt_health + rss_health
    items = gdelt_items + rss_items
    candidates, new_seen = process(items, state, config)
    day = now_utc().strftime("%Y-%m-%d")

    append_jsonl(Path(f"data/news/candidates/{day}.jsonl"), [c.data for c in candidates])
    write_latest(Path("data/news/latest.md"), candidates, len(items), new_seen, source_health)

    state["updated_at"] = iso(now_utc())
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    health = write_health(
        Path("data/news/health.json"),
        fetched=len(items),
        candidates=len(candidates),
        new_seen=new_seen,
        source_health=source_health,
    )

    print(
        f"status={health['status']} fetched={len(items)} new_seen={new_seen} "
        f"candidates={len(candidates)} sources_ok={health['sources_ok']} sources_failed={health['sources_failed']}"
    )
    return 0 if health["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
