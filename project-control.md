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
- 当前页面实现提交：`a31269f`（v3 奶油浅色主题）
- 已审查页面 tree：`07fe51abdca09d2518773948aca52e4e1203c4aa`

## Chinamaxxing Online 卡片 #30（2026-08-20）

- 新增卡片 #30：Chinamaxxing Online（`https://chinamaxxing.site/`），分类「创意实验」，标签「多语文化指南」，上线日期 2026-08-20。
- 筛选计数更新为：全部 30 / AI 3 / 游戏 10 / 工具 9 / 创意 8；Timeline 更新为 40 天、30 次真实上线，并新增 2026-08-20 节点；Changelog 更新为 30 entries / 30 releases。
- 缩略图来自生产站真实首屏，经 Playwright 抓取并转为 400×250 WebP（14,448 bytes）后 base64 内联；GitHub Pages workflow 白名单不变。
- 回归：pytest 30/30、Node 动态交互、确定性卡片检查均通过；1440×900、Android 390×844、Android 320×568 三视口通过，创意筛选 8 张、全部 30 张，无横向溢出、控制台错误、页面异常或同源失败请求。
- 390px 真实触摸 CTA 已验证到达 `https://chinamaxxing.site/`，页面标题为 `Chinamaxxing Online: Meaning, Quiz & Culture Guides`。

## v4 更新：筛选计数 + HLLV 卡片 #29（2026-08-19）

- 新增卡片 #29：HLLV Field Manual（hellletloosevietnam.blog，《Hell Let Loose: Vietnam》非官方野战手册），分类「游戏与内容」；上线日期 2026-08-17（按 Cloudflare Pages 首次 production 部署时间核实，08-16 仅为首个代码提交日）。
- 筛选按钮新增计数胶囊：`data-count` 属性经 CSS `::after` 渲染（全部 29 / AI 3 / 游戏 10 / 工具 9 / 创意 7），button.textContent 保持原样，live 状态栏契约与主脚本零改动。
- 「全部上线记录」subhead 新增 29 徽章；Timeline 标题 28→29，2026-08-17 变为 2 SHIPPED（牛来 + HLLV）；Changelog 28→29 entries，顶部新增 HLLV SHIP 记录。
- 缩略图：Playwright 实站抓取 → 400×250 WebP base64 内联（13KB），workflow 白名单不变。
- 回归：装配自检 38/38、pytest 27/27（新增 HLLV 卡片测试 + data-count 断言）、Node 交互测试通过；三视口（1440/390/320）零 JS 错误、零溢出、29 缩略图全加载。

## v3 换肤：奶油浅色编辑风（2026-08-19）

- 子凡反馈 v2 整体偏黑，选择「浅色奶油编辑风」方向。纯颜色层变换：`:root` 调色板翻转为暖白纸感底（`#f7f3e8`）+ 墨色文字（`#191510`），荧光绿保留作填充色、文字场景加深（`#5c6b12`）。
- 深色终端锚点保留：SHIPPING ENGINE、system-log、changelog、命令面板维持深色，形成「纸面 + 驾驶舱」双质感。
- 锁定内容零改动：74/74 自检、26/26 pytest、三视口验收全绿；线上字节一致 `1d7b67c4729ddccc`（382KB）。
- 目检修正两处对比度：contact-note 与 tl-count 加深一档。
- 已知事项：polskipilkarzsymulator.online 域名 DNS NXDOMAIN，缩略图为 NO SIGNAL 占位图；域名恢复后重跑 `scripts/shoot_thumbs.py` 中该条目即可替换。

## v2 升级：缩略图 + 时间轴 + 动效（2026-08-19）

- 本轮为发布证据强化与动效升级，不改变 28 项产品索引内容、信息架构与交互契约。
- 卡片升级：28 张真实站点截图（Playwright 实站抓取 → WebP 400×250 base64 内联，workflow 白名单不变）、LIVE 徽章、上线日期（git 历史 `-S` 首次出现提取）。
- 新增 `02 / Shipping Timeline` 时间轴：18 个上线日期、渐变轴线横向滚动；kicker 编号顺延（系统 03 / 宣言 04 / 合作 05）。
- 新增终端风格 `release.log`（28 条 SHIP 记录）于 OPC Operating System 区块。
- 动效层：缩略图 tilt+光泽扫过、scramble 标题解码、磁性 CTA、光标 glow（尊重 prefers-reduced-motion 与触屏降级）。
- 回归：装配自检 65/65、pytest 26/26、Node 交互测试通过；三视口浏览器验收（1440/390/320）零 JS 错误、零溢出、28 缩略图全加载。
- 线上字节一致性：SHA-256 `10c0fe676ff3f578…`（377KB），本地与 wangzifan.store 完全一致。
- 已知事项：polskipilkarzsymulator.online 域名 DNS NXDOMAIN，缩略图为 NO SIGNAL 占位图；域名恢复后重跑 `scripts/shoot_thumbs.py` 中该条目即可替换。

## 视觉系统重设计（2026-08-18）

