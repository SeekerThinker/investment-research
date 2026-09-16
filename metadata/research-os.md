# Research OS

本文件定义本仓库的统一研究操作系统。目标不是从新闻直接推导投资结论，而是把市场行为、产业领先指标、叙事扩散与正式验证组合成可证伪的研究链。

## 1. 核心研究架构

系统采用四路并行入口：

`Market Behavior + Leading Indicators + Narrative/Attention + Verification/Confirmation`

四路信号汇合后进入：

`EVT-* → THM-* → HYP-* / CAT-* → securities → Model Audit → 日报/周报/月报复盘`

其中：

- **Market Behavior** 负责价格、成交、相对强弱、拥挤与价格领先程度的发现。
- **Leading Indicators** 负责产业需求、价格、库存、CAPEX、订单、认证、产能、良率等前瞻变量。
- **Narrative / Attention** 负责新闻密度、媒体/机构关注和市场叙事扩散，只测量注意力，不代表事实。
- **Verification / Confirmation** 负责公司公告、交易所、监管、官方统计、客户/供应商材料以及最终财务兑现。

NEWS-* 只是 Narrative/Discovery 的一种来源，不再是研究系统唯一入口。

## 2. 证据属性：F / I / S / R

- **F — Fact**：已由公司公告、财报、交易所、政府/监管、官方统计、客户/供应商正式材料或其他可靠一手来源确认的事实。
- **I — Inference**：基于事实通过产业、工程、量价或财务逻辑推导出的结论；必须保留因果链。
- **S — Scenario**：对渗透率、ASP、市占率、良率、利润率、CAPEX、利润、估值等未来变量的情景假设。
- **R — Rumor / Unverified**：尚未可靠确认的客户、订单、良率、扩产、价格、市场份额、AI/HBM收入等。R 不得单独成为核心盈利预测基础。

核心结论应拆成原子判断分别标记，而不是给整篇报告只标一个字母。

## 3. 兑现阶段：V0–V5

V0–V5主要用于产业/公司商业化与盈利兑现；纯宏观或政策事件无法映射时可填 `N/A`。

- **V0 产业逻辑**：仅有产业趋势或理论逻辑。
- **V1 技术机制验证**：产品价值、工程机制、系统约束已得到一定验证。
- **V2 产品验证**：已有产品、样品、送样或实验验证。
- **V3 客户验证**：进入客户认证、小批量或供应商体系。
- **V4 商业化放量**：正式订单、批量供货、收入贡献或产能爬坡。
- **V5 利润与现金流确认**：收入、毛利率、净利润、CFO/FCF已经确认兑现。

V0/V1 可以有高潜在空间，但不能使用与 V4/V5 同等确定性的盈利假设。

## 4. Market Phase：M0–M5

Market Phase 描述价格行为与信息扩散阶段，不等于买卖信号。正式定义见 `metadata/market-behavior.md`。

- **M0 潜伏/早期异动**：相对强弱或成交开始异常，叙事弱。
- **M1 发现**：量价异常持续，产业线索增加。
- **M2 扩散**：价格、成交与注意力加速，基本面仍可能未充分确认。
- **M3 拥挤**：高相对涨幅、高成交和一致叙事同时出现，价格可能明显领先基本面。
- **M4 验证**：订单、认证、公告、经营数据或财务证据开始确认。
- **M5 兑现/背离**：V5已确认，重点观察新增利好是否还能推动价格，以及价格是否开始钝化或转弱。

机器量价层只生成 `phase_hint`；正式 `market_phase` 必须结合叙事、V阶段、领先指标与基本面确认。

## 5. Price–Fundamental Gap

用于衡量价格相对基本面兑现的领先程度：

- `PF-2`：基本面显著领先价格。
- `PF-1`：基本面轻度领先价格。
- `PF0`：大体同步。
- `PF1`：价格轻度领先基本面。
- `PF2`：价格显著领先基本面。
- `PF3`：价格极度领先基本面并伴随较高兑现前风险。
- `未判定`：证据不足。

