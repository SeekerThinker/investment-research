# 投资思想库修订与实施日志

本日志只记录**确实完成的工作**；所有者思想、编辑者操作化建议、Git 提交、自动任务和网站部署分开核对。思想文本版本不是市场事实版本；旧研报绝不因理念更新而回写。

## 2026-09-17｜v0.2 范围澄清：日报精简，不删除周报/月报（IDEA-20260917-10）

- **所有者澄清**：此前“5—7个面向、7—10条、最多12条”的限制只针对首页中的日报资讯，不应删除或隐藏周报与月报；每条资讯里的事实、影响、机会、风险、强度/期限、已定价/验证应分成独立视觉行，而不是挤在一个长段落。
- **思想台账**：`ideas.md` 新增 IDEA-20260917-10，并将 IDEA-20260917-09 的范围补充为“首页日报部分”的精选上限；这属于发布与阅读结构要求，不改变任何历史研究事实。
- **网站实现**：`site/assets/app.js` 恢复并明确首页三类研究栏目：日报精选、周报观察、月度视角；日报上限不传递给周/月。摘要解析新增 `analysisParts` / `analysisBlock`，把事实、影响、机会、风险、强度/期限、已定价/验证拆成独立行；`site/assets/feed.css` 已有白底单列 `.analysis-line` 样式，继续使用。[展示修正提交](https://github.com/SeekerThinker/investment-research/commit/3395c4bbd6e41aea40cc730942d7df3062d0ed89)。
- **发布检查修正**：此前 `publish-site.yml` 的断言错误地要求 `weekly/monthly` 为空，与 `monitor/curate_homepage.py` 的“只精简日报、保留周/月”设计相冲突。现改为：日报1—12条；market/risk可留完整报告；若存在最新周报/月报，首页 `feed.weekly` / `feed.monthly` 必须非空；同时机械检查分行分析组件存在。[CI修正提交](https://github.com/SeekerThinker/investment-research/commit/d9f213d2a8868bdf7f8b8c4a20d960dd19a627c8)。
- **日报自动任务**：任务 `6aaa04cee1548191898c93ee3ccc2f0e` 更新回执 SUCCESS，明确 IDEA-09/10：日报精选最多12条只作用于日报区；周报/月报继续独立显示；资讯卡片必须分行呈现投资分析。07:00 Asia/Shanghai 时间不变。周报/月报任务自身无需因本次视觉澄清改变研究周期或内容生成规则。
- **历史与数据无需修改**：`reports/`、`data/market/`、`data/news/`、`index/`、`tracking/` 没有新的市场事实，均不因页面结构修改而回写；所有历史报告仍免费且不可变。
- **验证状态**：本条记录写入时，新的 Pages 工作流已由展示与CI提交触发；最终部署成功与否以该运行的实际回执为准，不在回执完成前预先写 SUCCESS。

## 2026-09-17｜v0.2 广泛扫描、精选发布（IDEA-20260917-09，P07—P09）

- **所有者新要求（意旨整理，非逐字引语）**：全市场覆盖不等于堆满每日页面，优先5—7个投资面向、约7—10个最具投资意义的主题，最多12条，不应过度延展；每条仍须直接写明投资影响和风险。
- **编辑者落实方法**：把多则同一因果链的事实合并为一个主题；由研究者在可变 `latest/daily.md` 明确精选，站点不机械截取旧全文前12条；完整原研报、市场行为和独立风险仍在免费报告归档。未入选资料保留于来源与覆盖说明，不冒充已经核验。
- **思想库**：`ideas.md` 新增 IDEA-20260917-09；`core-beliefs.md` 增 P09 并标 v0.2；`philosophy/README.md` 更新阅读入口。`metadata/philosophy-integration.md` 同步执行合同；`metadata/daily-coverage-policy.md` 明确广扫描、5—7面向、通常7—10至多12条、正文层级及历史不可变。[规范提交](https://github.com/SeekerThinker/investment-research/commit/55391904077bcd036af7124ed3c144915d5503b6)。
- **当期可变摘要与网站**：把9月17日09:53原报告22条合并精选成**7个面向、10条**，只改 `latest/daily.md`，不更改 `reports/intraday/2026-09-17-0953.md` 及早报。[精选摘要提交](https://github.com/SeekerThinker/investment-research/commit/723f9f7fbb445c0c2d8e037cf48d6c578485c265)。`monitor/curate_homepage.py` 用精选摘要重建首页日报；其设计本身保留 `feed.weekly` 与 `feed.monthly`，日报精选上限不应影响周/月。超过12条、超过7面向或缺投资映射时报错。[站点精选脚本](https://github.com/SeekerThinker/investment-research/commit/32bc8e00dec9fa0d523798bd25cd198d7020cd36)；[发布检查](https://github.com/SeekerThinker/investment-research/commit/d6a327998e97e56ae2e27a611d9436a5b9bd52ee)。
- **自动任务**：日报任务 `6aaa04cee1548191898c93ee3ccc2f0e` 的更新回执 SUCCESS，原07:00 Asia/Shanghai不变；明确废除旧15—25条/12—20条目标，先扫九面再精选7—10条（≤12）。周报任务 `6aaa04d985a481918cc3115219063054` 和月报 `6aaa04e3e97c8191b53f52f6fb59f477` 已有“每次先读最新版思想库、日报覆盖规范”的要求，自身没有强制新日报条数，故此次不修改其运行时间或独立研究任务。
- **已验证**：[Pages 运行 35180514525](https://github.com/SeekerThinker/investment-research/actions/runs/35180514525) 的思想库结构检查、资讯提取、精选步骤、首页≤12及白色主题验收、构建与部署 job 全部 SUCCESS；该运行验证的是上一版首页结构，不代表本次周/月恢复与分行排版已经验证。
- **无需改动与边界**：`data/market/`、`data/news/`、`index/`、`tracking/` 无新增事实；历史日报、盘中原研报、周报和月报不回写；公开阅读、自愿赞助、白色单列排版维持原状。新方法从下一份新日报全文和当前可变摘要生效；本次不宣称已按新格式重新撰写旧报告。所有者对提炼措辞仍可继续修订；自动检查只管结构和最低字段，不能机械判断投资信息的重要性。

## 2026-09-17｜v0.1 建立可迭代思想库

- **起因**：所有者希望自由、不定期提出投资想法，由助手忠实整理并系统性传播到市场、行业、公司、估值研究和自动执行端；思想与有日期的资讯分离。
- **来源与状态**：当前项目对话意旨；`IDEA-20260917-01` 至 `IDEA-20260917-07`。核心思想 P01—P08 为编辑者的意旨整理，**尚未获得所有者逐字审核**；已明确的执行要求可以据此执行。`IDEA-20260917-08` 是编辑者工程建议，不是所有者投资观点。
- **思想与追踪文档（已入库）**：`philosophy/README.md`、`core-beliefs.md`、`research-constitution.md`、`intake-and-propagation.md`、`ideas.md`、`integration-map.md` 与本日志。
- **统一执行入口与根导航（已入库）**：`metadata/philosophy-integration.md` 负责思想到研究操作的桥接，根 `README.md` 增加思想库、理念来源和专业方法链接；以 `metadata/philosophy-integration.md` 为唯一入口。
- **三个定时任务**：日报、周报、月报均读取思想库、版本与执行桥接，新稿遵守全市场覆盖、逐条投资映射、长期估值、证据、风险与历史不可变纪律；原定时不变。
- **仍需人工工作**：所有者尚未逐字审核 P01—P08 的提炼措辞；自动检查仅证明文件/链接/任务接线等结构，不等于证明未来报告语义始终符合理念。以后新想法按 `intake-and-propagation.md` 做具体影响分析和更新，并逐次记录实际执行结果。

## 每次后续更新模板

`YYYY-MM-DD｜vX.Y｜IDEA-* 与 Pxx｜所有者意旨/编辑者补充的区别｜冲突与适用范围｜已更改文件及commit｜日周月任务ID和更新回执｜测试与Pages运行链接/结果｜无需修改的层级及理由｜未完成项`。

如发生失败，直接写失败、受影响范围和补救提交；不得删除已证伪历史或把未通过的CI写作已通过。