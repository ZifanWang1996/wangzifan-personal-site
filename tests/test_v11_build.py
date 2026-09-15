import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image


ROOT = Path(__file__).parents[1]
REGISTRY = ROOT / "data" / "projects.json"


def load_projects():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_registry_includes_live_genvid_atlas_release():
    projects = load_projects()
    genvid = next((project for project in projects if project["id"] == 34), None)

    assert genvid is not None
    assert genvid["name"] == "GenVid Atlas"
    assert genvid["url"] == "https://genvidatlas.wiki/"
    assert genvid["category"] == "ai"
    assert genvid["subtitle"] == "AI 视频模型与价格情报站"
    assert genvid["launched_at"] == "2026-09-06"
    assert genvid["status"] == "live"
    assert genvid["image"] == "assets/projects/project-34.webp"
    assert genvid["featured"] is False
    assert genvid["featured_order"] is None


def test_registry_includes_live_dawnwalker_field_guide_release():
    projects = load_projects()
    dawnwalker = next((project for project in projects if project["id"] == 35), None)

    assert dawnwalker is not None
    assert dawnwalker["name"] == "Dawnwalker Field Guide"
    assert dawnwalker["url"] == "https://thebloodofdawnwalker.info/"
    assert dawnwalker["category"] == "game"
    assert dawnwalker["subtitle"] == "Dawnwalker 攻略与旅程规划"
    assert dawnwalker["launched_at"] == "2026-09-09"
    assert dawnwalker["status"] == "live"
    assert dawnwalker["image"] == "assets/projects/project-35.webp"
    assert dawnwalker["featured"] is False
    assert dawnwalker["featured_order"] is None


def test_registry_includes_live_onimusha_atlas_release():
    projects = load_projects()
    onimusha = next((project for project in projects if project["id"] == 36), None)

    assert onimusha is not None
    assert onimusha["name"] == "Onimusha Atlas"
    assert onimusha["url"] == "https://onimushawayofthesword.space/"
    assert onimusha["category"] == "game"
    assert onimusha["subtitle"] == "鬼武者攻略与玩家日志"
    assert onimusha["launched_at"] == "2026-09-09"
    assert onimusha["status"] == "live"
    assert onimusha["image"] == "assets/projects/project-36.webp"
    assert onimusha["featured"] is False
    assert onimusha["featured_order"] is None


def test_registry_includes_live_astra_atlas_release():
    projects = load_projects()
    astra = next((project for project in projects if project["id"] == 37), None)

    assert astra is not None
    assert astra["name"] == "Astra Atlas"
    assert astra["url"] == "https://gpt6astra.best/"
    assert astra["category"] == "ai"
    assert astra["subtitle"] == "GPT-6 Astra 价格与选型指南"
    assert astra["launched_at"] == "2026-09-09"
    assert astra["status"] == "live"
    assert astra["image"] == "assets/projects/project-37.webp"
    assert astra["featured"] is False
    assert astra["featured_order"] is None


def test_registry_includes_live_narinig_mo_ba_guide_release():
    projects = load_projects()
    narinig = next((project for project in projects if project["id"] == 38), None)

    assert narinig is not None
    assert narinig["name"] == "Narinig Mo Ba? Guide"
    assert narinig["url"] == "https://narinigmoba.top/"
    assert narinig["category"] == "game"
    assert narinig["subtitle"] == "菲律宾恐怖游戏轻剧透攻略站"
    assert narinig["launched_at"] == "2026-09-11"
    assert narinig["status"] == "live"
    assert narinig["image"] == "assets/projects/project-38.webp"
    assert narinig["featured"] is False
    assert narinig["featured_order"] is None


def test_registry_includes_live_nightfall_halloween_guides_release():
    projects = load_projects()
    halloween = next((project for project in projects if project["id"] == 39), None)

    assert halloween is not None
    assert halloween["name"] == "Nightfall Halloween Guides"
    assert halloween["url"] == "https://halloweenthegame.top/"
    assert halloween["category"] == "game"
    assert halloween["subtitle"] == "《Halloween: The Game》三语生存攻略站"
    assert halloween["launched_at"] == "2026-09-12"
    assert halloween["status"] == "live"
    assert halloween["image"] == "assets/projects/project-39.webp"
    assert halloween["featured"] is False
    assert halloween["featured_order"] is None


