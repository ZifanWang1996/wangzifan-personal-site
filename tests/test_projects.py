import hashlib
import json
import re
import subprocess
import sys
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image

from scripts.build_v11 import render_ledger, render_structured_data


ROOT = Path(__file__).parents[1]
SITE = ROOT / "index.html"
PRIVACY = ROOT / "privacy.html"
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-pages.yml"
REGISTRY = ROOT / "data" / "projects.json"
PROJECT_CONTROL = ROOT / "project-control.md"


def contrast_ratio(first: str, second: str) -> float:
    def luminance(value: str) -> float:
        channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
            for channel in channels
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.images = []
        self.local_refs = []
        self.inline_handlers = []
        self.blank_links = []
        self.unsafe_blank_links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "img":
            self.images.append(attributes)
        if tag == "a" and attributes.get("target") == "_blank":
            href = attributes.get("href", "")
            self.blank_links.append(href)
            rel_tokens = set((attributes.get("rel") or "").split())
            if not {"noopener", "noreferrer"}.issubset(rel_tokens):
                self.unsafe_blank_links.append(href)
        for name, value in attrs:
            if name.startswith("on"):
                self.inline_handlers.append(name)
            if name in {"href", "src"} and value and not value.startswith(
                ("http://", "https://", "#", "mailto:")
            ):
                self.local_refs.append(value.split("#", 1)[0].split("?", 1)[0])


def test_tracked_public_candidate_matches_deterministic_builder(tmp_path):
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_v11.py"),
            "--output",
            str(tmp_path / "index.html"),
            "--privacy-output",
            str(tmp_path / "privacy.html"),
        ],
        cwd=ROOT,
        check=True,
    )
    for relative in (
        "index.html",
        "privacy.html",
        "assets/site.css",
        "assets/site.js",
        "assets/og-card.webp",
    ):
        assert (ROOT / relative).read_bytes() == (tmp_path / relative).read_bytes(), relative


def test_registry_assets_are_complete_lightweight_and_fixed_size():
    projects = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources = [project["image"] for project in projects]
    assert len(sources) == len(set(sources)) == 42
    for source in sources:
        image_path = ROOT / source
        assert image_path.is_file(), source
        assert image_path.suffix == ".webp"
        assert image_path.stat().st_size < 80_000
        with Image.open(image_path) as image:
            assert image.size == (400, 250), source
            assert image.format == "WEBP"


def test_parrygrid_project_41_contract():
    projects = json.loads(REGISTRY.read_text(encoding="utf-8"))
    parrygrid = next((project for project in projects if project["id"] == 41), None)
    assert parrygrid is not None
    assert parrygrid == {
        "id": 41,
        "name": "ParryGrid",
        "url": "https://parrygrid.wiki/",
        "category": "game",
        "subtitle": "ARPG 与 Soulslike 情报网格",
        "summary": "面向动作角色扮演与 Soulslike 玩家的一站式多语言情报站，提供版本信号、构筑、强度排行、游戏对比、故障排查和浏览器本地规划工具。",
        "problem": "补丁变化、构筑选择、强度排行、跨游戏比较和技术排障信息分散，玩家难以快速判断当前版本下一步该做什么。",
        "solution": "把五款游戏的可核验版本信号、指南、比较与本地决策工具组织成按问题推进的多语言情报网格。",
        "evidence": "公开站点可直接验证 5 个游戏、9 个语言根、46 个子 sitemap 与 202 个唯一 URL，以及版本信号、构筑、强度排行、对比、故障排查和浏览器本地工具。",
        "launched_at": "2026-09-12",
        "status": "live",
        "image": "assets/projects/project-41.webp",
        "featured": False,
        "featured_order": None,
    }

    image_path = ROOT / parrygrid["image"]
    assert image_path.is_file()
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == (
        "ee08c435f6a807e181e30e0d44dc95c6243556b1bd21670111f0377b9c0a8aa6"
    )


