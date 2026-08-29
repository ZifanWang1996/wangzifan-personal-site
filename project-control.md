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
- 当前生产页面实现提交：`0b8411ab5e1f1b8fdab44d437141a545aff5d388`（PR #5 squash merge）
- V11.1 页面实现基线 tree：`1dc85c8c56411d426cfcdd739d6c752a667a466c`；公开 artifact SHA-256：`787edd3dff833bb810111808bd3184810cfed6ba554ff5e1497811f48c209b87`

## V11.1 生产版：个人产品工作台（2026-08-29）

- **状态**：冻结候选 commit `4f511a45428ef0da56083994be098b73bd3416cf` 通过 PR #5 squash merge 为页面实现 commit `0b8411ab5e1f1b8fdab44d437141a545aff5d388`；两者 tree 均为 `1dc85c8c56411d426cfcdd739d6c752a667a466c`。GitHub Pages production run `33257007906` 已成功部署，deployment ID 为 `6156571565`。
- **授权边界**：用户于 2026-08-29 明确回复“全流程上线”；本次授权已用于 V11.1 的提交、推送、PR #5 合并与生产部署，后续新改动仍需重新验收和授权。未修改 DNS。
- **身份与首屏**：改为第一人称“你好，我是王子凡 / 我做小而完整的互联网产品”；右侧展示按上线时间排序的真实工作台状态，不再使用抽象工作室说明或重复项目截图。
- **内容结构**：保留最近三次上线与 33 条完整档案；代表案例由 6 个同构卡缩为 AI Scanner、Remove Matcha Filter、Chinese Coins Atlas 三个差异叙事；四步标准方法改为三条具体工作习惯；“在线/离线”明确为档案记录而非实时探测承诺。
- **视觉系统**：保留米白、墨黑、暗红、藏蓝；移除无信息量的英文章节编号、四等分数字墙、六宫格案例与整屏红色 CTA；最近卡按内容自然收口，案例桌面交替布局，工作习惯采用收敛的轻错层。三个重点案例重新从真实站点采集截图，先使用各站公开的拒绝/无 Cookie 统计选项，避免 Consent 弹层遮住核心界面；320px 首屏标题与 390/320px 重点案例标题均按语义行收口，不留中文孤字。
- **候选证据**：exact public artifact 为 41 文件，SHA-256 `787edd3dff833bb810111808bd3184810cfed6ba554ff5e1497811f48c209b87`；`pytest` 23/23、Node 筛选/零结果/展开/复制降级通过，构建漂移为 0。
- **PR 与生产证据**：PR run `33256850827` 的 quality 成功、deploy 跳过；production run `33257007906` 的 quality 与 deploy 均成功，两次 run 的 annotation 均为 0。两次 CI evidence 都绑定 41 文件、同一 artifact SHA-256、8 个视口和 0 failures。
- **正式域验收**：`https://wangzifan.store/`、隐私页、CSS、JS、OG 图及三张重点案例图与冻结 artifact 逐字节一致。正式域 Chromium 在 1440、1024、768、390、320、759/760/761 共 8 个视口均为 0 overflow、0 owner crossing、0 console/network failure；7 张页面图片均解码。无 JavaScript 时 3 个重点案例与 33 条档案仍完整可读；正常/减弱动画均无持续帧变化。
- **域名状态**：HTTP apex 单次 301 到 HTTPS；canonical 与 `og:url` 均为 `https://wangzifan.store/`。`www.wangzifan.store` 仍无 DNS 记录，属于非阻断后续项，不表述为已完成。
- **证据位置**：GitHub Actions artifacts `v11-browser-evidence-33256850827` 与 `v11-browser-evidence-33257007906`（按 workflow 保留期保存）；候选与 QA 临时目录由 `.gitignore` 排除，不进入提交或 Pages artifact。

## V11 生产版：一人产品档案（2026-08-27）