高 PF 不等于应卖出，低 PF 也不等于应买入；它只描述价格与兑现阶段之间的错位。

## 6. 研究生命周期

`research_stage` 与现有 `status` 分开维护：

- **新发现**：来自量价、新闻、公告或数据的候选，还没有形成正式假设。
- **待验证**：已形成机制链，但关键事实、公司映射或财务传导尚缺证据。
- **活跃研究**：存在可证伪假设、领先指标和明确观察窗口。
- **降级复核**：近期证据变弱、过期、价格/估值显著变化或核心条件需要重新验证。
- **关闭**：已经兑现、证伪或研究价值结束；历史记录保留。

`status` 仍统一使用：`观察 / 强化 / 弱化 / 部分兑现 / 兑现 / 证伪 / 结束`。

## 7. 发现与升级门槛

任何发现只有在可能改变以下至少一个变量时，才值得升级为正式研究：

- 出货/需求、渗透率、ASP / Mix、市占率；
- 名义/有效/合格产能、良率；
- 毛利率/净利率、CAPEX、营运资本、CFO / FCF；
- 盈利预测、风险概率、估值体系 / Price-Implied Expectation。

仅改变情绪、热度、涨跌幅、龙虎榜或讨论度的消息，不提高内在价值判断。但这些变量可以作为 Narrative/Attention 或 Market Behavior 的阶段证据。

## 8. 事件传导模板

正式事件研究至少按以下顺序写清楚：

1. **事实**：发生了什么？证据属性与来源等级是什么？
2. **市场行为**：价格/成交是否已提前反应？当前 M 阶段和 PF Gap 是什么？
3. **产业机制**：改变了什么物理/技术/供需/资本约束？
4. **产业链影响**：利润池、瓶颈、议价权向哪里迁移？
5. **公司暴露**：公司是普通相关、关键供应商还是瓶颈环节？
6. **盈利/现金流影响**：可能影响收入、ASP、Mix、利润率、CAPEX、CFO/FCF中的哪些变量？
7. **Price In**：当前价格可能隐含了什么预期？
8. **证伪条件**：可观察、可量化、有时间窗口。

无法量化时明确标记 I 或 S，不制造伪精确。

## 9. 行业 Beta 与公司 Alpha

任何公司研究必须尽量区分：行业需求 Beta、市占率 Alpha、产品升级 Alpha、单位价值量 Alpha、新客户 Alpha、ASP / Mix Alpha。

优先选择一种收入桥，避免重复计算：

- TAM 模型：`Revenue = TAM × AddressableRatio × Share`
- 单位需求模型：`Revenue = EndUnits × Penetration × ContentPerUnit × ASP × Share`

若行业停止高速增长，应回答公司自身还能创造多少增长。

## 10. 催化剂 A / B / C

- **A — 直接改变利润**：正式订单、批量供货、核心客户、实际涨价/降价、毛利率/财报变化等。
- **B — 提高兑现概率**：客户认证、产品验证、新产能投产、良率提升等。
- **C — 行业层面**：龙头CAPEX、技术新品、行业政策、产业价格等。

纯情绪事件不得直接提高合理企业价值。每个 CAT 同时保留强度、可信度、窗口、状态和证伪条件。

## 11. 三层领先指标

每个活跃 HYP 应尽量关联 `tracking/leading-indicators.md`：

1. **产业领先指标**：需求、库存、价格、利用率、CAPEX、出货等。
2. **公司领先指标**：订单、合同负债、客户认证、招聘、在建工程、原材料采购、新产线等。
3. **财务确认**：Revenue、Gross Margin、Net Profit、CFO、FCF。

领先指标可以提高或降低假设概率，但不能冒充最终财务事实。

## 12. 量价与拥挤风险

机器层 `data/market/` 计算可复现的5D/20D收益、相对基准收益、成交量比、成交量分位、距20日高点和实现波动率。研究层 `tracking/market-behavior.md` 维护正式 M0–M5、PF Gap、拥挤度和 Distribution Risk。

