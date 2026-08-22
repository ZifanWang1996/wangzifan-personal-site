import re
import subprocess
from datetime import date, timedelta
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
    assert html.count('data-status="live"') == 32
    assert html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 32


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
    assert '<span class="site-date">2026-08-18</span>' in card
    assert 'Hell Let Loose: Vietnam' in card
    assert '已知问题' in card
    assert '每条结论均标注日期与依据' in card


def test_projects_section_includes_live_chinamaxxing_card():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    matching = [card for card in cards if '<h3>Chinamaxxing Online</h3>' in card]

    assert len(matching) == 1
    card = matching[0]
    assert html.count('href="https://chinamaxxing.site/"') == 1
    assert 'data-category="creative"' in card
    assert '<span>30 · 已上线</span><span>多语文化指南</span>' in card
    assert '<span class="site-date">2026-08-20</span>' in card
    assert '英语、西班牙语和巴西葡萄牙语' in card
    assert '附来源解释、生活与旅行指南' in card
    assert '12 信号 Quiz 和浏览器本地路线生成器' in card


def test_projects_section_includes_live_sinking_city_2_field_guide_card():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    matching = [card for card in cards if '<h3>The Sinking City 2 Field Guide</h3>' in card]

    assert len(matching) == 1
    card = matching[0]
    assert html.count('href="https://thesinkingcity2.top/"') == 1
    assert 'data-category="game"' in card
    assert '<span>31 · 已上线</span><span>克苏鲁侦探攻略站</span>' in card
    assert '<span class="site-date">2026-08-20</span>' in card
    assert '保险柜密码、章节路线、成就、调查与战斗参考' in card
    assert '区分实证、实测与暂缺资料' in card


def test_projects_section_includes_live_oxalpha_card():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    matching = [card for card in cards if '<h3>OxAlpha</h3>' in card]

    assert len(matching) == 1
    card = matching[0]
    assert html.count('href="https://oxalpha.site/"') == 1
    assert 'data-category="tool"' in card
    assert '<span>32 · 已上线</span><span>AI 模型证据站</span>' in card
    assert '<span class="site-date">2026-08-22</span>' in card
    assert '身份、状态、API、定价、代码能力' in card
    assert '约 1M 上下文与基准测试' in card
    assert '平台记录、可复现证据、观察和推测' in card


def test_project_control_product_index_matches_live_card_ledger():
    html = SITE.read_text(encoding="utf-8")
    control = CONTROL.read_text(encoding="utf-8")
    live_count = html.count('<article class="site" data-status="live">')
    index = re.search(r'^## 产品索引（(\d+)）\n\n(.*?)(?=^## )', control, re.M | re.S)

    assert index is not None
    displayed_count = int(index.group(1))
    row_numbers = [int(value) for value in re.findall(r'^\|\s*(\d+)\s*\|', index.group(2), re.M)]
    assert row_numbers == list(range(1, live_count + 1))
    assert displayed_count == live_count == len(row_numbers)


def test_project_control_records_reproducible_public_artifact_manifest():
    control = CONTROL.read_text(encoding="utf-8")
    assert "sha256sum-compatible manifest" in control
    assert '每行 `<file_sha256>  <relative_path>\\n`，relative path 按字典序' in control
    assert "a6048999cf0d613d7702585f762686a7e6cbe9413c22291ace8e1e33b552a893" in control


