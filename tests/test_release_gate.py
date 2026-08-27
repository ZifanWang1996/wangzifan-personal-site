import hashlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.prepare_public_artifact import STATIC_PUBLIC_PATHS, public_files


ROOT = Path(__file__).resolve().parents[1]


def test_public_artifact_is_exact_allowlist(tmp_path):
    output = tmp_path / "_site"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "prepare_public_artifact.py"), "--output", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    files = sorted(path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file())
    assert len(files) == 41
    assert set(files[:0]) == set()
    assert {"index.html", "privacy.html", "favicon.svg"}.issubset(files)
    assert {
        "assets/site.css",
        "assets/site.js",
        "assets/og-card.webp",
        "assets/archivo.woff2",
        "assets/wechat-qr.webp",
    }.issubset(files)
    assert len([path for path in files if path.startswith("assets/projects/")]) == 33
    assert not any(
        part in {"src", "data", "tests", "scripts", ".hermes", ".git", ".github"}
        for path in files
        for part in Path(path).parts
    )
    assert "public artifact: 41 files" in completed.stdout
    assert "candidate sha256=" in completed.stdout

    reused = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "prepare_public_artifact.py"), "--output", str(output)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert reused.returncode != 0
    assert "refusing to reuse existing artifact directory" in reused.stderr


def test_pages_workflow_separates_quality_from_main_only_deploy():
    workflow = (ROOT / ".github" / "workflows" / "deploy-pages.yml").read_text(encoding="utf-8")
    assert "pull_request:" in workflow
    assert "quality:" in workflow
    assert "deploy:" in workflow
    assert "needs: quality" in workflow
    assert "github.event_name == 'push'" in workflow
    assert "github.ref == 'refs/heads/main'" in workflow
    assert "python-version: '3.12'" in workflow
    assert "node-version: '22'" in workflow
    assert "pip install -r requirements-ci.txt" in workflow
    assert "playwright install --with-deps chromium" in workflow
    assert "group: pages-${{ github.event_name }}-${{ github.ref }}" in workflow
    assert "git diff --exit-code -- index.html privacy.html assets/site.css assets/site.js assets/og-card.webp" in workflow
    assert "python scripts/prepare_public_artifact.py --output _site" in workflow
    assert (
        "python scripts/accept_v11.py --site-dir _site --evidence-dir _qa/v11"
        in workflow
    )
    action_refs = re.findall(r"uses:\s+[^@\s]+@([^\s]+)", workflow)
    assert len(action_refs) == 6
    assert all(re.fullmatch(r"[0-9a-f]{40}", reference) for reference in action_refs)
    assert "actions/upload-pages-artifact@7b1f4a764d45c48632c6b24a0339c27f5614fb0b" in workflow
    assert "actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e" in workflow

    accept = (ROOT / "scripts" / "accept_v11.py").read_text(encoding="utf-8")
    assert "target height below 44px" in accept
    assert "320px primary CTA is not fully visible" in accept


def test_public_allowlist_rejects_symlink_sources(tmp_path):
    source_root = tmp_path / "source"
    for relative in STATIC_PUBLIC_PATHS:
        path = source_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"public")
    projects = source_root / "assets" / "projects"
    projects.mkdir(parents=True, exist_ok=True)
    for project_id in range(1, 34):
        (projects / f"project-{project_id:02d}.webp").write_bytes(b"image")

    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"must not be copied")
    index = source_root / "index.html"
    index.unlink()
    index.symlink_to(outside)

    with pytest.raises(ValueError, match="symlink"):
        public_files(source_root)


def test_social_card_uses_repository_pinned_font():
    builder = (ROOT / "scripts" / "build_v11.py").read_text(encoding="utf-8")
    font = ROOT / "src" / "fonts" / "DejaVuSans-Bold.ttf"
    license_file = ROOT / "src" / "fonts" / "DEJAVU-LICENSE.txt"

    assert "/usr/share/fonts" not in builder
    assert 'ROOT / "src" / "fonts" / "DejaVuSans-Bold.ttf"' in builder
    assert hashlib.sha256(font.read_bytes()).hexdigest() == (
        "5c1247acef7f2b8522a31742c76d6adcb5569bacc0be7ceaa4dc39dd252ce895"
    )
    assert "Copyright (c) 2003 by Bitstream" in license_file.read_text(encoding="utf-8")
