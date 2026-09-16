#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DEFAULT_OUT = ROOT / "_site"
REPORTS = {
    "daily": ("日报", ROOT / "latest" / "daily.md", ROOT / "reports" / "daily"),
    "weekly": ("周报", ROOT / "latest" / "weekly.md", ROOT / "reports" / "weekly"),
    "monthly": ("月报", ROOT / "latest" / "monthly.md", ROOT / "reports" / "monthly"),
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def title_of(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def latest_public(out: Path) -> list[dict]:
    dest = out / "content" / "latest"
    dest.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for kind, (label, latest_path, _) in REPORTS.items():
        md = read_text(latest_path)
        if not md:
            continue
        (dest / f"{kind}.md").write_text(md, encoding="utf-8")
        rows.append({
            "type": kind,
            "label": label,
            "title": title_of(md, f"Latest {label}"),
            "path": f"content/latest/{kind}.md",
            "access": "public",
        })
    return rows


def archive_catalog() -> list[dict]:
    rows: list[dict] = []
    for kind, (label, _, archive_dir) in REPORTS.items():
        if archive_dir.exists():
            for path in sorted(archive_dir.glob("*.md"), reverse=True):
                rows.append({"type": kind, "label": label, "period": path.stem, "access": "member"})
    return rows


def health_public() -> dict:
    market = read_json(ROOT / "data" / "market" / "health.json")
    news = read_json(ROOT / "data" / "news" / "health.json")
    return {
        "market": {k: market.get(k) for k in ("status", "operational", "checked_at", "success", "failed")},
        "news": {k: news.get(k) for k in ("status", "operational", "checked_at", "sources_ok", "sources_failed", "primary_sources_ok")},
    }


def build(out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copy2(SITE / "index.html", out / "index.html")
    shutil.copytree(SITE / "assets", out / "assets")
    latest = latest_public(out)
    archive = archive_catalog()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "site": {"name": "SeekerThinker Research", "tagline": "可审计的独立投资研究"},
        "latest": latest,
        "archive": archive,
        "health": health_public(),
        "member_catalog": {
            "daily": sum(x["type"] == "daily" for x in archive),
            "weekly": sum(x["type"] == "weekly" for x in archive),
            "monthly": sum(x["type"] == "monthly" for x in archive),
            "full_text_in_public_artifact": False,
        },
        "publication_boundary": {
            "public": ["latest daily/weekly/monthly summaries", "archive catalog", "curated health", "methodology/disclosure"],
            "member_not_embedded": ["full historical reports", "theme dossiers", "leading indicators", "model audit", "comparison tools"],
            "private_never_auto_export": ["tracking/**", "index/**", "raw news candidates/state", "private notes", "credentials", "portfolio/positions"],
        },
    }
    content = out / "content"
    content.mkdir(exist_ok=True)
    (content / "index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"built allowlisted public site: {out}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    build(Path(args.output).resolve())


if __name__ == "__main__":
    main()
