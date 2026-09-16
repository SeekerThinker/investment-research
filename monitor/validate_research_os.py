#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_STATUS = {"观察", "强化", "弱化", "部分兑现", "兑现", "证伪", "结束"}
ALLOWED_RESEARCH_STAGE = {"新发现", "待验证", "活跃研究", "降级复核", "关闭"}
ALLOWED_VERIFICATION = {"V0", "V1", "V2", "V3", "V4", "V5", "N/A"}
ALLOWED_EVIDENCE = {"F", "I", "S", "R"}
ALLOWED_AUDIT = {"PASS", "PARTIAL", "FAIL", "待审计"}
ALLOWED_CATALYST_TYPE = {"A", "B", "C"}
ALLOWED_MARKET_PHASE = {"M0", "M1", "M2", "M3", "M4", "M5", "未判定"}
ALLOWED_PF_GAP = {"PF-2", "PF-1", "PF0", "PF1", "PF2", "PF3", "未判定"}
ALLOWED_RISK_LEVEL = {"低", "中", "高", "极高", "未判定"}
ALLOWED_INDICATOR_STATUS = {"待更新", "已触发", "强化", "弱化", "失效", "已被财务确认"}


def read(path: str) -> str:
    p = ROOT / path
    if not p.exists() or not p.is_file():
        raise AssertionError(f"missing required file: {path}")
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        raise AssertionError(f"empty required file: {path}")
    return text


