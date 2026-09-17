#!/usr/bin/env python3
"""Stdlib-only regression checks for dated, non-invented homepage brief extraction."""
import unittest

import build_public_site as site


class MarketWideFeedTests(unittest.TestCase):
    def test_extracts_all_twenty_five_real_source_bullets(self):
        raw = "# 日报\n\n## 今日全市场资讯速览\n" + "\n".join(
            f"{i}. **【栏目】示例标题{i}。** 可核验的模拟测试摘要{i}；仅用于测试。"
            for i in range(1, 26)
        ) + "\n\n## 今日市场行为观察\n1. **另一条。** 这是下一个栏目。\n"
        rows = site.section_items(raw, lambda h: "全市场资讯速览" in h,
                                  numbered_only=True, limit=40)
        self.assertEqual(len(rows), 25)
        self.assertEqual(rows[0][0], "【栏目】示例标题1")
        self.assertIn("模拟测试摘要25", rows[-1][1])
        self.assertFalse(any("另一条" in title for title, _ in rows))

    def test_preserves_investment_implications_in_homepage_summary(self):
        # Hypothetical fixture only: the builder must *copy* a source's analysis,
        # never infer its own winners, direction, magnitude or target price.
        raw = (
            "## 今日全市场资讯速览\n"
            "1. **【假设行业】模拟事件。** 事实：纯测试（S；2026-01-01）。"
            "｜影响：上下游可能双向分化，真实暴露待核实（I）。"
            "｜机会：只有订单兑现时才可进一步研究。"
            "｜风险：需求疲弱可能抵消收益。"
            "｜强度/期限：短期待量化，长期现金流未判定。"
            "｜已定价/验证：未判定；核查公告和现金流。\n"
        )
        rows = site.section_items(raw, lambda h: "全市场资讯速览" in h,
                                  numbered_only=True, limit=40)
        self.assertEqual(len(rows), 1)
        title, summary = rows[0]
        self.assertEqual(title, "【假设行业】模拟事件")
        for field in ("事实：", "影响：", "机会：", "风险：", "强度/期限：", "已定价/验证："):
            self.assertIn(field, summary, field)
        self.assertIn("真实暴露待核实", summary)
        self.assertIn("长期现金流未判定", summary)

    def test_separate_market_and_risk_columns_and_legacy_report(self):
        raw = ("## 今日最重要的3个市场行为变化\n"
               "1. **示例量价。** 来源截至上一真实交易日。\n"
               "\n## 误导性叙事 / 风险\n"
               "- 历史报道不能充当今日新增。\n")
        market = site.section_items(raw, lambda h: "市场行为观察" in h or "市场行为变化" in h,
                                    numbered_only=True, limit=18)
        risk = site.section_items(raw, lambda h: "主要风险与验证" in h or "误导性叙事" in h,
                                  numbered_only=False, limit=12)
        self.assertEqual(len(market), 1)
        self.assertEqual(len(risk), 1)

    def test_empty_day_is_not_filled_from_other_sections(self):
        raw = "## 昨日报告归档\n1. **旧闻。** 不应出现在今日。\n"
        self.assertEqual(site.section_items(raw, lambda h: "全市场资讯速览" in h,
                                            numbered_only=True, limit=40), [])


if __name__ == "__main__":
    unittest.main()
