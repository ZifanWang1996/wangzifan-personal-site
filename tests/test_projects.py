import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
SITE = ROOT / "index.html"
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-pages.yml"
FAVICON = ROOT / "favicon.svg"
CONTROL = ROOT / "project-control.md"
PRIVACY = ROOT / "privacy.html"


def test_projects_section_includes_live_palworldmap_v2_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>PalworldMap</h3>' in html
    assert 'href="https://palworldmap.best/"' in html
    assert '<span>04 · 已上线</span><span>Palworld 坐标图谱</span>' in html
    assert '89 条来源锁定导航记录（82 个快速传送点、7 座高塔）' in html
    assert '最近点计算与本地清单' in html


def test_projects_section_includes_live_codexskin_card():
    html = SITE.read_text(encoding="utf-8")

    assert 'data-status="live"' in html
    assert '<h3>CodexSkin.space</h3>' in html
    assert 'href="https://codexskin.space/"' in html
    assert '<span>05 · 已上线</span><span>Codex CLI TUI 指南站</span>' in html
    assert 'Codex CLI TUI 配置指南' in html


def test_projects_section_includes_live_llmstxt_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>llmstxt</h3>' in html
    assert 'href="https://llmstxt.best/"' in html
    assert '<span>06 · 已上线</span><span>llms.txt 实用指南</span>' in html
    assert 'llms.txt 的阅读、发布与维护' in html


def test_projects_section_includes_live_allwishescometrue_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>All Wishes Come True</h3>' in html
    assert 'href="https://allwishescometrue.site/"' in html
    assert '<span>07 · 已上线</span><span>八仙电影与民俗文化站</span>' in html
    assert '电影背景、八位角色、民俗源流' in html


def test_projects_section_includes_live_taskbarherowiki_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>TaskbarHeroWiki</h3>' in html
    assert 'href="https://taskbarherowiki.best/"' in html
    assert '<span>08 · 已上线</span><span>Task Bar Hero 数据库</span>' in html
    assert '关卡、怪物、宝箱、材料与关系记录' in html


def test_projects_section_includes_live_chinesecashcoins_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Chinese Coins Atlas</h3>' in html
    assert 'href="https://chinesecashcoins.wiki/"' in html
    assert '<span>09 · 已上线</span><span>中国古钱币图鉴</span>' in html
    assert '布币、刀币、五铢、开元通宝' in html


def test_projects_section_includes_live_rotcheck_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Rot Check</h3>' in html
    assert 'href="https://rotcheck.cyou/"' in html
    assert '<span>10 · 已上线</span><span>Gen Alpha 趣味测试站</span>' in html
    assert 'Am I Unc、Brainrot Test、Am I Cooked' in html


def test_projects_section_includes_live_spiritvale_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>SpiritVale Wiki</h3>' in html
    assert 'href="https://spiritvale.blog/"' in html
    assert '<span>11 · 已上线</span><span>SpiritVale 社区 Wiki</span>' in html
    assert '16 个职业流派、230+ 怪物数据库' in html
    assert html.count('data-status="live"') == 29
    assert html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 29


def test_projects_section_includes_live_mergeanuke_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Merge a Nuke! Guide</h3>' in html
    assert 'href="https://mergeanuke.space/"' in html
    assert '<span>19 · 已上线</span><span>核弹合成攻略站</span>' in html
    assert '可兑换代码、指挥官与突变情报、进度强度排行和合成计算器' in html


def test_projects_section_includes_live_aiscanner_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>AI Scanner</h3>' in html
    assert 'href="https://aiscanner.run/"' in html
    assert '<span>20 · 已上线</span><span>AI 文本检测工具</span>' in html
    assert '浏览器端免费检测' in html
    assert '多模型深度扫描、置信度和逐句原因说明' in html


def test_projects_section_includes_live_rspeditor_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>RSP Editor</h3>' in html
    assert 'href="https://rspeditor.app/"' in html
    assert '<span>21 · 已上线</span><span>AI 同款照片生成器</span>' in html
    assert '选择同款模板、上传照片并用 AI 在数秒内生成成片' in html
    assert '提示词库与交互式提示词构建器' in html


def test_projects_section_includes_live_remove_matcha_filter_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Remove Matcha Filter</h3>' in html
    assert 'href="https://remove-matcha-filter.com/"' in html
    assert '<span>22 · 已上线</span><span>图片视频校色工具</span>' in html
    assert '修正抹茶绿色偏色的图片与短视频' in html
    assert '浏览器本地处理、效果对比与导出' in html
    assert '媒体文件无需上传服务器' in html


def test_projects_section_includes_live_deepseek_harness_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>DSH Field Guide</h3>' in html
    assert 'href="https://deepseekharness.site/"' in html
    assert '<span>23 · 已上线</span><span>DeepSeek 工具指南</span>' in html
    assert '独立的 DeepSeek Harness 实用指南' in html
    assert '经来源核验且标注版本' in html
    assert '安装、模型配置、Python SDK、插件与故障排查' in html


