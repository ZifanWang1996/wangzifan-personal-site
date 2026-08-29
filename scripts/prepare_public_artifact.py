#!/usr/bin/env python3
"""Create and verify the exact GitHub Pages artifact for wangzifan.store."""

import argparse
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATIC_PUBLIC_PATHS = (
    "index.html",
    "privacy.html",
    "favicon.svg",
    "assets/site.css",
    "assets/site.js",
    "assets/og-card.webp",
    "assets/archivo.woff2",
    "assets/wechat-qr.webp",
)
PROJECT_PUBLIC_PATHS = tuple(
    f"assets/projects/project-{project_id:02d}.webp" for project_id in range(1, 34)
)
PUBLIC_PATHS = STATIC_PUBLIC_PATHS + PROJECT_PUBLIC_PATHS


def public_files(root: Path = ROOT) -> list[Path]:
    paths = [root / relative for relative in PUBLIC_PATHS]
    symlinks = []
    for path in paths:
        current = root
        for part in path.relative_to(root).parts:
            current /= part
            if current.is_symlink():
                symlinks.append(str(current.relative_to(root)))
                break
    if symlinks:
        raise ValueError(f"public allowlist contains symlink paths: {sorted(set(symlinks))}")
    missing = [str(path.relative_to(root)) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing public files: {missing}")
    return paths


def candidate_digest(root: Path = ROOT) -> str:
    digest = hashlib.sha256()
    for path in public_files(root):
        digest.update(str(path.relative_to(root)).encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def prepare_public_artifact(output: Path, root: Path = ROOT) -> list[Path]:
    if output.exists():
        raise FileExistsError(f"refusing to reuse existing artifact directory: {output}")
    expected = public_files(root)
    for source in expected:
        relative = source.relative_to(root)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    actual = sorted(path.relative_to(output) for path in output.rglob("*") if path.is_file())
    expected_relative = sorted(path.relative_to(root) for path in expected)
    if actual != expected_relative:
        raise RuntimeError(
            f"artifact allowlist mismatch: expected={expected_relative}, actual={actual}"
        )
    return [output / relative for relative in actual]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    files = prepare_public_artifact(args.output.resolve())
    print(
        f"public artifact: {len(files)} files; "
        f"candidate sha256={candidate_digest(ROOT)}; path={args.output.resolve()}"
    )


if __name__ == "__main__":
    main()