def test_timeline_and_changelog_derive_from_live_card_ledger():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    ledger = []
    for card in cards:
        name_html = re.search(r'<h3>(.*?)</h3>', card, re.S)
        shipped = re.search(r'<span class="site-date">(\d{4}-\d{2}-\d{2})</span>', card)
        href = re.search(r'<a class="site-link"[^>]* href="([^"]+)"', card)
        assert name_html and shipped and href
        name = re.sub(r'<[^>]+>', '', name_html.group(1))
        ledger.append((shipped.group(1), name, href.group(1)))

    shipped_dates = [date.fromisoformat(value) for value, _, _ in ledger]
    expected_days = (max(shipped_dates) - min(shipped_dates)).days + 1
    timeline_heading = re.search(
        r'<h2 id="timeline-title" aria-label="\d+ 天，\d+ 次真实上线。"><span aria-hidden="true" data-scramble-visual>(\d+) 天，(\d+) 次真实上线。</span></h2>', html
    )
    assert timeline_heading is not None
    assert int(timeline_heading.group(1)) == expected_days
    assert int(timeline_heading.group(2)) == len(ledger)

    timeline_counts = [
        int(value) for value in re.findall(r'<div class="tl-count">(\d+) SHIPPED</div>', html)
    ]
    timeline_names = [
        name
        for group in re.findall(r'<div class="tl-names">(.*?)</div>', html, re.S)
        for name in re.findall(r'<span>([^<]+)</span>', group)
    ]
    assert sum(timeline_counts) == len(ledger)
    assert timeline_names == [name for _, name, _ in ledger]

    chrome_count = re.search(r'release\.log — (\d+) entries', html)
    prompt_count = re.search(r'<b>(\d+) releases</b>', html)
    log_ledger = re.findall(
        r'<div class="log-line"><span class="log-d">\[(\d{4}-\d{2}-\d{2})\]</span>'
        r'<span class="log-ok">SHIP</span><span class="log-n">([^<]+)</span>'
        r'<span class="log-u">→ ([^<]+)</span></div>',
        html,
    )
    assert chrome_count and prompt_count
    assert int(chrome_count.group(1)) == len(ledger)
    assert int(prompt_count.group(1)) == len(ledger)
    # v5: cards render newest-first, and the changelog is also newest-first,
    # so the two sequences now agree in the same order.
    assert log_ledger == ledger


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
    assert html.count('data-status="live"') == 32
    assert html.count('<article class="site" data-status="live">') == 32
    assert html.count('data-category=') == 32
    assert 'id="visibleCount" aria-live="polite">ALL RELEASES' in html
    for value in ("all", "ai", "game", "tool", "creative"):
        assert f'data-filter="{value}"' in html
    for removed_label in ("全部 28", "AI 产品 3", "游戏与内容 9", "实用工具 9", "创意实验 7"):
        assert removed_label not in html
    # v4: count chips live in data-count attributes, rendered via CSS ::after
    # so button.textContent stays clean for the live status bar.
    for value, count in (("all", "32"), ("ai", "3"), ("game", "11"), ("tool", "10"), ("creative", "8")):
        assert f'data-filter="{value}" data-count="{count}"' in html
    assert '<span class="ledger-count">32</span>' in html

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


def test_browser_acceptance_harness_is_bound_to_its_own_checkout():
    harness = (ROOT / "scripts" / "accept_v5.py").read_text(encoding="utf-8")
    assert "Path(__file__).resolve().parents[1]" in harness
    assert "/root/projects/zf-wang-personal-site" not in harness
    assert "ThreadingHTTPServer" in harness
    assert "http://127.0.0.1" in harness
    assert ".as_uri()" not in harness
    assert 'playwright==1.' in harness
    assert "first.screenshot" in harness
    assert "requestfailed" in harness
    assert 'revealedCount\"] == 32' in harness


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



def test_narrow_mobile_release_metadata_does_not_split_status_or_date():
    html = SITE.read_text(encoding="utf-8")
    narrow_start = html.index("@media(max-width:360px){")
    narrow_end = html.index("@media(max-width:700px) and (max-height:380px)", narrow_start)
    narrow_css = html[narrow_start:narrow_end]

    assert ".site-meta{display:grid;grid-template-columns:1fr auto;gap:5px 12px}" in narrow_css
    assert ".site-meta span:first-child,.site-date{white-space:nowrap}" in narrow_css
    assert ".site-meta span:nth-child(2){grid-column:1/-1;grid-row:2}" in narrow_css
    assert ".site-date{grid-column:2;grid-row:1}" in narrow_css


