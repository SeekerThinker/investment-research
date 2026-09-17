#!/usr/bin/env python3
"""Structural checks for the evolving philosophy library; not investment verification."""
from __future__ import annotations

import re
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
        require(resolved == ROOT or ROOT in resolved.parents, f"link escapes repository: {path}: {target}")
        require(resolved.is_file() or resolved.is_dir(), f"broken relative link: {path.relative_to(ROOT)} -> {target}")
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
    integration = (ROOT / "metadata" / "philosophy-integration.md").read_text(encoding="utf-8")
    changelog = (LIBRARY / "change-log.md").read_text(encoding="utf-8")
    mapping = (LIBRARY / "integration-map.md").read_text(encoding="utf-8")
    policy = (ROOT / "metadata" / "news-investment-impact-policy.md").read_text(encoding="utf-8")
    for i in range(1, 11):
        require(re.search(rf"\bP{i:02d}\b", beliefs) is not None, f"P{i:02d} missing from beliefs")
    for i in range(1, 12):
        require(f"IDEA-20260917-{i:02d}" in ideas, f"IDEA {i} missing from register")
    require("idea-20260917-11.md" in ideas, "IDEA-11 audit record not linked")
    require("philosophy/README.md" in readme, "root README does not introduce philosophy")
    require("待逐字审核" in ideas or "尚未逐字" in beliefs, "owner/editor provenance is unclear")
    require("v0.1" in changelog and "v0.3" in changelog and "v0.3" in integration,
            "current philosophy version and baseline missing")
    require("投资机遇" in policy and "风险规避" in policy and "预期差" in policy,
            "impact policy has not adopted two-focus evidence checks")
    for marker in ("日报", "周报", "月报", "网站", "估值", "无需修改"):
        require(marker in mapping or (marker == "无需修改" and "无须修改" in mapping),
                f"dependency map missing layer: {marker}")
    files = [LIBRARY / f for f in LIBRARY_FILES] + [ROOT / "metadata" / "philosophy-integration.md"]
    nlinks = sum(check_relative_links(path) for path in files)
    require(nlinks >= 15, f"unexpectedly few cross-document links ({nlinks})")
    print(f"PASS philosophy integrity: {len(files)} docs, 10 core beliefs, 11 ideas, {nlinks} local links")
    print("NOTE: structural tests cannot validate investment theses, expectation gaps or automation semantics")


if __name__ == "__main__":
    main()
