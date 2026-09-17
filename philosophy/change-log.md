# 投资思想库修订与实施日志

本日志只记录**确实完成的工作**；所有者思想、编辑者操作化建议、Git 提交、自动任务和网站部署分开核对。思想文本版本不是市场事实版本；旧研报绝不因理念更新而回写。

## 2026-09-17｜v0.2 广泛扫描、精选发布（IDEA-20260917-09，P07—P09）

- **所有者新要求（意旨整理，非逐字引语）**：全市场覆盖不等于堆满每日页面，优先5—7个投资面向、约7—10个最具投资意义的主题，最多12条，不应过度延展；每条仍须直接写明投资影响和风险。
- **编辑者落实方法**：把多则同一因果链的事实合并为一个主题；由研究者在可变 `latest/daily.md` 明确精选，站点不机械截取旧全文前12条；完整原研报、市场行为和独立风险仍在免费报告归档。未入选资料保留于来源与覆盖说明，不冒充已经核验。
- **思想库**：`ideas.md` 新增 IDEA-20260917-09；`core-beliefs.md` 增 P09 并标 v0.2；`philosophy/README.md` 更新阅读入口。`metadata/philosophy-integration.md` 同步执行合同；`metadata/daily-coverage-policy.md` 明确广扫描、5—7面向、通常7—10至多12条、正文层级及历史不可变。[规范提交](https://github.com/SeekerThinker/investment-research/commit/55391904077bcd036af7124ed3c144915d5503b6)。
- **当期可变摘要与网站**：把9月17日09:53原报告22条合并精选成**7个面向、10条**，只改 `latest/daily.md`，不更改 `reports/intraday/2026-09-17-0953.md` 及早报。[精选摘要提交](https://github.com/SeekerThinker/investment-research/commit/723f9f7fbb445c0c2d8e037cf48d6c578485c265)。`monitor/curate_homepage.py` 用精选摘要重建首页日报，并将独立市场行为、风险及周/月重复条目留给免费报告页，保留原全文链接；超过12条、超过7面向或缺投资映射时报错。[站点精选脚本](https://github.com/SeekerThinker/investment-research/commit/32bc8e00dec9fa0d523798bd25cd198d7020cd36)；[发布检查](https://github.com/SeekerThinker/investment-research/commit/d6a327998e97e56ae2e27a611d9436a5b9bd52ee)。
- **自动任务**：日报任务 `6aaa04cee1548191898c93ee3ccc2f0e` 的更新回执 SUCCESS，原07:00 Asia/Shanghai不变；明确废除旧15—25条/12—20条目标，先扫九面再精选7—10条（≤12）。周报任务 `6aaa04d985a481918cc3115219063054` 和月报 `6aaa04e3e97c8191b53f52f6fb59f477` 已有“每次先读最新版思想库、日报覆盖规范”的要求，自身没有强制新日报条数，故此次不修改其运行时间或独立研究任务。
- **已验证**：[Pages 运行 35180514525](https://github.com/SeekerThinker/investment-research/actions/runs/35180514525) 的思想库结构检查、资讯提取、精选步骤、首页≤12及白色主题验收、构建与部署 job 全部 SUCCESS；站外重新读取首页，看到一组精选日报及十个指向完整09:53研报的详情链接。哲学文档后续更新触发的最新运行须各自另查，不能将本记录的成功扩大为尚未验证的未来执行质量。
- **无需改动与边界**：`data/market/`、`data/news/`、`index/`、`tracking/` 无新增事实；历史日报、盘中原研报、周报和月报不回写；公开阅读、自愿赞助、白色单列排版维持原状。新方法从下一份新日报全文和当前可变摘要生效；本次不宣称已按新格式重新撰写旧报告。所有者对提炼措辞仍可继续修订；自动检查只管结构和最低字段，不能机械判断投资信息的重要性。

## 2026-09-17｜v0.1 建立可迭代思想库

- **起因**：所有者希望自由、不定期提出投资想法，由助手忠实整理并系统性传播到市场、行业、公司、估值研究和自动执行端；思想与有日期的资讯分离。
- **来源与状态**：当前项目对话意旨；`IDEA-20260917-01` 至 `IDEA-20260917-07`。核心思想 P01—P08 为编辑者的意旨整理，**尚未获得所有者逐字审核**；已明确的执行要求可以据此执行。`IDEA-20260917-08` 是编辑者工程建议，不是所有者投资观点。
- **思想与追踪文档（已入库）**：`philosophy/README.md`、`core-beliefs.md`、`research-constitution.md`、`intake-and-propagation.md`、`ideas.md`、`integration-map.md` 与本日志。代表提交：[`538191c`](https://github.com/SeekerThinker/investment-research/commit/538191cc7e7b9eddcd704444a3894d62b54c7ee0)、[`3b77bbd`](https://github.com/SeekerThinker/investment-research/commit/3b77bbdd6646a212511567f0aa3e2b6e23e90fe3)、[`568a6d6`](https://github.com/SeekerThinker/investment-research/commit/568a6d60f2bbd6a39adf6888d8f41a76eeec1448)、[`1c93cf1`](https://github.com/SeekerThinker/investment-research/commit/1c93cf1575c779287094591530d919375d2c64cc)、[`eb06552`](https://github.com/SeekerThinker/investment-research/commit/eb06552e2893d7ee3e55d4cb895f1d5a66aa62c7)。
- **统一执行入口与根导航（已入库）**：`metadata/philosophy-integration.md` 负责思想到研究操作的桥接，根 `README.md` 增加思想库、理念来源和专业方法链接；意外产生的重复 `metadata/philosophy-integration-policy.md` 已在提交 [`2f07028`](https://github.com/SeekerThinker/investment-research/commit/2f07028837e390ec407790291802c7401905d5fe) 删除，以 `metadata/philosophy-integration.md` 为唯一入口。
- **网站（已部署）**：`site/index.html` 新增独立“投资思想”导航，指向公开仓库思想库 README（会打开 GitHub，不是假称已制作站内思想全文）；资讯仍白底单列、直接显示投资影响，历史报告仍免费。提交 [`5507dcc`](https://github.com/SeekerThinker/investment-research/commit/5507dccabd11ab6291c625290d4afbf48415ee80)。[Pages 运行 35179616613](https://github.com/SeekerThinker/investment-research/actions/runs/35179616613) 的思想结构核验、资讯提取、构建与部署 job 均成功。
- **独立检查（已通过）**：`monitor/validate_philosophy.py` 检查思想文件、P01—P08、初始 IDEA、相对文档链接、统一桥梁与 README；`publish-site.yml` 在相关更改时运行该检查，[独立 Philosophy Integrity 运行 35179743552](https://github.com/SeekerThinker/investment-research/actions/runs/35179743552) 的校验 job 成功。独立工作流由提交 [`c620139`](https://github.com/SeekerThinker/investment-research/commit/c620139ee017f29f2d4e72bb29bf114deb1726b2) 建立，支持思想文档变更与 PR。
- **三个定时任务（更新回执均 SUCCESS）**：日报 `6aaa04cee1548191898c93ee3ccc2f0e`、周报 `6aaa04d985a481918cc3115219063054`、月报 `6aaa04e3e97c8191b53f52f6fb59f477`。三者现均先读思想库、版本与 `metadata/philosophy-integration.md`，新稿标 Pxx/版本并保留各自原有的全市场覆盖、逐条投资映射、长期估值、证据、风险与历史不可变纪律；Asia/Shanghai 原定日报07:00、周一02:00、每月1日01:00不变。
- **无需更动（原因）**：`data/market/`、`data/news/`、`index/` 和 `tracking/` 没有新增市场事实，不凭理念回填；历史 `reports/` 已发布正文不改；公开阅读/自愿赞助政策及收款链接未变。专业 `metadata/` 原有方法保留，以 `metadata/philosophy-integration.md` 作统一上游入口，不为同一规则创建多个竞争版本。
- **仍需人工工作**：所有者尚未逐字审核 P01—P08 的提炼措辞；自动检查仅证明文件/链接/任务接线等结构，不等于证明未来报告语义始终符合理念。以后新想法按 `intake-and-propagation.md` 做具体影响分析和更新，并逐次记录实际执行结果。

## 每次后续更新模板

`YYYY-MM-DD｜vX.Y｜IDEA-* 与 Pxx｜所有者意旨/编辑者补充的区别｜冲突与适用范围｜已更改文件及commit｜日周月任务ID和更新回执｜测试与Pages运行链接/结果｜无需修改的层级及理由｜未完成项`。

如发生失败，直接写失败、受影响范围和补救提交；不得删除已证伪历史或把未通过的CI写作已通过。