- **状态**：已通过 PR #1 合并 `main` 并由 GitHub Pages workflow run `33094322395` 部署；quality 与 deploy 均成功，annotation 为 0。
- **架构**：`data/projects.json` 是 33 条发布记录、32 live / 1 offline、最近发布、代表案例、完整档案、JSON-LD 和 OG 图计数的单一数据源；`scripts/build_v11.py` 生成首页、隐私页和共享资产。
- **信息架构**：唯一身份为 `ZF WANG / ONE-PERSON PRODUCT STUDIO`，首页顺序为身份 → 最近发布 → 代表案例 → 合作入口 → 方法 → 完整档案 → 关于 → 联系；默认档案交互态展示 9 条，无 JS 时 33 条全部可读。
- **渐进增强**：筛选/搜索/展开与复制控件默认原生 `hidden`，仅在各自 DOM 完整并完成事件绑定后显示；JS 失败时不出现假按钮。
- **公开边界**：`scripts/prepare_public_artifact.py` 从全新目录生成 strict allowlist，拒绝 symlink；公开文件仅含两页 HTML、favicon、共享 CSS/JS/字体/OG/微信二维码和 33 张编号项目 WebP，不含源码、测试、数据、控制文档或 `.hermes/`。
- **发布闸门**：PR 与 main 都运行确定性构建漂移检查、pytest、Node 交互、Python compile、八宽度 Chromium、no-JS/reduced-motion/键盘/隐私 skip-link 和 exact artifact 验收；只有 `push main` 全绿后才有 deploy 权限。
- **发布授权**：子凡于 2026-08-27 明确回复“可以上线”；本次授权已用于 PR #1 合并与生产部署，后续新改动需重新验收和授权。
- **生产证据**：exact public artifact 为 41 文件；线上首页、隐私页、CSS、JS 和 OG 图逐字节 SHA 与冻结 artifact 一致；桌面/手机/no-JS 真实域浏览器验收全绿，10/10 懒加载图片在正常滚动下完成。只读本地副本位于 `/root/local-previews/wangzifan-store/v11-cf62d271/`。
- **域名状态**：`http://wangzifan.store/` 301 到 HTTPS apex；`www.wangzifan.store` 当前无 DNS 记录，作为非阻断后续配置项，不表述为已完成。
- **历史版本**：下方 v9、v8、v6 等段落仅为生产演进记录；对应旧装配和旧验收脚本已在 V11 清理，不是当前运行入口。

## v9 改版：设计 token 统一 + 移动健康（2026-08-25）

方案 A（子凡选定并确认）：不换 v8 骨架，纯做协调统一——圆角/色系/字重/间距 token 化，消除 v2→v8 叠加残留。

- **圆角收敛**：15 种半径 → 4 档（`--r-none` 0 / `--r-std` 3px / `--r-soft` 8px / `--r-pill` ∞）；所有卡片/按钮/表单统一引用 token。
- **色系统一**：残留旧色（v6 深空 `#0e7f9d`、v6 火焰 `#e8401a`、v5 石灰绿 `#c6ff3f`/`#6b8f00`）全部映射到 v8 信号橙/琥珀板（`--db-or` `#ff4d00` / `--db-amber` `#f5b800`）；新增 `--lime:var(--db-amber)` 兼容旧引用，消除同屏 4 套色相打架。
- **字重梯度**：Archivo 补 900 字重（大屏 H1），形成 900/800/500/400 四档；新增 `--sec-breath` section 呼吸间距（120px/80px 节拍）替代随手值（60/88/90/94）。
- **QR 修复**：`.qr-card` 从固定 `max-width:212px` 改为 `min(212px,100%)`，修复 320px 视口下被 `.contact-card` `overflow:hidden` 裁切的问题（实证：212px 卡进 198px 容器溢出 14px）。
- **实现**：纯 CSS/JS 皮肤层改动，DOM 锚点/33 卡/交互/workflow 零改动；`scripts/assemble_v9.py` 装配（原子性 + 自检）。
- **验证**：pytest 44/44 ✅（新增 `test_v9_design_token_unification` 4 断言）；`accept_v5.py` 三视口（1440/390/320）全 PASS（h1 weight 900、QR `fits:true`、零横向溢出、零 JS 错误）；生产实测 QR 192px 完整装入 212px 卡内。
- 生产发布：commit `0f95b60`，生产验证 `wangzifan.store` HTTP 200 + 三视口实测全绿。
- 子凡反馈确认：发布后子凡主动说"二维码在手机端显示不全"→ 定位修复 → 又说"几个页面感觉还能升级一版，整体协调性不足"→ 触发本方案 A。