def test_homepage_performance_assets_are_cacheable_and_below_fold_work_is_contained():
    html = SITE.read_text(encoding="utf-8")
    privacy = PRIVACY.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "data:image/webp;base64" not in html
    assert "data:font/woff2;base64" not in html
    assert "data:font/woff2;base64" not in privacy
    assert "url('assets/archivo.woff2')" in privacy

    image_refs = re.findall(r'src="(assets/projects/project-\d{2}\.webp)"', html)
    assert len(image_refs) == 32
    assert len(set(image_refs)) == 32
    for image_ref in image_refs:
        assert (ROOT / image_ref).is_file()

    image_tags = re.findall(r'<img\s+[^>]*src="assets/projects/project-\d{2}\.webp"[^>]*>', html)
    assert len(image_tags) == 32
    for image_tag in image_tags:
        assert 'width="400"' in image_tag
        assert 'height="250"' in image_tag
        assert 'loading="lazy"' in image_tag
        assert 'decoding="async"' in image_tag

    assert (ROOT / "assets" / "archivo.woff2").is_file()
    assert "url('assets/archivo.woff2')" in html
    assert 'class="grain"' not in html
    assert "glowLoop" not in html
    assert "requestAnimationFrame(glowLoop)" not in html
    assert "content-visibility:auto" not in html
    assert "contain-intrinsic-size" not in html

    assert "install -m 0644 assets/archivo.woff2 _site/assets/archivo.woff2" in workflow
    assert "install -m 0644 assets/projects/*.webp _site/assets/projects/" in workflow



def test_light_theme_and_privacy_footer_colors_meet_the_aa_token_contract():
    html = SITE.read_text(encoding="utf-8")
    privacy = PRIVACY.read_text(encoding="utf-8")

    assert ".brand small,.hero-credo,.footer{color:#6b675e}" in html
    assert ".subhead p,.visible-count,.site-meta,.site-date{color:#6b675e}" in html
    assert ".band.ghost .band-set{color:#6b675e;-webkit-text-stroke:0}" in html
    assert ".band.ghost .band-set i{color:#c86544;-webkit-text-stroke:0;opacity:.9}" in html
    assert ".filter:after" in html and "color:#625f57" in html
    assert "footer{padding:30px 0 48px" in privacy
    assert "color:#94928a" in privacy



def test_scrollable_timeline_and_changelog_are_named_keyboard_regions():
    html = SITE.read_text(encoding="utf-8")

    assert (
        '<div class="tl-rail" tabindex="0" role="region" '
        'aria-label="上线时间线，可横向滚动">'
    ) in html
    assert (
        '<div class="log-body" tabindex="0" role="region" '
        'aria-label="发布日志，可横向和纵向滚动">'
    ) in html
    assert '<h2 id="timeline-title" aria-label="42 天，32 次真实上线。">' in html
    assert '<span aria-hidden="true" data-scramble-visual>42 天，32 次真实上线。</span>' in html
    assert "document.querySelector('#timeline-title [data-scramble-visual]')" in html

    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
    assert len(cards) == 32
    for card in cards:
        title = re.sub(r'<[^>]+>', '', re.search(r'<h3>(.*?)</h3>', card, re.S).group(1))
        link = re.search(r'<a class="site-link" aria-label="([^"]+)" href="([^"]+)" target="_blank" rel="noopener noreferrer">', card)
        assert link is not None
        assert link.group(1) == f"访问 {title} 项目（新窗口）"



def test_command_palette_is_scroll_safe_in_low_height_viewports():
    html = SITE.read_text(encoding="utf-8")

    assert "@media(max-height:420px)" in html
    assert ".modal{align-items:flex-start;overflow-y:auto;padding:8px}" in html
    assert (
        ".palette{margin:auto;max-height:calc(100dvh - 16px);"
        "overflow-y:auto;overscroll-behavior:contain}"
    ) in html



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

    # CI must reject a broken page before artifact upload or deployment.
    for gate in (
        "actions/setup-python@v5",
        "python -m pip install --disable-pip-version-check pytest pillow",
        "python -m pytest -q",
        "node tests/browser_interactions.mjs",
        "python -m compileall -q scripts tests",
    ):
        assert gate in workflow
    gate_pos = workflow.index("python -m pytest -q")
    assert gate_pos < workflow.index("      - name: Upload site artifact")
    assert gate_pos < workflow.index("      - name: Deploy to GitHub Pages")

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
        "mkdir -p _site/assets/projects",
        "install -m 0644 index.html _site/index.html",
        "install -m 0644 favicon.svg _site/favicon.svg",
        "install -m 0644 privacy.html _site/privacy.html",
        "install -m 0644 assets/archivo.woff2 _site/assets/archivo.woff2",
        'test "$(printf \'%s\\n\' assets/projects/*.webp | wc -l)" -eq 32',
        "install -m 0644 assets/projects/*.webp _site/assets/projects/",
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


