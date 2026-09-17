# 思想 → 方法 → 报告 → 网站与任务：依赖关系图（v0.1）

> 每次思想对话入库都对**本表逐项做影响分析**，记录 `已修改 / 无需修改（理由） / 待处理（障碍）`。这是一份核对清单，不表示每个路径都必须改动；历史不可变报告不回写。具体成果和回执见 [`change-log.md`](change-log.md)，新增观点见 [`ideas.md`](ideas.md)。

| 层级 | 文件/对象 | 新思想必须核查的影响 | 2026-09-17 v0.1 接线情况 |
| --- | --- | --- | --- |
| 0 原始思想 | `philosophy/ideas.md`、`core-beliefs.md` | 忠实记录所有者意旨、状态、Pxx与冲突，编辑者推论另列 | 已建立 P01—P08、IDEA-20260917-01 至 -08；原意整理稿待逐字审核 |
| 1 研究宪章 | `philosophy/research-constitution.md`、`intake-and-propagation.md` | 研究一致性、反证、随时收纳与版本跟踪 | 已建立，后续逐次增量调整 |
| 2 统一操作系统 | `metadata/research-os.md`、`source-policy.md`、`continuity-policy.md`、[`metadata/philosophy-integration.md`](../metadata/philosophy-integration.md) | 证据层级、时间、证伪及不可变历史；思想不能覆盖事实 | 已建立统一思想桥接入口；既有专业纪律不被替换 |
| 3 专业方法 | `metadata/long-horizon-value-policy.md`、`news-investment-impact-policy.md`、`daily-coverage-policy.md`、`market-behavior.md` | 长期估值、逐条投资映射、独立全市场扫描、量价反证是否需修订 | 既有专业规范继续适用，桥接文件统一引用；本次无新增市场假设需改其定义 |
| 4 数据和研究状态 | `data/market/`、`data/news/`、`index/`、`tracking/` | 新证据/假设/反例可否入库、是否需要增量更新 | 无新市场事实，故不回填或改写 |
| 5 新研究产物 | `reports/daily/`、`reports/intraday/`、`reports/weekly/`、`reports/monthly/`、`latest/` | 新稿标思想版本/Pxx、证据缺口及冲突；摘要保留影响和风险 | 三个定时任务已更新；仅未来新稿生效，历史不回写 |
| 6 网站 | `monitor/build_public_site.py`、`include_intraday_site.py`、`site/`、`metadata/publication-*` | 摘要直读、全文免费、思想与日期资讯分离、白底单列 | 已加独立“投资思想”外链至 GitHub 公开思想库；Pages部署验证成功；未复制思想全文到网站内容包 |
| 7 日/周/月任务 | 日报 `6aaa04cee1548191898c93ee3ccc2f0e`、周报 `6aaa04d985a481918cc3115219063054`、月报 `6aaa04e3e97c8191b53f52f6fb59f477` | 每次先读最新思想库及专业规范、引用版本并保留既有研究纪律；检查真实任务回执 | 三项 `automations.update` 回执均 SUCCESS；原定北京时间 07:00/周一02:00/月首01:00不变 |
| 8 自动检查 | `monitor/validate_philosophy.py`、`.github/workflows/philosophy-integrity.yml`、`.github/workflows/publish-site.yml` | 文件/链接/Pxx/IDEA/入口/发布范围与站点回归；语义仍需人工审查 | [独立思想校验成功](https://github.com/SeekerThinker/investment-research/actions/runs/35179743552)；[Pages构建与部署成功](https://github.com/SeekerThinker/investment-research/actions/runs/35179616613) |
| 9 公开导航 | 根 `README.md`、`philosophy/README.md`、网站单独“投资思想”链接 | 区分个人思想、方法和日期资讯 | 已更新；思想仍为 v0.1 所有者意旨提炼草案 |

## 每次更新的传播记录模板

在 [`change-log.md`](change-log.md) 填写：`思想版本 / 触发IDEA / 涉及Pxx / 文件改动 / 日周月任务回执 / 测试与网站部署结果 / 无需改动及理由 / 未完成事项`。先改上游、后改执行端；若任务更新或测试失败，记录实际失败，不称“全面同步”。

**冲突处理**：可核验事实及安全/法律要求先于流程偏好，已确认的研究原则先于编辑者建议与探索性想法；这只是研究过程的处理约定，不是投资、证券或政治选择的价值排序。原则可由事实和后续讨论推动修订。