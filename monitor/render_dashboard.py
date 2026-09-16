#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str, fallback: str = "_暂无数据。_") -> str:
    p = ROOT / path
    if not p.exists():
        return fallback
    text = p.read_text(encoding="utf-8").strip()
    return text or fallback


def section_body(path: str) -> str:
    text = read(path)
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    return "\n".join(lines).strip() or "_暂无数据。_"


def markdown_rows(path: str):
    text = read(path, "")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [x.strip() for x in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [x.strip() for x in line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def news_health_summary() -> str:
    p = ROOT / "data/news/health.json"
    if not p.exists():
        return "| 新闻层 | 状态 |\n|---|---|\n| 新闻监控 | 尚无健康数据 |"
    try:
        h = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"| 新闻层 | 状态 |\n|---|---|\n| 新闻监控 | health.json 解析失败：{exc} |"

    status = h.get("status", "unknown")
    operational = h.get("operational", status == "ok")
    ok = h.get("sources_ok", 0)
    failed = h.get("sources_failed", 0)
    primary = h.get("primary_sources_ok", 0)
    fetched = h.get("items_fetched", 0)
    candidates = h.get("candidates", 0)
    checked = h.get("checked_at", "unknown")
    rows = [
        "| 新闻层 | 状态 |",
        "|---|---|",
        f"| 运行状态 | **{status}** / operational={operational} |",
        f"| 最近检查 | `{checked}` |",
        f"| 来源健康 | {ok} 正常 / {failed} 失败 / Tier-1正常 {primary} |",
        f"| 最近抓取 | {fetched} 条输入 / {candidates} 条研究候选 |",
    ]
    if failed:
        failed_names = [s.get("source", "unknown") for s in h.get("sources", []) if s.get("status") != "ok"]
        rows.append(f"| 降级来源 | {', '.join(failed_names[:8])} |")
    return "\n".join(rows)


def market_health_summary() -> str:
    p = ROOT / "data/market/health.json"
    if not p.exists():
        return "| 市场行为层 | 状态 |\n|---|---|\n| 量价采集 | 尚无机器快照；等待首次运行 |"
    try:
        h = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"| 市场行为层 | 状态 |\n|---|---|\n| 量价采集 | health.json 解析失败：{exc} |"
    return "\n".join([
        "| 市场行为层 | 状态 |",
        "|---|---|",
        f"| 运行状态 | **{h.get('status', 'unknown')}** / operational={h.get('operational', False)} |",
        f"| 最近检查 | `{h.get('checked_at', 'unknown')}` |",
        f"| 证券腿 | {h.get('success', 0)} 正常 / {h.get('failed', 0)} 失败 |",
        f"| 数据源 | {h.get('source', 'unknown')} |",
    ])


def research_summary() -> str:
    themes = markdown_rows("index/themes.md")
    hypotheses = markdown_rows("tracking/hypotheses.md")
    indicators = markdown_rows("tracking/leading-indicators.md")
    behaviors = markdown_rows("tracking/market-behavior.md")
    audits = markdown_rows("tracking/model-audit.md")
    securities = markdown_rows("index/securities.md")

    active_themes = sum(1 for r in themes if r.get("research_stage") == "活跃研究")
    pending_themes = sum(1 for r in themes if r.get("research_stage") == "待验证")
    active_hyp = sum(1 for r in hypotheses if r.get("research_stage") == "活跃研究")
    pending_hyp = sum(1 for r in hypotheses if r.get("research_stage") == "待验证")
    triggered = sum(1 for r in indicators if r.get("当前状态") in {"已触发", "强化"})
    audits_pass = sum(1 for r in audits if r.get("总体结果") == "PASS")
    audits_partial = sum(1 for r in audits if r.get("总体结果") == "PARTIAL")
    audits_pending = sum(1 for r in audits if r.get("总体结果") == "待审计")
    securities_active = sum(1 for r in securities if r.get("research_stage") == "活跃研究")
    behavior_judged = sum(1 for r in behaviors if r.get("market_phase") not in {"", "未判定"})
    high_distribution = sum(1 for r in behaviors if r.get("distribution_risk") in {"高", "极高"})
    high_gap = sum(1 for r in behaviors if r.get("price_fundamental_gap") in {"PF2", "PF3"})

    return "\n".join([
        "| 研究层 | 当前数量 |",
        "|---|---:|",
        f"| 活跃主题 | {active_themes} |",
        f"| 待验证主题 | {pending_themes} |",
        f"| 活跃假设 | {active_hyp} |",
        f"| 待验证假设 | {pending_hyp} |",
        f"| 活跃研究标的 | {securities_active} |",
        f"| 已形成正式M阶段判断 | {behavior_judged} |",
        f"| PF2/PF3 价格显著领先 | {high_gap} |",
        f"| 高/极高 Distribution Risk | {high_distribution} |",
        f"| 已触发/强化领先指标 | {triggered} |",
        f"| Model Audit PASS | {audits_pass} |",
        f"| Model Audit PARTIAL | {audits_partial} |",
        f"| Model Audit 待审计 | {audits_pending} |",
    ])


def main() -> int:
    updated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    out = f"""# Investment Research Workbench

> 私有投资研究工作台。系统不再以新闻作为唯一入口，而是并行观察市场行为、产业领先指标、叙事扩散与正式验证。机器信号只用于发现，不构成投资结论。

**工作台自动刷新时间（UTC）：** `{updated}`

## 快速入口

| 模块 | 最新 | 历史 / 数据库 |
|---|---|---|
| 市场行为机器层 | [最新量价快照](../data/market/latest.md) | [数据层说明](../data/market/README.md) |
| 市场行为研究层 | [M阶段 / PF Gap](../tracking/market-behavior.md) | MBH 历史判断 |
| 新闻监控 | [最新监控摘要](../data/news/latest.md) | [全部新闻候选](../data/news/candidates/) |
| 日报 | [最新日报](../latest/daily.md) | [日报归档](../reports/daily/) |
| 周报 | [最新周报](../latest/weekly.md) | [周报归档](../reports/weekly/) |
| 月报 | [最新月报](../latest/monthly.md) | [月报归档](../reports/monthly/) |
| 事件 | [事件索引](../index/events.md) | EVT 历史 |
| 主题 | [主题索引](../index/themes.md) | THM 历史 |
| 标的 | [标的索引](../index/securities.md) | A股 / 港股通 / ETF |
| 假设 | [研究假设](../tracking/hypotheses.md) | HYP 历史 |
| 催化 | [催化剂](../tracking/catalysts.md) | CAT 历史 |
| 领先指标 | [Leading Indicators](../tracking/leading-indicators.md) | 产业→公司→财务 |
| 模型审计 | [Model Audit](../tracking/model-audit.md) | PASS / PARTIAL / FAIL |
| 风险日历 | [风险/催化日历](../tracking/risk-calendar.md) | 滚动历史 |
| Research OS | [研究方法](../metadata/research-os.md) | F/I/S/R · V0–V5 · M0–M5 · PF Gap |

## 系统状态

### 新闻 / 验证发现层

{news_health_summary()}

### 市场行为机器层

{market_health_summary()}

- [Market Research Monitor Actions](https://github.com/seekerthinker/investment-research/actions/workflows/news-monitor.yml)
- [监控程序](../monitor/)
- [Research OS](../metadata/research-os.md)
- [Market Behavior方法](../metadata/market-behavior.md)
- [来源可信度规则](../metadata/source-policy.md)

## 研究管线状态

{research_summary()}

> `research_stage` 表示研究证据成熟度；V0–V5表示基本面兑现；M0–M5表示市场行为/信息扩散；PF Gap表示价格相对基本面的领先程度。这些维度必须分开维护。

---

## 最新市场行为机器快照

{section_body('data/market/latest.md')}

---

## Market Behavior 研究判断

{section_body('tracking/market-behavior.md')}

---

## 最新新闻监控

{section_body('data/news/latest.md')}

---

## 最新日报

{section_body('latest/daily.md')}

---

## 最新周报

{section_body('latest/weekly.md')}

---

## 最新月报

{section_body('latest/monthly.md')}

---

## 最新重大事件

{section_body('index/events.md')}

---

## 当前投资主题

{section_body('index/themes.md')}

---

## 当前研究标的

{section_body('index/securities.md')}

---

## 当前可证伪研究假设

{section_body('tracking/hypotheses.md')}

---

## 当前催化剂跟踪

{section_body('tracking/catalysts.md')}

---

## 领先指标

{section_body('tracking/leading-indicators.md')}

---

## Model Audit

{section_body('tracking/model-audit.md')}

---

## 近期风险 / 催化事件日历

{section_body('tracking/risk-calendar.md')}

---

## 数据纪律

- `reports/` 下原始日报、周报、月报不事后改写；`latest/` 可覆盖最新一期。
- `data/news/` 是机器新闻发现层；`data/market/` 是机器量价事实与 hint；二者都不是投资结论。
- 核心判断尽量标记 `F/I/S/R`；基本面兑现使用 `V0–V5`；市场行为使用 `M0–M5`；价格与基本面错位使用 `PF-2` 至 `PF3`。
- 媒体/新闻主要承担发现与注意力测量；官方/一手信息主要承担验证；收入、利润、CFO/FCF承担最终确认。
- 不得把放量机械解释为吸筹/出货，也不得把 machine `phase_hint` 直接写成正式 M阶段。
- 活跃 HYP 尽量关联领先指标；高置信公司结论进入正式重点池前执行 Model Audit。
- 证伪、失败、结束的研究判断保留历史状态，不删除。
- 重要研究尽量形成 `Market Behavior + Leading Indicators + Narrative/Attention + Verification → EVT/THM/HYP/CAT → Securities → Model Audit` 的追踪链。
"""
    target = ROOT / "dashboard/README.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out.rstrip() + "\n", encoding="utf-8")
    print(f"rendered {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