def test_v5_release_grid_is_newest_first_with_spotlight():
    html = SITE.read_text(encoding="utf-8")
    cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)

    def key(card):
        num = int(re.search(r'<span>(\d+)\s*·', card).group(1))
        shipped = re.search(r'<span class="site-date">(\d{4}-\d{2}-\d{2})</span>', card).group(1)
        return shipped, num

    keys = [key(card) for card in cards]
    assert keys == sorted(keys, reverse=True), "cards must run newest-first"
    assert '<h3>OxAlpha</h3>' in cards[0], "latest release must lead"
    assert '<h3>AIStoryNest</h3>' in cards[-1], "first release must come last"

    # Spotlight badge on the lead card only; NEW badges within the 7-day window.
    assert '<span class="site-latest">★ 最新上线</span>' in cards[0]
    assert html.count('<span class="site-latest">★ 最新上线</span>') == 1
    for card in cards[1:]:
        assert '<span class="site-latest">' not in card

    build_date = date(2026, 8, 22)
    cutoff = build_date - timedelta(days=7)
    for card in cards[1:]:
        shipped = date.fromisoformat(key(card)[0])
        if shipped >= cutoff:
            assert '<span class="site-new">NEW</span>' in card
        else:
            assert '<span class="site-new">' not in card

    # Timeline rail mirrors the newest-first card order (name-sequence contract).
    timeline_names = [
        name
        for group in re.findall(r'<div class="tl-names">(.*?)</div>', html, re.S)
        for name in re.findall(r'<span>([^<]+)</span>', group)
    ]
    card_names = [re.sub(r'<[^>]+>', '', re.search(r'<h3>(.*?)</h3>', card, re.S).group(1)) for card in cards]
    assert timeline_names == card_names
    assert html.index('tl-item latest') < html.index('<div class="tl-date">2026-07-12</div>')


def test_v5_card_grid_spotlight_and_motion_contracts():
    html = SITE.read_text(encoding="utf-8")

    # Responsive card grid: 3 columns -> 2 -> 1.
    assert '.sites{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))' in html
    assert '.sites{grid-template-columns:repeat(2,minmax(0,1fr))}' in html
    assert '.sites{grid-template-columns:1fr;gap:16px;padding:16px}' in html

    # Spotlight layout for the lead card.
    assert '.site:first-child{grid-column:1/-1;display:grid' in html

    # Hover lift + gradient accent + image zoom.
    assert '.site:hover{background:#fffef8;border-color:rgba(92,107,18,.55);translate:0 -5px' in html
    assert '.site:hover:after{opacity:1}' in html
    assert '.site:hover .site-shot img{transform:scale(1.05)}' in html

    # Scroll-in reveal wired through the existing motion observer.
    assert "var nodes=document.querySelectorAll('.reveal,.site');" in html
    assert 'html.js .site{opacity:0;transform:translateY(30px)}' in html
    assert 'html.js .site.in{opacity:1;transform:none}' in html

    # prefers-reduced-motion keeps every card visible and calm
    # (the v5 block is the last such media query, appended before </style>).
    reduced_start = html.rindex('@media(prefers-reduced-motion:reduce){')
    reduced_css = html[reduced_start:html.index('</style>', reduced_start)]
    assert 'html.js .site{opacity:1;transform:none}' in reduced_css
    assert '.site:hover{translate:none}' in reduced_css
    assert '.site:hover .site-shot img{transform:none}' in reduced_css

    # Newest-first hint next to the ledger subhead.
    assert 'Every release leaves a trail · 最新在前' in html

    # Card DOM anchor stays byte-identical for every assertion downstream.
    assert html.count('<article class="site" data-status="live">') == 32
    assert html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 32