## 微信二维码 + OPC 宣言金句（2026-08-25）

- Contact 区挂上个人微信二维码：源图为子凡提供的薄荷绿微信码（800×757），经 `zxing-cpp` 解码核验指向微信快加快链 `https://u.wechat.com/MHBiZ7OETdLY6mE--lrPphA?s=0`；裁出码区并加 10% quiet zone 后 Lanczos 缩为 560×560，另存 `assets/wechat-qr.webp`（34,694 bytes，SHA-256 `d303243aad00d65cb8ca045194a317b48f2573d1899ddb5617e3b2a0669eedfa`），缩放后二次解码仍通过。
- 二维码以 `<figure class="qr-card">` 挂入 `.contact-side`（微信号与复制按钮之上），`loading="lazy" decoding="async" width/height=560`，alt 含微信号 `wang1227928718`；配色沿用站点的米白卡底 + 薄荷绿码面。
- Pages artifact allowlist 新增 `install -m 0644 assets/wechat-qr.webp _site/assets/wechat-qr.webp`；公开 artifact 构成由 37 文件（33 图）变为 38 文件。历史 manifest 哈希记录（`a6048999…`，32 图时代）保留为历史事实，不做回溯改写。
- 三条跑马灯各新增 3 条 OPC 宣言金句（中/英混排，每条跑马灯的两个对称 set 同步更新）：
  - 橙色主带：一个人就是一支完整的船队 / ONE PERSON · FULL CREW · ZERO EXCUSES / 今天的上线胜过明天的计划
  - ghost 带：速度即诚意 · 交付即答案 / NO COMMITTEE · NO CONSENSUS · JUST SHIP / 每一次上线都在留下航迹
  - 尾部带：不等万事俱备 · 上线造东风 / SPEED IS THE STRATEGY / 单人不成军 · 但全世界都是甲板
- 测试：新增 `test_wechat_qr_is_publishable_and_allowlisted`（资产存在、<80KB、img 属性、CSS、workflow 行），全套 43 passed；`accept_v5.py` 每视口新增 `wechat qr rendered` 断言（complete + naturalWidth + 渲染宽度 >100px）。
- 验证：三视口浏览器验收全 PASS；1440px 实截图目检二维码清晰、无变形、无文字溢出。

## Mortal Shell II Wiki 卡片 #33（2026-08-25）

- 新增卡片 #33：Mortal Shell II Wiki（`https://mortalshell2.quest/`），分类「游戏与内容」，标签「MS2 粉丝维基」，上线日期 2026-08-25；文案依据正式站 title、H1 与公开页面内容现场核验。
- 筛选计数目标：全部 33 / AI 3 / 游戏 12 / 工具 10 / 创意 8；Timeline 更新为 45 天、33 次真实上线并新增 2026-08-25 节点；Changelog 更新为 33 entries / 33 releases；遥测流首位换为 Mortal Shell II Wiki，矩阵扩为 33 格（#32 = Mortal Shell II Wiki，最右）。
- `project-33.webp` 为 1440×900 正式站真实首屏，Lanczos 无裁切缩至 400×250 WebP；8,322 bytes，SHA-256 `ef268450a5098096f5a522e31d90524d103dc12a05182e9e4030f7b69d3edaa2`。
- Pages artifact allowlist 精确更新为 33 张 WebP。
- OxAlpha 卡片从 ★ 最新上线 降级为 NEW；NEW 徽章按构建日期 2026-08-25 的 7 天窗口重算（本轮 4 张：Mortal Shell II Wiki、OxAlpha、The Sinking City 2 Field Guide、Chinamaxxing Online）。
- 验证：`accept_v5.py` 断言目标同步切换为 Mortal Shell II Wiki（首卡/元数据/描述证据/游戏筛选探针/390px 真实 touch）。

## v8 改版：DEPARTURE BOARD 出发大屏皮肤（2026-08-24）

方案 D（子凡选定并确认）：全站从 v7 报纸编辑风切换为「一人航运公司出发大屏」。

