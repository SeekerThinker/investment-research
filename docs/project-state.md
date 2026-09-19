# Market Perspectives｜当前项目状态与交接点

> 这是**可更新的操作状态**，不是第二套投资思想、实时行情数据库或已批准投资结论。项目思想入口在 2026-09-19（北京时间）核对并更新；2026-09-20 对用户提供的投研文件完成选择性方法整合。Cloudflare 登录、市场行情和自动任务运行仍只沿用各自明确注明的上次核验状态，须重新查询，不得由本页推断。发生重要变化后由执行者更新本页并给出可验证回执。

## 当前目标（CURRENT OBJECTIVE）

- 维持 `SeekerThinker/investment-research` 作为唯一公开的代码、思想库、研究档案源；网站品牌使用 **Market Perspectives**。所有已发布报告免费，赞助自愿且不影响研究结论。
- 当前站点生成与 GitHub Pages 已有工作流；Cloudflare Pages 的构建入口和 CI 等价校验已入库。**Cloudflare 实际项目/生产网址状态未在本页更新时独立核验，不得把候选 `market-perspectives.pages.dev` 写成已注册或已上线。**

## 当前接续点（PRIMARY BLOCKER / IMMEDIATE NEXT ACTION）

- **阻碍（上次核验）**：2026-09-18 较早的一次 Cloudflare 控制台操作未获得可用的登录会话；ChatGPT/GitHub 授权不等于 Cloudflare 控制台 GitHub Git 集成已完成。**当前是否已由所有者后续创建项目：未知，必须先查询 Cloudflare 后台。**
- **下一步**：仅在获得 Cloudflare 账户合法授权后，先检查是否已有 `market-perspectives` Pages 项目；如已有，核对 GitHub 仓库、`main`、`bash monitor/build_cloudflare_pages.sh`、输出 `_site` 及生产构建；如没有，再按 [`cloudflare-pages.md`](cloudflare-pages.md) 建立免费 Git 集成。以真实部署和可访问页面验收；GitHub Pages 在此之前不下线。
- **停止条件**：需要登录、验证码、付款或新增权限时交给所有者在服务商界面操作；不得索取聊天内密码/Token，不声称已成功部署。

## 持续研究与内容边界

- 日／周／月流程的规范分别从 [`../philosophy/README.md`](../philosophy/README.md) 和 [`../metadata/philosophy-integration.md`](../metadata/philosophy-integration.md) 定位；最新报告与日期按 `latest/` 和 `reports/` 实际内容逐次读取，本页**不复制**报告数字、最新行情、任务回执或股票观点。
- **2026-09-19 思想入口更新**：所有者提出的 AI 长期发展基础判断已在 [`../philosophy/core-beliefs.md`](../philosophy/core-beliefs.md) P11 和 [`../philosophy/idea-20260919-01.md`](../philosophy/idea-20260919-01.md) 收录；当前思想库为 **v0.4 意旨提炼草案**，完整传播与研究证据边界见 [`../philosophy/change-log.md`](../philosophy/change-log.md) 和执行桥接规范。本页不重复其内容，不把预期当作市场已核验事实，也不代表所有者已逐字审定全部提炼稿。
- **2026-09-20 用户投研资料方法融合**：新增 [`../metadata/multi-horizon-capex-method.md`](../metadata/multi-horizon-capex-method.md) 用于确有上游资本开支传导的专题；逐份采纳/未采纳及历史价格风险见 [`research-material-review-20260920.md`](research-material-review-20260920.md)。执行桥接和 [`../AGENTS.md`](../AGENTS.md) 已加入入口。**没有验证附件的个股价格、目标市值、利润预测或仓位；没有将这些历史数字、排行或全文写入当前研究数据与公开报告；这不是新增 P12，也不是新的定时任务。**
- 2026-09-18 核验的 `reports/` 下有 `daily/`、`intraday/`、`weekly/`、`monthly/`；**季度／年度研究已是用户明确提出的时间尺度愿景，但仓库目前未建立对应独立报告目录、完整发布链与经确认的运行周期**。建立新目录、发布规则、首页模块或定时任务须先提出具体设计，不能倒填历史季度／年度报告或假装已经自动运行。

## 待确认（PENDING HUMAN DECISIONS）

- 季度与年度报告是否启动、何时运行、是否公开单独栏目及评估口径：**未决**；不影响已授权的日／周／月研究。
- Cloudflare 最终实际分配的免费网址及正式切换时点：**待平台核验**；网站品牌 Market Perspectives 已由用户选择，不能据此自动决定付费域名或停用旧站。
- 参考外部 HARC 后建议的更严格人类批准门、强制中英双语维护、项目许可选择：**未由所有者授权采纳**；只做兼容现有流程的轻量交接和明确的来源/状态区分，详见 [`collaboration-review.md`](collaboration-review.md)。

## 交接更新规则

重大用户决定、部署状态、未解决阻碍或项目结构变化后，在本文件更新「当前目标／阻碍／下一步／待确认」，并链接适当的 Git commit、CI 或服务商结果。过去的决策追溯在 [`../philosophy/change-log.md`](../philosophy/change-log.md)，研究阶段状态在 `tracking/`，历史正文在不可变 `reports/`。本文件只放行动指针，不复制这些来源的全部内容；若与权威文件冲突，回到该文件重新核实并修正本页。