def test_registry_includes_live_mimic_party_soundcheck_release():
    projects = load_projects()
    mimic = next((project for project in projects if project["id"] == 40), None)

    assert mimic is not None
    assert mimic["name"] == "Mimic Party Soundcheck"
    assert mimic["url"] == "https://mimicparty.space/"
    assert mimic["category"] == "game"
    assert mimic["subtitle"] == "《Mimic Party》四语玩家指南与派对工具站"
    assert mimic["launched_at"] == "2026-09-12"
    assert mimic["status"] == "live"
    assert mimic["image"] == "assets/projects/project-40.webp"
    assert mimic["featured"] is False
    assert mimic["featured_order"] is None


def test_v11_registry_has_complete_truthful_project_contract():
    projects = load_projects()

    required = {
        "id",
        "name",
        "url",
        "category",
        "subtitle",
        "summary",
        "problem",
        "solution",
        "evidence",
        "launched_at",
        "status",
        "image",
        "featured",
        "featured_order",
    }
    assert len(projects) == 45
    assert [project["id"] for project in projects] == list(range(1, 46))
    assert len({project["url"] for project in projects}) == 45
    assert sum(project["status"] == "live" for project in projects) == 44
    assert sum(project["status"] == "offline" for project in projects) == 1
    assert sum(project["featured"] for project in projects) == 3
    assert sorted(
        project["featured_order"] for project in projects if project["featured"]
    ) == list(range(1, 4))
    assert all(
        project["featured_order"] is None
        for project in projects
        if not project["featured"]
    )
    assert {
        project["id"] for project in projects if project["featured"]
    } == {9, 20, 22}

    for project in projects:
        assert required == set(project)
        assert project["category"] in {"ai", "game", "tool", "creative"}
        assert project["status"] in {"live", "offline", "archived"}
        assert urlparse(project["url"]).scheme == "https"
        assert urlparse(project["url"]).netloc
        assert date.fromisoformat(project["launched_at"])
        assert (ROOT / project["image"]).is_file()
        for field in ("name", "subtitle", "summary", "problem", "solution", "evidence"):
            assert project[field].strip()

    offline = next(project for project in projects if project["id"] == 24)
    assert offline["name"] == "Polski Piłkarz Simulator"
    assert offline["status"] == "offline"


def test_v11_registry_keeps_release_dates_monotonic():
    projects = load_projects()
    dates = [date.fromisoformat(project["launched_at"]) for project in projects]
    assert dates == sorted(dates)


def test_build_v11_generates_truthful_identity_and_counts(tmp_path):
    output = tmp_path / "index.html"
    command = [
        sys.executable,
        str(ROOT / "scripts" / "build_v11.py"),
        "--output",
        str(output),
    ]

    subprocess.run(command, cwd=ROOT, check=True)
    first = output.read_bytes()
    subprocess.run(command, cwd=ROOT, check=True)
    second = output.read_bytes()
    html = first.decode("utf-8")

    assert first == second
    assert "OPC 一人公司创业者" in html
    assert "一个人开局，把想法做成生意。" in html
    assert '<span class="title-line">一个人开局，</span>' in html
    assert '<span class="title-line"><em>把想法做成生意。</em></span>' in html
    assert 'data-hero-latest' not in html
    assert 'id="recent"' not in html
    assert 'id="selected"' not in html
    assert "1666 Amsterdam Field Desk" in html
    assert 'href="https://1666amsterdam.top/"' in html
    assert "2026-09-12" in html
    assert '<main id="main-content" tabindex="-1">' in html
    assert 'data-status="releases">45 条公开记录' in html
    assert 'data-status="live">44 条在线记录' in html
    assert 'data-status="offline">1 条离线记录' in html
    for retired in (
        "WZF PRESS",
        "LAUNCH CONSOLE",
        "T-MINUS",
        "SHIPS LIVE",
        "WZF / ONE-PERSON PRODUCT STUDIO",
        "不是传统简历，也不是项目数量墙",
        "问题、解法、证据，三件事讲清楚",
        "一个人，把具体问题做成真正能用的产品",
    ):
        assert retired not in html