不得把成交量放大机械解释成“主力吸筹/出货”。高 Distribution Risk 通常需要多个条件同时出现：价格明显领先基本面、高成交/高注意力、领先指标停止改善、盈利/V阶段未继续上修，以及新增正面信息无法推动价格创新高或相对强弱转差。

## 13. Model Audit

进入正式高置信公司结论、周报重点机会或月报Top研究池前，至少检查：

- **TAM**：CompanyRevenue ≤ AddressableTAM。
- **Share**：预测份额不明显违反竞争格局现实。
- **Capacity**：Sales ≤ QualifiedCapacity × ASP，除非明确存在外协/其他供给。
- **Margin**：价格、Mix、良率与毛利率假设逻辑一致。
- **Cash Flow**：增长对应的 CAPEX + ΔWorkingCapital 有资金来源，利润与CFO/FCF关系可解释。
- **Dilution**：增发、可转债、股权激励等纳入EPS/每股价值。
- **Valuation**：高估值需要增长、ROIC/Incremental ROIC、FCF、壁垒和增长久期支持。
- **Red Flags**：治理、杠杆、融资压力、客户集中、技术替代、周期顶部、估值、地缘硬约束等不能被高成长评分抵消。

审计结果统一为：`PASS / PARTIAL / FAIL / 待审计`。FAIL 不得进入高置信研究池；PARTIAL 必须列出缺口。

## 14. 信息源的功能定位

信息源不仅按可信度分层，也按功能分层：

- **Discovery**：量价异常、产业高频、GDELT、媒体、搜索/关注度、机构活动。
- **Verification**：交易所、央行、监管、政府统计、公司公告、客户/供应商正式材料。
- **Confirmation**：订单、ASP、产能利用率、收入、毛利、净利润、CFO、FCF。

官方信息源不是唯一的机会发现入口，但在验证与确认阶段具有更高权重。媒体不是 Truth Layer；其价值主要在发现和叙事扩散测量。

## 15. 信息新鲜度

“当前投资价值”优先使用今日/48小时、最近两周、最近季度和最近年度报告的信息。历史资料可用于产业机制、周期和长期比较，但不得用过期价格、市值、订单或客户状态支撑当前结论。

工作台与日报应区分：新发现候选、待验证研究、活跃研究、降级/过期复核、已兑现/证伪/结束，同时展示量价机器层与研究层 M/PF 状态。

## 16. 数据与判断分离

- `data/news/`：机器新闻发现层。
- `data/market/`：机器量价事实与 hint。
- `index/` 与 `tracking/`：研究判断数据库。
- `reports/`：不可变历史研究记录。
- `latest/` 与 `dashboard/`：最新阅读层。

机器 NEWS score、phase_hint、gap_hint、crowding_hint、distribution_risk_hint 都只是筛选工具，不是投资结论。

## 17. 评分与交易边界

多维评分只作为诊断，不作为机械交易信号。严重风险红线优先于总分；不因热门主题、高涨幅或单一催化自动提高评级。仓位、买卖节奏和组合优化只有在用户明确要求时才进入组合层分析，并且不得把 M阶段或PF Gap直接映射成机械买卖指令。

## 18. Research Writing Quality Gate

日报、周报、月报中的重点研究机会在定稿前，应尽量通过以下六问质量门槛：

1. **What changed?** 新增事实、市场行为或领先指标到底发生了什么变化？标明时间、F/I/S/R与来源层级。
2. **Why does it matter?** 变化是否足以改变需求、供给、ASP/Mix、份额、产能/良率、利润率、CAPEX、营运资本、CFO/FCF、风险概率或估值框架？
3. **What is the transmission mechanism?** 尽量写清 `Industry mechanism → Company exposure → Revenue → Gross Margin/Expenses → Profit → CFO/FCF`，避免从行业景气直接跳到公司利润结论。
4. **What does the market appear to price in?** 结合正式M阶段、PF Gap、crowding、distribution_risk、相对强弱、成交和阶段高点距离说明已定价程度；证据不足时写 `未判定`。
5. **What evidence would confirm it?** 指定下一层一手验证、Leading Indicator、公司公告、订单、经营或财务确认。
6. **What evidence would falsify it?** 给出可观察、尽量可量化且有时间窗口的证伪条件。

