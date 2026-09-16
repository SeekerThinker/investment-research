# Daily Continuity Recovery Policy

本文件定义日报发生日期缺口时的恢复规则。它是 `metadata/research-os.md` 的补充规则，不改变既有 V / M / PF / Catalyst / evidence schema；若与 Research OS、Market Behavior 或 Source Policy 冲突，以三份核心 metadata 文件为准。

## 1. 触发条件

每次日报启动时，先读取 `reports/daily/` 中最新不可变日报日期，并与当前日报日期比较，同时核对 `latest/daily.md`、当前 `index/` / `tracking/` 最近更新时间以及 `data/market/`、`data/news/` 可用时间范围。

如果最新不可变日报不是前一自然日，不自动视为错误。必须先判断缺口中是否包含交易日，或是否存在已经到期但未闭环的下一验证、Catalyst、Leading Indicator、Hypothesis、Market Behavior 或 risk-calendar 项目。

## 2. Continuity Recovery 模式

如果存在缺失研究日或未闭环验证，则进入 `continuity recovery` 模式。

- 不得事后创建、补写或伪造缺失日期的 `reports/daily/YYYY-MM-DD.md`。
- 不得用当前已知结果回写过去判断，不得制造 hindsight contamination。
- 只允许在当前日期不可变日报中加入 `连续性补核 / Continuity Recovery` 部分。
- 按时间顺序复核从上一份日报截止之后到当前正常约24小时研究窗口之前的关键事实、machine market data、NEWS discovery、已到期 CAT / LID / HYP / MBH 验证项和风险日历。
- 明确区分“当时可知信息”和“之后才出现的信息”。

## 3. 状态更新纪律

连续性补核的目的，是关闭或重新标记未决验证，而不是补造历史报告。

- 能由现有可审计证据确认的事项，可以更新当前 `index/` / `tracking/` 状态。
- 无法确认的事项继续标记 `待验证`。
- 不得因为日报缺失本身机械升级或降级 HYP、V、M、PF、crowding 或 distribution_risk。
- NEWS、machine hints 和后验价格表现不得被倒推为过去已知事实。
- 若缺口期间 machine market/news 数据缺失、陈旧或 degraded，必须披露数据截止时间和失败源，不得补造价格、5D/20D、成交量或历史 NEWS。

## 4. 当前日报结构

完成 continuity recovery 后，再执行正常的当前约24小时日报研究。

当前日报必须清楚区分：

1. `连续性补核 / Continuity Recovery`
2. `今日新增信息`

同一事实、催化或验证结果不得为了数量同时重复计入补核与“今日最重要”列表。若进入 continuity recovery 模式，应在日报开头说明覆盖日期范围和主要待闭环事项。

## 5. 无有效缺口时

如果日期间隔只来自周末、节假日或其他非交易日，并且没有未闭环的研究验证事项，则不需要制造补核内容。正常执行当日日报，并简要说明不存在需要恢复的研究缺口。

## 6. 审计目标

Continuity Recovery 的目标是保持 Research OS 的连续性、可审计性和时间顺序完整性，而不是追求每天都有一份历史文件。任何历史缺口都必须保留为真实项目历史的一部分。