def test_build_renders_one_complete_visual_product_wall(tmp_path):
    output = tmp_path / "index.html"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_v11.py"), "--output", str(output)], cwd=ROOT, check=True)
    html = output.read_text(encoding="utf-8")
    assert 'data-latest-card' not in html
    assert 'data-featured-card' not in html
    assert html.count('class="project-window"') == 45
    assert html.count('class="project-number"') == 45
    for project in load_projects():
        row = re.search(rf'<article[^>]+data-ledger-id="{project["id"]}".*?</article>', html, re.S).group()
        assert project["name"] in row
        assert project["subtitle"] in row
        assert f'src="{project["image"]}"' in row
        assert (f'href="{project["url"]}"' in row) == (project["status"] == "live")
    assert 'data-view="wall" aria-pressed="true"' in html
    assert 'data-view="list" aria-pressed="false"' in html


def test_build_v11_closes_collaboration_method_ledger_and_contact_flow(tmp_path):
    output = tmp_path / "index.html"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_v11.py"), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )
    html = output.read_text(encoding="utf-8")

    ordered_ids = ("top", "ledger", "method", "about", "contact")
    positions = [html.index(f'id="{section_id}"') for section_id in ordered_ids]
    assert positions == sorted(positions)

    assert html.count('data-method-note="') == 3
    assert 'data-method-step="' not in html
    assert "公司的行动力" in html
    for habit in ("从需求出发，不等万事俱备", "让 AI 放大一个人的行动力", "先上线，再用反馈走下一步"):
        assert habit in html
    assert html.count('data-ledger-id="') == 45
    ledger_positions = [html.index(f'data-ledger-id="{project_id}"') for project_id in range(45, 0, -1)]
    assert ledger_positions == sorted(ledger_positions)
    assert html.count('data-ledger-status="live"') == 44
    assert html.count('data-ledger-status="offline"') == 1

    offline_row = re.search(
        r'<article[^>]+data-ledger-id="24".*?</article>', html, re.S
    )
    assert offline_row is not None
    assert 'href="https://polskipilkarzsymulator.online/"' not in offline_row.group()
    assert "离线记录" in offline_row.group()

    for category in ("all", "ai", "game", "tool", "creative"):
        assert f'data-ledger-filter="{category}"' in html
    assert 'id="ledger-search"' in html
    assert 'id="ledger-status"' in html
    assert 'id="ledger-count" aria-live="polite">45 / 45' in html
    assert "这个页面记录着 45 次公开上线" in html
    assert 'class="ledger-tools" hidden' in html
    assert 'class="ledger-empty" id="ledger-empty" role="status" hidden' in html
    assert "没有匹配记录，试试别的关键词或筛选。" in html
    assert 'class="button ledger-more" type="button" id="ledger-more" hidden' in html

    assert html.count('href="#contact"') >= 3
    assert 'src="assets/wechat-qr.webp"' in html
    assert 'class="button copy-button" type="button" hidden' in html
    assert 'alt="王子凡微信二维码，微信号 wang1227928718"' in html
    assert 'data-copy-value="wang1227928718"' in html
    assert "一人公司、AI 产品或出海项目" in html and "真实用户" in html
    assert "不承诺虚构增长" not in html
    assert "<canvas" not in html
    assert "requestAnimationFrame" not in html
    for decorative_heading in (
        "RECENT RELEASES",
        "SELECTED WORK",
        "COLLABORATION",
        "WORKING METHOD",
        "RELEASE LEDGER",
        "FOUNDER NOTE",
        "WECHAT / DIRECT CONTACT",
    ):
        assert decorative_heading not in html


