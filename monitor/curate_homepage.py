#!/usr/bin/env python3
"""Curate the latest DAILY into two explicit focus groups; preserve weekly/monthly.

No model-generated classifications or claims: the researcher marks each latest
summary title as 【投资机遇·面向】 or 【风险规避·面向】. This program validates and
copies those existing statements, with the immutable full report linked intact.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import build_public_site as base

ROOT = Path(__file__).resolve().parents[1]
MAX_ITEMS = 12
MAX_FACETS = 7
FOCUS = re.compile(r"^【(投资机遇|风险规避)·([^】]+)】")
COMMON = ("事实：", "传导：", "潜在预期差：", "强度/期限：", "验证：")
SPECIAL = {"投资机遇": "成立条件：", "风险规避": "风险触发："}


def curated_items(latest: str) -> tuple[list[tuple[str, str, str]], set[str]]:
    selected = base.section_items(latest, lambda h: "核心结论" in h,
                                  numbered_only=True, limit=MAX_ITEMS + 1)
    if not selected or len(selected) > MAX_ITEMS:
        raise ValueError("latest daily must explicitly curate 1-12 genuine themes; do not truncate")
    found: list[tuple[str, str, str]] = []
    facets: set[str] = set()
    for title, summary in selected:
        marker = FOCUS.match(title)
        if not marker:
            raise ValueError(f"daily title needs explicit opportunity/risk and facet: {title}")
        group, facet = marker.groups()
        if not facet.strip():
            raise ValueError(f"empty research facet: {title}")
        missing = [part for part in (*COMMON, SPECIAL[group]) if part not in summary]
        if missing:
            raise ValueError(f"focus item lacks its own investment analysis {missing}: {title}")
        # No redundant symmetrical checklist on each card; the opposing
        # scenario remains available in the original linked full report.
        other = "风险触发：" if group == "投资机遇" else "成立条件："
        if other in summary:
            raise ValueError(f"focus item contains both focus-specific fields: {title}")
        facets.add(facet)
        found.append((group, title, summary))
    if len(facets) > MAX_FACETS:
        raise ValueError(f"daily has {len(facets)} facets; consolidate to seven or fewer")
    return found, facets


def curate(out: Path) -> None:
    index = out / "content" / "index.json"
    data = json.loads(index.read_text(encoding="utf-8"))
    latest = base.read_text(ROOT / "latest" / "daily.md")
    selected, facets = curated_items(latest)
    daily = next((x for x in data["latest"] if x["type"] == "daily"), None)
    if not daily:
        raise ValueError("missing published latest daily")
    period = daily.get("archive_period")
    if not period or not any(x["type"] == "daily" and x["period"] == period
                             and (out / x["path"]).is_file() for x in data["archive"]):
        raise ValueError("focus entries must link to an actually published complete report")
    source = (f"reports/intraday/{period}.md" if re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{4}", period)
              else f"reports/daily/{period}.md")
    rows = []
    for group, title, summary in selected:
        item = base.feed_rows([(title, summary)], "daily", daily["label"],
                              daily["period"], period, source, "精选投资主题")[0]
        item["focus"] = "opportunity" if group == "投资机遇" else "risk"
        rows.append(item)
    data["feed"]["daily"] = rows
    # These remain inside the detailed daily report; not a second homepage feed.
    data["feed"]["market"] = []
    data["feed"]["risk"] = []
    for kind in ("weekly", "monthly"):
        existing = next((x for x in data["latest"] if x["type"] == kind), None)
        if existing and not data["feed"].get(kind):
            raise ValueError(f"{kind} report exists but its independent homepage section vanished")
    counts = {"opportunity": sum(x["focus"] == "opportunity" for x in rows),
              "risk": sum(x["focus"] == "risk" for x in rows)}
    data["editorial"] = {"selection": "researcher-marked-two-focus-latest-summary",
                         "max_daily": MAX_ITEMS, "daily_count": len(rows),
                         "focus_counts": counts, "facets": sorted(facets),
                         "weekly_monthly_independent": True,
                         "expectation_gap_verified": False,
                         "details_in_free_reports": True}
    index.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS two-focus daily: {counts}, {len(facets)} facets; weekly {len(data['feed']['weekly'])}, monthly {len(data['feed']['monthly'])}; full archive preserved")


if __name__ == "__main__":
    curate(ROOT / "_site")
