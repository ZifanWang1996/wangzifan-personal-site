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

## 本地候选状态（未授权上线）

- 候选方向：**Launch Ledger / 持续发布引擎**。
- 候选 `index.html` SHA-256：`f7ca5ba489b9b014d9e8346450b03745a915cd2d189c864c6cc12504dc6c8e95`。
- 本地 Pages 白名单产物仅含 `index.html` 与 `favicon.svg`，页面源文件与产物逐字节一致。
- 回归测试：`21 passed`；其中仓库内 Node 动态交互测试执行真实页面脚本，覆盖五种筛选、命令面板状态/焦点及四种复制结果，并验证初始 `BODY`、普通可聚焦元素、点击触发器三类焦点恢复。
- 真实浏览器候选验收：1440×900、390×844、320×568 均通过；`BODY → Ctrl+K → Escape` 稳定回退到命令按钮，原焦点元素被移除时同样安全回退；强制 Clipboard API 与 `execCommand` 同时抛异常时仍显示明文并清理临时节点；尚未提交、推送或部署。
- 本轮 independent exact-tree 审查结果记录于交接报告，不在审查后反写候选树。

## 当前生产状态（2026-08-16）

- 独立 exact-tree 审查：**PASS**。
- GitHub Actions Pages run `31927459835`：**success**。
- Pages 配置：`build_type: workflow`、`cname: wangzifan.store`、`https_enforced: true`。
- TLS：Let's Encrypt 证书有效，SAN 包含 `wangzifan.store`。
- HTTP 已验证自动跳转至 HTTPS。
- 生产 `index.html` SHA-256：`9668d1a5e5b1a5640bd3368a040a4130d80ed966b504be8a695633d24a909be4`，与上一轮已审查文件逐字节一致。
- 生产 `favicon.svg` SHA-256：`88c7718f853c633d012afbb79ebc08bfd89294f49babc26add6831b719e6abed`。

## 候选公开定位与信息架构

1. **Hero / Shipping Engine**
   - 核心标题：`先把想法做出来，再让世界给答案。`
   - 公开身份：面向真实用户持续构建、上线和迭代产品的 OPC 创业者。
   - 视觉叙事：`SHIP REAL.` 持续发布引擎；首屏不再陈列产品数、证书数或精选成绩板。

2. **Launch Ledger**
   - 核心标题：`把想法做成网址，把网址做成复利。`
   - 完整产品索引中的全部记录等权展示，不再重复设置重点精选区。
   - 支持五个语义筛选状态：全部、AI 产品、游戏与内容、实用工具、创意实验；按钮标签不显示计数。

3. **OPC Operating System**
   - 判断：别追逐所有机会，找到真实需求，选中那个值得立刻动手的问题。
   - 构建：压缩范围，用 AI 把想法尽快变成可用产品。
   - 上线：把真实版本交给用户，让产品接受世界的检验。
   - 反馈：让行为、搜索和运营结果推动下一轮更快出发。

4. **Founder Manifesto**
   - See the signal.
   - Make the move.
   - Ship the truth.
   - Earn momentum.
   - 核心口号：`没有完美时机。上线就是时机。`

5. **Collaboration**
   - 核心标题：`下一件值得上线的事，现在就开始。`
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

## 候选浏览器验收

- 真实 CSS 视口 `1440×900`、`390×844`、`320×568` 均无页面级横向溢出。
- 320px 首屏主、次 CTA 完整可见；`HowManySleepsUntil` 在极窄宽度完整显示。
- 全部记录与 AI 产品筛选分别显示 26 / 3 条，类别标签和 `aria-pressed` 同步；页面不展示数字成绩板。
- 320px 筛选器保持双列三行并保有 44px 最小触控高度。
- 命令面板支持点击与 `Ctrl+K`；打开后聚焦第一目的地，正反向 Tab 循环与 Escape 焦点恢复均通过；初始焦点为 `BODY` 或原焦点节点已断开/隐藏时，关闭后回退到可见的命令按钮。
- 微信复制具有 Clipboard API、`execCommand` 和明文提示三层路径；`execCommand` 返回 `false` 或抛异常时均保证清理临时 textarea 并显示明文。
- 仓库内 `tests/browser_interactions.mjs` 动态执行页面真实脚本，覆盖五种筛选、命令面板状态、初始 `BODY`/普通元素/点击触发器焦点恢复、正反向 Tab 与四种复制结果，避免只靠源码字符串断言。
- favicon 返回 200；候选控制台、页面异常、失败请求及第三方请求均为 0。

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
