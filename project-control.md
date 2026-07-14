# Project Control Board

- 项目：zf-wang-personal-site
- 类型：个人作品集 / 履历网站
- 站长：王子凡（ZF Wang）
- 当前模式：总控直做（未调用群内阶段 Bot）
- 源码：`/root/projects/zf-wang-personal-site`
- 仓库：`https://github.com/ZifanWang1996/wangzifan-personal-site`
- 分支：`main`
- 部署：GitHub Pages workflow
- Pages 预览：`https://zifanwang1996.github.io/wangzifan-personal-site/`
- 正式域名：`wangzifan.store`
- 最新提交：`eec6da6`（`feat: add concise resume overview`）
- 工作区：干净（截至 2026-07-12）

## 上线与域名状态（2026-07-12）

- GitHub Actions 最新 Pages 工作流 `29193206616`：**success**。
- GitHub Pages 已登记自定义域：`wangzifan.store`。
- HTTP `http://wangzifan.store/` 可访问站点内容。
- HTTPS 仍**未完成**：GitHub Pages API 显示 `https_enforced: false`；外部访问 `https://wangzifan.store/` 返回 `ERR_CERT_COMMON_NAME_INVALID`。
- 结论：GitHub Pages 预览 HTTPS 可用；正式域名当前仅能确认 HTTP 访问正常，不能对外称 HTTPS 已就绪。后续应等待/复查证书签发状态，不应重复改动已生效的 DNS。

## 网站信息架构与公开内容

1. **首屏定位**
   - 主业：项目经理。
   - 副业：AI 编程产品出海、OPC 探索者。
   - 英文辅助定位：`Project Management / AI Product Globalization / OPC Explorer`。

2. **01 / Projects & Works**（首个内容栏目）
   - `AIStoryNest` — `https://aistorynest.mom/` — 状态：已上线；卡片显示：`01· 已上线 / 睡前故事生成站`。
   - `Build a Hooper` — `https://buildahooper.best/` — 状态：已上线；篮球训练内容站。
   - `FalloutDay` — `https://falloutday.online/` — 状态：已上线；Fallout 76 攻略站。
   - `PalworldMap` — `https://palworldmap.best/` — 状态：已上线；Palworld 非官方地图与指南，提供已验证地点记录、地图图层、搜索与坐标点导航。
   - 四个外部链接均使用新窗口和 `noopener noreferrer`；“访问项目 ↗”为高对比度按钮 CTA。
   - 不展示本站 `wangzifan.store` 作为项目卡。

3. **02 / Resume**
   - 履历概览：角色「项目经理」、开始工作「2021」、教育背景「光学工程 · 硕士」。
   - 工作经历仅展示时间、公司、职位、部门：
     - `2024.06 — 至今`｜北京蓝天多维科技有限公司｜项目经理 · 技术部
     - `2021.07 — 2024.05`｜中电智能科技有限公司｜项目经理 · 产品总体部
     - `2021.07 — 2023.03`｜中电智能科技有限公司｜C++ 软件工程师 · 工业软件研发部
   - 不展示职责段落；已删除「快速信息」模块。

4. **03 / Credentials**
   - PMP、PRINCE2、NPDP、HCSA-PM、CSPM-4（高级）、系统集成项目管理工程师。

5. **04 / More / 联系方式**
   - 主题：AI 编程产品出海、OPC 探索、产品实践、快速原型、全球化用户。
   - 已公开联系方式：微信号 `wang1227928718`。

## 隐私与内容边界

- 不公开简历内的私人手机号、私人 QQ 邮箱、年龄、性别、详细住址或其他无必要个人信息。
- 原始简历与提取文本仅供本地核对，均由 `.gitignore` 排除，不得发布或提交。
- 公开联系渠道当前仅为用户明确授权的微信号。

## 维护方式

- 主页面：`index.html`（单文件静态站）。
- 自动部署：`.github/workflows/deploy-pages.yml`；推送到 `main` 后触发 GitHub Pages。
- 每次内容变更后至少执行：源码/隐私检查 → `git diff --check` → 提交推送 → 等待 Pages workflow 成功 → 同时复核预览 URL 与正式域名的 HTTP/HTTPS 状态。
- 任何涉及自定义域 HTTPS 的结论，都需以独立外部访问和 GitHub Pages 的 `https_enforced` 状态为准。