def table(text: str):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        raise AssertionError("markdown table not found")
    headers = [x.strip() for x in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [x.strip() for x in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise AssertionError(f"table column mismatch: expected {len(headers)}, got {len(cells)} in {line}")
        rows.append(dict(zip(headers, cells)))
    return headers, rows


def require_columns(path: str, columns):
    headers, rows = table(read(path))
    missing = [c for c in columns if c not in headers]
    if missing:
        raise AssertionError(f"{path}: missing columns {missing}")
    return rows


def require_unique(rows, key: str, label: str) -> None:
    seen = set()
    for row in rows:
        value = row.get(key, "").strip()
        assert value, f"missing {label} id: {row}"
        assert value not in seen, f"duplicate {label} id: {value}"
        seen.add(value)


def evidence_ok(value: str) -> bool:
    value = value.replace("+", "/")
    parts = [p.strip() for p in value.split("/") if p.strip()]
    return bool(parts) and all(p in ALLOWED_EVIDENCE for p in parts)


def verification_ok(value: str) -> bool:
    value = value.strip()
    if value == "N/A":
        return True
    value = value.replace("+", "/")
    parts = [p.strip() for p in value.split("/") if p.strip()]
    return bool(parts) and all(p in ALLOWED_VERIFICATION for p in parts)


def main() -> int:
    for path in (
        "metadata/research-os.md",
        "metadata/market-behavior.md",
        "metadata/source-policy.md",
        "tracking/market-behavior.md",
        "tracking/leading-indicators.md",
        "tracking/model-audit.md",
    ):
        read(path)

    events = require_columns("index/events.md", ["event_id", "来源等级", "证据属性", "兑现阶段", "当前状态"])
    themes = require_columns("index/themes.md", ["theme_id", "evidence_mix", "verification_stage", "research_stage", "当前状态"])
    securities = require_columns("index/securities.md", [
        "代码", "research_stage", "当前研究状态", "verification_stage", "market_behavior_id", "market_phase",
        "price_fundamental_gap", "crowding", "distribution_risk", "industry_beta",
        "company_alpha", "model_audit", "freshness"
    ])
    hypotheses = require_columns("tracking/hypotheses.md", ["hypothesis_id", "evidence_type", "verification_stage", "research_stage", "leading_indicator_ids", "audit_status", "当前状态"])
    catalysts = require_columns("tracking/catalysts.md", ["catalyst_id", "catalyst_type", "evidence_type", "verification_stage", "主要传导变量", "当前状态"])
    indicators = require_columns("tracking/leading-indicators.md", ["indicator_id", "层级", "关联HYP/THM", "证据属性", "当前状态"])
    behaviors = require_columns("tracking/market-behavior.md", [
        "behavior_id", "标的", "market_phase", "machine_phase_hint", "price_fundamental_gap",
        "crowding", "distribution_risk", "verification_stage", "关联HYP/THM", "最近更新"
    ])
    audits = require_columns("tracking/model-audit.md", ["audit_id", "标的/主题", "总体结果", "主要缺口/下一步"])

    require_unique(events, "event_id", "event")
    require_unique(themes, "theme_id", "theme")
    require_unique(securities, "代码", "security")
    require_unique(hypotheses, "hypothesis_id", "hypothesis")
    require_unique(catalysts, "catalyst_id", "catalyst")
    require_unique(indicators, "indicator_id", "leading-indicator")
    require_unique(behaviors, "behavior_id", "market-behavior")
    require_unique(audits, "audit_id", "model-audit")

    for row in events:
        assert evidence_ok(row["证据属性"]), f"invalid event evidence: {row}"
        assert verification_ok(row["兑现阶段"]), f"invalid event verification stage: {row}"
        assert row["当前状态"] in ALLOWED_STATUS, f"invalid event status: {row}"

    for row in themes:
        assert evidence_ok(row["evidence_mix"]), f"invalid theme evidence: {row}"
        assert verification_ok(row["verification_stage"]), f"invalid theme verification stage: {row}"
        assert row["research_stage"] in ALLOWED_RESEARCH_STAGE, f"invalid theme research stage: {row}"
        assert row["当前状态"] in ALLOWED_STATUS, f"invalid theme status: {row}"

    behavior_by_id = {r["behavior_id"]: r for r in behaviors}
    for row in securities:
        assert row["research_stage"] in ALLOWED_RESEARCH_STAGE, f"invalid security research stage: {row}"
        assert row["当前研究状态"] in ALLOWED_STATUS, f"invalid security status: {row}"
        assert verification_ok(row["verification_stage"]), f"invalid security verification stage: {row}"
        assert row["market_phase"] in ALLOWED_MARKET_PHASE, f"invalid market phase: {row}"
        assert row["price_fundamental_gap"] in ALLOWED_PF_GAP, f"invalid PF gap: {row}"
        assert row["crowding"] in ALLOWED_RISK_LEVEL, f"invalid crowding: {row}"
        assert row["distribution_risk"] in ALLOWED_RISK_LEVEL, f"invalid distribution risk: {row}"
        assert row["industry_beta"], f"missing industry_beta: {row}"
        assert row["company_alpha"], f"missing company_alpha: {row}"
        if row["research_stage"] in {"活跃研究", "待验证"}:
            assert row["market_behavior_id"] in behavior_by_id, f"tracked security without valid market behavior id: {row}"
        if row["market_behavior_id"] in behavior_by_id:
            behavior = behavior_by_id[row["market_behavior_id"]]
            for field in ("market_phase", "price_fundamental_gap", "crowding", "distribution_risk"):
                assert row[field] == behavior[field], (
                    f"security/market-behavior mismatch for {row['代码']} field={field}: "
                    f"security={row[field]} behavior={behavior[field]} behavior_id={row['market_behavior_id']}"
                )

    indicator_ids = {r["indicator_id"] for r in indicators}
    for row in hypotheses:
        assert evidence_ok(row["evidence_type"]), f"invalid hypothesis evidence: {row}"
        assert verification_ok(row["verification_stage"]), f"invalid hypothesis verification stage: {row}"
        assert row["research_stage"] in ALLOWED_RESEARCH_STAGE, f"invalid hypothesis research stage: {row}"
        assert row["当前状态"] in ALLOWED_STATUS, f"invalid hypothesis status: {row}"
        if row["research_stage"] == "活跃研究":
            assert row["leading_indicator_ids"], f"active hypothesis without leading indicators: {row}"
            linked = [x.strip() for x in row["leading_indicator_ids"].replace(",", "/").split("/") if x.strip()]
            missing = [x for x in linked if x.startswith("LID-") and x not in indicator_ids]
            assert not missing, f"active hypothesis references missing leading indicators {missing}: {row}"

    for row in catalysts:
        assert row["catalyst_type"] in ALLOWED_CATALYST_TYPE, f"invalid catalyst type: {row}"
        assert evidence_ok(row["evidence_type"]), f"invalid catalyst evidence: {row}"
        assert verification_ok(row["verification_stage"]), f"invalid catalyst verification stage: {row}"
        assert row["当前状态"] in ALLOWED_STATUS, f"invalid catalyst status: {row}"

    for row in indicators:
        assert evidence_ok(row["证据属性"]), f"invalid leading-indicator evidence: {row}"
        assert row["当前状态"] in ALLOWED_INDICATOR_STATUS, f"invalid leading-indicator status: {row}"

    for row in behaviors:
        assert row["market_phase"] in ALLOWED_MARKET_PHASE, f"invalid behavior market phase: {row}"
        assert row["price_fundamental_gap"] in ALLOWED_PF_GAP, f"invalid behavior PF gap: {row}"
        assert row["crowding"] in ALLOWED_RISK_LEVEL, f"invalid behavior crowding: {row}"
        assert row["distribution_risk"] in ALLOWED_RISK_LEVEL, f"invalid behavior distribution risk: {row}"
        assert verification_ok(row["verification_stage"]), f"invalid behavior verification stage: {row}"

    for row in audits:
        assert row["总体结果"] in ALLOWED_AUDIT, f"invalid audit result: {row}"

    print(
        "Research OS validated:",
        f"events={len(events)}",
        f"themes={len(themes)}",
        f"securities={len(securities)}",
        f"hypotheses={len(hypotheses)}",
        f"catalysts={len(catalysts)}",
        f"market_behaviors={len(behaviors)}",
        f"indicators={len(indicators)}",
        f"audits={len(audits)}",
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Research OS validation failed: {exc}", file=sys.stderr)
        raise