- **隐喻**：单人航运公司（WZF LINES · ONE-PERSON FREIGHT）——每个产品是一班已起飞的航班，域名是目的地；42 天 32 次发布的节奏本身就是品牌。
- **色板**：米色场 `#f5f1e6` + 黑板墨色 `#121212` + 信号橙 `#ff4d00` + 琥珀 `#f5b800` + 板绿 `#0e7c3d`；方角、2-3px 墨线、硬偏移阴影、等宽字主导、零衬线（与 v7 完全断开）。
- **实现**：纯 CSS 皮肤 `scripts/_v8.css`（155 规则），原子替换 v7 GAZETTE 块（8389→12053 字符）；DOM 锚点、内联脚本、workflow 零改动。`scripts/assemble_v8.py` 装配（原子性 + 19 项自检）。
- **Hero**：v6 发射控制台重蒙皮为琥珀色系出发大屏（T-MINUS、遥测流、32 格状态矩阵全部保留功能）。
- **解锁文案**：顶条改为 `WZF LINES · 一人航运 · ONE-PERSON FREIGHT` / `32 SHIPS LIVE · EVERY RELEASE IS A DEPARTURE`；theme-color `#f5f1e6`。
- **验证**：pytest 42/42 ✅、Node 动态交互 ✅、`accept_v8.py` 三视口（1440/390/320）全 PASS（零溢出、零 JS 错误、米色底生效）；桌面程序化 QA 0 裁切 0 对比度问题。
- 生产发布：commit `cbdff37`，GitHub Actions run `32662793075`。

## v6 改版：Launch Console 发射指挥舱 hero（2026-08-22）

方案 A（子凡选定并确认）：hero 从"编辑宣言"升级为"实时发射控制台"。

- **深空仪表色板**：深墨底 `#0b0d09` + 电青 `#0e7f9d` / 火焰橙 `#e8401a` 径向光晕 + 青柠信号光 `#c6ff3f`；正文区保留暖纸编辑感，hero 下方用 `.launch-bridge` 渐变桥过渡。
- **Canvas 星场轨道**：`orbit-canvas` 画星点 + 32 个轨道光点（每个代表一次发布），鼠标视差 + 光标引力弯曲轨道；`prefers-reduced-motion` 下静止。
- **T- 倒计时**：`#tminus` 按真实发布节奏（1.3 天/船）从最新发布日期推算下次发射 ETA，秒级跳动。
- **遥测流**：最新 5 条 SHIP 日志逐行浮入（日期/SHIP/项目名）。
- **32 状态矩阵**：16×2 像素阵（最老在左 #1，最新在右 #32），hover tooltip 显项目名+日期，点击平滑滚动到对应卡片并高亮。
- **零 DOM 锚点破坏**：32 卡、filter chips、timeline、changelog、32 条 visit 链接全部原样。
- 构建：`scripts/assemble_v6.py`（原子性，CSS/JS 片段来自 `scripts/_v6.css`/`_v6.js`，JS 注入前 `node --check`）。
- 验证：pytest 42/42（新增 `test_v6_launch_console_hero_contract`）、Node 交互、accept_v6 三视口（1440/390/320）全 PASS。
- 旧 hero 文案 `SHIPPING ENGINE` 演进为 `LAUNCH CONSOLE`（IA 测试同步更新）。

## OxAlpha 卡片 #32（2026-08-22）