def test_build_v11_generates_shared_assets_seo_and_privacy_page(tmp_path):
    output = tmp_path / "index.html"
    privacy = tmp_path / "privacy.html"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_v11.py"),
            "--output",
            str(output),
            "--privacy-output",
            str(privacy),
        ],
        cwd=ROOT,
        check=True,
    )

    html = output.read_text(encoding="utf-8")
    privacy_html = privacy.read_text(encoding="utf-8")
    css = (tmp_path / "assets" / "site.css")
    javascript = (tmp_path / "assets" / "site.js")
    social_image = tmp_path / "assets" / "og-card.webp"

    assert css.read_bytes() == (ROOT / "src" / "styles.css").read_bytes()
    css_text = css.read_text(encoding="utf-8")
    assert 'src: url("archivo.woff2") format("woff2")' in css_text
    assert 'url("assets/archivo.woff2")' not in css_text
    # Responsive behavior is exercised by the existing browser acceptance matrix;
    # keep the source contract independent of one design's exact column widths.
    for breakpoint in (1100, 900, 760, 380):
        assert f"@media (max-width: {breakpoint}px)" in css_text
    assert "prefers-reduced-motion" in css_text
    assert "overflow-wrap: anywhere" in css_text
    assert "object-fit: contain" in css_text
    assert javascript.read_bytes() == (ROOT / "src" / "site.js").read_bytes()
    assert "<style" not in html and "<style" not in privacy_html
    assert '<link rel="stylesheet" href="assets/site.css">' in html
    assert '<script defer src="assets/site.js"></script>' in html
    assert "requestAnimationFrame" not in javascript.read_text(encoding="utf-8")
    assert Image.open(social_image).size == (1200, 630)
    builder_source = (ROOT / "scripts" / "build_v11.py").read_text(encoding="utf-8")
    assert '"33 RELEASE RECORDS"' not in builder_source
    assert '"32 ONLINE  /  1 OFFLINE"' not in builder_source
    assert "33 条历史发布记录" not in builder_source
    assert ">33 / 33<" not in builder_source
    assert "查看全部 33 条记录" not in builder_source

    assert '<link rel="canonical" href="https://wangzifan.store/">' in html
    assert '<meta property="og:url" content="https://wangzifan.store/">' in html
    assert '<meta property="og:image" content="https://wangzifan.store/assets/og-card.webp">' in html
    assert '<meta property="og:image:type" content="image/webp">' in html
    assert '<meta property="og:image:alt" content="王子凡的个人产品工作台分享图">' in html
    assert 'data-domain="wangzifan.store" src="https://plausible.shipsolo.io/js/script.js"' in html
    graph_match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    )
    assert graph_match is not None
    graph = json.loads(graph_match.group(1))["@graph"]
    assert {node["@type"] for node in graph} == {"Person", "WebSite", "ItemList"}
    release_list = next(node for node in graph if node["@type"] == "ItemList")
    assert release_list["numberOfItems"] == 45
    assert len(release_list["itemListElement"]) == 45
    structured_statuses = [
        item["item"]["additionalProperty"]["value"]
        for item in release_list["itemListElement"]
    ]
    assert structured_statuses.count("live") == 44
    assert structured_statuses.count("offline") == 1

    assert '<link rel="canonical" href="https://wangzifan.store/privacy.html">' in privacy_html
    for social_contract in (
        '<meta property="og:title" content="隐私说明 — ZF Wang">',
        '<meta property="og:url" content="https://wangzifan.store/privacy.html">',
        '<meta property="og:image" content="https://wangzifan.store/assets/og-card.webp">',
        '<meta property="og:image:type" content="image/webp">',
        '<meta property="og:image:alt" content="王子凡的个人产品工作台分享图">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:image" content="https://wangzifan.store/assets/og-card.webp">',
    ):
        assert social_contract in privacy_html
    assert "隐私，直接说清楚。" in privacy_html
    assert '<main class="privacy-main" id="privacy-content" tabindex="-1">' in privacy_html
    assert "最近更新：2026-08-28" in privacy_html
    for disclosure in (
        "Plausible Analytics",
        "不设置分析 Cookie",
        "不进行跨站跟踪",
        "GitHub Pages",
        "wang1227928718",
    ):
        assert disclosure in privacy_html
