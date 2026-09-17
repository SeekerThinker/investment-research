#!/usr/bin/env python3
"""Enforce a source-backed, deliberately curated one-screen daily feed.

Run after build_public_site.py and include_intraday_site.py. The selection is made
in latest/daily.md by the researcher, not by a ranking algorithm or first-N cut.
Full immutable reports and latest summaries remain available under Reports.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import build_public_site as base

ROOT = Path(__file__).resolve().parents[1]
MAX_ITEMS = 12
MAX_FACETS = 7
FIELDS = ("影响：", "机会：", "风险：", "强度/期限：", "已定价/验证：")
FACET = re.compile(r"^【([^】]+)】")


def curate(out: Path) -> None:
    index = out / "content" / "index.json"
    data = json.loads(index.read_text(encoding="utf-8"))
    latest = base.read_text(ROOT / "latest" / "daily.md")
    selected = base.section_items(latest, lambda h: "核心结论" in h,
                                  numbered_only=True, limit=MAX_ITEMS + 1)
    if not selected or len(selected) > MAX_ITEMS:
        raise ValueError("latest/daily.md must explicitly curate 1-12 real investment themes; do not truncate")
    facets = set()
    for title, summary in selected:
        match = FACET.match(title)
        if not match:
            raise ValueError(f"curated daily title requires a 【facet】: {title}")
        facets.add(match.group(1))
        missing = [field for field in FIELDS if field not in summary]
        if missing:
            raise ValueError(f"curated brief lacks investment mapping {missing}: {title}")
    if len(facets) > MAX_FACETS:
        raise ValueError(f"daily has {len(facets)} facets; consolidate to at most seven")
    daily = next((x for x in data["latest"] if x["type"] == "daily"), None)
    if not daily:
        raise ValueError("missing published latest daily")
    period = daily.get("archive_period")
    if not period or not any(x["type"] == "daily" and x["period"] == period
                             and (out / x["path"]).is_file() for x in data["archive"]):
        raise ValueError("curated entries must link to an actually published full report")
    source = (f"reports/intraday/{period}.md" if re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{4}", period)
              else f"reports/daily/{period}.md")
    data["feed"]["daily"] = base.feed_rows(selected, "daily", daily["label"],
                                            daily["period"], period, source,
                                            "精选投资主题")
    # These detailed sections and dated weekly/monthly analyses remain accessible
    # through Reports, rather than being counted again as today's homepage news.
    for channel in ("market", "risk", "weekly", "monthly"):
        data["feed"][channel] = []
    data["editorial"] = {"selection": "researcher-curated-latest-summary", "max_daily": MAX_ITEMS,
                         "daily_count": len(selected), "facets": sorted(facets),
                         "details_in_free_reports": True}
    index.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS curated homepage: {len(selected)} real investment themes across {len(facets)} facets; full archive preserved")


if __name__ == "__main__":
    curate(ROOT / "_site")