如果关键机会无法回答第1、5、6项，不应为了报告数量强行升级为正式高优先级研究机会；应保留在 discovery / 待验证层。

## 19. Repository Integrity Audit

GitHub 仓库是项目 canonical state。研究工作流遵循：

`READ → VERIFY STATE → RESEARCH → VERIFY → ANALYZE → UPDATE STATE → WRITE REPORT → UPDATE TRACKERS → COMMIT`

每次结构化写入前至少进行轻量一致性检查：

- 目标仓库存在、`visibility=private` 且当前连接具备 write/push 权限；任一条件不满足立即停止写入，不得改写到其他仓库。
- 对应日期/周次/月度的不可变报告是否已经存在；已存在时不得覆盖。
- 新 EVT / THM / HYP / CAT / MBH / LID / AUD ID 必须从仓库当前实际最大编号继续，检查重复 ID。
- `index/securities.md` 的正式 `market_phase / price_fundamental_gap / crowding / distribution_risk` 与 `tracking/market-behavior.md` 当前记录保持一致。
- `latest/` 指向的报告日期/周次/月度与实际最新不可变报告一致。
- 数据健康和 freshness 必须可见；陈旧或 degraded 的 machine data 不得伪装成当前数据。

周报与月报执行前应进行更完整的 Repository Integrity Audit，额外检查：

- 结构化文件中的 EVT / THM / HYP / CAT / MBH / LID / AUD 交叉引用是否存在断链或引用不存在的 ID。
- 是否存在重复 ID、缺失 tracker、孤立但仍被活跃研究引用的记录。
- `latest/`、当前 trackers/index 与最近不可变报告之间是否出现未解释的状态漂移。
- 已 `证伪 / 结束 / 兑现` 的历史记录是否被错误删除或重新编号。
- machine market/news 数据与 health 的截止时间是否足以支持当前周期判断。

发现一致性问题时，不得修改历史不可变报告来“修正过去”；应在当前周期报告中说明问题，并通过合法的 tracker/index/latest 更新修复当前状态。无法确定正确状态时标记 `待验证`，不得静默猜测。

## 20. Monthly Research Process Audit

每月除研究结果复盘外，必须审计研究过程本身，重点回答：

- 是否过度依赖 NEWS / 媒体发现层，而没有回到 Verification / Confirmation？
- 是否因为 Narrative / Attention 升温而提前升级 V、M、PF 或盈利判断？
- 是否忽视价格、相对强弱、成交或利好钝化等 Market Behavior 反证？
- 是否把 Industry Beta 错当成 Company Alpha，或缺少公司暴露与收入桥？
- 是否从 Revenue 直接跳到利润，遗漏 Margin、费用、CAPEX、Working Capital、CFO/FCF？
- 是否在高 crowding 状态下低估 Distribution Risk，尤其忽视相对强弱恶化、距离高点扩大与利好不涨？
- 是否把 I/S/R 不当地升级为 F，或在证据不足时过早给出正式 V/M/PF 状态？
- 哪些 Leading Indicator / Catalyst 出现 false positive、miss 或验证延迟？原因是指标设计、数据质量、时间窗口还是传导机制错误？
- 哪些 Model Audit 缺口长期没有收敛，却仍被反复列入高优先级研究？

月度流程审计应输出：本月有效的研究纪律、重复出现的失败模式、需要在下月调整的验证规则/指标设计，以及仍无法判断的问题。任何命中率、转化率、误报率或其他统计都只能基于仓库中可审计的历史记录计算；样本不足时明确写 `启动期回溯 / 样本不足`，不得制造统计显著性。