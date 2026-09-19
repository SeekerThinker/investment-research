# 思想 → 方法 → 报告 → 网站与任务：依赖关系图（v0.4）

每次投资思想讨论后逐层记录 `已修改 / 无需修改（理由） / 待处理（障碍）`，不以新增理念回写已发布历史。思想原意和编辑者落实建议分别登记在 [`ideas.md`](ideas.md)、[`idea-20260919-01.md`](idea-20260919-01.md) 与历史 [`idea-20260917-11.md`](idea-20260917-11.md)；执行及失败记录见 [`change-log.md`](change-log.md)。

## 2026-09-19｜IDEA-20260919-01／P11 的逐层影响

| 层级 | 对象 | 此轮影响及边界 |
| --- | --- | --- |
| 0 投资思想 | [`core-beliefs.md`](core-beliefs.md)、[`ideas.md`](ideas.md)、[`idea-20260919-01.md`](idea-20260919-01.md) | **已修改**：将所有者对 AI 新型生产力长期需求与中美战略投入的判断登记为 P11、IDEA-20260919-01；为所有者长期研究观点，未来事实仍待检验；全文 v0.4 仍非逐字审定。 |
| 1 研究宪章与收纳 | `research-constitution.md`、`intake-and-propagation.md` | **无需修改**：既有 F/I/S/R、反证、现金流和入库状态规则足以约束 P11；不新增必须看多 AI 的规定。 |
| 2 统一操作系统 | [`../metadata/philosophy-integration.md`](../metadata/philosophy-integration.md)、`research-os.md`、`source-policy.md`、`continuity-policy.md` | **已修改桥接至 v0.4**：新增 AI 应用需求／生产率、政策预算与实际支出、产业利润/现金流、估值和反证的条件性核查；专业文件既有证据规则继续适用，无需重复造另一套。 |
| 3 专业方法 | `daily-coverage-policy.md`、`news-investment-impact-policy.md`、`long-horizon-value-policy.md`、`market-behavior.md` | **无需修改**：全市场广扫描、日报精选/双主线、长期估值与数据纪律均适用。P11 不是强制每日 AI 置顶或预设收益。 |
| 4 证据与状态 | `data/market/`、`data/news/`、`index/`、`tracking/` | **无需修改**：本轮未独立核实任何新的 AI 需求数据、中美预算/政策或企业经营事实；不回填未来结论。后续研究有新证据时按真实日期更新。 |
| 5 发布产物 | `latest/**`、`reports/**` | **无需修改**：旧报告不可变，当前最新摘要不可凭长期信念添加伪新闻；P11 仅约束后续相关研究提问及核验。 |
| 6 网站与托管 | `site/**`、`monitor/build_public_site.py`、Cloudflare/GitHub Pages | **无需修改**：网站结构、公开免费及托管行为不因本观点变化；不声称 Cloudflare 已上线。 |
| 7 日／周／月任务 | 现有周期任务及其读取最新思想库的约定 | **无需改动时间和计划**：执行时应读取 P11，但只有出现对应真实新信息才进入日报；周/月可跟踪兑现与反证。本轮不声称已逐项修改或核验外部自动任务回执。季度/年度机制仍待决定。 |
| 8 自动检查 | [`../monitor/validate_philosophy.py`](../monitor/validate_philosophy.py)、现有 CI | **已修改校验**：检查 P11 和 IDEA-20260919-01 入库、版本和互链；结构检查不能证明 AI 长期发展强度。最终 CI 状态须另以实际运行回执为准。 |
| 9 公开导航与交接 | [`README.md`](README.md)、[`../metadata/philosophy-integration.md`](../metadata/philosophy-integration.md)、`../docs/project-state.md` | **已更新思想库导航及执行桥接**；项目交接状态仅记录新长期判断的权威入口，不复制成第二个知识真值源。根 README/网站呈现无须因本次新增领域观点改版。 |

## 2026-09-17｜IDEA-20260917-11／P10 的历史传播记录（v0.3）

