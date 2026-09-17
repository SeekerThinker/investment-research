# 思想 → 方法 → 报告 → 网站与任务：依赖关系图（v0.3）

每次投资思想讨论后逐层记录 `已修改 / 无需修改（理由） / 待处理（障碍）`，不以新增理念回写已发布历史。思想原意和编辑者落实建议分别登记在 [`ideas.md`](ideas.md) 与 [`idea-20260917-11.md`](idea-20260917-11.md)；执行及失败记录见 [`change-log.md`](change-log.md)。

| 层级 | 文件／对象 | IDEA-20260917-11 与 P10 的影响及状态 |
| --- | --- | --- |
| 0 投资思想 | `philosophy/ideas.md`、`idea-20260917-11.md`、`core-beliefs.md` | **已修改**：IDEA-11 已登记，P10 归纳投资机遇／风险规避双主线；明确“重大预期差”是待检验问题，不是已确认的收益预测。v0.3 仍为所有者意旨提炼草案。 |
| 1 研究宪章与收纳 | `philosophy/research-constitution.md`、`intake-and-propagation.md` | **无需修改**：既有事实优先、证伪、版本记录与历史不可变纪律适用；双主线由专业规则实现。 |
| 2 统一操作系统 | [`metadata/philosophy-integration.md`](../metadata/philosophy-integration.md)、`research-os.md`、`source-policy.md`、`continuity-policy.md` | **已修改桥接规范至v0.3**；其他文件**无需修改**：证据分层、时间与不可变历史纪律不变。 |
| 3 专业方法 | [`metadata/news-investment-impact-policy.md`](../metadata/news-investment-impact-policy.md)、[`metadata/daily-coverage-policy.md`](../metadata/daily-coverage-policy.md)、`long-horizon-value-policy.md`、`market-behavior.md` | **已修改前两份**：日报仅在两个主要方向下选7—10、最多12条，按事实／传导／潜在预期差／成立条件或风险触发／强度期限／验证编排，不机械每条双字段。长期现金流与量价证据规则**无需修改**。 |
| 4 证据与状态 | `data/market/`、`data/news/`、`index/`、`tracking/` | **无需修改**：本次是研究与阅读结构变化，没有新增经核验的市场事实，不据此回填。 |
| 5 发布产物 | `latest/daily.md`、`reports/daily/`、`reports/intraday/`、`reports/weekly/`、`reports/monthly/` | **已修改最新可变摘要**：9月17日09:53全文的22条归纳为机遇4项、风险6项，七个面向；旧不可变全文与早报不修改。新日周月任务执行新版规范，历史旧稿不会被事后改写。 |
| 6 网站 | `monitor/build_public_site.py`、`include_intraday_site.py`、[`monitor/curate_homepage.py`](../monitor/curate_homepage.py)、[`site/assets/two-focus.js`](../site/assets/two-focus.js)、`site/index.html`、`site/assets/feed.css` | **已修改精选器与首页**：研究者显式分组，白底单列并分行；日报按机遇／风险两大组显示，周报月报继续独立，所有详情链接免费全文。基础生成器和浅色单列CSS无需更动。 |
| 7 定时研究 | 日报 `6aaa04cee1548191898c93ee3ccc2f0e`、周报 `6aaa04d985a481918cc3115219063054`、月报 `6aaa04e3e97c8191b53f52f6fb59f477` | **三项更新回执 SUCCESS**，均要求读取v0.3与最新规范并按双主线分析，周/月独立；原 Asia/Shanghai 日报07:00、周一02:00、每月首日01:00不变。 |
| 8 自动检查 | [`monitor/validate_philosophy.py`](../monitor/validate_philosophy.py)、[`monitor/test_two_focus.py`](../monitor/test_two_focus.py)、`.github/workflows/publish-site.yml`、`.github/workflows/philosophy-integrity.yml` | **已增双主线单元测试及发布检查**：验证显式分类、分行、日报总量及周/月未丢失，且网站仍白底、免费归档。[已通过的完整部署运行 35185056449](https://github.com/SeekerThinker/investment-research/actions/runs/35185056449)；后续提交需另验最新CI。自动检查不证明任何个股估值正确。 |
| 9 公开导航 | 根 `README.md`、[`philosophy/README.md`](README.md)、网站“投资思想”链接 | **已修改思想库目录说明**；网站继续单独区分跨期思想与当期资讯，不制造付费入口。 |

## 每次后续更新

在 [`change-log.md`](change-log.md) 记录版本、IDEA/Pxx、已改文件与提交、日周月任务回执、测试及Pages结果、无需修改的层级与原因、待处理事项。若检查失败如实记录，不把未验证的投资命题当事实。