def test_projects_section_includes_live_polski_pilkarz_simulator_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>Polski Piłkarz Simulator</h3>' in html
    assert 'href="https://polskipilkarzsymulator.online/"' in html
    assert '<span>24 · 已上线</span><span>波兰足球生涯模拟器</span>' in html
    assert '可免费在线游玩 v1.90' in html
    assert '8400+ 家俱乐部与 101 个生涯事件' in html
    assert '比赛胜率计算器和新手指南' in html


def test_projects_section_includes_live_burnt_for_you_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>burnt for you</h3>' in html
    assert 'href="https://burncd.xyz/"' in html
    assert '<span>25 · 已上线</span><span>数字混音带制作器</span>' in html
    assert '挑选歌曲、写下留言并生成数字混音带 CD' in html
    assert '通过单个链接分享' in html
    assert '无需注册，每首歌以 30 秒片段播放' in html


def test_projects_section_includes_live_matchafilter_card():
    html = SITE.read_text(encoding="utf-8")

    assert '<h3>MatchaFilter</h3>' in html
    assert 'href="https://matchafilter.cc/"' in html
    assert '<span>26 · 已上线</span><span>照片抹茶滤镜校色</span>' in html
    assert '修正照片黄绿色偏色' in html
    assert '支持 PNG、JPG 和 WebP 浏览器本地处理' in html
    assert '调节校正强度、对比原图并导出 PNG' in html
    assert '无需账户，免费处理时照片不会上传服务器' in html


def test_projects_section_includes_live_craveloop_card():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    matching = [card for card in cards if '<h3>CraveLoop</h3>' in card]

    assert len(matching) == 1
    card = matching[0]
    assert html.count('href="https://foodnevercomes.online/"') == 1
    assert 'data-category="creative"' in card
    assert '<span>27 · 已上线</span><span>全球美食点单模拟器</span>' in card
    assert 'href="https://foodnevercomes.online/"' in card
    assert '8 个国家的 48 道菜' in card
    assert '加入虚拟购物车' in card
    assert '以 $0 结账' in card
    assert '永远不会送达的虚构订单' in card


def test_projects_section_includes_live_niulai_card():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    matching = [card for card in cards if '<h3>牛来</h3>' in card]

    assert len(matching) == 1
    card = matching[0]
    assert html.count('href="https://niulai.blog/"') == 1
    assert 'data-category="creative"' in card
    assert '<span>28 · 已上线</span><span>牛来电影资料站</span>' in card
    assert 'href="https://niulai.blog/"' in card
    assert '首日 342 元到 150 万元' in card
    assert '票房逆袭时间线' in card
    assert '差评墙、黑话词典与在线答题' in card


def test_projects_section_includes_live_hllv_card():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    matching = [card for card in cards if '<h3>HLLV Field Manual</h3>' in card]

    assert len(matching) == 1
    card = matching[0]
    assert html.count('href="https://hellletloosevietnam.blog/"') == 1
    assert 'data-category="game"' in card
    assert '<span>29 · 已上线</span><span>HLLV 越南战场手册</span>' in card
    assert '<span class="site-date">2026-08-17</span>' in card
    assert 'Hell Let Loose: Vietnam' in card
    assert '已知问题' in card
    assert '每条结论均标注日期与依据' in card


def test_homepage_uses_opc_launch_ledger_information_architecture():
    html = SITE.read_text(encoding="utf-8")
    control = CONTROL.read_text(encoding="utf-8")

    # OPC-only identity across the production page and current public repository docs.
    for removed in (
        "主" "业",
        "项目" "经理",
        "项目" "管理",
        "Project" " Management",
        "个人" "履历",
        "Res" "ume",
        "工作" "经历",
    ):
        assert removed not in html
        assert removed not in control

    # The hero is an action-led shipping statement, not a scorecard.
    assert "先把想法做出来" in html
    assert "再让世界给答案。" in html
    assert "SHIPPING ENGINE" in html
    for removed in (
        "26 个产品",
        "6 项证书",
        "六个重点产品",
        "Selected Deployments",
        'id="proof"',
        'data-featured="true"',
    ):
        assert removed not in html

    # One complete, equal-weight release ledger carries every live product.
    assert 'class="release-ledger"' in html
    assert "全部上线记录" in html
    assert "把想法做成网址" in html
    assert html.count('data-status="live"') == 29
    assert html.count('<article class="site" data-status="live">') == 29
    assert html.count('data-category=') == 29
    assert 'id="visibleCount" aria-live="polite">ALL RELEASES' in html
    for value in ("all", "ai", "game", "tool", "creative"):
        assert f'data-filter="{value}"' in html
    for removed_label in ("全部 28", "AI 产品 3", "游戏与内容 9", "实用工具 9", "创意实验 7"):
        assert removed_label not in html
    # v4: count chips live in data-count attributes, rendered via CSS ::after
    # so button.textContent stays clean for the live status bar.
    for value, count in (("all", "29"), ("ai", "3"), ("game", "10"), ("tool", "9"), ("creative", "7")):
        assert f'data-filter="{value}" data-count="{count}"' in html
    assert '<span class="ledger-count">29</span>' in html

    # Required section order and evidence-led motivational language.
    ordered_sections = (
        'id="top"',
        'id="work"',
        'id="system"',
        'id="manifesto"',
        'id="contact"',
    )
    positions = [html.index(section) for section in ordered_sections]
    assert positions == sorted(positions)
    assert "不把灵感收藏起来" in html
    assert "少一点等待" in html and "多一次真实发布" in html
    assert "上线就是时机" in html
    assert "下一件值得上线的事" in html and "现在就开始" in html
    for step in ("判断", "构建", "上线", "反馈"):
        assert f'data-step="{step}"' in html

    assert "Founder Manifesto" in html
    assert "wang1227928718" in html
    assert "复制微信号" in html
    assert 'aria-live="polite"' in html


