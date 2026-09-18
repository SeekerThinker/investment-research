# Market Perspectives 对 HARC 的选择性协作升级审查

**审查日期**：2026-09-18（北京时间）。**性质**：本项目的工程／协作评估及编辑者实施记录，不是新的投资思想、不代表所有者逐字批准外部协议，也不证明任何投资结论正确。

**参考**：[Human–AI Research Collaboration Protocol](https://github.com/ChongLiuPhil/Human-AI-Research-Collaboration-Protocol)（审查时 `HARC_MANIFEST.yaml` 显示 `0.2.0-draft`）。主要对照其 `README.zh-CN.md`、`START_HERE.zh-CN.md`、`AGENTS.zh-CN.md`、`HARC_CONTEXT_INTERFACE.yaml`、`protocol/FORM_CONTENT_ROUTING.zh-CN.md`、`protocol/REPOSITORY_CONTEXT_INTERFACE.zh-CN.md`、`protocol/FRAMEWORK_APPROVAL.zh-CN.md` 及 `LICENSE-DECISION.zh-CN.md`。外部仓库只有参考效力；其文档写明许可决定尚待发起人确认，因此**只独立写出本项目专属实施文字，不整体复制模板或宣布继承其许可**。

## 对照与决定

| HARC 提出的协作问题／机制 | 本项目原有基础及差距 | 本轮处理与边界 |
| --- | --- | --- |
| 换 AI、换对话后恢复当前工作 | `philosophy/`、`latest/`、`reports/`、`metadata/`、`index/`、`tracking/` 已在 GitHub；缺一份统一从零接管入口和当前阻碍清单 | **已实现轻量版** [`../START_HERE.md`](../START_HERE.md) + [`project-state.md`](project-state.md)，状态仅保存行动指针，不把报告全文复制成第二套真值源。 |
| 作者决定、AI 建议、外部来源区分 | [`../philosophy/intake-and-propagation.md`](../philosophy/intake-and-propagation.md) 已区分原意/编辑者建议，核心 v0.3 仍是意旨提炼草案 | **已补项目执行契约** [`../AGENTS.md`](../AGENTS.md)：人类明确决定、临时实现默认值和 AI 提案分开；外部仓库不是本项目规范性权威。无需平行造 `CONTENT_CORE`。 |
| 内容、呈现、协作协议分别路由 | 投资思想在 `philosophy/`；页面在 `site/`；执行规范在 `metadata/` 和 workflows，但缺一处 Agent 明示路由 | **已补 AGENTS 和启动入口**：内容偏好进既有思想收纳流程，形式改站点，平台/权限改部署流程；一项要求可有多个影响，但每个下游要验证。 |
| 最新 revision、写前校验与写后失效 | 已有每次写前确认 PUBLIC/push、读取 blob SHA 和不可变历史原则 | **保留并显式写入 AGENTS**；不另建 HARC manifest/YAML 并维护两份目录。若 SHA 改变重新读取，不覆盖并发更新。 |
| 框架批准与最终成果批准 | 本项目持续自动发布有日期的财经资讯，并非 HARC 的双语方法论论文；现行授权支持既定日／周／月例行发布 | **不移植逐篇人工双门槛**，避免阻断已授权自动任务；改变投资思想实质、付费模式、项目所有权、季度年度新发布制度等才另求明确决定；不宣称已批准的理念稿或证券判断。 |
| 双语 canonical/mirror、正式论文论证图及全套模板 | 本项目中文阅读为主，已建证据/模型/研究阶段结构，没有用户要求维护全量英文镜像或 HARC 论文体系 | **暂不采纳**；不引入 `HARC_MANIFEST.yaml`、`FORM_CORE`、论文批准快照或中英双份文件。若未来用户明确决定再评估成本和许可证。 |
| 校验与自测 | 现有哲学结构、研究选摘、网页与 Pages 构建 CI 能验证部分机械一致性，但不能验证预期差真实性 | **保留现有 CI**；新增入口、状态和协作约定必须有有效相互链接，人工在跨任务交接时审查状态是否过时。未来可以独立添加自动入口链接/状态检查，但在有真实测试运行前不能声称该项已自动覆盖。 |
| 版权与发布责任 | 公开仓库与免费静态网站已有 [`../metadata/publication-policy.md`](../metadata/publication-policy.md)；既有发布规范要求来源/隐私审查 | **延续现有边界**：公开可见不等于第三方内容可复制，生成网页不含某文件也不代表公开 Git 历史中不可见；HARC 来源只引用不搬运。 |

## 明确不修改的区域与理由

- `philosophy/core-beliefs.md`、`research-constitution.md`：外部协作协议不是所有者新增投资信念；现有实质原则不需要改写。
- `reports/**`、`latest/**`、`data/**`、`index/**`、`tracking/**`：本次没有新市场事实、价格或研究结论；旧正式报告保持不可变，最新摘要不因协作文件改动而重编。
- 日／周／月定时任务和网站展示：原执行要求未变；协作升级不增加强制审批步骤，不声称季度／年度已自动生成。Cloudflare 创建/域名授权仍须服务商实际回执。

## 验收方法与未完项

- **文档验收**：从 `START_HERE.md` 能导航到 `AGENTS.md`、`docs/project-state.md`、思想库和发布规则；状态页可区分已经核实／上次核实／未知／待人类确认。
- **运行验收**：未来每次高影响写入仍必须验证仓库身份及目标文件 revision，CI 与真实部署分别核对；结构检查通过不等于投资结论正确。任何新生成的年度/季度、Cloudflare 地址或 HARC 全套批准状态都不可凭本页声称存在。
- **待后续决定**：季度／年度研究具体实施、Cloudflare 正式网址、是否引入独立人类审核门以及许可方案均应在得到真实指示/回执后更新 [`project-state.md`](project-state.md)；无需因本次审查反复追问用户或虚构确认。