def test_1666_amsterdam_field_desk_project_42_contract():
    projects = json.loads(REGISTRY.read_text(encoding="utf-8"))
    amsterdam = next((project for project in projects if project["id"] == 42), None)
    assert amsterdam is not None
    assert amsterdam == {
        "id": 42,
        "name": "1666 Amsterdam Field Desk",
        "url": "https://1666amsterdam.top/",
        "category": "game",
        "subtitle": "《1666: Amsterdam》三语攻略与排障工作台",
        "summary": "面向《1666: Amsterdam》抢先体验玩家的英中荷三语资料站，把任务、谜题、性能与报错排障整理成可搜索的 31 条指南。",
        "problem": "抢先体验期的官方信息、玩家报告与任务线索分散，玩家很难确认下一步，并区分事实、传闻和安全排障建议。",
        "solution": "用来源分级和最近核验日期组织 31 条指南，再加入本地收藏与已读、搜索筛选、PC 需求比较和故障分诊工具。",
        "evidence": "公开站点可直接验证英语、简体中文、荷兰语入口、117 条 sitemap URL、每语 31 条指南，以及浏览器本地收藏与已读、PC 需求比较、Fix My Game 分诊和 Roadmap Decoder。",
        "launched_at": "2026-09-12",
        "status": "live",
        "image": "assets/projects/project-42.webp",
        "featured": False,
        "featured_order": None,
    }

    image_path = ROOT / amsterdam["image"]
    assert image_path.is_file()
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == (
        "9539fb2ca4cbea657b58c70b19351dab9581f62ed2daeb9880111a6f811ef096"
    )


def test_project_control_product_index_matches_registry():
    projects = json.loads(REGISTRY.read_text(encoding="utf-8"))
    control = PROJECT_CONTROL.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## 产品索引（(\d+)）$", control, re.MULTILINE))
    assert len(headings) == 1

    heading = headings[0]
    assert int(heading.group(1)) == len(projects)
    table = control[heading.end():].split("\n## ", 1)[0]
    table_ids = re.findall(r"^\|\s*(\d+)\s*\|", table, re.MULTILINE)
    expected_ids = [f"{project['id']:02d}" for project in projects]
    assert table_ids == expected_ids


def test_current_browser_acceptance_docs_match_registry():
    projects = json.loads(REGISTRY.read_text(encoding="utf-8"))
    latest = projects[-1]
    control = PROJECT_CONTROL.read_text(encoding="utf-8")
    current = control.split("## 浏览器验收", 1)[1].split("## 隐私与内容边界", 1)[0]

    assert f"{len(projects)} 条展开" in current
    assert f"{len(projects)} 条档案全部可读" in current
    assert f"{latest['name']} 搜索唯一命中 #{latest['id']}" in current
    assert (
        f"`project-01.webp` 至 `project-{latest['id']:02d}.webp`，"
        f"不接受任意 {len(projects)} 个 WebP"
    ) in current


def test_qr_font_favicon_and_social_card_are_publishable():
    qr = ROOT / "assets" / "wechat-qr.webp"
    font = ROOT / "assets" / "archivo.woff2"
    favicon = ROOT / "favicon.svg"
    social = ROOT / "assets" / "og-card.webp"
    assert qr.is_file() and qr.stat().st_size < 80_000
    assert font.is_file() and font.stat().st_size < 200_000
    assert favicon.is_file() and "<svg" in favicon.read_text(encoding="utf-8")
    with Image.open(qr) as image:
        assert image.size == (560, 560)
    with Image.open(social) as image:
        assert image.size == (1200, 630)


def test_generated_pages_have_valid_local_refs_and_basic_accessibility():
    for page in (SITE, PRIVACY):
        parser = AuditParser()
        parser.feed(page.read_text(encoding="utf-8"))
        assert len(parser.ids) == len(set(parser.ids)), f"duplicate id in {page.name}"
        assert not parser.inline_handlers
        assert not parser.unsafe_blank_links
        for image in parser.images:
            assert image.get("alt", "").strip()
            assert image.get("width") and image.get("height")
        for reference in parser.local_refs:
            if not reference or reference == "index.html":
                continue
            assert (ROOT / reference).exists(), f"{page.name}: missing {reference}"


def test_builder_escapes_adversarial_registry_values_and_json_ld():
    projects = deepcopy(json.loads(REGISTRY.read_text(encoding="utf-8")))
    payload = '\"><script>alert(1)</script><img src=x onerror="alert(2)'
    for project in projects:
        if project["id"] in {20, 33}:
            project["name"] = payload
            project["subtitle"] = payload
            project["url"] = f'https://example.com/?q={payload}'
            project["image"] = f'assets/projects/{payload}.webp'

    fragment = render_ledger(projects)
    parser = AuditParser()
    parser.feed(fragment)
    assert not parser.inline_handlers
    assert not parser.unsafe_blank_links
    assert "<script>" not in fragment
    assert "onerror=\"alert(2)\"" not in fragment

    structured = render_structured_data(projects)
    assert "<" not in structured
    assert "\\u003cscript>" in structured


