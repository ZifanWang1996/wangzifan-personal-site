# Project Control Board

- 项目：`zf-wang-personal-site`
- 类型：OPC 创业者个人主页 / 全球产品发布索引
- 站长：王子凡（ZF Wang）
- 当前模式：总控直做（未调用群内阶段 Bot）
- 源码：本仓库
- 公开仓库：`https://github.com/ZifanWang1996/wangzifan-personal-site`
- 默认分支：`main`
- 部署：GitHub Pages workflow
- 正式域名：`https://wangzifan.store/`
- 当前发布提交：`283799bde2540856d785d14653882ba7eca9d08c`
- 已审查 tree：`5f8da9244e774bd14371a0bf6f1188fb3d1bceab`

## 发布状态（2026-08-16）

- 独立 exact-tree 审查：**PASS**。
- GitHub Actions Pages run `31927459835`：**success**。
- Pages 配置：`build_type: workflow`、`cname: wangzifan.store`、`https_enforced: true`。
- TLS：Let's Encrypt 证书有效，SAN 包含 `wangzifan.store`。
- HTTP 已验证自动跳转至 HTTPS。
- 生产 `index.html` SHA-256：`9668d1a5e5b1a5640bd3368a040a4130d80ed966b504be8a695633d24a909be4`，与已审查文件逐字节一致。
- 生产 `favicon.svg` SHA-256：`88c7718f853c633d012afbb79ebc08bfd89294f49babc26add6831b719e6abed`，与已审查文件逐字节一致。

## 公开定位与信息架构

1. **Hero / OPC 定位**
   - 核心标题：`一个人，也能把产品推向全球。`
   - 公开身份：面向全球用户持续构建、上线和迭代产品的 OPC 创业者。
   - 方法论：用 AI 放大单人产能，用真实反馈决定下一步。

2. **成果证据**
   - 26 个已上线产品。
   - 6 项专业证书。
   - 自 2026 年开始持续构建。
   - 运行循环：判断 → 构建 → 上线 → 反馈。

3. **Selected Deployments**
   - 六个重点产品：RSP Editor、AI Scanner、AIStoryNest、PalworldMap、Chinese Coins Atlas、MatchaFilter。
   - 完整产品索引支持五个筛选状态：全部 26、AI 产品 3、游戏与内容 9、实用工具 9、创意实验 5。

4. **OPC Operating System**
   - 判断：从搜索需求、社区信号和真实痛点中筛选机会。
   - 构建：把需求压缩为最短可验证路径，以 AI 放大单人产能。
   - 上线：先交付真实可用版本，再补齐可靠性、隐私与增长基础。
   - 反馈：以用户行为、搜索数据和运营结果决定下一轮迭代。

5. **Founder Manifesto**
   - Think clearly.
   - Build small.
   - Ship real.
   - Compound fast.

6. **Collaboration**
   - 交流方向：OPC 创业、AI 产品、出海增长、网站工具与联合实验。
   - 公开联系渠道：微信号 `wang1227928718`。

## 产品索引（26）

| # | 产品 | 分类 | 地址 |
|---:|---|---|---|
| 01 | AIStoryNest | AI 产品 | https://aistorynest.mom/ |
| 02 | Build a Hooper | 游戏与内容 | https://buildahooper.best/ |
| 03 | FalloutDay | 游戏与内容 | https://falloutday.online/ |
| 04 | PalworldMap | 游戏与内容 | https://palworldmap.best/ |
| 05 | CodexSkin.space | 实用工具 | https://codexskin.space/ |
| 06 | llmstxt | 实用工具 | https://llmstxt.best/ |
| 07 | All Wishes Come True | 创意实验 | https://allwishescometrue.site/ |
| 08 | TaskbarHeroWiki | 游戏与内容 | https://taskbarherowiki.best/ |
| 09 | Chinese Coins Atlas | 创意实验 | https://chinesecashcoins.wiki/ |
| 10 | Rot Check | 创意实验 | https://rotcheck.cyou/ |
| 11 | SpiritVale Wiki | 游戏与内容 | https://spiritvale.blog/ |
| 12 | DragonSword Wiki | 游戏与内容 | https://dragonswordawakening.fun/ |
| 13 | CopyPlaintext | 实用工具 | https://copyplaintext.com/ |
| 14 | IsItDown | 实用工具 | https://isitdown.click/ |
| 15 | HowManySleepsUntil | 实用工具 | https://howmanysleepsuntil.rest/ |
| 16 | Cash Flow Lifestyle | 创意实验 | https://cashflow.lifestyle/ |
| 17 | 竹知了 | 实用工具 | https://zhuzhiliao.buzz/ |
| 18 | Shift at Midnight Guide | 游戏与内容 | https://shiftatmidnight.blog/ |
| 19 | Merge a Nuke! Guide | 游戏与内容 | https://mergeanuke.space/ |
| 20 | AI Scanner | AI 产品 | https://aiscanner.run/ |
| 21 | RSP Editor | AI 产品 | https://rspeditor.app/ |
| 22 | Remove Matcha Filter | 实用工具 | https://remove-matcha-filter.com/ |
| 23 | DSH Field Guide | 实用工具 | https://deepseekharness.site/ |
| 24 | Polski Piłkarz Simulator | 游戏与内容 | https://polskipilkarzsymulator.online/ |
| 25 | burnt for you | 创意实验 | https://burncd.xyz/ |
| 26 | MatchaFilter | 实用工具 | https://matchafilter.cc/ |

## 发布产物边界

- workflow 先创建全新的 `_site` 目录。
- 仅复制 `index.html` 与 `favicon.svg`。
- `upload-pages-artifact` 的路径固定为 `_site`，不得改回仓库根目录。
- 测试、控制文档、Git 元数据及本地资料不得进入 Pages artifact。
- 页面不加载第三方脚本；26 个外部链接均使用新窗口及 `noopener noreferrer`。

## 浏览器验收

- 桌面 1440px、移动 390px、极窄 320px 均无页面级横向溢出。
- `HowManySleepsUntil` 在极窄宽度按语义断点显示完整。
- 筛选计数为 `26 / 3 / 9 / 9 / 5`，显示计数和 `aria-pressed` 同步。
- 命令面板支持点击与 `Ctrl+K`，Escape 关闭后恢复触发按钮焦点。
- 微信复制具有 Clipboard API、`execCommand` 和明文提示三层路径。
- 首次加载 favicon 返回 200；生产控制台无 JavaScript 错误。

## 隐私与内容边界

- 不公开私人手机号、私人邮箱、年龄、性别、详细住址或其他无必要个人信息。
- 原始个人资料及提取文本仅供本地核对，由 `.gitignore` 排除，不得发布或提交。
- 当前唯一公开联系渠道为用户明确授权的微信号。

## 维护方式

- 页面：`index.html`。
- 图标：`favicon.svg`。
- 自动部署：`.github/workflows/deploy-pages.yml`；推送到 `main` 后触发 GitHub Pages。
- 每次内容变更至少执行：内容与隐私检查 → 全量测试 → 真实浏览器响应式验收 → exact-tree 独立审查 → 提交推送 → Pages workflow 验证 → 生产 HTTPS 与字节哈希复核。
- 自定义域结论必须同时依据 GitHub Pages API、有效 TLS 证书和独立安全访问结果。