- 新增卡片 #32：OxAlpha（`https://oxalpha.site/`），分类「实用工具」，标签「AI 模型证据站」，上线日期 2026-08-22；文案依据正式站 title、H1、description 与公开能力现场核验。
- 筛选计数目标：全部 32 / AI 3 / 游戏 11 / 工具 10 / 创意 8；Timeline 更新为 42 天、32 次真实上线并新增 2026-08-22 节点；Changelog 更新为 32 entries / 32 releases。
- `project-32.webp` 来自 Chrome 147 的 1440×900 正式站拒绝分析态真实首屏，经 Lanczos 无裁切缩至 400×250 WebP；11,178 bytes，SHA-256 `d850fc9eb00ab13996f37c448f8b284eb553e162029b75f4b61f960776189f19`。
- Pages artifact allowlist 精确更新为 32 张 WebP；源码、测试、控制文档仍不得进入公开 artifact。
- 本地回归：pytest 41/41、Node 动态交互、Python syntax、`git diff --check` 全绿；exact artifact 为 36 个文件（32 图）。公开 artifact 使用 sha256sum-compatible manifest（每行 `<file_sha256>  <relative_path>\n`，relative path 按字典序），manifest SHA-256 `a6048999cf0d613d7702585f762686a7e6cbe9413c22291ace8e1e33b552a893`；`accept_v5.py` 从自身 checkout 启动本地 HTTP，可在 immutable snapshot 内验收 exact tree。
- Pages workflow 在 artifact upload/deploy 前强制运行 pytest、Node 动态交互与 Python syntax；将 `index.html` 置空的 mutation 使 pytest 返回 1，部署在 upload 前被阻断。Timeline H2 使用 `aria-hidden` 视觉副本执行 scramble，14 次动画期 accessibility snapshot 始终只暴露稳定名称；32 个项目 CTA 均提供项目专属“新窗口”可访问名。
- Chrome 147 三视口 1440×900 / 390×844 / 320×568 全 PASS：32 卡、32 图、timeline 顺序、tool=10、OxAlpha 可见、CTA 46px、横向溢出与 JS error 均为 0；三张完整卡片元素截图（含 320px 下高于视口的整卡）目检无重叠、裁切、破图或异常拆行。
- 390px `has_touch` 真实触摸 CTA 到达 `https://oxalpha.site/`，title 为 `Ox Alpha AI — Model, API, Benchmarks, Pricing & Identity`。
- 独立只读复审：冻结 tree `cd22a287693713bb5315fea7e71bb1aaddc24a39` 判定 READY；旧 manifest、v3 基线、mutable-path harness、CI false-green、scramble a11y、CTA 名称和 320px 整卡证据问题均已关闭。
- 生产发布：commit `0cb015703ab75e53b966c98c16c14d1ef027412d`；GitHub Actions run `32568517376` 全步骤成功（含 regression gates、artifact、deploy）。
- 生产字节：`index.html` SHA-256 `591492bb0543edb5a432281aeadb9327b5d86a286f9d0e17beaadc0bbad86a40` 与候选一致；`project-32.webp` SHA-256 `d850fc9eb00ab13996f37c448f8b284eb553e162029b75f4b61f960776189f19`，WebP 400×250；HTTP 单次 301 到 HTTPS，HTTPS 200。
- 生产浏览器：1440×900 / 390×844 / 320×568 全 PASS；32 卡/32 图/32 reveal、tool=10、NEW=9、唯一 latest、32 个唯一 CTA 名称、Timeline 键盘、无横向溢出/JS error/同源网络错误；390px 真实 touch 到达 OxAlpha；三张完整卡片元素截图目检通过。
- 生产 artifact 边界：`privacy.html`、`favicon.svg`、`assets/archivo.woff2` 为 200；`project-control.md`、`scripts/`、`tests/`、`.github/` 探针均为 404。

## v5 改版：最新在前的发布网格 + Spotlight + 动效（2026-08-22）

方案 A（子凡选定）：全站信息架构从"编号列表"改为"最新在前"。

- **卡片倒序**：31 张卡按上线日期降序（同日按卡片编号降序）。Sinking City 2 Field Guide 居首，AIStoryNest 收尾。
- **Spotlight 大卡**：最新一张全宽展示（桌面左图右文，移动端上图下文）；带红色 ★ 最新上线 徽章。
- **NEW 徽章**：构建日期（2026-08-22）7 天内的发布自动挂绿色 NEW，本轮 8 张。
- **卡片网格**：3 → 2 → 1 列响应式；悬停上浮 + 顶部渐变条 + 缩略图微缩放；卡片并入既有 .reveal 观察器做滚动进场 + 级联错峰；prefers-reduced-motion 下全部可见、无位移。
- **联动契约**：时间轴跑马灯同步倒序（最新在左，latest 标记移到头部）；changelog 本就最新在上，测试断言改为同向。
- **DOM 零改动**：`<article class="site" data-status="live">` 锚点原样保留，只重排 + 加 CSS + 徽章，30+ 处既有断言不碎。
- **回归**：pytest 38/38 ✅；node 交互 ✅；accept_v5.py 三视口（1440/390/320）全 PASS；截图目检无溢出无缺图。
- **生产**：commit a15c07a，GitHub Actions 部署成功，wangzifan.store 已验证（倒序/徽章/网格/动效全部命中）。
- 文件：`scripts/assemble_v5.py`（装配）、`scripts/accept_v5.py`（验收）。

