from __future__ import annotations

import argparse
import re
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".codex-migration-backup"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".wav", ".mp3", ".zip"}
PATTERNS = {
    "huggingface_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "generic_api_assignment": re.compile(
        r"(?i)(api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]"
    ),
    "bearer_token": re.compile(r"(?i)authorization\s*[:=]\s*['\"]bearer\s+[A-Za-z0-9._-]{16,}"),
}


def scan(root: Path) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in SKIP_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            for name, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append((path.relative_to(root), number, name))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Procura padrões de segredo versionável.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    findings = scan(root)
    if findings:
        print("Possíveis segredos encontrados; valores foram ocultados:")
        for path, line, name in findings:
            print(f"- {path}:{line} ({name})")
        return 1
    print("Nenhum padrão de segredo detectado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
