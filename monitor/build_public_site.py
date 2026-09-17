#!/usr/bin/env python3
"""Build the public reading site from actual, dated research; never synthesize news."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DEFAULT_OUT = ROOT / "_site"
MANIFEST = ROOT / "metadata" / "publication-manifest.json"
REPORTS = {
    "daily": ("日报", ROOT / "latest" / "daily.md", ROOT / "reports" / "daily", re.compile(r"\d{4}-\d{2}-\d{2}")),
    "weekly": ("周报", ROOT / "latest" / "weekly.md", ROOT / "reports" / "weekly", re.compile(r"\d{4}-W\d{2}")),
    "monthly": ("月报", ROOT / "latest" / "monthly.md", ROOT / "reports" / "monthly", re.compile(r"\d{4}-\d{2}")),
}


def read_text(path: Path) -> str:
    if path.is_symlink():
        raise ValueError(f"symlink not allowed in publication source: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def read_json(path: Path) -> dict:
    try:
        return json.loads(read_text(path))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def title_of(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def checked_manifest() -> dict:
    manifest = read_json(MANIFEST)
    public = manifest.get("public", {})
    if (manifest.get("version") != 2 or public.get("latest_summaries") != list(REPORTS)
            or public.get("historical_full_text") is not True or public.get("health") != "curated-only"
            or manifest.get("publication_model") != "open-reading-voluntary-support"):
        raise ValueError("publication manifest missing or not approved for open full-report reading")
    sponsor = manifest.get("sponsorship", {})
    if sponsor.get("enabled"):
        u = urlparse(sponsor.get("url") or "")
        if u.scheme != "https" or not u.hostname or u.username or u.password:
            raise ValueError("sponsorship URL must be an explicitly approved HTTPS URL")
    return manifest


def plain_markdown(value: str) -> str:
    """Remove presentation-only Markdown, without changing source claims."""
    value = re.sub(r"\[([^\]]+)\]\(https?://[^)]+\)", r"\1", value)
    value = value.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", value).strip()


def split_brief(raw: str) -> tuple[str, str]:
    strong = re.match(r"^\*\*(.+?)\*\*\s*[：:]?\s*(.*)$", raw)
    if strong:
        return plain_markdown(strong.group(1)).rstrip("：:。 "), plain_markdown(strong.group(2)).lstrip("：: ")
    clean = plain_markdown(raw)
    for mark in ("。", "：", ":"):
        if mark in clean and 5 <= clean.index(mark) <= 90:
            title, detail = clean.split(mark, 1)
            return title.strip(), detail.strip()
    return clean, ""


def section_items(markdown: str, heading_match, *, numbered_only: bool, limit: int) -> list[tuple[str, str]]:
    """Extract only actual bullets from one source section, never invent or backfill."""
    in_section = False
    result: list[tuple[str, str]] = []
    for line in markdown.splitlines():
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if heading:
            if in_section:
                break
            in_section = bool(heading_match(heading.group(1)))
            continue
        if not in_section:
            continue
        bullet = re.match(r"^\s*(\d+[.、)]|[-*])\s+(.+?)\s*$", line)
        if bullet and (not numbered_only or bullet.group(1)[0].isdigit()):
            title, summary = split_brief(bullet.group(2))
            if title:
                result.append((title, summary))
            if len(result) >= limit:
                break
    return result


def published_period(summary: str, kind: str, fallback: str | None) -> str:
    label = {"daily": "日报", "weekly": "周报", "monthly": "月报"}[kind]
    found = re.search(r"最新" + label + r"[：:]\s*\*\*([^*]+)\*\*", summary)
    return found.group(1).strip() if found else (fallback or "未注明日期")


def feed_rows(rows: list[tuple[str, str]], kind: str, label: str, period: str,
              detail_period: str | None, source: str, section: str) -> list[dict]:
    return [{"type": kind, "label": label, "period": period, "title": title,
             "summary": summary, "section": section, "source": source,
             "detail_period": detail_period} for title, summary in rows]


def build(out: Path) -> None:
    manifest = checked_manifest()
    resolved = out.resolve()
    if resolved in (ROOT.resolve(), SITE.resolve()) or (ROOT.resolve() in resolved.parents and resolved != DEFAULT_OUT.resolve()):
        raise ValueError("output must be the dedicated _site directory or a location outside repository")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copy2(SITE / "index.html", out / "index.html")
    shutil.copytree(SITE / "assets", out / "assets")
    content = out / "content"
    (content / "latest").mkdir(parents=True)
    (content / "reports").mkdir(parents=True)
    latest: list[dict] = []
    archive: list[dict] = []
    feed: dict[str, list[dict]] = {k: [] for k in ("daily", "market", "weekly", "monthly", "risk")}
    for kind, (label, latest_path, archive_dir, period_pattern) in REPORTS.items():
        for path in sorted(archive_dir.glob("*.md"), reverse=True) if archive_dir.is_dir() else []:
            if not period_pattern.fullmatch(path.stem):
                continue
            body = read_text(path)
            dest = content / "reports" / kind
            dest.mkdir(exist_ok=True)
            (dest / path.name).write_text(body, encoding="utf-8")
            archive.append({"type": kind, "label": label, "period": path.stem,
                            "title": title_of(body, f"{label} {path.stem}"),
                            "path": f"content/reports/{kind}/{path.name}", "access": "public"})
        summary = read_text(latest_path)
        if not summary:
            continue
        (content / "latest" / f"{kind}.md").write_text(summary, encoding="utf-8")
        match = re.search(r"reports/" + kind + r"/([A-Za-z0-9-]+)\.md", summary)
        period = match.group(1) if match and period_pattern.fullmatch(match.group(1)) else None
        if period and not any(x["type"] == kind and x["period"] == period for x in archive):
            period = None
        report_date = published_period(summary, kind, period)
        latest.append({"type": kind, "label": label, "title": title_of(summary, f"Latest {label}"),
                       "path": f"content/latest/{kind}.md", "archive_period": period,
                       "period": report_date, "access": "public"})
        summary_points = section_items(summary, lambda heading: "核心结论" in heading,
                                       numbered_only=True, limit=40 if kind == "daily" else 12)
        if kind == "daily" and period:
            body = read_text(archive_dir / f"{period}.md")
            # New daily reports publish their independent whole-market panorama;
            # old reports retain their actual, smaller summary rather than fictional padding.
            panorama = section_items(body, lambda heading: "全市场资讯速览" in heading,
                                     numbered_only=True, limit=40)
            if panorama:
                feed["daily"] = feed_rows(panorama, kind, label, report_date, period,
                                          f"reports/daily/{period}.md", "全市场资讯速览")
            else:
                feed["daily"] = feed_rows(summary_points, kind, label, report_date, period,
                                          f"latest/{kind}.md", "核心结论")
            market = section_items(body, lambda heading: "市场行为观察" in heading or "市场行为变化" in heading,
                                   numbered_only=True, limit=18)
            risks = section_items(body, lambda heading: "主要风险与验证" in heading or "误导性叙事" in heading
                                  or "伪催化" in heading or "价格领先风险" in heading,
                                  numbered_only=False, limit=12)
            feed["market"] = feed_rows(market, kind, label, report_date, period,
                                       f"reports/daily/{period}.md", "市场行为")
            feed["risk"] = feed_rows(risks, kind, label, report_date, period,
                                     f"reports/daily/{period}.md", "验证与风险")
        elif kind == "daily":
            feed["daily"] = feed_rows(summary_points, kind, label, report_date, period,
                                      f"latest/{kind}.md", "核心结论")
        else:
            feed[kind] = feed_rows(summary_points, kind, label, report_date, period,
                                   f"latest/{kind}.md", "核心结论")
    market_health = read_json(ROOT / "data" / "market" / "health.json")
    news_health = read_json(ROOT / "data" / "news" / "health.json")
    sponsor = manifest.get("sponsorship", {})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "site": {"name": "SeekerThinker Research", "tagline": "免费开放的可审计独立研究"},
        "latest": latest, "archive": archive, "feed": feed,
        "health": {
            "market": {k: market_health.get(k) for k in ("status", "operational", "checked_at", "success", "failed")},
            "news": {k: news_health.get(k) for k in ("status", "operational", "checked_at", "sources_ok", "sources_failed", "primary_sources_ok")},
        },
        "sponsorship": {"enabled": sponsor.get("enabled") is True,
                        "url": sponsor.get("url") if sponsor.get("enabled") is True else None,
                        "no_access_benefit": True},
        "publication_boundary": {
            "website_includes": ["latest summaries", "homepage source-grounded briefs", "all historical report markdown", "curated health", "methodology/disclosure"],
            "not_copied_into_site": ["tracking/**", "index/**", "raw news candidates/state", "credentials/tokens"],
            "repository_visibility": "public",
        },
    }
    (content / "index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"built open-reading site: {out}; reports: {len(archive)}; visible briefs: {sum(map(len, feed.values()))}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    build(Path(args.output).resolve())


if __name__ == "__main__":
    main()
