# 思想 → 方法 → 报告 → 网站与任务：依赖关系图（v0.1）

> 用途：每次思想对话入库，都对**本表逐项做影响分析**，记录 `已修改 / 无需修改（理由） / 待处理（障碍）`。这里是核对清单，不等于声称每个路径都必须改动。涉及已有历史报告时一律不回写。变更日志见 [`change-log.md`](change-log.md)；增量意旨见 [`ideas.md`](ideas.md)。

| 层级 | 文件/对象 | 依赖关系与必查动作 | 本次基线状态（2026-09-17） |
| --- | --- | --- | --- |
| 0 思想原意 | `philosophy/ideas.md`, `core-beliefs.md` | 记录所有者意旨、状态、Pxx及冲突；编辑者推论另列 | 已建立；提炼稿尚未逐字审核 |
| 1 研究原则 | `philosophy/research-constitution.md`, `intake-and-propagation.md` | 研究一致性门槛、随时收纳与版本追踪 | 已建立；可迭代 |
| 2 统一操作系统 | `metadata/research-os.md`, `metadata/source-policy.md`, `metadata/continuity-policy.md` | 核对事件传导、F/I/S/R、证伪与不可变记录；不得以思想覆盖事实 | 已有；需引用思想入口 |
| 3 专业方法 | `metadata/long-horizon-value-policy.md`, `metadata/news-investment-impact-policy.md`, `metadata/daily-coverage-policy.md`, `metadata/market-behavior.md` | 将长周期估值、逐条投资映射、全市场独立扫描、量价纪律具体化 | 已有；需引用思想入口 |
| 4 研究数据与状态 | `data/market/`, `data/news/`, `index/`, `tracking/` | 检查实际可得数据、证据链接、失败/证伪，按当期新证据增量维护 | 不回填事实；无新事实无需改动 |
| 5 新研究产物 | `reports/daily/`, `reports/intraday/`, `reports/weekly/`, `reports/monthly/`, `latest/` | 新稿注明思想版本/原则、证据缺口；各摘要保留影响、机会/风险；旧报告不可变 | 新稿起生效；历史不回写 |
| 6 网站呈现 | `monitor/build_public_site.py`, `monitor/include_intraday_site.py`, `site/`, `metadata/publication-*` | 摘要直接可读、正文免费、思想库与当期资讯分别展示、白色单列阅读 | 网站需补独立思想入口；不得暴露机器候选/敏感数据 |
| 7 定时执行 | 日报 `6aaa04cee1548191898c93ee3ccc2f0e`；周报 `6aaa04d985a481918cc3115219063054`；月报 `6aaa04e3e97c8191b53f52f6fb59f477` | 每次先读思想库和最新版专业规范、报告记录版本；既有亚洲/上海执行时间不变 | 本次将同步检查和更新；核对实际任务回执 |
| 8 测试与发布 | `monitor/validate_philosophy.py`, `.github/workflows/philosophy-integrity.yml`, `.github/workflows/publish-site.yml` | 检查引用存在、Pxx/IDEA、版本、关键依赖及网站公开边界；工作流失败不能声称部署成功 | 待建立/接线并验证 |
| 9 导航和说明 | 根 `README.md`、`philosophy/README.md`、网站独立页面 | 让读者能区分个人研究思想、具体方法和有日期的投资资讯 | 根README及网站待加入口 |

## 变更传播检查模板

每次新增 `IDEA-*` 后，在 [`change-log.md`](change-log.md) 写：`思想版本 / 触发IDEA / 涉及Pxx / 文件改动 / 日周月任务回执 / 测试与网站部署结果 / 无需改动及理由 / 未完成事项`。先改上游，后改执行端；若任务改动失败，必须注明待处理，不应称“全体系已同步”。

**冲突优先顺序**：可复核事实及法律/安全限制 > 可验证的证据纪律/历史不可变 > 已确认研究原则 > 编辑者操作化建议 > 探索性想法。这里的顺序是**研究流程冲突解决办法**，不是对政治、证券或投资结果的排名；任何核心思想都可在新事实出现时被公开修订。