def test_homepage_truth_and_link_security_match_registry():
    html = SITE.read_text(encoding="utf-8")
    assert html.count('data-ledger-id="') == 42
    assert html.count('data-ledger-status="live"') == 41
    assert html.count('data-ledger-status="offline"') == 1
    assert 'data-ledger-id="24"' in html and "Polski Piłkarz Simulator" in html
    # Each online product appears once; the offline project has no outbound link.
    expected_safe_external_links = 41
    parser = AuditParser()
    parser.feed(html)
    assert len(parser.blank_links) == expected_safe_external_links
    assert not parser.unsafe_blank_links
    for stale in ("WZF PRESS", "LAUNCH CONSOLE", "T-MINUS", "SHIPS LIVE"):
        assert stale not in html
    assert "<canvas" not in html and "requestAnimationFrame" not in html


def test_css_has_responsive_focus_motion_and_overflow_contracts():
    css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
    for token in ("--bg:", "--ink:", "--accent:", "--navy:", "--max:"):
        assert token in css
    assert "@media (max-width: 1100px)" in css
    assert "@media (max-width: 760px)" in css
    assert ":focus-visible" in css
    assert "overflow-wrap: anywhere" in css
    assert "overflow-x: hidden" not in css
    assert "prefers-reduced-motion" in css
    assert re.search(r"\[hidden\]\s*\{\s*display:\s*none\s*!important", css)


def test_accent_supports_wcag_aa_normal_text():
    css = (ROOT / "src" / "styles.css").read_text(encoding="utf-8")
    match = re.search(r"--accent:\s*(#[0-9a-fA-F]{6})", css)
    assert match is not None
    accent = match.group(1)
    assert contrast_ratio("#ffffff", accent) >= 4.5
    assert contrast_ratio("#fcfbf7", accent) >= 4.5


def test_privacy_and_analytics_are_consistent():
    html = SITE.read_text(encoding="utf-8")
    privacy = PRIVACY.read_text(encoding="utf-8")
    script = '<script defer data-domain="wangzifan.store" src="https://plausible.shipsolo.io/js/script.js"></script>'
    assert html.count(script) == privacy.count(script) == 1
    for disclosure in (
        "Plausible Analytics",
        "plausible.shipsolo.io",
        "不设置分析 Cookie",
        "不进行跨站跟踪",
        "GitHub Pages",
        "wang1227928718",
    ):
        assert disclosure in privacy


def test_workflow_builds_and_tests_before_exact_allowlist_upload():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    for gate in (
        "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
        "pip install -r requirements-ci.txt",
        "python -m playwright install --with-deps chromium",
        "python scripts/build_v11.py",
        "git diff --exit-code -- index.html privacy.html assets/site.css assets/site.js assets/og-card.webp",
        "python -m pytest -q",
        "node tests/browser_interactions.mjs",
        "python -m compileall -q scripts tests",
        "python scripts/prepare_public_artifact.py --output _site",
        "python scripts/accept_v11.py --site-dir _site --evidence-dir _qa/v11",
    ):
        assert gate in workflow
    assert workflow.index("python scripts/build_v11.py") < workflow.index("git diff --exit-code")
    assert workflow.index("git diff --exit-code") < workflow.index("python -m pytest -q")
    assert workflow.index("python -m pytest -q") < workflow.index(
        "python scripts/prepare_public_artifact.py"
    )
    assert workflow.index("python scripts/prepare_public_artifact.py") < workflow.index(
        "python scripts/accept_v11.py"
    )
    assert workflow.index("python scripts/accept_v11.py") < workflow.index(
        "name: Upload Pages artifact"
    )
    assert "path: _site" in workflow and "path: ." not in workflow

    manifest = (ROOT / "scripts" / "prepare_public_artifact.py").read_text(encoding="utf-8")
    for public_path in (
        '"index.html"',
        '"privacy.html"',
        '"favicon.svg"',
        '"assets/site.css"',
        '"assets/site.js"',
        '"assets/og-card.webp"',
        '"assets/archivo.woff2"',
        '"assets/wechat-qr.webp"',
    ):
        assert public_path in manifest
    assert 'glob("*.webp")' not in manifest
    assert 'f"assets/projects/project-{project_id:02d}.webp"' in manifest
    assert "for project_id in range(1, 43)" in manifest
    assert "PUBLIC_PATHS = STATIC_PUBLIC_PATHS + PROJECT_PUBLIC_PATHS" in manifest
    assert "if output.exists()" in manifest
    assert "if actual != expected_relative" in manifest


def test_build_sources_and_registry_are_not_referenced_as_public_assets():
    manifest = (ROOT / "scripts" / "prepare_public_artifact.py").read_text(encoding="utf-8")
    static_block = manifest.split("STATIC_PUBLIC_PATHS = (", 1)[1].split(")", 1)[0]
    for private_source in ("data/projects.json", "src/", "scripts/", "tests/", ".hermes/"):
        assert private_source not in static_block