- 本轮为全站视觉系统重设计，不改变信息架构、28 项产品索引与交互契约。
- 设计方向：编辑级排版（Archivo 可变字体 wght 100-900 / wdth 75-125% 子集内联）+ 暖米色"纸感"宣言区 + 火焰橙（`#ff4b1f`）强调色 + 颗粒噪点纹理 + 旋转徽章与跑马灯装饰。
- 锁定内容按字节保留：28 张卡片、5 个筛选按钮、命令面板、主内联脚本（filters/modal/copy/pointermove/year）。
- 页面 `index.html` SHA-256：`0c1caa102fc34292195b96a25d1aae0e28b266f5d61b783cf970e121f287137a`。
- 回归测试：`26 passed`；Node 动态交互测试通过。
- 真实浏览器验收（headless Chrome）：1440×900、390×844、320×568 三视口 `30/30` 全绿，无横向溢出、无控制台错误、无页面异常、Archivo 字体激活、筛选/命令面板/复制/reveal 动画全部通过。
- 视觉目检：首屏（桌面+移动）与发布台账区排版层次清晰、无溢出重叠；宣言区暖米色纸感反色和谐、有"高级感"，原则列表中文注释对比度已加深一档（`#5f5b52`）。
- 外部发布产物仅含 `index.html`、`favicon.svg`、`privacy.html`，三者均已按新视觉系统重做；privacy.html 保留全部隐私披露项（Plausible、不设置分析 Cookie、不进行跨站跟踪、GitHub Pages、微信号）。

## 本轮牛来发布状态（2026-08-17）

- 新增第 28 项 `牛来`，正式链接为 `https://niulai.blog/`，归入“创意实验”，标签为“牛来电影资料站”。
- 页面 `index.html` SHA-256：`53feb0928d4d7bb1c777543af96c5002c5e7e7c2f8bc5897b1e7ad759c97ab09`。
- 独立 exact-tree 复审：**PASS**；正式发布仅绑定 tree `07fe51abdca09d2518773948aca52e4e1203c4aa`，staged diff SHA-256 为 `6e95b7854a1f990c8c71c82ed99c3727dd2927dc6dd60636f4f258d15511ac33`。
- 回归测试：`26 passed`；Node 动态交互测试直接从正式页面提取 28 张 live 卡片，绑定 `牛来=creative`，验证 `AI 3 / game 9 / tool 9 / creative 7 / all 28`。
- 真实浏览器候选验收：1440×900、Android 390×844、Android 320×568 均通过；创意实验筛选显示 7 张，切回全部显示 28 张，无页面级横向溢出、控制台错误、页面异常或同源失败请求。
- Android 390×844 触摸上下文实点外链后正确打开 `https://niulai.blog/`，页面标题为“牛来 (2026) 电影：342元逆袭150万的暑期档传奇 | Niu Lai Movie”。
- 外部发布产物仅含 `index.html`、`favicon.svg`、`privacy.html`；排序清单 SHA-256 为 `d03c5dfe531a2c2cf587d92db9723445f7596ff17c38406a9c0332c3b879c7ca`。

## 发布前生产基线（2026-08-17）

- 使用 `https://wangzifan.store/?predeploy=07fe51ab` 完成生产 RED 校准：HTTP 200、27 张 live 卡片、编号 `01..27` 连续、`niulai.blog` 出现 0 次。
- 发布前生产 `index.html` SHA-256：`86d49c0d2aae7e7bbced5e8bfcb9dc492e57df1d41ff1ec839aae819983893a9`；该旧版本基线用于判别本轮 GitHub Pages 更新是否真实生效。

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

## 产品索引（30）

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
| 27 | CraveLoop | 创意实验 | https://foodnevercomes.online/ |
| 28 | 牛来 | 创意实验 | https://niulai.blog/ |
| 29 | HLLV Field Manual | 游戏与内容 | https://hellletloosevietnam.blog/ |
| 30 | Chinamaxxing Online | 创意实验 | https://chinamaxxing.site/ |

## 发布产物边界

- workflow 先创建全新的 `_site` 目录。
- 仅复制 `index.html`、`favicon.svg` 与 `privacy.html`。
- `upload-pages-artifact` 的路径固定为 `_site`，不得改回仓库根目录。
- 测试、控制文档、Git 元数据及本地资料不得进入 Pages artifact。
- 页面仅加载已批准的 Plausible 统计脚本，隐私页已披露；30 个项目外链均使用新窗口及 `noopener noreferrer`。

## 候选浏览器验收

- 真实 CSS 视口 `1440×900`、`390×844`、`320×568` 均无页面级横向溢出。
- 320px 首屏主、次 CTA 完整可见；`HowManySleepsUntil` 在极窄宽度完整显示。
- 全部记录、AI 产品与创意实验筛选分别显示 30 / 3 / 8 条，类别标签和 `aria-pressed` 同步；Chinamaxxing Online 卡片在“创意实验”下唯一且可见，页面不展示数字成绩板。
- 320px 筛选器保持双列三行并保有 44px 最小触控高度；Chinamaxxing Online 卡片正文、元数据和 CTA 完整位于容器内，CTA 高度不低于 44px。
- 命令面板支持点击与 `Ctrl+K`；打开后聚焦第一目的地，正反向 Tab 循环与 Escape 焦点恢复均通过；初始焦点为 `BODY` 或原焦点节点已断开/隐藏时，关闭后回退到可见的命令按钮。
- 微信复制具有 Clipboard API、`execCommand` 和明文提示三层路径；`execCommand` 返回 `false` 或抛异常时均保证清理临时 textarea 并显示明文。
- 仓库内 `tests/browser_interactions.mjs` 从 `index.html` 提取全部 30 张 live 卡片后动态执行页面真实脚本，覆盖五种筛选、`HLLV Field Manual=game` 与 `Chinamaxxing Online=creative` 分类绑定、命令面板状态、焦点恢复、正反向 Tab 与四种复制结果，避免测试数据与页面脱节。
- favicon 返回 200；候选验收中的控制台错误、页面异常及同源失败请求均为 0；390px 触摸 Chinamaxxing Online CTA 打开 `https://chinamaxxing.site/`。

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
