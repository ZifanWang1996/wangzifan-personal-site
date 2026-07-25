from pathlib import Path


SITE = Path(__file__).parents[1] / "index.html"


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
    assert html.count('data-status="live"') == 7
    assert html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 7