## HLLV 上线日期修正 + 跑马灯 ✦ 配色（2026-08-20）

- 子凡确认 HLLV Field Manual 上线日期应为 **2026-08-18**（08-17 为部署迭代日）。Cloudflare API 核实：首次 production 部署 08-16 23:42 CST，08-17 全天 6 次迭代部署，08-18 15:30 CST 为域名绑定后的首次正式生产部署——与 08-18 口径一致。
- 全链路修正：卡片 #29 日期 08-17→08-18；Timeline 08-17 恢复为牛来 1 SHIPPED、新增 2026-08-18 独立节点（HLLV 1 SHIPPED）；Changelog HLLV SHIP 行改为 `[2026-08-18]`；pytest 断言与 assemble_v4.py 记录同步。时间轴跨度与标题不变（07-12→08-20，40 天，31 次真实上线）。
- 跑马灯（ghost band）配色调整：✦ 分隔符由高饱和 `var(--flame)`（#e8401a）改为陶土色 `#c86544`（opacity .9），与奶油底和 `#6b675e` 实心文字形成受控暖色节奏；文字实心化已于 d747a13 完成。

## The Sinking City 2 Field Guide 卡片 #31（2026-08-20）

- 新增卡片 #31：The Sinking City 2 Field Guide（`https://thesinkingcity2.top/`），分类「游戏与内容」，标签「克苏鲁侦探攻略站」，上线日期 2026-08-20。
- 筛选计数目标：全部 31 / AI 3 / 游戏 11 / 工具 9 / 创意 8；Timeline 保持 40 天并更新为 31 次真实上线，2026-08-20 节点更新为 2 SHIPPED；Changelog 更新为 31 entries / 31 releases。
- 缩略图来自生产站真实首屏，经系统 Chrome 抓取并以 Lanczos 缩为 400×250 WebP；GitHub Pages artifact allowlist 同步要求精确发布 31 张缩略图。
- 回归结果：pytest 36/36、Node 动态交互通过；1440×900、390×844、320×568 三视口均显示 31 张卡，游戏筛选 11 张，31 张图片全部加载，控制台错误、页面异常、横向溢出、同源失败请求均为 0。
- 390px CDP 真实 touch 已打开 `https://thesinkingcity2.top/`；320px 目检后将 metadata 优化为“状态+日期同排、标签独占第二行”，复测无拆字、重叠、裁切或破图。
- `project-31.webp` 为 400×250、11,154 bytes，SHA-256 `3abf05208ba7ee89ceca3adec358f95c30c67de6ff220de0c38c026093a7bd6e`；exact-tree 独立复审及线上字节核验通过后才允许发布。

## Chinamaxxing Online 卡片 #30（2026-08-20）

- 新增卡片 #30：Chinamaxxing Online（`https://chinamaxxing.site/`），分类「创意实验」，标签「多语文化指南」，上线日期 2026-08-20。
- 筛选计数更新为：全部 30 / AI 3 / 游戏 10 / 工具 9 / 创意 8；Timeline 更新为 40 天、30 次真实上线，并新增 2026-08-20 节点；Changelog 更新为 30 entries / 30 releases。
- 缩略图来自生产站真实首屏，经 Playwright 抓取并转为 400×250 WebP（14,448 bytes）后 base64 内联；GitHub Pages workflow 白名单不变。
- 回归：pytest 30/30、Node 动态交互、确定性卡片检查均通过；1440×900、Android 390×844、Android 320×568 三视口通过，创意筛选 8 张、全部 30 张，无横向溢出、控制台错误、页面异常或同源失败请求。
- 390px 真实触摸 CTA 已验证到达 `https://chinamaxxing.site/`，页面标题为 `Chinamaxxing Online: Meaning, Quiz & Culture Guides`。

