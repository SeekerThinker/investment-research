#!/usr/bin/env python3
"""Structural checks for the expanding philosophy library, not investment verification."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "philosophy"
LIBRARY_FILES = (
    "README.md", "core-beliefs.md", "research-constitution.md",
    "intake-and-propagation.md", "ideas.md", "idea-20260917-11.md",
    "integration-map.md", "change-log.md",
)
METHODS = (
    "research-os.md", "daily-coverage-policy.md", "news-investment-impact-policy.md",
    "long-horizon-value-policy.md", "market-behavior.md", "source-policy.md",
    "continuity-policy.md", "philosophy-integration.md",
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
PRINCIPLE = re.compile(r"^\*\*P(\d{2})｜", re.M)
IDEA_ROW = re.compile(r"^\|\s*(IDEA-(\d{8})-(\d{2}))\s*\|", re.M)
VERSION = re.compile(r"^# 投资基础思想 · (v\d+\.\d+)", re.M)


def require(condition: bool, explanation: str) -> None:
    if not condition:
        raise AssertionError(explanation)


def check_relative_links(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    checked = 0
    for match in LINK.finditer(text):
        target = match.group(1).strip().split("#", 1)[0].split("?", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        require(resolved == ROOT or ROOT in resolved.parents,
                f"link escapes repository: {path}: {target}")
        require(resolved.is_file() or resolved.is_dir(),
                f"broken relative link: {path.relative_to(ROOT)} -> {target}")
        checked += 1
    return checked


def main() -> None:
    for filename in LIBRARY_FILES:
        require((LIBRARY / filename).is_file(), f"missing philosophy/{filename}")
    for filename in METHODS:
        require((ROOT / "metadata" / filename).is_file(), f"missing metadata/{filename}")
    beliefs = (LIBRARY / "core-beliefs.md").read_text(encoding="utf-8")
    ideas = (LIBRARY / "ideas.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    library_readme = (LIBRARY / "README.md").read_text(encoding="utf-8")
    integration = (ROOT / "metadata" / "philosophy-integration.md").read_text(encoding="utf-8")
    changelog = (LIBRARY / "change-log.md").read_text(encoding="utf-8")
    mapping = (LIBRARY / "integration-map.md").read_text(encoding="utf-8")
    policy = (ROOT / "metadata" / "news-investment-impact-policy.md").read_text(encoding="utf-8")

    principles = [int(x) for x in PRINCIPLE.findall(beliefs)]
    require(len(principles) >= 10, "P01–P10 must remain present")
    require(principles == list(range(1, len(principles) + 1)),
            f"principle IDs must be continuous, unique and ordered: {principles}")
    match = VERSION.search(beliefs)
    require(match is not None, "missing philosophy version header")
    version = match.group(1)
    for name, text in (("philosophy/README.md", library_readme),
                       ("metadata/philosophy-integration.md", integration),
                       ("philosophy/integration-map.md", mapping),
                       ("philosophy/change-log.md", changelog)):
        require(version in text, f"{name} does not refer to current {version}")

    # Read actual idea table rows: historical mentions are not a registration.
    idea_rows = IDEA_ROW.findall(ideas)
    idea_ids = [item[0] for item in idea_rows]
    require(len(idea_ids) >= 11, "IDEA-20260917-01 through -11 must remain")
    require(len(idea_ids) == len(set(idea_ids)), "duplicate idea IDs")
    by_day: dict[str, list[int]] = defaultdict(list)
    for _, day, ordinal in idea_rows:
        by_day[day].append(int(ordinal))
    for day, ordinals in by_day.items():
        require(ordinals == list(range(1, len(ordinals) + 1)),
                f"idea IDs for {day} have a gap or incorrect order: {ordinals}")
    require("IDEA-20260917-11" in idea_ids and "idea-20260917-11.md" in ideas,
            "IDEA-11 or original intent record missing from register")
    for name, text in (("philosophy/change-log.md", changelog),
                       ("philosophy/integration-map.md", mapping)):
        require(idea_ids[-1] in text, f"{name} has not tracked newest idea {idea_ids[-1]}")
    require("philosophy/README.md" in readme, "root README does not introduce philosophy")
    require("待逐字审核" in ideas or "尚未逐字" in beliefs,
            "owner/editor provenance is unclear")
    require("v0.1" in changelog and "v0.1" in integration,
            "baseline version missing")
    require(all(word in policy for word in ("投资机遇", "风险规避", "预期差")),
            "news impact policy lacks two-focus evidence requirements")
    for marker in ("日报", "周报", "月报", "网站", "估值", "无需修改"):
        require(marker in mapping or (marker == "无需修改" and "无须修改" in mapping),
                f"dependency map missing layer: {marker}")
    files = ([LIBRARY / f for f in LIBRARY_FILES]
             + [f for f in sorted(LIBRARY.glob("idea-*.md")) if f.name not in LIBRARY_FILES]
             + [ROOT / "metadata" / "philosophy-integration.md"])
    nlinks = sum(check_relative_links(path) for path in files)
    require(nlinks >= 15, f"unexpectedly few cross-document links ({nlinks})")
    print(f"PASS philosophy integrity {version}: {len(files)} docs, "
          f"{len(principles)} core principles, {len(idea_ids)} registered ideas, "
          f"{nlinks} local links")
    print("NOTE: structural checks cannot verify theses, expectation gaps or task semantics")


if __name__ == "__main__":
    main()
