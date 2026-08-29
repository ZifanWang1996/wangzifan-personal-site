import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.accept_v11 import assert_artifact_closure
from scripts.prepare_public_artifact import (
    PROJECT_PUBLIC_PATHS,
    STATIC_PUBLIC_PATHS,
    public_files,
)


ROOT = Path(__file__).resolve().parents[1]


def test_local_candidate_and_qa_evidence_are_gitignored():
    patterns = {
        line.strip()
        for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert {"_site/", "_qa/"}.issubset(patterns)


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
    expected = set(STATIC_PUBLIC_PATHS + PROJECT_PUBLIC_PATHS)
    assert len(files) == 41
    assert set(files) == expected
    assert not any(
        part in {"src", "data", "tests", "scripts", ".hermes", ".git", ".github"}
        for path in files
        for part in Path(path).parts
    )
    assert "public artifact: 41 files" in completed.stdout
    assert "candidate sha256=" in completed.stdout
    assert len(assert_artifact_closure(output)) == 41

    injected = output / "debug.txt"
    injected.write_text("must fail closed", encoding="utf-8")
    with pytest.raises(ValueError, match=r"extra=\['debug.txt'\]"):
        assert_artifact_closure(output)
    injected.unlink()

    reused = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "prepare_public_artifact.py"), "--output", str(output)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert reused.returncode != 0
    assert "refusing to reuse existing artifact directory" in reused.stderr


def test_public_allowlist_rejects_renamed_project_image_even_when_count_stays_33(tmp_path):
    source = tmp_path / "source"
    for original in public_files(ROOT):
        relative = original.relative_to(ROOT)
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, target)

    expected_image = source / "assets/projects/project-33.webp"
    expected_image.rename(source / "assets/projects/private-review-evidence.webp")

    with pytest.raises(FileNotFoundError, match="project-33.webp"):
        public_files(source)


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
    expected_actions = {
        "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
        "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
        "actions/setup-node": "820762786026740c76f36085b0efc47a31fe5020",
        "actions/upload-artifact": "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
        "actions/upload-pages-artifact": "fc324d3547104276b827a68afc52ff2a11cc49c9",
        "actions/deploy-pages": "cd2ce8fcbc39b97be8ca5fce6e763baed58fa128",
    }
    for action, reference in expected_actions.items():
        assert f"{action}@{reference}" in workflow

    accept = (ROOT / "scripts" / "accept_v11.py").read_text(encoding="utf-8")
    assert "target height below 44px" in accept
    assert 'task["copyFailure"]["manualHeight"] >= 44' in accept
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