def test_command_palette_opens_on_first_destination():
    html = SITE.read_text(encoding="utf-8")

    assert "modal.querySelector('a').focus()" in html


def test_interactions_execute_across_filters_keyboard_and_copy_fallbacks():
    result = subprocess.run(
        ["node", str(ROOT / "tests" / "browser_interactions.mjs")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "dynamic interactions: OK" in result.stdout


def test_release_filters_remain_compact_at_narrowest_width():
    html = SITE.read_text(encoding="utf-8")

    assert ".filters{display:grid;grid-template-columns:1fr 1fr}" in html
    assert ".filters{grid-template-columns:1fr}" not in html
    filter_rule = re.search(r"\.filter\{([^}]*)\}", html)
    assert filter_rule
    assert "border:1px solid var(--line2)" in filter_rule.group(1)


def test_oem_android_fonts_do_not_inherit_font_specific_opentype_features():
    html = SITE.read_text(encoding="utf-8")
    body_rule = re.search(r"body\{([^}]*)\}", html)

    assert body_rule
    body_css = body_rule.group(1)
    assert "font-feature-settings:normal" in body_css
    assert 'font-feature-settings:"cv01","ss03"' not in body_css
    heading = re.search(r"<h3>(Build a Hooper)</h3>", html)
    assert heading
    assert [ord(char) for char in "Build a Hooper"] == [
        ord(char) for char in heading.group(1)
    ]


def test_mobile_release_card_microcopy_is_legible():
    html = SITE.read_text(encoding="utf-8")
    mobile_start = html.index("@media(max-width:700px){")
    mobile_end = html.index("@media(max-width:360px){", mobile_start)
    mobile_css = html[mobile_start:mobile_end]

    meta_rule = re.search(r"\.site-category,\.site-meta\{([^}]*)\}", mobile_css)
    link_rule = re.search(r"\.site-link\{([^}]*)\}", mobile_css)
    assert meta_rule and "font-size:11px" in meta_rule.group(1)
    assert link_rule and "font-size:12px" in link_rule.group(1)


def test_release_artifact_is_allowlisted_and_mobile_safe():
    html = SITE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    # Long unbroken product names must wrap instead of being clipped at 320px.
    site_heading_rule = re.search(r"\.site h3\{([^}]*)\}", html)
    assert site_heading_rule
    assert "overflow-wrap:anywhere" in site_heading_rule.group(1)
    assert "font-size:clamp(25px,8vw,28px)" in site_heading_rule.group(1)
    assert "<h3>HowManySleeps<wbr>Until</h3>" in html

    # A real favicon prevents the browser's implicit /favicon.ico 404.
    assert '<link rel="icon" href="favicon.svg" type="image/svg+xml">' in html
    assert FAVICON.exists()
    favicon = FAVICON.read_text(encoding="utf-8")
    assert "<svg" in favicon and "</svg>" in favicon

    # GitHub Pages may publish only the explicit public allowlist.
    assert "path: _site" in workflow
    assert "path: ." not in workflow
    assert "test ! -e _site" in workflow
    assert "install -m 0644 index.html _site/index.html" in workflow
    assert "install -m 0644 favicon.svg _site/favicon.svg" in workflow

    prepare_block = workflow.split("      - name: Prepare public artifact", 1)[1].split(
        "      - name: Upload site artifact", 1
    )[0]
    prepare_commands = [
        line.strip()
        for line in prepare_block.splitlines()
        if line.strip() and line.strip() != "run: |"
    ]
    assert prepare_commands == [
        "test ! -e _site",
        "mkdir _site",
        "install -m 0644 index.html _site/index.html",
        "install -m 0644 favicon.svg _site/favicon.svg",
        "install -m 0644 privacy.html _site/privacy.html",
    ]


def test_plausible_analytics_is_disclosed_and_allowlisted():
    html = SITE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    script = '<script defer data-domain="wangzifan.store" src="https://plausible.shipsolo.io/js/script.js"></script>'

    assert html.count(script) == 1
    assert 'href="privacy.html">PRIVACY / 隐私</a>' in html
    assert PRIVACY.exists()

    privacy = PRIVACY.read_text(encoding="utf-8")
    assert privacy.count(script) == 1
    for disclosure in (
        "Plausible Analytics",
        "plausible.shipsolo.io",
        "不设置分析 Cookie",
        "不进行跨站跟踪",
        "GitHub Pages",
        "wang1227928718",
    ):
        assert disclosure in privacy

    assert "install -m 0644 privacy.html _site/privacy.html" in workflow
