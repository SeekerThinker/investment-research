#!/usr/bin/env python3
"""Check only handoff document links and explicit authority/status boundaries.

Not a test of investment facts, human approvals, external licensing or live deployment.
"""
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
FILES = ("START_HERE.md", "AGENTS.md", "docs/project-state.md", "docs/collaboration-review.md")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def main():
    contents = {}
    count = 0
    for relative in FILES:
        path = ROOT / relative
        assert path.is_file(), f"missing handoff document: {relative}"
        text = path.read_text(encoding="utf-8")
        contents[relative] = text
        for found in LINK.finditer(text):
            target = found.group(1).strip().split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            assert resolved == ROOT or ROOT in resolved.parents, f"link escapes repo: {relative}: {target}"
            assert resolved.is_file() or resolved.is_dir(), f"broken link: {relative}: {target}"
            count += 1
    start = contents["START_HERE.md"]
    agents = contents["AGENTS.md"]
    state = contents["docs/project-state.md"]
    review = contents["docs/collaboration-review.md"]
    assert "AGENTS.md" in start and "docs/project-state.md" in start
    assert "philosophy/README.md" in start and "metadata/publication-policy.md" in start
    assert "permissions.push=true" in agents and "AI-PROPOSED" in agents
    assert "reports/" in agents and "不可回写" in agents
    assert all(marker in state for marker in ("CURRENT OBJECTIVE", "PRIMARY BLOCKER", "PENDING HUMAN DECISIONS", "未知", "未决"))
    assert "HARC" in review and "不移植" in review and "许可" in review
    assert count >= 18, f"too few checked cross-document links: {count}"
    print(f"PASS repository handoff: {len(FILES)} documents, {count} valid local links; status/approval boundaries present")
    print("NOTE: structural checks do not certify live Cloudflare status, investment claims or human consent")


if __name__ == "__main__":
    main()
