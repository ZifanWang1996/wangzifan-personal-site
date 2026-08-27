import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parents[1]
SITE = ROOT / "index.html"
PRIVACY = ROOT / "privacy.html"
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-pages.yml"
REGISTRY = ROOT / "data" / "projects.json"


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

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "img":
            self.images.append(attributes)
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
    assert len(sources) == len(set(sources)) == 33
    for source in sources:
        image_path = ROOT / source
        assert image_path.is_file(), source
        assert image_path.suffix == ".webp"
        assert image_path.stat().st_size < 80_000
        with Image.open(image_path) as image:
            assert image.size == (400, 250), source
            assert image.format == "WEBP"


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
        for image in parser.images:
            assert image.get("alt", "").strip()
            assert image.get("width") and image.get("height")
        for reference in parser.local_refs:
            if not reference or reference == "index.html":
                continue
            assert (ROOT / reference).exists(), f"{page.name}: missing {reference}"


def test_homepage_truth_and_link_security_match_registry():
    html = SITE.read_text(encoding="utf-8")
    assert html.count('data-ledger-id="') == 33
    assert html.count('data-ledger-status="live"') == 32
    assert html.count('data-ledger-status="offline"') == 1
    assert 'data-ledger-id="24"' in html and "Polski Piłkarz Simulator" in html
    expected_safe_external_links = (3 * 2) + 6 + 32
    assert html.count('target="_blank" rel="noopener noreferrer"') == expected_safe_external_links
    for stale in ("WZF PRESS", "LAUNCH CONSOLE", "T-MINUS", "SHIPS LIVE"):
        assert stale not in html
    assert "<canvas" not in html and "requestAnimationFrame" not in html


def test_css_has_responsive_focus_motion_and_overflow_contracts():
    css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
    for token in ("--bg:", "--ink:", "--accent:", "--navy:", "--max:"):
        assert token in css
    assert "@media (max-width: 1000px)" in css
    assert "@media (max-width: 760px)" in css
    assert ":focus-visible" in css
    assert "overflow-wrap: anywhere" in css
    assert "overflow-x: hidden" not in css
    assert "prefers-reduced-motion" in css
    assert "[hidden] { display: none !important; }" in css


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
    assert 'glob("*.webp")' in manifest
    assert "len(project_images) != 33" in manifest
    assert "if output.exists()" in manifest
    assert "if actual != expected_relative" in manifest


def test_build_sources_and_registry_are_not_referenced_as_public_assets():
    manifest = (ROOT / "scripts" / "prepare_public_artifact.py").read_text(encoding="utf-8")
    static_block = manifest.split("STATIC_PUBLIC_PATHS = (", 1)[1].split(")", 1)[0]
    for private_source in ("data/projects.json", "src/", "scripts/", "tests/", ".hermes/"):
        assert private_source not in static_block
