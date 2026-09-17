#!/usr/bin/env python3
"""Attach the current immutable intraday research to the free Pages archive.

This runs only after build_public_site.py. Never generates or paraphrases research.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import build_public_site as base

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"reports/intraday/(\d{4}-\d{2}-\d{2}-\d{4})\.md")


def include(out: Path) -> None:
    index = out / "content" / "index.json"
    data = json.loads(index.read_text(encoding="utf-8"))
    latest = base.read_text(ROOT / "latest" / "daily.md")
    found = NAME.search(latest)
    if not found:
        print("no current intraday update: ordinary daily publication unchanged")
        return
    period = found.group(1)
    source = ROOT / "reports" / "intraday" / f"{period}.md"
    if not source.is_file() or source.is_symlink():
        raise ValueError(f"current intraday source missing or unsafe: {source}")
    body = base.read_text(source)
    if not body.strip() or "## 今日全市场资讯速览" not in body:
        raise ValueError("intraday report must contain its real source-grounded full text")
    target = out / "content" / "reports" / "intraday"
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target / source.name)
    published_path = f"content/reports/intraday/{source.name}"
    archive = {"type": "daily", "label": "当日增量", "period": period,
               "title": base.title_of(body, f"当日增量 {period}"),
               "path": published_path, "access": "public"}
    if any(x["type"] == "daily" and x["period"] == period for x in data["archive"]):
        raise ValueError("duplicate intraday archive period")
    data["archive"].append(archive)
    daily = next((x for x in data["latest"] if x["type"] == "daily"), None)
    if daily is None:
        raise ValueError("latest daily summary is required")
    daily["archive_period"] = period
    label = base.published_period(latest, "daily", period)
    daily["period"] = label
    summaries = base.section_items(latest, lambda h: "核心结论" in h,
                                   numbered_only=True, limit=40)
    if not summaries:
        raise ValueError("intraday homepage needs actual latest news and analysis")
    data["feed"]["daily"] = base.feed_rows(summaries, "daily", "当日增量", label,
                                            period, f"reports/intraday/{source.name}", "全市场资讯与投资影响")
    market = base.section_items(body, lambda h: "市场行为观察" in h,
                                numbered_only=True, limit=18)
    risk = base.section_items(body, lambda h: "主要风险与验证" in h,
                              numbered_only=False, limit=12)
    data["feed"]["market"] = base.feed_rows(market, "daily", "当日增量", label,
                                             period, f"reports/intraday/{source.name}", "市场行为")
    data["feed"]["risk"] = base.feed_rows(risk, "daily", "当日增量", label,
                                           period, f"reports/intraday/{source.name}", "验证与风险")
    index.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"published full intraday report {period}; homepage: {len(summaries)} news, {len(market)} market, {len(risk)} risks")


if __name__ == "__main__":
    include(ROOT / "_site")
