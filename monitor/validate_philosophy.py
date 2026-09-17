#!/usr/bin/env python3
"""Dependency sanity checks for the evolving philosophy library; stdlib only.

This checks structural integrity, not the truth of any investment thesis or whether
an assistant semantically propagated every newly discussed idea.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "philosophy"
LIBRARY_FILES = (
    "README.md", "core-beliefs.md", "research-constitution.md",
    "intake-and-propagation.md", "ideas.md", "integration-map.md", "change-log.md",
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
    for i in range(1, 9):
        require(re.search(rf"\bP{i:02d}\b", beliefs) is not None, f"P{i:02d} missing from beliefs")
    for i in range(1, 8):
        require(f"IDEA-20260917-{i:02d}" in ideas, f"initial IDEA {i} missing")
    require("philosophy/README.md" in readme, "root README does not introduce philosophy")
    require("待逐字审核" in ideas or "尚未逐字" in beliefs, "owner/editor provenance is unclear")
    require("v0.1" in changelog and "v0.1" in integration, "version baseline missing")
    for marker in ("日报", "周报", "月报", "网站", "估值", "无须修改"):
        # Wording varies between '无须' and '无需'; accept either for the latter.
        if marker == "无须修改":
            require("无需修改" in mapping or "无须修改" in mapping, "missing no-change audit")
        else:
            require(marker in mapping, f"dependency map missing layer: {marker}")
    files = [LIBRARY / f for f in LIBRARY_FILES] + [ROOT / "metadata" / "philosophy-integration.md"]
    nlinks = sum(check_relative_links(path) for path in files)
    require(nlinks >= 15, f"unexpectedly few cross-document links ({nlinks})")
    print(f"PASS philosophy integrity: {len(files)} docs, 8 core beliefs, 7 owner-related ideas, {nlinks} local links")
    print("NOTE: manual semantic review and automation receipts remain required for each philosophy change")


if __name__ == "__main__":
    main()
