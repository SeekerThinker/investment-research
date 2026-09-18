# Cloudflare Pages 免费托管接入说明

**状态：仓库构建入口已准备；Cloudflare 账户尚未授权、Pages 项目尚未创建，不能把示例地址当成已上线站点。** GitHub 仓库 `SeekerThinker/investment-research` 继续是代码、思想库与历史研报的唯一资料来源。GitHub Pages 保留为可用的旧站及回退渠道，直到新的 Cloudflare 网址真实部署并核验成功；不复制、重写历史报告或开通付费阅读。

## Cloudflare 控制台需要完成的首次授权

在 Cloudflare 的 [Workers & Pages](https://dash.cloudflare.com/) 中登录自己的账户，创建 **Pages** 应用，选择 **Import an existing Git repository / Connect to Git**，在 GitHub 授权界面仅允许访问 `SeekerThinker/investment-research`（若 GitHub App 已安装则授权该仓库）。请勿在聊天、仓库、工作流或第三方表单中提供账户密码、Cloudflare API Token 或其他凭据。必须在 Cloudflare 后台完成登录和 GitHub 授权；项目名称是否可用，以控制台实际创建结果为准。

| Cloudflare Pages 配置 | 项目实际填写值 |
| --- | --- |
| Git provider / repository | GitHub / `SeekerThinker/investment-research` |
| Project name | 首选 `investment-research`，占用则选择另一个简短、不包含账户名的可用项目名 |
| Production branch | `main` |
| Framework preset | `None` / 无框架 |
| Root directory | 仓库根目录（留空或 `/`，不要填 `site`） |
| Build command | `bash monitor/build_cloudflare_pages.sh` |
| Build output directory | `_site` |
| Python | 构建脚本只使用 Python 标准库；如果平台使用旧镜像，可在环境变量中设置 `PYTHON_VERSION=3.12` |
| Plan | Free（不升级付费方案） |

此仓库 `site/` 是**网页模板**，并非最终可部署目录；完整日报／周报／月报和历史归档、盘中报告以及精选 JSON 均通过构建命令生成至仓库根目录的 `_site/`。**不可**直接部署仓库根目录、`site/`、`reports/` 或包含 `tracking/`、`index/` 的工作目录。构建脚本先验证思想库和日报两类内容，再用已有 Python 建站工具生成、补录盘中报告与精选日报；最后核验周报/月报、全文免费可读、页面资产完整以及不泄漏内部工作数据。脚本任一步出错会非零退出并阻止发布。

## 首次发布验收与回退

1. 在 Cloudflare 控制台确认生产部署状态为 **Success**，以平台实际分配的 `*.pages.dev` 地址为准；示例 `investment-research.pages.dev` **未核实可用性，不可先对外宣传**。
2. 访问新网站根路径，应有“投资机遇 / 风险规避 / 周报观察 / 月度视角”四个首页板块；打开日报详情、周报全文、月报全文、历史报告和投资思想库导航，确认正文与免费可读状态。打开 `content/index.json` 检查 `editorial.focus_counts` 之和与日报条目数一致，日报不超过12条。
3. 对照同时期旧 GitHub Pages 的报告版本、日期和详情链接；确保新站没有误用过时、预览分支或半成品报告。完成以后再决定是否将项目正式对外链接指向 Cloudflare；现有 GitHub Pages 可以继续提供备用入口。
4. 遇到 Cloudflare 构建失败、资源404、遗漏周报/月报、缓存过旧或错误公开内部文件，**先不切换正式网址**。查看 Cloudflare 构建日志和 GitHub 的独立 Cloudflare build-check 工作流，修复并再次验证；旧站保持不变。

Cloudflare 官方文档：[Git 集成](https://developers.cloudflare.com/pages/get-started/git-integration/)、[构建配置](https://developers.cloudflare.com/pages/configuration/build-configuration/)、[静态站点部署](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/)。Git 集成会在仓库更新后自动构建，构建产物的根页面为 `_site/index.html`。首次连接 GitHub 需要账户所有者授权；只改仓库文件不能替代 Cloudflare 端的项目创建。