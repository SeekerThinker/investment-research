#!/usr/bin/env python3
"""Offline regression: daily focus categories come from editor, not inferred news."""
import unittest
from pathlib import Path

import curate_homepage as focus

HERE = Path(__file__).resolve().parents[1]


def entry(group: str, n: int, *, omit: str = "") -> str:
    field = "成立条件：以实际回款确认。" if group == "投资机遇" else "风险触发：现金流无法覆盖到期债务。"
    fields = ["事实：假设事件与日期（S）。", "传导：假设盈利或债务发生变化（I）。",
              "潜在预期差：现价和市场预期未核验。", field,
              "强度/期限：待量化。", "验证：查公司公告。"]
    fields = [f for f in fields if not f.startswith(omit)]
    return f"{n}. **【{group}·测试面向】纯假设{n}。** " + "｜".join(fields)


class TwoFocusTests(unittest.TestCase):
    def test_two_explicit_groups_have_distinct_required_fields(self):
        raw = "## 今日核心结论\n" + entry("投资机遇", 1) + "\n" + entry("风险规避", 2) + "\n"
        found, facets = focus.curated_items(raw)
        self.assertEqual([x[0] for x in found], ["投资机遇", "风险规避"])
        self.assertEqual(facets, {"测试面向"})
        self.assertNotIn("风险触发：", found[0][2])
        self.assertNotIn("成立条件：", found[1][2])

    def test_rejects_missing_focus_or_verification(self):
        with self.assertRaisesRegex(ValueError, "explicit"):
            focus.curated_items("## 今日核心结论\n1. **【测试面向】无归类。** 事实：假设。\n")
        with self.assertRaisesRegex(ValueError, "lacks"):
            focus.curated_items("## 今日核心结论\n" + entry("投资机遇", 1, omit="验证：") + "\n")

    def test_rejects_both_primary_focus_fields(self):
        raw = "## 今日核心结论\n" + entry("投资机遇", 1) + "｜风险触发：不应机械重复。\n"
        with self.assertRaisesRegex(ValueError, "both focus-specific"):
            focus.curated_items(raw)

    def test_rejects_thirteen_rather_than_silently_truncating(self):
        raw = "## 今日核心结论\n" + "\n".join(entry("投资机遇", i) for i in range(1, 14))
        with self.assertRaisesRegex(ValueError, "1-12"):
            focus.curated_items(raw)

    def test_actual_latest_is_explicitly_curated_and_archive_untouched(self):
        raw = (HERE / "latest" / "daily.md").read_text(encoding="utf-8")
        found, facets = focus.curated_items(raw)
        self.assertLessEqual(len(found), 12)
        self.assertLessEqual(len(facets), 7)
        self.assertTrue(all(x[0] in ("投资机遇", "风险规避") for x in found))
        self.assertIn("reports/intraday/2026-09-17-0953.md", raw)
        self.assertTrue((HERE / "reports" / "intraday" / "2026-09-17-0953.md").is_file())


if __name__ == "__main__":
    unittest.main()