## v4 更新：筛选计数 + HLLV 卡片 #29（2026-08-19）

- 新增卡片 #29：HLLV Field Manual（hellletloosevietnam.blog，《Hell Let Loose: Vietnam》非官方野战手册），分类「游戏与内容」；上线日期 2026-08-17（按 Cloudflare Pages 首次 production 部署时间核实，08-16 仅为首个代码提交日）。**该日期已于 2026-08-20 修正为 2026-08-18**（08-17 属部署迭代，08-18 为域名绑定后正式发布），见顶部修正记录。
- 筛选按钮新增计数胶囊：`data-count` 属性经 CSS `::after` 渲染（全部 29 / AI 3 / 游戏 10 / 工具 9 / 创意 7），button.textContent 保持原样，live 状态栏契约与主脚本零改动。
- 「全部上线记录」subhead 新增 29 徽章；Timeline 标题 28→29，2026-08-17 变为 2 SHIPPED（牛来 + HLLV；后于 2026-08-20 拆分为 08-17 / 08-18 两个节点）；Changelog 28→29 entries，顶部新增 HLLV SHIP 记录。
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

## 产品索引（33）

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
| 31 | The Sinking City 2 Field Guide | 游戏与内容 | https://thesinkingcity2.top/ |
| 32 | OxAlpha | 实用工具 | https://oxalpha.site/ |
| 33 | Mortal Shell II Wiki | 游戏与内容 | https://mortalshell2.quest/ |

## 发布产物边界

- `scripts/prepare_public_artifact.py` 只向全新 `_site` 目录复制 strict allowlist，并拒绝复用已有目录与 symlink 来源。
- 当前 allowlist 精确为 41 个文件：`index.html`、`privacy.html`、`favicon.svg`、共享 CSS/JS、Archivo 字体、OG 图、微信二维码和 33 张编号项目 WebP。
- `upload-pages-artifact` 的路径固定为 `_site`，不得改回仓库根目录；源码、测试、数据、控制文档、Git 元数据、`.hermes/`、`_qa/` 不得进入 Pages artifact。
- `_site/` 与 `_qa/` 均由 `.gitignore` 排除；候选证据不进入提交。
- 页面仅加载已批准并在隐私页披露的 Plausible 统计脚本；全部新窗口外链使用 `noopener noreferrer`。

## 候选浏览器验收

- 真实 CSS 视口 `1440×900`、`1024×768`、`768×1024`、`390×844`、`320×568` 与断点边界 `759/760/761×800` 均无页面级横向溢出、owner crossing、控制台错误、页面异常、同源失败请求或坏响应。
- 320px 首屏主 CTA 完整可见；验收覆盖的按钮与表单控件高度不低于 44px，复制失败后出现的手动输入框也在 1440/390/320 三档实测为 44px；首页与隐私页 skip link 均将焦点送到对应 main。
- 默认档案展示 9 条；类别、关键词、在线/离线组合筛选与 33 条展开状态均通过；离线筛选唯一命中 Polski Piłkarz Simulator。
- 搜索零结果会明确显示空状态；微信复制覆盖 Clipboard API 成功与 `execCommand` 失败后的明文选择降级；无 JavaScript 时筛选/展开/复制按钮不出现，3 个重点案例与 33 条档案全部可读。
- 正常动画与 `prefers-reduced-motion` 均无持续帧变化；7 张当前页面图片全部完成解码。
- 验收脚本会独立拒绝 artifact 后插文件或 symlink；项目图片 allowlist 固定为 `project-01.webp` 至 `project-33.webp`，不再接受任意 33 个 WebP；所有 `target="_blank"` 逐链接验证 `noopener noreferrer`，并用恶意 registry payload 回归 HTML/JSON-LD escaping。
- 证据绑定候选 SHA-256 `787edd3dff833bb810111808bd3184810cfed6ba554ff5e1497811f48c209b87`，位于 `_qa/v11.1/report.json` 与同目录全页截图。

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