| 层级 | 文件／对象 | IDEA-20260917-11 与 P10 的影响及状态 |
| --- | --- | --- |
| 0 投资思想 | `philosophy/ideas.md`、`idea-20260917-11.md`、`core-beliefs.md` | **已修改**：IDEA-11 已登记，P10 归纳投资机遇／风险规避双主线；明确“重大预期差”是待检验问题，不是已确认的收益预测。v0.3 为当时的所有者意旨提炼草案。 |
| 1 研究宪章与收纳 | `philosophy/research-constitution.md`、`intake-and-propagation.md` | **无需修改**：既有事实优先、证伪、版本记录与历史不可变纪律适用；双主线由专业规则实现。 |
| 2 统一操作系统 | [`metadata/philosophy-integration.md`](../metadata/philosophy-integration.md)、`research-os.md`、`source-policy.md`、`continuity-policy.md` | **当时已修改桥接规范至v0.3**；其他文件**无需修改**：证据分层、时间与不可变历史纪律不变。 |
| 3 专业方法 | [`metadata/news-investment-impact-policy.md`](../metadata/news-investment-impact-policy.md)、[`metadata/daily-coverage-policy.md`](../metadata/daily-coverage-policy.md)、`long-horizon-value-policy.md`、`market-behavior.md` | **已修改前两份**：日报仅在两个主要方向下选7—10、最多12条，按事实／传导／潜在预期差／成立条件或风险触发／强度期限／验证编排，不机械每条双字段。长期现金流与量价证据规则**无需修改**。 |
| 4 证据与状态 | `data/market/`、`data/news/`、`index/`、`tracking/` | **无需修改**：当次是研究与阅读结构变化，没有新增经核验的市场事实，不据此回填。 |
| 5 发布产物 | `latest/daily.md`、`reports/daily/`、`reports/intraday/`、`reports/weekly/`、`reports/monthly/` | **当时已修改最新可变摘要**：9月17日09:53全文的22条归纳为机遇4项、风险6项，七个面向；旧不可变全文与早报不修改。新日周月任务执行当时规范，历史旧稿不会被事后改写。 |
| 6 网站 | `monitor/build_public_site.py`、`include_intraday_site.py`、[`monitor/curate_homepage.py`](../monitor/curate_homepage.py)、[`site/assets/two-focus.js`](../site/assets/two-focus.js)、`site/index.html`、`site/assets/feed.css` | **当时已修改精选器与首页**：研究者显式分组，白底单列并分行；日报按机遇／风险两大组显示，周报月报继续独立，所有详情链接免费全文。基础生成器和浅色单列CSS无需更动。 |
| 7 定时研究 | 日报 `6aaa04cee1548191898c93ee3ccc2f0e`、周报 `6aaa04d985a481918cc3115219063054`、月报 `6aaa04e3e97c8191b53f52f6fb59f477` | **当时三项更新回执 SUCCESS**，均要求读取v0.3与最新规范并按双主线分析，周/月独立；原 Asia/Shanghai 日报07:00、周一02:00、每月首日01:00不变。 |
| 8 自动检查 | [`monitor/validate_philosophy.py`](../monitor/validate_philosophy.py)、[`monitor/test_two_focus.py`](../monitor/test_two_focus.py)、`.github/workflows/publish-site.yml`、`.github/workflows/philosophy-integrity.yml` | **当时已增双主线单元测试及发布检查**：验证显式分类、分行、日报总量及周/月未丢失，且网站仍白底、免费归档。[已通过的完整部署运行 35185056449](https://github.com/SeekerThinker/investment-research/actions/runs/35185056449)；后续提交需另验最新CI。自动检查不证明任何个股估值正确。 |
| 9 公开导航 | 根 `README.md`、[`philosophy/README.md`](README.md)、网站“投资思想”链接 | **当时已修改思想库目录说明**；网站继续单独区分跨期思想与当期资讯，不制造付费入口。 |

## 每次后续更新

在 [`change-log.md`](change-log.md) 记录版本、IDEA/Pxx、已改文件与提交、日周月任务回执、测试及Pages结果、无需修改的层级与原因、待处理事项。若检查失败如实记录，不把未验证的投资命题当事实。
