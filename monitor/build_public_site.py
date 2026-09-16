#!/usr/bin/env python3
"""Build only the approved, freely readable research website artifact."""
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


def build(out: Path) -> None:
    manifest = checked_manifest()
    if out.resolve() in (ROOT.resolve(), SITE.resolve()) or ROOT.resolve() in out.resolve().parents and out.resolve() not in (DEFAULT_OUT.resolve(),):
        raise ValueError("output must be the dedicated _site directory or a location outside repository")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copy2(SITE / "index.html", out / "index.html")
    shutil.copytree(SITE / "assets", out / "assets")
    content = out / "content"
    (content / "latest").mkdir(parents=True)
    (content / "reports").mkdir(parents=True)
    latest, archive = [], []
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
        latest.append({"type": kind, "label": label, "title": title_of(summary, f"Latest {label}"),
                       "path": f"content/latest/{kind}.md", "archive_period": period, "access": "public"})
    market = read_json(ROOT / "data" / "market" / "health.json")
    news = read_json(ROOT / "data" / "news" / "health.json")
    sponsor = manifest.get("sponsorship", {})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "site": {"name": "SeekerThinker Research", "tagline": "免费开放的可审计独立研究"},
        "latest": latest, "archive": archive,
        "health": {
            "market": {k: market.get(k) for k in ("status", "operational", "checked_at", "success", "failed")},
            "news": {k: news.get(k) for k in ("status", "operational", "checked_at", "sources_ok", "sources_failed", "primary_sources_ok")},
        },
        "sponsorship": {"enabled": sponsor.get("enabled") is True,
                        "url": sponsor.get("url") if sponsor.get("enabled") is True else None,
                        "no_access_benefit": True},
        "publication_boundary": {
            "website_includes": ["latest summaries", "all historical report markdown", "curated health", "methodology/disclosure"],
            "not_copied_into_site": ["tracking/**", "index/**", "raw news candidates/state", "credentials/tokens"],
            "repository_visibility": "public",
        },
    }
    (content / "index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"built open-reading site: {out}; historical reports: {len(archive)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    build(Path(args.output).resolve())


if __name__ == "__main__":
    main()
